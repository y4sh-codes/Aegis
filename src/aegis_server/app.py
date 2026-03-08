import sys
from pathlib import Path

# Add 'src' to the path
src_root = str(Path(__file__).parent.parent)
if src_root not in sys.path:
    sys.path.append(src_root)

import uvicorn
from threading import Thread
from datetime import datetime
from textual.app import App
from aegis_server import api, aggregator
from ui.views import AegisDashboard

class AegisServerApp(App):
    CSS_PATH = "../ui/dashboard.tcss"

    def on_mount(self):
        api.tui_instance = self
        self.agg = aggregator.FedAggregator()
        self.min_clients = 1
        self.connected_clients = set()
        self.client_rows = {}  # Map client_id to row key for updates
        self.dashboard = AegisDashboard()
        self.push_screen(self.dashboard)
        Thread(target=lambda: uvicorn.run(api.app_api, host="0.0.0.0", port=8000), daemon=True).start()

    def log_message(self, msg):
        try:
            log = self.screen.query_one("#main-log")
            log.write_line(msg)
        except Exception as e:
            pass

    async def handle_update(self, client_id, weights):
        try:
            # Track connected clients
            if client_id not in self.connected_clients:
                self.connected_clients.add(client_id)
                self.call_from_thread(self.add_client_row, client_id)
                self.call_from_thread(self.update_client_count)
            
            self.agg.add_update(weights)
            self.call_from_thread(self.log_message, f"Update received from {client_id}")
            self.call_from_thread(self.update_client_row, client_id, "Updated")
            
            # If we reached MIN_CLIENTS, perform aggregation
            if len(self.agg.updates) >= self.min_clients:
                self.call_from_thread(self.log_message, "Threshold reached. Aggregating...")
                new_global = self.agg.aggregate()
                self.call_from_thread(self.update_round_counter)
                self.call_from_thread(self.update_status, "AGGREGATING")
                self.call_from_thread(self.update_client_row, client_id, "Synced")
                return new_global
            
            # IF NOT READY:
            # Instead of doing nothing (which closes the connection),
            # return the CURRENT global model so the client can stay in sync.
            self.call_from_thread(self.update_status, "WAITING")
            return self.agg.global_model.state_dict()
        except Exception as e:
            self.call_from_thread(self.log_message, f"Error in handle_update: {e}")
            # Return current weights even on error to keep connection alive
            return self.agg.global_model.state_dict()
    
    def update_client_count(self):
        try:
            self.screen.query_one("#c-count").update(f"Clients: {len(self.connected_clients)}")
        except Exception as e:
            pass
    
    def add_client_row(self, client_id):
        try:
            table = self.screen.query_one("#client-table")
            timestamp = datetime.now().strftime("%H:%M:%S")
            row_key = table.add_row(client_id, "Connected", timestamp)
            self.client_rows[client_id] = row_key
        except Exception as e:
            pass
    
    def update_client_row(self, client_id, status):
        try:
            table = self.screen.query_one("#client-table")
            if client_id in self.client_rows:
                row_key = self.client_rows[client_id]
                timestamp = datetime.now().strftime("%H:%M:%S")
                table.update_cell(row_key, "Status", status)
                table.update_cell(row_key, "Last Update", timestamp)
        except Exception as e:
            pass
    
    def update_round_counter(self):
        try:
            self.screen.query_one("#r-count").update(f"Round: {self.agg.round_count}")
        except Exception as e:
            pass
    
    def update_status(self, status):
        try:
            self.screen.query_one("#status").update(f"Status: {status}")
        except Exception as e:
            pass

if __name__ == "__main__":
    AegisServerApp().run()