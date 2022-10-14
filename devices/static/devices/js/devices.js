var colorPicker = new iro.ColorPicker('#colpicker234', {
  borderWidth: 2,
  layout: [
    {
      component: iro.ui.Wheel,
    },
  ]
});

var headerbg = document.getElementById("modalHeader1");
var outputHue = document.getElementById("testModalLabel");
outputHue.innerHTML = 'Lampe XXX'

colorPicker.on('color:change', function(color){
 console.log(color.hue);
 console.log(color.saturation);
 headerbg.style.backgroundColor = color.hexString;
 outputHue.innerHTML ='Lampe XXX ' + 'Hue: ' + color.hue + ' Sat: ' + color.saturation;

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


slider.oninput = function(){
    let bri = this.value;
    output.innerHTML = bri + '%';   // Update the current slider value (each time you drag the slider handle)
    bri = Math.round(bri * 2.55);

    // sending Brightness
    let formData = new FormData();
    formData.append('bri', bri);
    formData.append('csrfmiddlewaretoken', csrftoken);

    const http = new XMLHttpRequest();
    http.open('POST', '/setbri/');
    http.send(formData);

}

// Licht an / aus
let switchLight1 = document.getElementById('switchLight1');
let switchModalLight1 = document.getElementById('switchModalLight1');

switchLight1.addEventListener('change', function(){lightOnOff(switchLight1.checked); switchModalLight1.checked = switchLight1.checked;});
switchModalLight1.addEventListener('change', function(){lightOnOff(switchModalLight1.checked); switchLight1.checked = switchModalLight1.checked;});

function lightOnOff(state){
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


