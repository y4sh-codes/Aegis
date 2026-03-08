import io
import torch

def serialize(state_dict):
    buffer = io.BytesIO()
    torch.save(state_dict, buffer)
    return buffer.getvalue()

def deserialize(data):
    # weights_only=True is required for modern PyTorch security
    return torch.load(io.BytesIO(data), weights_only=True)