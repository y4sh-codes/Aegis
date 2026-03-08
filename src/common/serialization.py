import io
import torch

def serialize_weights(state_dict):
    buffer = io.BytesIO()
    torch.save(state_dict, buffer)
    return buffer.getvalue()

def deserialize_weights(data):
    return torch.load(io.BytesIO(data), weights_only=True)