import asyncio
import websockets
import sys
from common.models import AegisModel
from common.serialization import serialize_weights, deserialize_weights
from aegis_client.trainer import train_local

async def start_client(name):
    model = AegisModel()
    uri = f"ws://localhost:8000/ws/{name}"
    
    async with websockets.connect(uri) as ws:
        for round in range(5):
            print(f"Round {round}: Training...")
            local_weights = train_local(model)
            await ws.send(serialize_weights(local_weights))
            
            global_data = await ws.recv()
            model.load_state_dict(deserialize_weights(global_data))
            print(f"Round {round}: Global Model Synced.")

if __name__ == "__main__":
    client_name = sys.argv[1] if len(sys.argv) > 1 else "Node-1"
    asyncio.run(start_client(client_name))