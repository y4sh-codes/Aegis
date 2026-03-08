import torch
from common.models import AegisModel

class FedAggregator:
    def __init__(self):
        self.global_model = AegisModel()
        self.updates = []

    def add_update(self, state_dict):
        self.updates.append(state_dict)

    def aggregate(self):
        if not self.updates: return
        
        new_state = {}
        keys = self.updates[0].keys()
        for key in keys:
            new_state[key] = torch.stack([u[key] for u in self.updates]).mean(dim=0)
        
        self.global_model.load_state_dict(new_state)
        self.updates = []
        return self.global_model.state_dict()