function displayVehiclesInAFleet() {
    const { value: id } = document.getElementById('fleet_id');
    //fetch(`http://127.0.0.1:5000/fleets/${id}/vehicles`, {
    fetch(`https://supply.team21.sweispring22.gq/supply/fleets/${id}/vehicles`,{
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        }//,
        //body: JSON.stringify({ name, service, owner, description, city })
    })
        .then(response => response.json())
        .then(json => {
            console.log(json)
            var str = JSON.stringify(json)
            document.getElementById('data_display').innerHTML = str

        });
}







