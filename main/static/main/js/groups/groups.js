var colorPicker = new iro.ColorPicker('#colpicker234', {
    borderWidth: 2,
    layout: [
        {
        component: iro.ui.Wheel,
        },
    ]
});

var headerbg = document.getElementById("ModalGroupHeader");
var outputHue = document.getElementById("ModalGroupLabel");
outputHue.innerHTML = 'Gruppe XXX'

colorPicker.on('color:change', function(color){
    console.log(color.hue);
    console.log(color.saturation);
    headerbg.style.backgroundColor = color.hexString;
    outputHue.innerHTML ='Gruppe XXX ' + 'Hue: ' + color.hue + ' Sat: ' + color.saturation;
});
var slider = document.getElementById("customBrightness1");
var output = document.getElementById("color1");
output.innerHTML = slider.value + '%';

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function(){
    output.innerHTML = this.value + '%';
}

let switchGroup1 = document.getElementById('switchGroup1');
let switchModalGroup1 = document.getElementById('switchModalGroup1');

switchGroup1.addEventListener('change', function(){groupOnOff(switchGroup1.checked, 1); switchModalGroup1.checked = switchGroup1.checked;});
switchModalGroup1.addEventListener('change', function(){groupOnOff(switchModalGroup1.checked, 1); switchGroup1.checked = switchModalGroup1.checked;});

// Group ON / OFF
function groupOnOff(state, groupID){
    let formData = new FormData();
    formData.append('groupID', groupID);
    formData.append('state', state);
    formData.append('csrfmiddlewaretoken', csrftoken);

    const http = new XMLHttpRequest();
    http.open('POST', '/grouponoff/');
    http.send(formData);
}

let newGroupName = document.getElementById('inputGroupName');

document.getElementById('createGroup').addEventListener('click', function(){
    let formData = new FormData();
    formData.append('groupName', newGroupName.value);
    formData.append('csrfmiddlewaretoken', csrftoken);

    const http = new XMLHttpRequest();

    http.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            location.reload();
        }
    }

    http.open('POST','/creategroup/');
    http.send(formData);


})