/*function  validateForm()
{
    let name = document.getElementById('fleet_name').valueOf()
    if (name === "") {
        alert("Name must be filled out");
        return false;
    }
}*/
function createFleet() {
    const {value: name} = document.getElementById('fleet_name');
    const {value: service} = document.getElementById('fleet_service');
    const {value: owner} = document.getElementById('fleet_owner');
    const {value: description} = document.getElementById('fleet_desc');
    const {value: city} = document.getElementById('fleet_city');

    //fetch(`http://127.0.0.1:5000/fleets`, {
    fetch(`https://supply.team21.sweispring22.gq/supply/fleets`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({name, service, owner, description, city})
         })
        .then(response => response.json())
        .then(data => {

            if (data.id) {
                alert(`${data.id} created`);
            } else {
                alert("Fleet creation failed.")
            }
        });
}