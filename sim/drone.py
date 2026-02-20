from dataclasses import dataclass
import math
import random

from sim.coverage import find_best_coverage_target
from sim.avoidance import get_avoidance_velocity


@dataclass
class DroneState:
    id: int
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    battery: float = 100.0
    mode: str = "SEARCH"  # SEARCH | RTB

class Drone:
    def __init__(self, state: DroneState, home=(5,5)):
        self.s = state
        self.home = home
        self.known_peers = {}  # id -> (x,y,vx,vy,battery)

    def broadcast(self):
        return {"id": self.s.id, "x": self.s.x, "y": self.s.y, "vx": self.s.vx, "vy": self.s.vy, "battery": self.s.battery, "mode": self.s.mode}

    def ingest(self, msg):
        if msg["id"] == self.s.id:
            return
        self.known_peers[msg["id"]] = (msg["x"], msg["y"], msg["vx"], msg["vy"], msg["battery"], msg["mode"])

    def decide(self, world, cfg):
        # 1. Update mode based on battery
        if self.s.battery <= cfg.rtb_threshold and self.s.mode != "RTB":
            self.s.mode = "RTB"

        # 2. Determine target based on mode
        if self.s.mode == "RTB":
            target = self.home
        else: # SEARCH mode
            target = find_best_coverage_target(self.s, world, cfg)
            if target is None:
                # No valid target found, stay put
                target = (self.s.x, self.s.y)

        # 3. Calculate desired velocity towards the target
        dx = target[0] - self.s.x
        dy = target[1] - self.s.y
        dist = math.hypot(dx, dy) + 1e-9  # avoid division by zero
        
        desired_vx = (dx / dist) * cfg.max_speed
        desired_vy = (dy / dist) * cfg.max_speed

        # 4. Adjust velocity for collision avoidance (peers and obstacles)
        final_vx, final_vy = get_avoidance_velocity(
            self.s, self.known_peers, world, desired_vx, desired_vy, cfg
        )

        self.s.vx, self.s.vy = final_vx, final_vy

    def step(self, world, cfg):
        nx = self.s.x + self.s.vx * cfg.dt
        ny = self.s.y + self.s.vy * cfg.dt

        # Clamp to world bounds
        nx = min(max(nx, 0.5), world.w - 0.5)
        ny = min(max(ny, 0.5), world.h - 0.5)

        # Final check for obstacles before moving
        if not world.is_obstacle(nx, ny):
            self.s.x, self.s.y = nx, ny

        # Mark new position as covered and drain battery
        world.mark_covered(self.s.x, self.s.y, r=1) # smaller radius for marking
        self.s.battery = max(0.0, self.s.battery - cfg.battery_drain_per_sec * cfg.dt)
