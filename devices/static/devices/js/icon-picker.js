selectedIcon
icons

$(document).ready(() => {

})

function getIconId(IconId){
    icons = ["lamp-fill.svg", "lamp.svg", "lightbulb.svg", "lightbulb-fill.svg", "plug.svg", "plug-fill.svg", "brezel.png", "plugin.svg", "robot.svg"];
    for (const tmp in icons){
        document.getElementById(icons[tmp]).style.backgroundColor = "transparent";
    }
    selectedIcon = IconId;
    document.getElementById(selectedIcon).style.backgroundColor = "var(--tertiary-color)";
    console.log("hier oder was?")
}

function saveIcon(){
    document.getElementById('modal-body-edit').hidden = true;
    document.getElementById('modal-body-normal').hidden = false;
    let editDeviceName = deviceControlModalLabel.innerHTML;
    console.log(selectedIcon);
    console.log(editDeviceName);
    console.log(deviceControlModal.dataset['deviceId']);
    
    
    let formData = new FormData();
    formData.append('deviceId', deviceControlModal.dataset['deviceId']);
    formData.append('deviceName', editDeviceName);
    formData.append('selectedIcon', selectedIcon);
    formData.append('csrfmiddlewaretoken', csrftoken);
    const http = new XMLHttpRequest();

    http.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            location.reload();
            console.log(http.response);
        } 
    }
    http.open('POST', './updatedevice/');
    http.send(formData);
   
    
}
