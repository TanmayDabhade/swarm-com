from collections import deque
import random

class Comms:
    def __init__(self, drop_prob: float, latency_ticks: int):
        self.drop_prob = drop_prob
        self.lat = max(0, latency_ticks)
        self.queue = deque()  # (deliver_tick, msg)

    def send(self, tick: int, msg: dict):
        if random.random() < self.drop_prob:
            return
        self.queue.append((tick + self.lat, msg))

    def recv_all(self, tick: int):
        out = []
        while self.queue and self.queue[0][0] <= tick:
            _, msg = self.queue.popleft()
            out.append(msg)
        return out
