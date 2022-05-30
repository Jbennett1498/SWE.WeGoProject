
function displayAllFleets() {
    //fetch(`http://127.0.0.1:5000/fleets`, {
    fetch(`https://supply.team21.sweispring22.gq/supply/fleets`,{
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        }//,
        //body: JSON.stringify({ name, service, owner, description, city })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            var str = JSON.stringify(data)
            document.getElementById('fleet_data_display').innerHTML = str
        });
}

/*
async function loadIntoTable(url, table) {

    const tableHead = document.getElementById('thead')//table.querySelector('thead');
    const tableBody = document.getElementById('tbody')//table.querySelector('tbody');
    fetch(`http://127.0.0.1:5000/fleets`, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data =>
            Object.entries(data).forEach(([key, value]) => {
                console.log(`${key}: ${value}`);
            })
        )
}
    /*
            console.log(dataObj)
            const {headers, rows} = dataObj;

            tableHead.innerHTML = "<tr></tr>";
            tableBody.innerHTML = " ";
            for (const headerText of Object.keys(headers)) {
                const headerElement = document.createElement("th");
                headerElement.textContent = headerText;
                tableHead.querySelector("tr").appendChild(headerElement);
            }
        });
}
/*
    const responseObj = JSON.stringify(response)
    console.log(responseObj)
    const { headers, rows } = await response.json();

    tableHead.innerHTML = "<tr></tr>";
    tableBody.innerHTML = " ";
    for(const headerText of Object.keys(headers))
    {
        const headerElement = document.createElement("th");
        headerElement.textContent = headerText;
        tableHead.querySelector("tr").appendChild(headerElement);
    }
}
*/
//loadIntoTable(`http://supply.team21.sweispring22.gq/supply/fleets`, document.querySelector("table"));
//loadIntoTable(`http://127.0.0.1:5000/fleets`, document.querySelector("table"));





