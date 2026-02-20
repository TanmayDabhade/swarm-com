from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
import asyncio
import random
import json

app = FastAPI()

# In-memory list to keep track of active WebSocket connections
active_connections: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            sim_state = await websocket.receive_text()
            # Forwards the message to all connected clients
            await broadcast_message(sim_state)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Client disconnected.")
    except Exception as e:
        print(f"WebSocket error: {e}")

async def broadcast_message(message: str):
    """
    Sends a message to all active WebSocket connections.
    This will be used by the simulation to send state updates.
    """
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except WebSocketDisconnect:
            active_connections.remove(connection)
        except Exception as e:
            print(f"Error broadcasting message: {e}")
