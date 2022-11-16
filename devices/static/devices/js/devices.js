let colorPicker;
let deviceControlModal;
let deviceControlModalHeader;
let deviceControlModalLabel;
let deviceControlModalSwitch;
let deviceControlModalBrightnessSlider;
let deviceControlModalBrightnessDisplay;

$(document).ready(() => {
    colorPicker = new iro.ColorPicker('#device-control-modal-colorpicker', {
        borderWidth: 2,
        layout: [
            {
                component: iro.ui.Wheel,
            },
        ]
    });

    deviceControlModal = document.getElementById('device-control-modal')
    deviceControlModalHeader = document.getElementById('device-control-modal-header');
    deviceControlModalLabel = document.getElementById('device-control-modal-label');
    // deviceControlModalLabel.innerHTML = 'Lampe XXX';

    colorPicker.on('color:change', function (color) {
        console.log(color.hue);
        console.log(color.saturation);
        deviceControlModalHeader.style.backgroundColor = color.hexString;
        deviceControlModalLabel.innerText = deviceControlModal.dataset['deviceName'] + ' ' + 'Hue: ' + color.hue + ' Sat: ' + color.saturation;

        let hue = Math.round(color.hue * 65535 / 360);
        let sat = Math.round(color.saturation * 2.55);

        let formData = new FormData();
        formData.append('hue', hue);
        formData.append('sat', sat);
        formData.append('csrfmiddlewaretoken', csrftoken);

        const http = new XMLHttpRequest();
        http.open('POST', '/sethue/');
        http.send(formData);
    });

    deviceControlModalSwitch = document.getElementById('device-control-modal-switch');
    deviceControlModalBrightnessSlider = document.getElementById("device-control-modal-brightness");
    deviceControlModalBrightnessDisplay = document.getElementById("device-control-modal-brightness-display");
    deviceControlModalBrightnessDisplay.innerText = deviceControlModalBrightnessSlider.value + ' %';


    deviceControlModalBrightnessSlider.oninput = function () {
        let bri = this.value;
        deviceControlModalBrightnessDisplay.innerText = bri + '%';   // Update the current slider value (each time you drag the slider handle)
        bri = Math.round(bri * 2.55);

        // sending Brightness
        let formData = new FormData();
        formData.append('bri', bri);
        formData.append('csrfmiddlewaretoken', csrftoken);

        let http = new XMLHttpRequest();
        http.open('POST', '/setbri/');
        http.send(formData);

        http = new XMLHttpRequest();
        http.open('POST', '/sethue/');
        http.send(formData);
    }

    // Suche Geräte
    let startDeviceSearch = document.getElementById('startDeviceSearch');
    let searchProgress = document.getElementById('searchProgress');
    startDeviceSearch.addEventListener('click', () => {
        let buttonClass = startDeviceSearch.className;
        startDeviceSearch.className += " collapse";
        searchProgress.className = "collapse show";

        // API-Start-Search
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrftoken);

        const http = new XMLHttpRequest();

        http.onreadystatechange = function () {
            let tag;
            let text;
            let element;
            if (this.readyState === 4 && this.status === 200) {
                if (this.response === 'none') {
                    document.getElementById('nodevicesfound').innerHTML = "Keine Geräte gefunden.";
                } else {

                    const data = JSON.parse(this.response);

                    tag = document.createElement("p");
                    text = document.createTextNode("Gefundene Geräte: ");
                    tag.appendChild(text);
                    element = document.getElementById("foundDevices");
                    element.appendChild(tag);

                    for (var prop in data) {

                        tag = document.createElement("p");

                        text = document.createTextNode(data[prop].manufacturername + ", " + data[prop].name);
                        tag.appendChild(text);
                        const node = document.getElementById("plusimg");
                        node.setAttribute("style", "height:25px; float: right");
                        const clone = node.cloneNode(true);
                        tag.appendChild(clone);
                        element = document.getElementById("foundDevices");
                        element.appendChild(tag);

                    }
                }
            }
        }

        http.open('POST', '/startsearch/');
        http.send(formData);

        // Progress-Bar
        let i = 0;
        document.getElementById('searchText').innerHTML = 'Suche läuft';

        const searchCounter = setInterval(function () {
            i++;
            if (i < 101) {
                document.getElementById('searchProgressBar').style.width = i + '%';
                const progressTime = Math.ceil((180 - (i * 1.8)) / 60);
                document.getElementById('searchText').innerHTML = 'Suche läuft noch ' + progressTime + " Minuten";
            } else {
                clearInterval(searchCounter);
                startDeviceSearch.className = buttonClass;
                document.getElementById('searchText').innerHTML = 'Suche beendet';
            }
        }, 1800);
    });
});

function lightOnOff(state, deviceId) {
    console.log("aha thats it", state);
    let formData = new FormData();
    formData.append('lightID', deviceId);
    formData.append('state', state);
    formData.append('csrfmiddlewaretoken', csrftoken);


    // TODO: @Niklas warum zwei Requests?
    const http = new XMLHttpRequest();
    http.open('POST', '/turnonoff/');
    http.send(formData);
    const http2 = new XMLHttpRequest();
    http2.open('POST', '/turnonoff/');
    http2.send(formData);

    let data = JSON.parse(window.localStorage.getItem('devices'))
    data[deviceId]['on'] = state;
    window.localStorage.setItem('devices', JSON.stringify(data));
}

function loadDeviceDataToModal(deviceId) {
    let devices = JSON.parse(window.localStorage.getItem("devices"));

    if (devices.hasOwnProperty(deviceId)) {
        let currentDevice = devices[deviceId];

        deviceControlModalSwitch.checked = currentDevice['on'];
        colorPicker.color.hue = currentDevice['hue'];
        colorPicker.color.saturation = currentDevice['saturation'];
        deviceControlModalBrightnessSlider.value = currentDevice['brightness'];
        deviceControlModalBrightnessDisplay.innerText = currentDevice['brightness'] + ' %';
        deviceControlModalLabel.innerText = currentDevice['name'] + ' ' + 'Hue: ' + currentDevice['hue'] + ' Sat: ' + currentDevice['saturation'];
        deviceControlModal.dataset['deviceId'] = currentDevice['id'];
        deviceControlModal.dataset['deviceName'] = currentDevice['name'];

        return 0;
    } else {
        return null;
    }
}

function saveDeviceDataToLocalStorage(deviceId) {
    let devices = JSON.parse(window.localStorage.getItem('devices'));

    if (devices.hasOwnProperty(deviceId)) {
        devices[deviceId]['on'] = deviceControlModalSwitch.checked;
        devices[deviceId]['hue'] = colorPicker.color.hue;
        devices[deviceId]['saturation'] = colorPicker.color.saturation;
        devices[deviceId]['brightness'] = deviceControlModalBrightnessSlider.value;

        window.localStorage.setItem('devices', JSON.stringify(devices));

        document.getElementById('switchLight-' + deviceId.toString()).checked = devices[deviceId]['on'];

        return 0;
    } else {
        return null;
    }
}
