import sys
from pathlib import Path

# Calculate the path to the 'src' directory (two levels up from this file)
src_root = str(Path(__file__).parent.parent)
if src_root not in sys.path:
    sys.path.append(src_root)

import asyncio
import websockets
import torch
import sys
from common.models import AegisModel
from common.serialization import serialize, deserialize
from aegis_client.trainer import train_local 

async def start_client(name):
    model = AegisModel().cpu()
    uri = "ws://localhost:8000/ws/" + name
    
    async with websockets.connect(uri, ping_interval=20, ping_timeout=60) as ws:
        print(f"🚀 {name} connected.")
        for r in range(5):
            # Local Training
            weights, loss = train_local(model)
            
            # Send weights
            await ws.send(serialize(weights))
            print(f"Round {r}: Weights sent. Waiting for aggregator...")
            
            # Receive Global Model
            try:
                global_data = await ws.recv()
                model.load_state_dict(deserialize(global_data))
                print(f"Round {r}: Success. Global model synced.")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"❌ Connection closed: {e}")
                break
            except Exception as e:
                print(f"❌ Failed to receive data: {e}")
                break

if __name__ == "__main__":
    asyncio.run(start_client(sys.argv[1] if len(sys.argv) > 1 else "Node-1"))