from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from common.serialization import serialize, deserialize
import traceback

app_api = FastAPI()
tui_instance = None 

@app_api.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    if tui_instance:
        tui_instance.log_message(f"Client {client_id} connected")
    
    try:
        while True:
            data = await websocket.receive_bytes()
            weights = deserialize(data)
            
            if tui_instance:
                tui_instance.log_message(f"Received weights from {client_id}")
                # Process weights and wait for the global model
                global_weights = await tui_instance.handle_update(client_id, weights)
                
                # CRITICAL: Always send a response back
                await websocket.send_bytes(serialize(global_weights))
                tui_instance.log_message(f"Sent global model to {client_id}")
            else:
                # If no TUI instance, still need to respond to keep connection alive
                await websocket.send_bytes(serialize({}))
    except WebSocketDisconnect:
        if tui_instance:
            tui_instance.log_message(f"Client {client_id} disconnected")
    except Exception as e:
        if tui_instance:
            tui_instance.log_message(f"Socket error with {client_id}: {e}")
            tui_instance.log_message(f"Traceback: {traceback.format_exc()}")
        raise
    finally:
        # Ensure proper WebSocket closure
        if tui_instance:
            tui_instance.log_message(f"Closing connection for {client_id}")
        try:
            await websocket.close()
        except:
            pass