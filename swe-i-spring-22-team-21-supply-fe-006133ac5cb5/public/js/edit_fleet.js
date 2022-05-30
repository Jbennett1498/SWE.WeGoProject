function editFleet() {
    const { value: id } = document.getElementById('fleet_id');
    const { value: name } = document.getElementById('fleet_name');
    const { value: service } = document.getElementById('fleet_service');
    const { value: description } = document.getElementById('fleet_desc');
    const { value: city } = document.getElementById('fleet_city');
    //const { value: add_vehicles } = add_vehicles;

    //fetch(`http://127.0.0.1:5000/fleets/${id}`, {
    fetch(`https://supply.team21.sweispring22.tk/supply/fleets/${id}`, {
        method: 'PATCH',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({name, service, description, city})
    })
        .then(function(response) {
            if(response.status === 200)
            {
                alert(`Fleet details successfully updated.`)
            }
            else
            {
                alert(`Fleet details not updated.`)
            }
        });
}