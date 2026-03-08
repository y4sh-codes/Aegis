from fastapi import FastAPI, WebSocket
from common.serialization import serialize_weights, deserialize_weights

app_api = FastAPI()

# We use a placeholder for the TUI instance which will be injected at runtime
tui_instance = None 

@app_api.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            weights = deserialize_weights(data)
            
            # Call the TUI's update handler
            if tui_instance:
                new_global = await tui_instance.handle_update(client_id, weights)
                if new_global:
                    await websocket.send_bytes(serialize_weights(new_global))
    except Exception:
        pass # Handle disconnection logic here