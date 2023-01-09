function loadDevices() {
    $.ajax({
        url: './device_info/all',
        type: 'get',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.info(data);

            let devicesJson = {};
            for (let entry of data.devices.reverse()) {
                // ID = 1 ==> Configuration-Tool überspringen
                if (entry['id'] == ''){
                    console.log(entry['id'] + ' übersprungen');
                } else if (entry['reachable'] == false){
                    devicesJson[entry['id']] = entry;
                    $.ajax({
                        url: '/kit/device-tile-not-reachable',
                        type: 'get',
                        data: {
                            "csrfmiddlewaretoken": getCookie('csrftoken'),
                            "device-id": entry['id'].toString(),
                            "device-name": entry['name'].toString(),
                        },
                        headers: {
                            'Content-type': 'application/json', 'Accept': 'text/plain',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        dataType: 'json',
                        mode: 'same-origin'
                    }).always((data) => {
                        if (data.readyState === 4 && data.status === 200) {
                            document.getElementById('device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                        }
                    });
                } else {
                    devicesJson[entry['id']] = entry;
                    $.ajax({
                        url: '/kit/device-tile',
                        type: 'get',
                        data: {
                            "csrfmiddlewaretoken": getCookie('csrftoken'),
                            "device-id": entry['id'].toString(),
                            "device-name": entry['name'].toString(),
                        },
                        headers: {
                            'Content-type': 'application/json', 'Accept': 'text/plain',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        dataType: 'json',
                        mode: 'same-origin'
                    }).always((data) => {
                        if (data.readyState === 4 && data.status === 200) {
                            document.getElementById('device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                            document.getElementById('switchLight-' + entry['id'].toString()).checked = entry['on'];
                        }
                    });
                }
            }
            window.localStorage.setItem('devices', JSON.stringify(devicesJson));
        }
    });
}

$(document).ready(() => {
    loadDevices();
});

function test() {
    console.log("yes sir i am working");
}
