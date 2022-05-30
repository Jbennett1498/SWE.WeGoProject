const phoneNumField = document.getElementById('number');
const addressField = document.getElementById('address');
const cityField = document.getElementById('city');
const stateField = document.getElementById('state');
const zipField = document.getElementById('zip');


function doOrderForm() {
    const { value: number } = phoneNumField;
    const { value: address } = addressField;
    const { value: city } = cityField;
    const { value: state } = stateField;
    const { value: zip } = zipField;

    fetch('https://demand.team21.sweispring22.gq/demand/order', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ number, address, city, state, zip })
        })
        .then(response => response.json())
        .then(data => {

            if (data.status && data.status === 'fail') {
                alert("Order form failed");
                return false;
            } else {
                alert(data.ETA)
                window.location.href = "OrderMap.html";
            }
        });



}

function validateForm() {
    var number = document.forms["Form"]["number"].value;
    var address = document.forms["Form"]["address"].value;
    var city = document.forms["Form"]["city"].value;
    var state = document.forms["Form"]["state"].value;
    var zip = document.forms["Form"]["zip"].value;
    if (number == null || number === "", address == null || address === "", city == null || city === "", state == null || state === "", zip == null || zip === "") {
        alert("Please Fill All Required Fields");
        return false;
    }
    if (state != "Alabama" || "Alaska" || "Arizona" || "Arkansas" || "California" || "Colorado" || "Connecticut" || "Delaware" || "Florida" || "Georgia" || "Hawaii" || "Idaho" || "Illinois" || "Indiana" || "Iowa" || "Kansas" || "Kentucky" || "Louisiana" || "Maine" || "Maryland" || "Massachusetts" || "Michigan" || "Minnesota" || "Mississippi" || "Missouri" || "Montana" || "Nebraska" || "Nevada" || "New Hampshire" || "New Jersey" || "New Mexico" || "New York" || "North Carolina" || "North Dakota" || "Ohio" || "Oklahoma" || "Oregon" || "Pennsylvania" || "Rhode Island" || "South Carolina" || "South Dakota" || "Tennessee" || "Texas" || "Utah" || "Vermont" || "Virginia" || "Washington" || "West Virginia" || "Wisconsin" || "Wyoming") {
        alert("Please enter a valid state (Format: West Virginia) ")
        return false;
    }
}