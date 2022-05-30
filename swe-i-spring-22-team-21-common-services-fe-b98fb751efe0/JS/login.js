const emailField = document.getElementById('typeEmailX');
const passwordField = document.getElementById('typePasswordX');

function doLogin() {
    const { value: password } = passwordField;
    const { value: email } = emailField;

    fetch('https://demand.team21.sweispring22.gq/common/login', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password, email })
        })
        .then(response => response.json())
        .then(data => {
            const { status } = data;
            if (status === 'success') {
                // This will have to change --> goes to different either demand or supply dashboard

                window.location.href = "dashboard.html";
            } else if (status === 'failed') {
                alert("Email or password is incorrect");

                document.getElementById('typeEmailX').value = "";
                document.getElementById('typePasswordX').value = "";
                return false;
            }
        });



}

// test