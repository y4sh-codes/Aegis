import torch
import torch.nn as nn
import torch.optim as optim

def train_local(model, epochs=1):
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()
    # Dummy data for demonstration
    x = torch.randn(32, 784)
    y = torch.randint(0, 10, (32,))
    
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.step()
    return model.state_dict(), loss.item()