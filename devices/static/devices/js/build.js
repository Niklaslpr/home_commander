function loadDevices() {


    // let xhr = new XMLHttpRequest();
    // xhr.open('GET', '/kit/device-tile-2', true);
    // xhr.onreadystatechange = function () {
    //     console.log("readyState", this.readyState);
    //     console.log("status", this.status);
    //     if (this.readyState !== 4) return;
    //     if (this.status !== 200) return; // or whatever error handling you want
    //     document.getElementById('device-list').insertAdjacentHTML('beforeend', this.responseText.toString());
    // };
    // xhr.send();

    $.ajax({
        url: '/device_info/all',
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

            console.log("start");


            // $.ajax({
            //     url: '/kit/device-tile-2',
            //     type: 'get',
            //     data: {
            //         "csrfmiddlewaretoken": getCookie('csrftoken'),
            //         "device-id": '12345',
            //         "device-name": 'fuckThis',
            //     },
            //     headers: {
            //         'Content-type': 'application/json', 'Accept': 'text/plain',
            //         'X-CSRFToken': getCookie('csrftoken')
            //     },
            //     dataType: 'json',
            //     mode: 'same-origin'
            // }).always((data) => {
            //     console.log("i was here");
            //     console.log("sus", data);
            //     if (data.readyState === 4 && data.status === 200) {
            //         document.getElementById('device-list').insertAdjacentHTML('beforeend', data.responseText.toString());
            //     }
            // });

            // $(document).load('/kit/device-tile-2', {"device-id": "12344"}, (responseText) => {
            //     console.log("jo");
            //     console.log(responseText);
            // });

            // let xhr = new XMLHttpRequest();
            // xhr.open('GET', '/kit/device-tile-2', true);
            // xhr.onreadystatechange = function () {
            //     console.log("readyState", this.readyState);
            //     console.log("status", this.status);
            //     if (this.readyState !== 4) return;
            //     if (this.status !== 200) return; // or whatever error handling you want
            //     document.getElementById('device-list').insertAdjacentHTML('beforeend', this.responseText.toString());
            // };
            // xhr.send();

            console.log("zwerg");


            // let xhr;
            //
            // xhr = new XMLHttpRequest();
            // xhr.open('GET', '/kit/device-tile-2', true);
            // xhr.onreadystatechange = function () {
            //     console.log("readyState", this.readyState);
            //     console.log("status", this.status);
            //     if (this.readyState !== 4) return;
            //     if (this.status !== 200) return; // or whatever error handling you want
            //     document.getElementById('device-list').insertAdjacentHTML('beforeend', this.responseText.toString());
            // };
            //

            let devciesJson = {};
            for (let entry of data.devices.reverse()) {
                console.log("entry", entry);
                devciesJson[entry['id']] = entry;

                $.ajax({
                    url: '/kit/device-tile',
                    type: 'get',
                    data: {
                        "csrfmiddlewaretoken": getCookie('csrftoken'),
                        "device-id": entry['id'],
                        "device-name": entry['name'],
                    },
                    headers: {
                        'Content-type': 'application/json', 'Accept': 'text/plain',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    dataType: 'json',
                    mode: 'same-origin'
                }).always((data) => {
                    console.log("i was here");
                    console.log("sus", data);
                    if (data.readyState === 4 && data.status === 200) {
                        document.getElementById('device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                    }
                });
            }

            window.localStorage.setItem('devices', JSON.stringify(devciesJson));

            // let formData = new FormData();
            // formData.append('max', 'hello');
            // xhr.send();
            // $('#device-list').append(this.)
            console.log("end");
        }
    });
}

$(document).ready(() => {
    loadDevices();
});

function test() {
    console.log("yes sir i am working")
}