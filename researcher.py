import asyncio
import random
import time
from typing import Dict

class Researcher:
    def __init__(self):
        self.vix = 18.5
        self.btc_hashrate = 600.0 # EH/s

    async def fetch_gpu_pricing(self) -> float:
        """Simulate fetching Live GPU Spot Pricing (e.g., A100 per hour)"""
        await asyncio.sleep(0.1) # Simulate network delay
        return random.uniform(1.2, 2.5) # A100 hourly cost in USD

    async def fetch_market_data(self) -> Dict[str, float]:
        """Simulate fetching VIX and BTC Hashrate"""
        await asyncio.sleep(0.1)
        self.vix += random.uniform(-0.5, 0.5)
        self.btc_hashrate += random.uniform(-10, 10)
        return {"vix": self.vix, "btc_hashrate": self.btc_hashrate}

    async def calculate_compute_to_market_ratio(self) -> float:
        """Categorize Compute-to-Market ratio dynamically"""
        gpu_price = await self.fetch_gpu_pricing()
        market_data = await self.fetch_market_data()
        
        # Arbitrary but dynamic logic
        raw_ratio = (market_data["btc_hashrate"] / gpu_price) / market_data["vix"]
        return raw_ratio
