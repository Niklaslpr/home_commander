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
    console.log(selectedIcon);
}
