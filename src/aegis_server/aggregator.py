import torch
from common.models import AegisModel

class FedAggregator:
    def __init__(self):
        self.global_model = AegisModel().cpu()
        self.updates = []
        self.round_count = 0

    def add_update(self, weights):
        # Ensure weights are on CPU before storing
        self.updates.append({k: v.cpu() for k, v in weights.items()})

    def aggregate(self):
        if not self.updates:
            return self.global_model.state_dict()
        
        new_state = {}
        for key in self.updates[0].keys():
            # Standard FedAvg aggregation
            new_state[key] = torch.stack([u[key] for u in self.updates]).mean(dim=0)
        
        self.global_model.load_state_dict(new_state)
        self.updates = [] # Clear the buffer
        self.round_count += 1
        return new_state

    def get_current_weights(self):
        return self.global_model.state_dict()