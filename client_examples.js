var xhr = new XMLHttpRequest();
xhr.open('POST', 'http://localhost:5000/add_sensors_data', true);
xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

data = [
    {
        "location_id" : 3,
        "type": "temperature",
        "source_type": "local_dht22",
        "value": 20
    },
    {
        "location_id" : 3,
        "type": "humidity",
        "source_type": "local_dht22",
        "value": 69
    }
];

// send the collected data as JSON
xhr.send(JSON.stringify(data));

xhr.onloadend = function () {
    // done
};