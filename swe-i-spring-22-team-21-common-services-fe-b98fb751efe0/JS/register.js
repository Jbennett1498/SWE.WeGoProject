const firstNameField = document.getElementById('first');
const lastNameField = document.getElementById('last');
const dateOfBirthField = document.getElementById('doB');
const passwordField = document.getElementById('password');
const emailField = document.getElementById('email');


function doSignUp() {
    const { value: firstName } = firstNameField;
    const { value: lastName } = lastNameField;
    const { value: DoB } = dateOfBirthField;
    const { value: email } = emailField;
    const { value: password } = passwordField;

    fetch('https://demand.team21.sweispring22.gq/common/signup', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ firstName, lastName, DoB, password, email })
        })
        .then(response => response.json())
        .then(data => {
            const { status } = data;
            if (status === 'success') {
                window.location.href = "login.html";
            } else if (status === 'fail') {
                alert("Email already exists");

                document.getElementById('typeEmailX').value = "";
                return false;
            }
        });



}

function validateForm() {
    var firstName = document.forms["Form"]["first"].value;
    var lastName = document.forms["Form"]["last"].value;
    var DoB = document.forms["Form"]["doB"].value;
    var email = document.forms["Form"]["email"].value;
    var password = document.forms["Form"]["password"].value;
    if (firstName == null || firstName === "", lastName == null || lastName === "", DoB == null || DoB === "", email == null || email === "", password == null || password === "") {
        alert("Please Fill All Required Field");
        return false;
    }

}