// let sceneDeviceControlColorPicker;
// let sceneDeviceControlModal;
// let sceneDeviceControlModalHeader;
// let sceneDeviceControlModalLabel;
// let sceneDeviceControlModalSwitch;
// let sceneDeviceControlModalBrightnessSlider;
// let sceneDeviceControlModalBrightnessDisplay;

let sceneControlModal;
let sceneControlModalHeader;
let sceneControlModalLabel;

$(document).ready(() => {
    // sceneDeviceControlColorPicker = new iro.ColorPicker('#device-control-modal-colorpicker', {
    //     borderWidth: 2,
    //     layout: [
    //         {
    //             component: iro.ui.Wheel,
    //         },
    //     ]
    // });

    sceneControlModal = document.getElementById("scene-control-modal")
    sceneControlModalHeader = document.getElementById("scene-control-modal-header");
    sceneControlModalLabel = document.getElementById("scene-control-modal-label");

    // sceneDeviceControlModal = document.getElementById("device-control-modal")
    // sceneDeviceControlModalHeader = document.getElementById("device-control-modal-header");
    // sceneDeviceControlModalLabel = document.getElementById("device-control-modal-label");

    // sceneDeviceControlColorPicker.on('color:change', function (color) {
    //     console.log(color.hue);
    //     console.log(color.saturation);
    //     sceneDeviceControlModalHeader.style.backgroundColor = color.hexString;
    //     sceneDeviceControlModalLabel.innerHTML = sceneDeviceControlModal.dataset['deviceName'] + 'Hue: ' + color.hue + ' Sat: ' + color.saturation;
    // });
    // groupControlModalBrightnessSlider = document.getElementById("group-control-modal-brightness");
    // groupControlModalBrightnessDisplay = document.getElementById("group-control-modal-brightness-display");
    // groupControlModalBrightnessDisplay.innerHTML = groupControlModalBrightnessSlider.value + '%';

// Update the current slider value (each time you drag the slider handle)
//     groupControlModalBrightnessSlider.oninput = function () {
//         groupControlModalBrightnessDisplay.innerHTML = this.value + '%';
//     }

// let switchGroup1 = document.getElementById('switchGroup1');
//     groupControlModalSwitch = document.getElementById('group-control-modal-switch');
//
//     let newGroupName = document.getElementById('inputGroupName');
//
//     document.getElementById('createGroup').addEventListener('click', function () {
//         let formData = new FormData();
//         formData.append('groupName', newGroupName.value);
//         formData.append('csrfmiddlewaretoken', csrftoken);
//
//         const http = new XMLHttpRequest();
//
//         http.onreadystatechange = function () {
//             if (this.readyState == 4 && this.status == 200) {
//                 location.reload();
//             }
//         }
//
//         http.open('POST', '/creategroup/');
//         http.send(formData);
//
//
//     })
});

function loadSceneDataToModal(sceneId) {
    let scenes = JSON.parse(window.localStorage.getItem("scenes"));
    console.log(scenes);

    if (scenes.hasOwnProperty(sceneId)) {
        let currentScene = scenes[sceneId];

        document.getElementById('scene-control-device-list').innerHTML = '';

        sceneControlModal.dataset['sceneId'] = currentScene['id'];
        sceneControlModal.dataset['sceneName'] = currentScene['name'];
        sceneControlModalLabel.innerText = currentScene['name'];

        let deviceType = null;
        for (let entry of currentScene["lights"]) {
            $.ajax({
                url: './kit/device-item',
                type: 'get',
                data: {
                    "csrfmiddlewaretoken": getCookie('csrftoken'),
                    "device-id": entry['id'].toString(),
                    "device-name": entry['name'].toString(),
                    // "device-type": entry['type'].toString(),
                },
                headers: {
                    'Content-type': 'application/json', 'Accept': 'text/plain',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                dataType: 'json',
                mode: 'same-origin'
            }).always((data) => {
                if (data.readyState === 4 && data.status === 200) {
                    document.getElementById('scene-control-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                }
            });
        }

        // console.log('currentGroup', currentGroup);
        // groupControlModalSwitch.checked = currentGroup['on'];
        // groupControlColorPicker.color.hue = currentGroup['hue'];
        // groupControlColorPicker.color.saturation = currentGroup['saturation'];
        // groupControlModalBrightnessSlider.value = currentGroup['brightness'];
        // groupControlModalBrightnessDisplay.innerText = currentGroup['brightness'] + ' %';
        // groupControlModalLabel.innerText = currentGroup['name'] + ' ' + 'Hue: ' + currentGroup['hue'] + ' Sat: ' + currentGroup['saturation'];

        return 0;
    } else {
        return null;
    }
}

function saveSceneDataToLocalStorage(sceneId) {
    let scenes = JSON.parse(window.localStorage.getItem('scenes'));

    // TODO: korrektieren :D
    if (scenes.hasOwnProperty(sceneId)) {
        // scenes[sceneId]['on'] = sceneDeviceControlModalSwitch.checked;
        // scenes[sceneId]['hue'] = sceneDeviceControlColorPicker.color.hue;
        // scenes[sceneId]['saturation'] = sceneDeviceControlColorPicker.color.saturation;
        // scenes[sceneId]['brightness'] = sceneDeviceControlModalBrightnessSlider.value;

        window.localStorage.setItem('scenes', JSON.stringify(scenes));

        return 0;
    } else {
        return null;
    }
}
