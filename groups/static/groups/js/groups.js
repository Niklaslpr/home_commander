let groupControlColorPicker;
let groupControlModal;
let groupControlModalHeader;
let groupControlModalLabel;
let groupControlModalSwitch;
let groupControlModalBrightnessSlider;
let groupControlModalBrightnessDisplay;
let newGroupName;
let selectedIcon;
let icons;
let deleteGroupButton;
let deviceList;
let selectedDevices;
let updateGroupName;


$(document).ready(() => {

    get_all_devices();

    groupControlColorPicker = new iro.ColorPicker('#group-control-modal-colorpicker', {
        borderWidth: 2,
        layout: [
            {
                component: iro.ui.Wheel,
            },
        ]
    });

    groupControlModal = document.getElementById("group-control-modal")
    groupControlModalHeader = document.getElementById("group-control-modal-header");
    groupControlModalLabel = document.getElementById("group-control-modal-label");
    updateGroupName = document.getElementById("updateGroupName");
// groupControlModalLabel.innerHTML = 'Gruppe XXX';

    groupControlModal.addEventListener('hide.bs.modal', function(){
            for (let x of deviceList){
                document.getElementById("checkInEditGroup-" + x).style.backgroundColor = "transparent";
            }
            document.getElementById('group-control-modal-switch').hidden = false;
            document.getElementById('group-control-modal-label').hidden = false;
            document.getElementById('updateGroupName').hidden = true;
            document.getElementById('modal-body-edit').hidden = true;
            document.getElementById('modal-body-normal').hidden = false;
        })


    groupControlColorPicker.on('color:change', function (color) {
        if (groupControlModal.classList.contains('show') === true) {
            console.log(color.hue);
            console.log(color.saturation);
            groupControlModalHeader.style.backgroundColor = color.hexString;
            if (color.saturation > 55 && color.hue > 212) {
                groupControlModalLabel.style.color = 'white';
            } else {
                groupControlModalLabel.style.color = 'black';
            }
            let hue = Math.round(color.hue * 65535 / 360);
            let sat = Math.round(color.saturation * 2.55);

            let formData = new FormData();
            formData.append('hue', hue);
            formData.append('sat', sat);
            formData.append('groupId', groupControlModal.dataset['groupId']);
            formData.append('csrfmiddlewaretoken', csrftoken);

            const http = new XMLHttpRequest();
            http.open('POST', './groupsethue/');
            http.send(formData);
        }
    });

    groupControlModalBrightnessSlider = document.getElementById("group-control-modal-brightness");
    groupControlModalBrightnessDisplay = document.getElementById("group-control-modal-brightness-display");
    groupControlModalBrightnessDisplay.innerHTML = groupControlModalBrightnessSlider.value + '%';

// Update the current slider value (each time you drag the slider handle)
    groupControlModalBrightnessSlider.oninput = function () {
        let bri = this.value;
        groupControlModalBrightnessDisplay.innerHTML = bri + '%';
        bri = Math.round(bri * 2.55);

        // sending Brightness
        let formData = new FormData();
        formData.append('bri', bri);
        formData.append('groupId', groupControlModal.dataset['groupId']);
        formData.append('csrfmiddlewaretoken', csrftoken);

        let http = new XMLHttpRequest();
        http.open('POST', './groupsetbri/');
        http.send(formData);

    }

// let switchGroup1 = document.getElementById('switchGroup1');
    groupControlModalSwitch = document.getElementById('group-control-modal-switch');

    let newGroupName = document.getElementById('inputGroupName');

    document.getElementById('createGroup').addEventListener('click', function () {
        // let formData = new FormData();
        // formData.append('groupName', newGroupName.value);
        // formData.append('csrfmiddlewaretoken', csrftoken);
        //
        // const http = new XMLHttpRequest();
        //
        // http.onreadystatechange = function () {
        //     if (this.readyState == 4 && this.status == 200) {
        //         location.reload();
        //     }
        // }
        //
        // http.open('POST', '/creategroup/');
        // http.send(formData);

        $.ajax({
            url: './group_change/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                action: 'create',
                attributes: {'name': newGroupName.value},
                features: {'icon': selectedIcon}
            },
            headers: {
                'Content-type': 'application/json', 'Accept': 'text/plain',
                'X-CSRFToken': getCookie('csrftoken')
            },
            dataType: 'json',
            mode: 'same-origin',
            success: function (data) {
                console.info(data);

                // let groups = JSON.parse(window.localStorage.getItem('groups'))
                // groups[data.group_id]['name'] = data.name;
                // window.localStorage.setItem('groups', JSON.stringify(groups));
            }
        }).always((data) => {
            if (data.readyState === 4 && data.status === 200) {
                location.reload();
            }
        });
    })
    deleteGroupButton = document.getElementById("deleteGroup");
    deleteGroupButton.addEventListener('click', function () {

        if (confirm('Bist Du sicher?')) {
            deleteGroup(groupControlModal.dataset['groupId'], groupControlModal.dataset['groupName']);
        }
    })

});

// switchGroup1.addEventListener('change', function(){groupOnOff(switchGroup1.checked, 1); groupControlModalSwitch.checked = switchGroup1.checked;});
// groupControlModalSwitch.addEventListener('change', function(){groupOnOff(groupControlModalSwitch.checked, 1); switchGroup1.checked = groupControlModalSwitch.checked;});

// Group ON / OFF
function groupOnOff(state, groupID) {
    document.getElementById("switchGroup-" + groupID).checked = state;
    let formData = new FormData();
    formData.append('groupID', groupID);
    formData.append('state', state);
    formData.append('csrfmiddlewaretoken', csrftoken);

    const http = new XMLHttpRequest();
    http.open('POST', './grouponoff/');
    http.send(formData);
}

function loadGroupDataToModal(groupId) {
    let groups = JSON.parse(window.localStorage.getItem("groups"));
    console.log(groups);

    if (groups.hasOwnProperty(groupId)) {
        let currentGroup = groups[groupId];

        document.getElementById('group-control-device-list').innerHTML = '';

        groupControlModal.dataset['groupId'] = currentGroup['id'];
        groupControlModal.dataset['groupName'] = currentGroup['name'];


        let deviceType = null;
        for (let entry of currentGroup["devices"]) {
            $.ajax({
                url: './kit/device-item',
                type: 'get',
                data: {
                    "csrfmiddlewaretoken": getCookie('csrftoken'),
                    "device-id": entry['id'].toString(),
                    "device-name": entry['name'].toString(),
                    "device-type": entry['type'].toString(),
                },
                headers: {
                    'Content-type': 'application/json', 'Accept': 'text/plain',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                dataType: 'json',
                mode: 'same-origin'
            }).always((data) => {
                if (data.readyState === 4 && data.status === 200) {

                    document.getElementById('group-control-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                }
            });

            set_background_color('checkInEditGroup-' + entry['id']);
            set_background_color('checkInNewGroup-' + entry['id']);
            $.ajax({
                url: '../devices/device_info/' + entry['id'],
                type: 'GET',
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    device_id: entry['id'],
                },
                headers: {
                    'Content-type': 'application/json', 'Accept': 'text/plain',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                dataType: 'json',
                mode: 'same-origin',
                success: function (data) {
                    document.getElementById("switchInGroup-" + data["id"]).checked = data["on"];
                }
            });

        }

        console.log('currentGroup', currentGroup);
        groupControlModalSwitch.checked = currentGroup['on'];
        groupControlColorPicker.color.hue = currentGroup['hue'];
        groupControlColorPicker.color.saturation = currentGroup['saturation'];
        groupControlModalBrightnessSlider.value = currentGroup['brightness'];
        groupControlModalBrightnessDisplay.innerText = currentGroup['brightness'] + ' %';
        groupControlModalLabel.innerText = currentGroup['name'];
        updateGroupName.value = currentGroup['name'];
        groupControlModalHeader.style.backgroundColor = 'hsl(' + currentGroup['hue'] + ', 100%, 50%)';

        return 0;
    } else {
        return null;
    }
}

function saveGroupDataToLocalStorage(groupId) {
    let groups = JSON.parse(window.localStorage.getItem('groups'));

    if (groups.hasOwnProperty(groupId)) {
        console.log("Ja");

        groups[groupId]['on'] = groupControlModalSwitch.checked;
        groups[groupId]['hue'] = groupControlColorPicker.color.hue;
        groups[groupId]['saturation'] = groupControlColorPicker.color.saturation;
        groups[groupId]['brightness'] = groupControlModalBrightnessSlider.value;

        window.localStorage.setItem('groups', JSON.stringify(groups));

        return 0;
    } else {
        return null;
    }
}

// setIcon for createGroup()
function setIcon(IconId) {
    icons = ["tmp_collection.svg", "tmp_house.svg", "tmp_controller.svg", "tmp_archive.svg", "tmp_book.svg", "tmp_wrench.svg", "tmp_brezel.png", "tmp_plugin.svg", "tmp_robot.svg"];
    for (const tmp in icons) {
        document.getElementById(icons[tmp]).style.backgroundColor = "transparent";
    }
    document.getElementById(IconId).style.backgroundColor = "var(--tertiary-color)";
    const tmp_array = IconId.split("_");
    selectedIcon = tmp_array[1];
}

function createGroup() {
    selectedDevices = [];
    newGroupName = document.getElementById('inputGroupName');
    console.log(newGroupName.value);
    console.log(selectedIcon);
    console.log(deviceList);

    for (let entry of deviceList) {
        if (document.getElementById("checkInGroup-" + entry).style.backgroundColor == 'var(--tertiary-color)') {
            selectedDevices.push(entry);
        }
    }
    console.log("Selected Devices: " + selectedDevices);

    let formData = new FormData();
    formData.append('groupName', newGroupName.value);
    formData.append('selectedDevices', selectedDevices);
    formData.append('csrfmiddlewaretoken', csrftoken);
    const http = new XMLHttpRequest();

    http.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            location.reload();
        } else {
            console.log("Fehler beim Erstellen der Gruppe");
        }
    }
    http.open('POST', './creategroup/');
    http.send(formData);

}


// getIconId for saveIcon()
function getIconId(IconId) {
    icons = ["collection.svg", "house.svg", "controller.svg", "archive.svg", "book.svg", "wrench.svg", "brezel.png", "plugin.svg", "robot.svg"];
    for (const tmp in icons) {
        document.getElementById(icons[tmp]).style.backgroundColor = "transparent";
    }
    selectedIcon = IconId;
    document.getElementById(selectedIcon).style.backgroundColor = "var(--tertiary-color)";
}

function saveIcon() {
    document.getElementById('modal-body-edit').hidden = true;
    document.getElementById('modal-body-normal').hidden = false;
    selectedDevices = [];


    for (let entry of deviceList) {
        if (document.getElementById("checkInGroup-" + entry).style.backgroundColor === 'var(--tertiary-color)') {
            selectedDevices.push(entry);
        }
    }
    let groupName = updateGroupName.value;



    console.log("Selected Devices: " + selectedDevices);
    console.log(groupControlModal.dataset['groupId']);
    console.log(selectedIcon);
    console.log(groupName);

    let formData = new FormData();
    formData.append('groupId', groupControlModal.dataset['groupId']);
    formData.append('groupName', updateGroupName.value);
    formData.append('selectedDevices', selectedDevices);
    formData.append('csrfmiddlewaretoken', csrftoken);
    const http = new XMLHttpRequest();

    http.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            location.reload();
        } else {
            console.log("Fehler beim Erstellen der Gruppe");
        }
    }
    http.open('POST', './updategroup/');
    http.send(formData);
}

function toggleEdit(isActive) {
    if (isActive) {
        document.getElementById('modal-body-edit').hidden = true;
        document.getElementById('modal-body-normal').hidden = false;
    } else {
        document.getElementById('modal-body-edit').hidden = false;
        document.getElementById('modal-body-normal').hidden = true;
    }
}

function deleteGroup(groupId, groupName){

    let formData = new FormData();
    formData.append('groupId', groupId);
    formData.append('groupName', groupName);
    formData.append('csrfmiddlewaretoken', csrftoken);
    let http = new XMLHttpRequest();
    http.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            location.reload();
        }
    }
    http.open('POST', './deletegroup/');
    http.send(formData);
}

function get_all_devices() {
    deviceList = [];
    document.getElementById('new-group-device-list').innerHTML = '';
    document.getElementById('edit-group-device-list').innerHTML = '';
    $.ajax({
        url: '../devices/device_info/all',
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
            for (let entry of data["devices"]) {
                deviceList.push(entry["id"].toString());


                $.ajax({
                    url: './kit/device-item2',
                    type: 'get',
                    data: {
                        "csrfmiddlewaretoken": getCookie('csrftoken'),
                        "device-id": entry['id'].toString(),
                        "device-name": entry['name'].toString(),
                        "device-type": entry['type'].toString(),
                    },
                    headers: {
                        'Content-type': 'application/json', 'Accept': 'text/plain',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    dataType: 'json',
                    mode: 'same-origin'
                }).always((data) => {
                    if (data.readyState === 4 && data.status === 200) {
                        document.getElementById('new-group-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                    }
                });
                $.ajax({
                    url: './kit/device-item3',
                    type: 'get',
                    data: {
                        "csrfmiddlewaretoken": getCookie('csrftoken'),
                        "device-id2": entry['id'].toString(),
                        "device-name2": entry['name'].toString(),
                        "device-type2": entry['type'].toString(),
                    },
                    headers: {
                        'Content-type': 'application/json', 'Accept': 'text/plain',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    dataType: 'json',
                    mode: 'same-origin'
                }).always((data) => {
                    if (data.readyState === 4 && data.status === 200) {
                        document.getElementById('edit-group-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                    }
                });
            }
        }
    });
}

function set_background_color(id) {
    if (document.getElementById(id).style.backgroundColor == 'var(--tertiary-color)') {
        document.getElementById(id).style.backgroundColor = "transparent";
    } else {
        document.getElementById(id).style.backgroundColor = 'var(--tertiary-color)';
    }
}

function deviceOnOff(state, deviceId){
    $.ajax({
        url: '../devices/device_change/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'update',
            device_id: deviceId,
            type: "light", // TODO: dynamisch
            state: {'on': state}
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.log('Hier bin cih erfolgreich');
            console.info(data);
        }
    });

}
