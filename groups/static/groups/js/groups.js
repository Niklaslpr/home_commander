let groupControlColorPicker;
let groupControlModal;
let groupControlModalHeader;
let groupControlModalLabel;
let groupControlModalSwitch;
let groupControlModalBrightnessSlider;
let groupControlModalBrightnessDisplay;

$(document).ready(() => {
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
// groupControlModalLabel.innerHTML = 'Gruppe XXX';

    groupControlColorPicker.on('color:change', function (color) {
        console.log(color.hue);
        console.log(color.saturation);
        groupControlModalHeader.style.backgroundColor = color.hexString;
        groupControlModalLabel.innerHTML = groupControlModal.dataset['groupName'] + 'Hue: ' + color.hue + ' Sat: ' + color.saturation;
    });
    groupControlModalBrightnessSlider = document.getElementById("group-control-modal-brightness");
    groupControlModalBrightnessDisplay = document.getElementById("group-control-modal-brightness-display");
    groupControlModalBrightnessDisplay.innerHTML = groupControlModalBrightnessSlider.value + '%';

// Update the current slider value (each time you drag the slider handle)
    groupControlModalBrightnessSlider.oninput = function () {
        groupControlModalBrightnessDisplay.innerHTML = this.value + '%';
    }

// let switchGroup1 = document.getElementById('switchGroup1');
    groupControlModalSwitch = document.getElementById('group-control-modal-switch');

    let newGroupName = document.getElementById('inputGroupName');

    document.getElementById('createGroup').addEventListener('click', function () {
        let formData = new FormData();
        formData.append('groupName', newGroupName.value);
        formData.append('csrfmiddlewaretoken', csrftoken);

        const http = new XMLHttpRequest();

        http.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                location.reload();
            }
        }

        http.open('POST', '/creategroup/');
        http.send(formData);


    })
});

// switchGroup1.addEventListener('change', function(){groupOnOff(switchGroup1.checked, 1); groupControlModalSwitch.checked = switchGroup1.checked;});
// groupControlModalSwitch.addEventListener('change', function(){groupOnOff(groupControlModalSwitch.checked, 1); switchGroup1.checked = groupControlModalSwitch.checked;});

// Group ON / OFF
function groupOnOff(state, groupID) {
    let formData = new FormData();
    formData.append('groupID', groupID);
    formData.append('state', state);
    formData.append('csrfmiddlewaretoken', csrftoken);

    const http = new XMLHttpRequest();
    http.open('POST', '/grouponoff/');
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
        }

        console.log('currentGroup', currentGroup);
        groupControlModalSwitch.checked = currentGroup['on'];
        groupControlColorPicker.color.hue = currentGroup['hue'];
        groupControlColorPicker.color.saturation = currentGroup['saturation'];
        groupControlModalBrightnessSlider.value = currentGroup['brightness'];
        groupControlModalBrightnessDisplay.innerText = currentGroup['brightness'] + ' %';
        groupControlModalLabel.innerText = currentGroup['name'] + ' ' + 'Hue: ' + currentGroup['hue'] + ' Sat: ' + currentGroup['saturation'];

        return 0;
    } else {
        return null;
    }
}

function saveGroupDataToLocalStorage(groupId) {
    let groups = JSON.parse(window.localStorage.getItem('groups'));

    if (groups.hasOwnProperty(groupId)) {
        console.log("i hasse Dennis");

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
