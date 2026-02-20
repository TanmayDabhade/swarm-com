import math

def get_avoidance_velocity(drone_state, known_peers, world, desired_vx, desired_vy, cfg):
    """
    Adjusts the drone's desired velocity to avoid peers and obstacles.
    """
    vx, vy = desired_vx, desired_vy

    # Repulsion from peers (collision avoidance)
    for _pid, (px, py, _, _, _, _) in known_peers.items():
        rx = drone_state.x - px
        ry = drone_state.y - py
        d = math.hypot(rx, ry) + 1e-9 # Add epsilon to avoid division by zero
        
        # If a peer is within the avoidance radius, apply a repulsion force
        if d < cfg.avoid_radius:
            strength = (cfg.avoid_radius - d) / cfg.avoid_radius
            # The repulsion force is proportional to how close the peer is
            vx += (rx / d) * cfg.max_speed * 1.2 * strength
            vy += (ry / d) * cfg.max_speed * 1.2 * strength

    # Soft obstacle avoidance: if the next step hits an obstacle, turn.
    # This is a simple but effective strategy. A more advanced implementation
    # might use potential fields or pathfinding.
    next_x = drone_state.x + vx * cfg.dt
    next_y = drone_state.y + vy * cfg.dt
    
    if world.is_obstacle(next_x, next_y):
        # Rotate velocity vector by 90 degrees as a simple escape maneuver
        vx, vy = -vy, vx

    return vx, vy
