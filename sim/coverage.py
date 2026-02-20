import random

def find_best_coverage_target(drone_state, world, cfg):
    """
    Scans a local window around the drone to find the most valuable
    uncovered cell to target next.
    """
    best_target = None
    best_score = -1.0
    
    # Search in a square area around the drone
    radius = cfg.sensor_radius
    cx, cy = int(drone_state.x), int(drone_state.y)
    
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            tx, ty = cx + dx, cy + dy

            # Ensure the target is within world bounds
            if not world.in_bounds(tx, ty):
                continue
            
            # Skip obstacles
            if world.is_obstacle(tx, ty):
                continue

            # Score is based on being uncovered, with a bit of randomness
            # to break ties and prevent drones from getting stuck.
            coverage_value = world.coverage[ty, tx]
            score = (1.0 - coverage_value) + 0.05 * random.random()

            if score > best_score:
                best_score = score
                best_target = (tx + 0.5, ty + 0.5) # Target the center of the cell
                
    return best_target
