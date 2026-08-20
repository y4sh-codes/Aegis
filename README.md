# Aegis-FL 

Aegis-FL is a federated learning framework designed for real-time distributed training with high visibility. It allows multiple clients to collaboratively train a global model without sharing their private datasets, all managed through a centralized Terminal User Interface (TUI) dashboard.

## 🏗️ Architecture Overview

Aegis utilizes a centralized aggregation server to orchestrate training across distributed nodes. The server manages global weights while clients handle local data processing and stochastic gradient descent (SGD).

### The Federated Cycle

1. **Global Broadcast**: Server pushes current model weights to all active clients.
2. **Local Training**: Clients perform training on private local datasets.
3. **Weight Upload**: Clients send updated parameters back to the Aegis Server.
4. **Aggregation**: The server applies the FedAvg algorithm to generate the new global model.

## 📁 Project Structure

The project is organized into a modular package structure to ensure maintainability and scalability:

```
aegis-fl/
├── src/
│   ├── aegis_server/    # Server/Aggregator logic, TUI & WebSocket API
│   ├── aegis_client/    # Client-side trainer & network connector
│   ├── common/          # Shared model definitions & serialization
│   └── ui/              # TUI Views and .tcss styling files
├── data/                # Local datasets (ignored by git)
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

##  Quick Start

### 1. Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/aegis-fl.git
cd aegis-fl
pip install -r requirements.txt
```

### 2. Launching the Server

Start the Aegis Aggregator. This will initialize the TUI dashboard and open the WebSocket port (Default: 8000).

```bash
python -m src.aegis_server.app
```

### 3. Connecting Clients

Open new terminal windows for each client you wish to connect to the federation:

```bash
# Terminal 2: Connect Node Alpha
python -m src.aegis_client.client Node-Alpha

# Terminal 3: Connect Node Beta
python -m src.aegis_client.client Node-Beta
```

## 📊 TUI Dashboard Features

The Aegis TUI is built with Textual and provides real-time metrics:

- **Client Table**: Tracks every connected node, their last update status, and latency.
- **Round Counter**: Displays the current global training round.
- **Activity Log**: A scrollable log providing detailed information on aggregation events and network connections.
- **Status HUD**: Quick-glance cards showing the health and status of the federation.

## 🧠 Technical Specifications

| Component    | Technology                                  |
|--------------|---------------------------------------------|
| Backend      | PyTorch (Neural Networks)                   |
| Networking   | FastAPI & WebSockets (Asynchronous)         |
| Interface    | Textual (Terminal User Interface)           |
| Aggregation  | Federated Averaging (FedAvg)                |
| Data Format  | Binary serialized PyTorch state_dicts       |

## 🛠️ Configuration

You can customize the behavior of Aegis-FL by editing [src/aegis_server/app.py](src/aegis_server/app.py):

- **MIN_CLIENTS**: Set the threshold of clients needed before an aggregation round begins.
- **LEARNING_RATE**: Adjust local training steps.
- **WS_PORT**: Change the listening port for different network environments.

## 🛡️ License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
