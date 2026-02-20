import numpy as np

class World:
    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        self.coverage = np.zeros((height, width), dtype=np.float32)  # 0..1
        self.obstacles = np.zeros((height, width), dtype=np.uint8)

    def add_random_obstacles(self, seed=1, density=0.04):
        rng = np.random.default_rng(seed)
        self.obstacles = (rng.random((self.h, self.w)) < density).astype(np.uint8)

    def in_bounds(self, x: float, y: float) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h

    def is_obstacle(self, x: float, y: float) -> bool:
        xi, yi = int(x), int(y)
        if not self.in_bounds(xi, yi): 
            return True
        return self.obstacles[yi, xi] == 1

    def mark_covered(self, x: float, y: float, r: int):
        x0, y0 = int(x), int(y)
        ys = slice(max(0, y0 - r), min(self.h, y0 + r + 1))
        xs = slice(max(0, x0 - r), min(self.w, x0 + r + 1))
        self.coverage[ys, xs] = 1.0
