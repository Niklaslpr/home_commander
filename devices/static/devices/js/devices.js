let colorPicker;
let deviceControlModal;
let deviceControlModalHeader;
let deviceControlModalLabel;
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

        const http = new XMLHttpRequest();
        http.open('POST', '/setbri/');
        http.send(formData);

    }

    console.log("bye");

// Licht an / aus
//     let switchLight1 = document.getElementById('switchLight1');
//     let switchModalLight1 = document.getElementById('switchModalLight1');
//
//     switchLight1.addEventListener('change', function () {
//         lightOnOff(switchLight1.checked);
//         switchModalLight1.checked = switchLight1.checked;
//     });
//     switchModalLight1.addEventListener('change', function () {
//         lightOnOff(switchModalLight1.checked);
//         switchLight1.checked = switchModalLight1.checked;
//     });

});

function lightOnOff(state) {
    let formData = new FormData();
    formData.append('state', state);
    formData.append('csrfmiddlewaretoken', csrftoken);

    const http = new XMLHttpRequest();
    http.open('POST', '/devices/');
    http.send(formData);
    const http2 = new XMLHttpRequest();
    http2.open('POST', '/turnonoff/');
    http2.send(formData);
}

function loadDeviceDataToModal(deviceId) {
    console.log("huhu");
    let devices = JSON.parse(window.localStorage.getItem("devices"));

    if (devices.hasOwnProperty(deviceId)) {
        let currentDevice = devices[deviceId];

        console.log("currentDevice", currentDevice);

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

        return 0;
    } else {
        return null;
    }
}
