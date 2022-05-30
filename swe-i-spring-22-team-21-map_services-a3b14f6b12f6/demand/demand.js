// default values
// const customer = [-97.754205,30.228165]; // at St Edwards
// const vehicle = [-97.74352,30.26946];    // at Perry's steakhouse
// const destination =[-97.7972561238,30.21654839]; // at Menchaca Public Library

//establish token
mapboxgl.accessToken = 'pk.eyJ1IjoidGdyYXUiLCJhIjoiY2t6YTRyaHlmMGVlcDJvczhkZWJvd3g0dSJ9.ihqqYGiq6MIHVpJd_7gkJg';

// create new map instance
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/tgrau/ckzalemq9000c15nzehcalik7',
  center: [-97.75643520570105,30.266735657138515] ,  // start position, downtown Austin
  zoom: 12
});

// set the bounds of the map
const bounds = [
  [-98.750885, 29.229687],
  [-96.755589, 31.226747]
];
map.setMaxBounds(bounds);

// create a function to make a directions request
async function getRoute() {

  //retreive vehicle details and status and extract route data
  const query = await fetch('/dispatchResponse.json')
  const json = await query.json();
  const data = json.route.routes[0];
  const route = data.geometry.coordinates;
  const vehicle = json.route.waypoints[0].location;
  const customer = json.route.waypoints[1].location;
  const destination = json.route.waypoints[2].location;
  
  // extraxct coordinate details for route
  const geojson = {
    type: 'Feature',
    properties: {},
    geometry: {
      type: 'LineString',
      coordinates: route
    }
  };

  // if the route already exists on the map, we'll reset it using setData
  if (map.getSource('route')) {
    map.getSource('route').setData(geojson);
  }
  // otherwise, we'll make a new request
  else {
    map.addLayer({
      id: 'route',
      type: 'line',
      source: {
        type: 'geojson',
        data: geojson
      },
      layout: {
        'line-join': 'round',
        'line-cap': 'round'
      },
      paint: {
        'line-color': '#3887be',
        'line-width': 5,
        'line-opacity': 0.75
      }
    });
  }

  //get the sidebar and add the length and time of arrival
  const instructions = document.getElementById('instructions');
  const date = new Date();
  const hour = date.getHours() ;
  const minutes = date.getMinutes();
  const travelTime = data.duration / 60;
  let arrivalTimeMin = Math.floor(travelTime) + minutes;
  let arrivalTimeHours = hour
  let ampm = "AM"
  while (arrivalTimeMin >= 60) {
    arrivalTimeMin -= 60;
    arrivalTimeHours += 1
  }
  if (arrivalTimeHours > 12) {
    arrivalTimeHours -= 12;
    ampm = "PM"
  }
  if (arrivalTimeMin < 10) {arrivalTimeMin = "0"+arrivalTimeMin;}
  instructions.innerHTML = `<p><strong>Trip duration: ${Math.floor(travelTime)} min <br>Time of arrival: ${arrivalTimeHours}:${arrivalTimeMin} ${ampm} </strong></p>`;

  // add vehicle point to the map
  map.loadImage(
  'car.png',
  (error, image) => {
    if (error) throw error;

    // Add the image to the map style.
    map.addImage('carImage', image);

    // Add a data source containing one point feature.
    map.addSource('vehicleImage', {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': vehicle
                    }
                }
            ]
        }
    });

    // Add a layer to use the image to represent the data.
    map.addLayer({
        'id': 'vehicleLayer',
        'type': 'symbol',
        'source': 'vehicleImage', // reference the data source
        'layout': {
          'icon-image': 'carImage', // reference the image
          'icon-size': 0.1
        }
    });
    }
  );  

  // add customer point to the map
  map.loadImage(
    'user.png',
    (error, image) => {
      if (error) throw error;


      // Add the image to the map style.
      map.addImage('user', image);

      // Add a data source containing one point feature.
      map.addSource('userImage', {
          'type': 'geojson',
          'data': {
              'type': 'FeatureCollection',
              'features': [
                  {
                      'type': 'Feature',
                      'geometry': {
                          'type': 'Point',
                          'coordinates': customer
                      }
                  }
              ]
          }
      });

        // Add a layer to use the image to represent the data.
        map.addLayer({
          'id': 'userLayer',
          'type': 'symbol',
          'source': 'userImage', // reference the data source
          'layout': {
              'icon-image': 'user', // reference the image
              'icon-size': 2
        }
      });
    }
  );  

  // add destination image
  map.loadImage(
    'mapbox-icon.png',
    (error, image) => {
        if (error) throw error;

        // Add the image to the map style.
        map.addImage('icon', image);

        // Add a data source containing one point feature.
        map.addSource('destination', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': destination
                        }
                    }
                ]
            }
        });

        // Add a layer to use the image to represent the data.
        map.addLayer({
            'id': 'points',
            'type': 'symbol',
            'source': 'destination', // reference the data source
            'layout': {
                'icon-image': 'icon', // reference the image
                'icon-size': 0.25
        }
      });
    }
  );  
}

map.on('load', () => {
  
  // make an initial directions request that
  // starts and ends at the same location
  getRoute();

});