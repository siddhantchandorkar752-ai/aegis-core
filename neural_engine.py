import asyncio
import hashlib
import json
import time
from typing import List, Dict, Any, Optional

import torch
import torch.nn as nn
import torch.optim as optim

class LinearPredictor(nn.Module):
    def __init__(self):
        super(LinearPredictor, self).__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)

class MerkleTree:
    def __init__(self, data_blocks: List[str]):
        self.root: Optional[str] = None
        self.leaves = [self._hash(block) for block in data_blocks]
        if self.leaves:
            self.root = self._build_tree(self.leaves)

    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _build_tree(self, nodes: List[str]) -> str:
        if len(nodes) == 1:
            return nodes[0]
        new_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i+1] if i+1 < len(nodes) else left
            new_level.append(self._hash(left + right))
        return self._build_tree(new_level)

class NeuralExecutionEngine:
    def __init__(self):
        self.model: nn.Module = LinearPredictor()
        self.criterion = nn.MSELoss()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01)
        self.logs = [] # In-memory simple store for mocked redis/pg

    def train_step(self, x_data: List[float], y_data: List[float]):
        """Simple train loop for the predictor based on volatility -> cost-efficiency"""
        x = torch.tensor(x_data, dtype=torch.float32).view(-1, 1)
        y = torch.tensor(y_data, dtype=torch.float32).view(-1, 1)

        self.optimizer.zero_grad()
        predictions = self.model(x)
        loss = self.criterion(predictions, y)
        loss.backward()
        self.optimizer.step()

        return float(loss.item())

    def predict(self, volatility: float) -> float:
        """Forecasts the next 10 minutes (represented by the output)"""
        x = torch.tensor([[volatility]], dtype=torch.float32)
        with torch.no_grad():
            return float(self.model(x).item())

    async def edge_node_heartbeat(self, node_id: int):
        """Simulate an Edge Node reporting heartbeat"""
        while True:
            await asyncio.sleep(2.0)
            log_entry = {
                "node_id": node_id,
                "timestamp": time.time(),
                "status": "active"
            }
            self.persist_log(log_entry)

    def persist_log(self, data: Dict[str, Any]):
        """Simulates Redis + Postgres persistence with Merkle Tree immutability"""
        # Create Merkle tree over all previous logs + this new one
        temp_logs = self.logs + [json.dumps(data, sort_keys=True)]
        tree = MerkleTree(temp_logs)
        data["merkle_root"] = tree.root
        
        log_str = json.dumps(data, sort_keys=True)
        self.logs.append(log_str)

    async def run_nodes(self, num_nodes: int = 50):
        tasks = [self.edge_node_heartbeat(i) for i in range(num_nodes)]
        await asyncio.gather(*tasks)

