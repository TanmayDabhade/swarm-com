import time
import asyncio
import json
import websockets # Client-side websockets

from sim.config import SimConfig
from sim.world import World
from sim.drone import Drone, DroneState
from sim.comms import Comms
from sim.metrics import coverage_percent

async def run_sim_and_stream():
    cfg = SimConfig()
    world = World(cfg.width, cfg.height)
    world.add_random_obstacles(seed=2, density=0.045)

    comms = Comms(cfg.comms_drop_prob, cfg.comms_latency_ticks)

    drones = []
    for i in range(cfg.n_drones):
        s = DroneState(id=i, x=6 + (i % 6) * 1.2, y=6 + (i // 6) * 1.2, battery=cfg.battery_start)
        drones.append(Drone(s, home=(5,5)))

    tick = 0
    last_print = 0

    # Connect to the WebSocket server
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to WebSocket server at {uri}")
        while True:
            # broadcast
            for d in drones:
                comms.send(tick, d.broadcast())

            # receive
            for msg in comms.recv_all(tick):
                for d in drones:
                    d.ingest(msg)

            # decide + step
            for d in drones:
                d.decide(world, cfg)
            for d in drones:
                d.step(world, cfg)

            # Prepare state for streaming
            drone_states = [d.s.__dict__ for d in drones]
            sim_state = {
                "tick": tick,
                "coverage_percent": coverage_percent(world),
                "drones": drone_states,
                "world_width": world.w,
                "world_height": world.h,
                "obstacles": world.obstacles.tolist() # Convert numpy array to list for JSON serialization
            }

            try:
                await websocket.send(json.dumps(sim_state))
            except websockets.exceptions.ConnectionClosedOK:
                print("WebSocket connection closed by server.")
                break
            except Exception as e:
                print(f"Error sending data over WebSocket: {e}")
                break # Exit loop if connection fails

            if tick - last_print >= 20:
                last_print = tick
                print(f"tick={tick} coverage={coverage_percent(world):.2f}% drop={cfg.comms_drop_prob} lat={cfg.comms_latency_ticks}")

            tick += 1
            # Adjust sleep time for async operations
            await asyncio.sleep(cfg.dt)

if __name__ == "__main__":
    asyncio.run(run_sim_and_stream())