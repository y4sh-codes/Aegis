from textual.app import ComposeResult
from textual.widgets import Header, Footer, Static, DataTable, Log
from textual.containers import Horizontal
from textual.screen import Screen

class AegisDashboard(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="stats-container"):
            yield Static("Clients: 0", id="c-count", classes="card")
            yield Static("Round: 0", id="r-count", classes="card")
            yield Static("Status: IDLE", id="status", classes="card")
        yield DataTable(id="client-table")
        yield Log(id="main-log")
        yield Footer()