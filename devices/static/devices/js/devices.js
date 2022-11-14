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

       const http = new XMLHttpRequest();
       http.open('POST', '/sethue/');
       http.send(formData);
});

var headerbg2 = document.getElementById("modalHeader2");
var outputHue2 = document.getElementById("modalLight2Label");
outputHue2.innerHTML = 'Lampe 2'

colorPicker2.on('color:change', function(color){
 console.log(color.hue);
 console.log(color.saturation);
 headerbg2.style.backgroundColor = color.hexString;
 outputHue2.innerHTML ='Lampe 2 ' + 'Hue: ' + color.hue + ' Sat: ' + color.saturation;

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


var slider = document.getElementById("customBrightness1");
var output = document.getElementById("color1");
output.innerHTML = slider.value + '%';

    }

    console.log("bye");

// Licht an / aus
let switchLight1 = document.getElementById('switchLight1');
let switchModalLight1 = document.getElementById('switchModalLight1');
let switchModalLight2 = document.getElementById('switchModalLight2');
let switchLight2 = document.getElementById('switchLight2');
let switchModalPlug1 = document.getElementById('switchModalPlug1');
let switchPlug1 = document.getElementById('switchPlug1');


switchLight1.addEventListener('change', function(){lightOnOff(switchLight1.checked, 2); switchModalLight1.checked = switchLight1.checked;});
switchLight2.addEventListener('change', function(){lightOnOff(switchLight2.checked, 5); switchModalLight2.checked = switchLight2.checked;});
switchPlug1.addEventListener('change', function(){lightOnOff(switchPlug1.checked, 3); switchModalPlug1.checked = switchPlug1.checked;});
switchModalLight1.addEventListener('change', function(){lightOnOff(switchModalLight1.checked, 2); switchLight1.checked = switchModalLight1.checked;});
switchModalLight2.addEventListener('change', function(){lightOnOff(switchModalLight2.checked, 5); switchLight2.checked = switchModalLight2.checked;});
switchModalPlug1.addEventListener('change', function(){lightOnOff(switchModalPlug1.checked, 3); switchPlug1.checked = switchModalPlug1.checked;});

function lightOnOff(state, lightID){
    let formData = new FormData();
    formData.append('lightID', lightID);
    formData.append('state', state);
    formData.append('csrfmiddlewaretoken', csrftoken);

    const http = new XMLHttpRequest();
    http.open('POST', '/turnonoff/');
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
 // Suche Geräte
let startDeviceSearch = document.getElementById('startDeviceSearch');
let searchProgress = document.getElementById('searchProgress');
startDeviceSearch.addEventListener('click', function(){
    let buttonClass = startDeviceSearch.className;
    startDeviceSearch.className += " collapse";
    searchProgress.className = "collapse show";
    // API-Start-Search
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrftoken);

    const http = new XMLHttpRequest();

    http.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
           if (this.response == 'none'){
               document.getElementById('nodevicesfound').innerHTML = "Keine Geräte gefunden.";
           }else {

               var data = JSON.parse(this.response);

               var tag = document.createElement("p");
               var text = document.createTextNode("Gefundene Geräte: ");
               tag.appendChild(text);
               var element = document.getElementById("foundDevices");
               element.appendChild(tag);

               for (var prop in data) {

                   var tag = document.createElement("p");

                   var text = document.createTextNode(data[prop].manufacturername + ", " + data[prop].name);
                   tag.appendChild(text);
                   const node = document.getElementById("plusimg");
                   node.setAttribute("style", "height:25px; float: right");
                   const clone = node.cloneNode(true);
                   tag.appendChild(clone);
                   var element = document.getElementById("foundDevices");
                   element.appendChild(tag);

               }
           }
        }
    }

    http.open('POST', '/startsearch/');
    http.send(formData);


    // Progress-Bar
    var i = 0;
    document.getElementById('searchText').innerHTML = 'Suche läuft';

    var searchCounter = setInterval(function(){
      i++;
      if (i < 101){
        document.getElementById('searchProgressBar').style.width = i+'%';
        var progressTime = Math.ceil((180 - (i * 1.8)) / 60);
        document.getElementById('searchText').innerHTML = 'Suche läuft noch ' + progressTime + " Minuten";
      } else {
          clearInterval(searchCounter);
          startDeviceSearch.className = buttonClass;
          document.getElementById('searchText').innerHTML = 'Suche beendet';
      }
    }, 1800);
});
