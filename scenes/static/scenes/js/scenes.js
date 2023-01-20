// let sceneDeviceControlColorPicker;
// let sceneDeviceControlModal;
// let sceneDeviceControlModalHeader;
// let sceneDeviceControlModalLabel;
// let sceneDeviceControlModalSwitch;
// let sceneDeviceControlModalBrightnessSlider;
// let sceneDeviceControlModalBrightnessDisplay;

let deviceList;
let selectedDevices;
let updateSceneName;
let sceneControlModal;
let sceneControlModalHeader;
let selectedIcon2;
let icons2;
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
    getAllGroups();

    groupControlModal = document.getElementById("group-control-modal")
    sceneControlModal = document.getElementById("scene-control-modal")
    sceneControlModalHeader = document.getElementById("scene-control-modal-header");
    sceneControlModalLabel = document.getElementById("scene-control-modal-label");
    updateSceneName = document.getElementById("updateSceneName");

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

function createScene() {
    let groupId = null;

    for (let dev of document.getElementById('new-scene-group-list').children) {
        if (document.getElementById("checkInNewScene-" + dev.dataset["groupId"]).style.backgroundColor === 'var(--tertiary-color)') {
            groupId = dev.dataset["groupId"];
        }
    }

    $.ajax({
        url: './scene_change/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'create',
            group_id: groupId.toString(),
            attributes: {'name': document.getElementById('inputSceneName').value.toString()},
            features: {'icon': selectedIcon2.toString()},
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.info(data);

            location.reload();

            // $.ajax({
            //     url: './scene_change/',
            //     type: 'POST',
            //     data: {
            //         csrfmiddlewaretoken: getCookie('csrftoken'),
            //         action: 'update',
            //         scene_id: data.response[0]["success"]["id"],
            //         attributes: {'lights': lights}
            //     },
            //     headers: {
            //         'Content-type': 'application/json', 'Accept': 'text/plain',
            //         'X-CSRFToken': getCookie('csrftoken')
            //     },
            //     dataType: 'json',
            //     mode: 'same-origin',
            //     success: function (data) {
            //         console.info(data);
            //
            //         location.reload();
            //     }
            // });
        }
    });
}

function deleteScene() {
    $.ajax({
        url: './scene_change/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'delete',
            group_id: sceneControlModal.dataset['groupId'],
            scene_id: sceneControlModal.dataset['sceneId']
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.info(data);

            location.reload();
        }
    });
}

function saveSceneState() {
    $.ajax({
        url: './scene_change/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'delete',
            group_id: sceneControlModal.dataset['groupId'],
            scene_id: sceneControlModal.dataset['sceneId'],
            states: {"all": "store_current_states"}
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.info(data);

            location.reload();
        }
    });
}

function loadSceneDataToModal(sceneId) {
    let scenes = JSON.parse(window.localStorage.getItem("scenes"));
    document.getElementById('deviceEditToggle').hidden = true;

    if (scenes.hasOwnProperty(sceneId)) {
        let currentScene = scenes[sceneId];

        document.getElementById('scene-control-device-list').innerHTML = '';

        sceneControlModal.dataset['sceneId'] = currentScene['id'];
        sceneControlModal.dataset['sceneName'] = currentScene['name'];
        sceneControlModal.dataset['groupId'] = currentScene['group_id'];
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

        let groups = JSON.parse(window.localStorage.getItem("groups"));

        $.ajax({
                url: './kit/group-item3',
                type: 'get',
                data: {
                    "csrfmiddlewaretoken": getCookie('csrftoken'),
                    "group-id2": currentScene['group_id'].toString(),
                    "group-name2": groups[currentScene['group_id']]['name'],
                    "group-icon2": groups[currentScene['group_id']]['icon'],
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

function getAllGroups() {
    document.getElementById('new-scene-group-list').innerHTML = "";
    // document.getElementById('edit-scene-group-list').innerHTML = "";

    $.ajax({
        url: '/groups/group_info/all',
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

            let groupsJson = {};
            for (let entry of data.groupsCollection.reverse()) {
                groupsJson[entry['id']] = entry;
                if (entry['name'].startsWith('room_')) {

                } else {
                    $.ajax({
                        url: './kit/group-item2',
                        type: 'get',
                        data: {
                            "csrfmiddlewaretoken": getCookie('csrftoken'),
                            "group-id": entry['id'].toString(),
                            "group-name": entry['name'].toString(),
                            "group-icon": entry['icon'].toString(),
                        },
                        headers: {
                            'Content-type': 'application/json', 'Accept': 'text/plain',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        dataType: 'json',
                        mode: 'same-origin'
                    }).always((data) => {
                        if (data.readyState === 4 && data.status === 200) {
                            document.getElementById('new-scene-group-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                        }
                    });
                }
            }

            window.localStorage.setItem('groups', JSON.stringify(groupsJson));
        }
    });

    // let devices = JSON.parse(window.localStorage.getItem("devices"));
    // document.getElementById('new-scene-device-list').innerHTML = "";
    // document.getElementById('edit-scene-device-list').innerHTML = "";
    // for (let entry in devices) {
    //     $.ajax({
    //         url: './kit/device-item2',
    //         type: 'get',
    //         data: {
    //             "csrfmiddlewaretoken": getCookie('csrftoken'),
    //             "device-id": devices[entry]['id'].toString(),
    //             "device-name": devices[entry]['name'].toString(),
    //             "device-type": devices[entry]['type'].toString(),
    //         },
    //         headers: {
    //             'Content-type': 'application/json', 'Accept': 'text/plain',
    //             'X-CSRFToken': getCookie('csrftoken')
    //         },
    //         dataType: 'json',
    //         mode: 'same-origin'
    //     }).always((data) => {
    //         if (data.readyState === 4 && data.status === 200) {
    //             document.getElementById('new-scene-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
    //         }
    //     });
    //     $.ajax({
    //         url: './kit/device-item3',
    //         type: 'get',
    //         data: {
    //             "csrfmiddlewaretoken": getCookie('csrftoken'),
    //             "device-id2": devices[entry]['id'].toString(),
    //             "device-name2": devices[entry]['name'].toString(),
    //             "device-type2": devices[entry]['type'].toString(),
    //         },
    //         headers: {
    //             'Content-type': 'application/json', 'Accept': 'text/plain',
    //             'X-CSRFToken': getCookie('csrftoken')
    //         },
    //         dataType: 'json',
    //         mode: 'same-origin'
    //     }).always((data) => {
    //         if (data.readyState === 4 && data.status === 200) {
    //             document.getElementById('scene-control-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
    //         }
    //     });
    // }
}

function set_background_color(id) {
    for (let dev of document.querySelectorAll('.checkInNewScene')) {
        dev.style.backgroundColor = "transparent";
    }

    if (document.getElementById(id).style.backgroundColor === 'var(--tertiary-color)') {
        document.getElementById(id).style.backgroundColor = "transparent";
    } else {
        document.getElementById(id).style.backgroundColor = 'var(--tertiary-color)';
    }
}

function activateScene() {
    $.ajax({
        url: './scene_change/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'update',
            scene_id: sceneControlModal.dataset['sceneId'],
            group_id: sceneControlModal.dataset['groupId'],
            states: {'on': 'y'}
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.info(data);
            console.log("yes sir it hat wat jetan");
        }
    });
}

function getIconId2(IconId) {
    icons2 = ["collection.svg", "house.svg", "controller.svg", "archive.svg", "book.svg", "wrench.svg", "brezel.png", "plugin.svg", "robot.svg"];
    for (const tmp in icons2) {
        document.getElementById(icons2[tmp]).style.backgroundColor = "transparent";
    }
    selectedIcon2 = IconId;
    document.getElementById(selectedIcon2).style.backgroundColor = "var(--tertiary-color)";
}

function saveIcon2() {
    console.log("aba hier oda was");
    document.getElementById('modal-body-edit').hidden = true;
    document.getElementById('modal-body-normal').hidden = false;

    $.ajax({
        url: './scene_change/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'update',
            scene_id: sceneControlModal.dataset['sceneId'],
            group_id: sceneControlModal.dataset['groupId'],
            features: {'icon': selectedIcon2} // TODO: CHANGE
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.info(data);
            console.log("yes sir it hat wat jetan");
            location.reload();
        }
    });
    // selectedDevices = [];
    //
    //
    // for (let entry of deviceList) {
    //     if (document.getElementById("checkInEditGroup-" + entry).style.backgroundColor === 'var(--tertiary-color)') {
    //         selectedDevices.push(entry);
    //     }
    // }
    // let sceneName = updateSceneName.value;
    //
    //
    // console.log("Selected Devices: " + selectedDevices);
    // console.log(sceneControlModal.dataset['sceneId']);
    // console.log(selectedIcon2);
    // console.log(sceneName);
    //
    // let formData = new FormData();
    // formData.append('sceneId', sceneControlModal.dataset['sceneId']);
    // formData.append('sceneName', updateSceneName.value);
    // formData.append('selectedDevices', selectedDevices);
    // formData.append('selectedIcon', selectedIcon2);
    // formData.append('csrfmiddlewaretoken', csrftoken);
    // const http = new XMLHttpRequest();
    //
    // http.onreadystatechange = function () {
    //     if (this.readyState == 4 && this.status == 200) {
    //         location.reload();
    //     } else {
    //         console.log("Fehler beim Erstellen der Gruppe");
    //     }
    // }
    // http.open('POST', './updategroup/');
    // http.send(formData);
}

function setIcon2(IconId) {
    icons = ["tmp_collection.svg", "tmp_house.svg", "tmp_controller.svg", "tmp_archive.svg", "tmp_book.svg", "tmp_wrench.svg", "tmp_brezel.png", "tmp_plugin.svg", "tmp_robot.svg"];
    for (const tmp in icons) {
        document.getElementById(icons[tmp]).style.backgroundColor = "transparent";
    }
    document.getElementById(IconId).style.backgroundColor = "var(--tertiary-color)";
    const tmp_array = IconId.split("_");
    selectedIcon2 = tmp_array[1];
}

function set_color_background_devices() {
    document.getElementById("list-device-item-" + deviceControlModal.dataset["deviceId"]).style.backgroundColor = deviceControlModalHeader.style.backgroundColor;
}


function saveSceneName() {
    console.log("do it");
    $.ajax({
        url: './scene_change/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'update',
            scene_id: sceneControlModal.dataset['sceneId'],
            group_id: sceneControlModal.dataset['groupId'],
            attributes: {'name': document.getElementById('updateSceneName').value} // TODO: CHANGE
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.info(data);
            console.log("yes sir it hat wat jetan");
            location.reload();
        }
    });
}
