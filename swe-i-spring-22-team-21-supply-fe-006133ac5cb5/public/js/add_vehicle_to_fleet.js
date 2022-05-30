function addVehicle() {
    const { value: fleet_id } = document.getElementById('fleet_id');
    const { value: vin } = document.getElementById('vin');
    const { value: make } = document.getElementById('make');
    const { value: model } = document.getElementById('model');
    const { value: year } = document.getElementById('year');

    //fetch(`http://127.0.0.1:5000/fleets/${fleet_id}/vehicles`, {
    fetch(`https://supply.team21.sweispring22.gq/supply/fleets/${fleet_id}/vehicles`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vin, make, model, year })
    })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                alert(`${data.id} registered`);
            } else {
                alert("Vehicle registration failed.")
            }
        });
}