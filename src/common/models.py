import torch.nn as nn

class AegisModel(nn.Module):
    def __init__(self, input_size=784, num_classes=10):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        return self.model(x)