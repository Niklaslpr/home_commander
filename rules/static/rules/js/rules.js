var date = new Date();
var time = date.getHours() + ':' + (date.getMinutes() < 10 ? '0' : '') + date.getMinutes();
var input = document.getElementById('input');
input.value = time;

var timePicker = new Picker(input, {
    date: new Date(),
    container: '#picker-container',
    format: 'HH:mm',
    controls: true,
    rows: 3,
    text: {
        title: 'Uhrzeit auswählen',
        cancel: 'Abbrechen',
    }
});


var dict = {};
dict['Mo, '] = document.getElementById('checkMonday');
dict['Di, '] = document.getElementById('checkTuesday');
dict['Mi, '] = document.getElementById('checkWednesday');
dict['Do, '] = document.getElementById('checkThursday');
dict['Fr, '] = document.getElementById('checkFriday');
dict['Sa, '] = document.getElementById('checkSaturday');
dict['So, '] = document.getElementById('checkSunday');

document.getElementById('checkboxRepeatRule').addEventListener('change', function () {
    if (document.getElementById('checkboxRepeatRule').checked == true) {
        for (const [key, value] of Object.entries(dict)) {
            value.disabled = false;
        }
    } else {
        for (const [key, value] of Object.entries(dict)) {
            value.disabled = true;
        }
    }
})

document.getElementById('saveRule').addEventListener("click", function () {

    var savedTime = timePicker.getDate(true);
    document.getElementById('savedTimeRule1').innerHTML = savedTime;
    console.log(savedTime);


    var savedDaysOutput = '';
    var selectedDays = '';
    for (const [key, value] of Object.entries(dict)) {
        if (value.checked == true) {
            savedDaysOutput += key;
            selectedDays += '1';
        } else if (value.checked == false) {
            selectedDays += '0';
        }
    }

    var days = parseInt(selectedDays, 2); // Format für deCONZ
    if (document.getElementById('checkboxRepeatRule').checked == false) {
        savedDaysOutput = '';
        days = 0;
    }
    document.getElementById('savedDays1').innerHTML = savedDaysOutput; //Ausgabe der gewählten Tage
    console.log(days); //Consolenausgabe Wert für deCONZ

    let apiTime = 'W' + days + '/T' + savedTime + ':00';
    let formData = new FormData();
    formData.append('groupID', 1);
    formData.append('time', apiTime);
    formData.append('csrfmiddlewaretoken', csrftoken);

    const http = new XMLHttpRequest();
    http.open('POST', '/createschedule/');
    http.send(formData);

});

function loadRuleDataToModal(ruleId) {
    let rules = JSON.parse(window.localStorage.getItem("rules"));

    if (rules.hasOwnProperty(ruleId)) {
        let currentRule = rules[ruleId];

        // TODO

        return 0;
    } else {
        return null;
    }
}

function saveRuleDataToLocalStorage(ruleId) {
    let rules = JSON.parse(window.localStorage.getItem('rules'));

    if (rules.hasOwnProperty(ruleId)) {
        // TODO

        window.localStorage.setItem('rules', JSON.stringify(rules));

        return 0;
    } else {
        return null;
    }
}
