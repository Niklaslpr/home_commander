let favoritedevices;
let colorPicker;
let deviceControlModal;
let deviceControlModalHeader;
let deviceControlModalLabel;
let deviceControlModalSwitch;
let deviceControlModalBrightnessSlider;
let deviceControlModalBrightnessDisplay;
let deviceToFav
let deviceToFavLabel
let deviceToFavText

$(document).ready(() => {
    createFavoriteGroup();
    colorPicker = new iro.ColorPicker('#device-control-modal-colorpicker', {
    borderWidth: 2,
    layout: [
        {
            component: iro.ui.Wheel,
        },
    ]
    });

    deviceControlModal = document.getElementById('device-control-modal');
    deviceControlModalHeader = document.getElementById('device-control-modal-header');
    deviceControlModalLabel = document.getElementById('device-control-modal-label');
    // deviceControlModalLabel.innerHTML = 'Lampe XXX';

    deviceToFav = document.getElementById('deviceToFav');
    deviceToFavLabel = document.getElementById('deviceToFavLabel');
    deviceToFavText = document.getElementById('deviceToFavText');

    deviceToFav.addEventListener('click', function(){
    if (deviceToFav.checked == true){
        deviceToFavLabel.style.backgroundColor = 'var(--tertiary-color)';
        deviceToFavText.innerHTML = 'Von Favoriten entfernen';

        let formData = new FormData();
        formData.append('deviceId', deviceControlModal.dataset['deviceId']);
        formData.append('csrfmiddlewaretoken', csrftoken);

        let http = new XMLHttpRequest();
        http.open('POST', './addDeviceToFavorites/');
        http.send(formData);

    } else {
        deviceToFavLabel.style.backgroundColor = 'white';
        deviceToFavText.innerHTML = 'Zu Favoriten hinzufügen';

        let formData = new FormData();
        formData.append('deviceId', deviceControlModal.dataset['deviceId']);
        formData.append('csrfmiddlewaretoken', csrftoken);

        let http = new XMLHttpRequest();
        http.open('POST', './deleteDeviceFromFavorites/');
        http.send(formData);
    }
})

        colorPicker.on('color:change', function (color) {
            if (deviceControlModal.classList.contains('show') == true) {
                console.log(deviceControlModal.classList.contains('show'));
                console.log('Textfarbe: ' + color.hue);
                console.log('Saturation: ' + color.saturation);

                deviceControlModalHeader.style.backgroundColor = color.hexString;
                deviceControlModalLabel.innerText = deviceControlModal.dataset['deviceName'];

                if (color.saturation > 55 && color.hue > 212){
                    deviceControlModalLabel.style.color = 'white';
                } else {deviceControlModalLabel.style.color = 'black';}

                let hue = Math.round(color.hue * 65535 / 360);
                let sat = Math.round(color.saturation * 2.55);

                let formData = new FormData();
                formData.append('hue', hue);
                formData.append('sat', sat);
                formData.append('deviceId', deviceControlModal.dataset['deviceId']);
                formData.append('csrfmiddlewaretoken', csrftoken);

                const http = new XMLHttpRequest();
                http.open('POST', './sethue/');
                http.send(formData);
            }
        })


    deviceControlModalSwitch = document.getElementById('device-control-modal-switch');
    deviceControlModalBrightnessSlider = document.getElementById("device-control-modal-brightness");
    deviceControlModalBrightnessDisplay = document.getElementById("device-control-modal-brightness-display");
    deviceControlModalBrightnessDisplay.innerText = deviceControlModalBrightnessSlider.value + ' %';

    deviceControlModalSwitch.addEventListener('change', function(){
        lightOnOff(deviceControlModalSwitch.checked, deviceControlModal.dataset['deviceId']);
    })

    deviceControlModalBrightnessSlider.oninput = function () {
        let bri = this.value;
        deviceControlModalBrightnessDisplay.innerText = bri + '%';   // Update the current slider value (each time you drag the slider handle)
        bri = Math.round(bri * 2.55);

        // sending Brightness
        let formData = new FormData();
        formData.append('bri', bri);
        formData.append('deviceId', deviceControlModal.dataset['deviceId']);
        formData.append('csrfmiddlewaretoken', csrftoken);

        let http = new XMLHttpRequest();
        http.open('POST', './setbri/');
        http.send(formData);

        // http = new XMLHttpRequest();
        // http.open('POST', '/sethue/');
        // http.send(formData);
    }

    // Suche Geräte
    let startDeviceSearch = document.getElementById('startDeviceSearch');
    let searchProgress = document.getElementById('searchProgress');
})

function createFavoriteGroup(){
    let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrftoken);

        let http = new XMLHttpRequest();

        http.onreadystatechange = function (){
             if (this.readyState === 4 && this.status === 200){
                 favoritedevices = this.response;
                 console.log(favoritedevices);
                 if (favoritedevices == ""){
                     document.getElementById("favoritedevices").innerHTML = "Es wurde noch kein Gerät als Favorit gesetzt.";
                 }
                 else{

                 }
             }
        }

        http.open('POST', './createFavoriteGroup/');
        http.send(formData);

}

function lightOnOff(state, deviceId) {
    console.log("aha thats it", state);
    let formData = new FormData();
    formData.append('lightID', deviceId);
    formData.append('state', state);
    formData.append('csrfmiddlewaretoken', csrftoken);


    const http = new XMLHttpRequest();
    http.open('POST', './turnonoff/');
    http.send(formData);


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
        deviceControlModalLabel.innerText = currentDevice['name'];
        if (currentDevice['has_color'] == true ){
            deviceControlModalHeader.style.backgroundColor = 'hsl(' + currentDevice['hue'] + ', 100%, 50%)';
        } else { deviceControlModalHeader.style.backgroundColor = 'hsl(' + currentDevice['hue'] + ', 100%, 100%)';}
        deviceControlModal.dataset['deviceId'] = currentDevice['id'];
        deviceControlModal.dataset['deviceName'] = currentDevice['name'];


        // Check, if Device is in Favorites
        let formData = new FormData();
        formData.append('deviceId', deviceId);
        formData.append('csrfmiddlewaretoken', csrftoken);
        let http = new XMLHttpRequest();

         http.onreadystatechange = function (){
             if (this.readyState === 4 && this.status === 200){
                 if (this.response == "True"){
                     deviceToFav.checked = true;
                     deviceToFavLabel.style.backgroundColor = 'var(--tertiary-color)';
                     deviceToFavText.innerHTML = 'Von Favoriten entfernen';
                 } else{
                     deviceToFav.checked = false;
                     deviceToFavLabel.style.backgroundColor = 'white';
                     deviceToFavText.innerHTML = 'Zu Favoriten hinzufügen';
                 }
             }
        }

        http.open('POST', './isDeviceinFavorites/');
        http.send(formData);



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


