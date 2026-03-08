import uvicorn
from threading import Thread
from textual.app import App
from aegis_server.aggregator import FedAggregator
from aegis_server import api  # Import the api module
from ui.views import AegisDashboard

class AegisServerApp(App):
    CSS_PATH = "../ui/dashboard.tcss"

    def __init__(self):
        super().__init__()
        self.aggregator = FedAggregator()
        self.min_clients = 2

    def on_mount(self):
        # Inject this app instance into the API module so it can call handle_update
        api.tui_instance = self 
        
        self.push_screen(AegisDashboard())
        
        # Start the API server in a background thread
        Thread(target=lambda: uvicorn.run(api.app_api, host="0.0.0.0", port=8000, log_level="error"), daemon=True).start()

    async def handle_update(self, client_id, weights):
        dashboard = self.query_one(AegisDashboard)
        self.aggregator.add_update(weights)
        
        # Update UI Table
        dashboard.query_one("#client-table").add_row(client_id, "Success", "Synced")
        dashboard.query_one("#main-log").write_line(f"Received update from {client_id}")
        
        if len(self.aggregator.updates) >= self.min_clients:
            new_global = self.aggregator.aggregate()
            dashboard.query_one("#r-count").update("Round: Processed")
            return new_global
        return None

if __name__ == "__main__":
    app = AegisServerApp()
    app.run()