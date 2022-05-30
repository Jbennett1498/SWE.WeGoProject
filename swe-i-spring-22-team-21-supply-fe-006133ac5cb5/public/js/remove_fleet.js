function removeFleet() {
    const fleet_id = document.getElementById('fleet_id').value;

    //fetch(`http://127.0.0.1:5000/fleets/${fleet_id}`, {
    fetch(`https://supply.team21.sweispring22.gq/supply/fleets/${fleet_id}`, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(function(response) {
            if(response.status === 200)
            {
                alert(`Fleet successfully deleted.`)
            }
            else
            {
                alert(`Fleet not deleted.`)
            }
    });
}
