# Swarm Monitor Sim

A real-time swarm simulator and monitoring dashboard. This project simulates a swarm of drones navigating a 2D space, performing coverage tasks, avoiding obstacles, and managing battery life, while streaming their live state to a web-based dashboard via WebSockets.

## Features

- **Swarm Simulation**: Physics and logic-based simulator for multiple drones. Controls movement, collision avoidance, battery depletion, and return-to-base mechanics.
- **Realistic Constraints**: Incorporates communication latency and message drop probability into the drone swarm logic.
- **WebSocket Streaming**: A FastAPI-powered server that acts as a real-time message broker between the simulation and web clients.
- **Lightweight Monitoring UI**: A vanilla HTML/JS dashboard that connects to the WebSockets to display live telemetry (ID, Position, State) for each automated drone.

## Codebase Structure

- **`sim/`**: The core Python simulator. `main.py` is the entry point, and it orchestrates the `World`, `Drone`, and `Comms` environments based on settings in `config.py`.
- **`server/`**: A lightweight FastAPI application (`app.py`) providing a WebSocket endpoint (`/ws`) for broadcasting simulation data to any connected clients.
- **`ui/`**: The front-end monitor. Simply open `index.html` in your browser to see the simulation state rendered via `app.js`.

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- Depending on your system, you might want to run this in a virtual environment (`venv`).

## Setup & Installation

1. Clone or download this repository.
2. Navigate to the project root directory:
   ```bash
   cd swarm-monitor-sim
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

To run the project, you need to start the WebSocket Server, the UI, and the Simulator simultaneously. It's recommended to use multiple terminal windows or tabs.

### 1. Start the Server
In your first terminal, from the project root, launch the FastAPI server:
```bash
uvicorn server.app:app --reload --port 8000
```
This will start the WebSocket broker at `ws://localhost:8000/ws`.

### 2. Open the Monitoring UI
You can simply open the `ui/index.html` file in your preferred web browser:
- **macOS:** `open ui/index.html`
- **Linux:** `xdg-open ui/index.html`
- **Windows:** Double-click the file in File Explorer.

Alternatively, you can serve it via a simple Python HTTP server from the `ui/` directory:
```bash
cd ui
python -m http.server 8080
```
And navigate to `http://localhost:8080` in your browser.

### 3. Run the Simulator
In a second terminal, from the project root, start the simulation. The simulation will connect to the local WebSocket server and begin streaming data.
```bash
python -m sim.main
```
You will see simulation progress in the terminal (ticks, coverage, metrics), and the drones will appear dynamically in your connected web UI!

## Configuration

You can easily adjust simulation parameters (number of drones, battery life, map size, max speed, and communication reliability) by modifying the `SimConfig` dataclass found in `sim/config.py`.
# swarm-com
