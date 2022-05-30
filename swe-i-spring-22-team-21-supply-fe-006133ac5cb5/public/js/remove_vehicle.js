function removeVehicle() {
    const vehicle_id = document.getElementById('vehicle_id').value;

    //fetch(`http://127.0.0.1:5000/vehicles/${vehicle_id}`, {
    fetch(`https://supply.team21.sweispring22.gq/supply/vehicles/${vehicle_id}`, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(function(response) {
            if(response.status === 200)
            {
                alert(`Vehicle successfully deleted.`)
            }
            else
            {
                alert(`Vehicle not deleted.`)
            }
        });
}
