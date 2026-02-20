from dataclasses import dataclass

@dataclass
class SimConfig:
    width: int = 120
    height: int = 80
    n_drones: int = 20
    dt: float = 0.1  # seconds per tick
    max_speed: float = 2.5  # cells/sec
    comms_drop_prob: float = 0.15
    comms_latency_ticks: int = 3
    sensor_radius: int = 6
    avoid_radius: float = 2.5
    battery_start: float = 100.0
    battery_drain_per_sec: float = 0.25
    rtb_threshold: float = 15.0  # return-to-base
