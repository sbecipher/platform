import asyncio
import json
import random
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

# Simulate a Redis Pub/Sub receiver that gets live ticks from LSEG
async def simulate_market_data():
    symbols = ['IE', 'UEC', 'AA', 'AMR', 'BTU', 'CDE', 'CLF', 'URG', 'USAR', 'AAPL', 'MSFT', 'TSLA']
    base_prices = {
        'IE': 18.86, 'UEC': 16.09, 'AA': 58.15, 'AMR': 208.76, 'BTU': 35.01,
        'CDE': 20.75, 'CLF': 14.53, 'URG': 1.65, 'USAR': 23.53,
        'AAPL': 175.20, 'MSFT': 410.10, 'TSLA': 180.40
    }
    
    while True:
        await asyncio.sleep(1.0) # Tick every 1 second
        if not manager.active_connections:
            continue
            
        # Generate 1-3 random ticks
        num_ticks = random.randint(1, 3)
        ticks = []
        for _ in range(num_ticks):
            sym = random.choice(symbols)
            # Random walk +- 0.5%
            change = base_prices[sym] * random.uniform(-0.005, 0.005)
            base_prices[sym] += change
            ticks.append({
                "symbol": sym,
                "last_price": round(base_prices[sym], 2),
                "timestamp": asyncio.get_event_loop().time()
            })
            
        await manager.broadcast(json.dumps({"type": "MARKET_TICK", "data": ticks}))

@router.websocket("/ws/market-data")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming commands if necessary (e.g. subscribe to specific symbols)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
