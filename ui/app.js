const dronesContainer = document.getElementById('drones');
const socket = new WebSocket('ws://localhost:8000/ws');

socket.onmessage = function(event) {
    const sim_state = JSON.parse(event.data);
    updateDrones(sim_state);
};

function updateDrones(sim_state_str) {
    const sim_state = JSON.parse(sim_state_str);
    dronesContainer.innerHTML = '';
    sim_state.drones.forEach(drone => {
        const droneElement = document.createElement('div');
        droneElement.classList.add('drone');
        droneElement.innerHTML = `
            <strong>ID:</strong> ${drone.s.id}<br>
            <strong>Position:</strong> (${drone.s.x.toFixed(2)}, ${drone.s.y.toFixed(2)})<br>
            <strong>State:</strong> ${drone.s.state}
        `;
        dronesContainer.appendChild(droneElement);
    });
}
