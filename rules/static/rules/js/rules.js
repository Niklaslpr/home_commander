let date;
let time;
let inputTimeNewRule;
let dict_weekdays;
let savedTimeNewRule;
let selectedDaysNewRule;
let checkboxRepeatNewRule;
let createNewRuleButton;
let newRuleName;
let selectedDeviceNewRule;
let timePickerNewRule;

$(document).ready(() => {
    
    get_all_devices();
    date = new Date();
    time = date.getHours() + ':' + (date.getMinutes()<10?'0':'') + date.getMinutes();
    inputTimeNewRule = document.getElementById('inputTimeNewRule');
    checkboxRepeatNewRule = document.getElementById('checkboxRepeatNewRule');
    inputTimeNewRule.value = time;
    
    timePickerNewRule = new Picker(inputTimeNewRule, {
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
    
    dict_weekdays = {
            'Mo, ' : document.getElementById('checkNewRuleMonday'),
            'Di, ' : document.getElementById('checkNewRuleTuesday'),
            'Mi, ' : document.getElementById('checkNewRuleWednesday'),
            'Do, ' : document.getElementById('checkNewRuleThursday'),
            'Fr, ' : document.getElementById('checkNewRuleFriday'),
            'Sa, ' : document.getElementById('checkNewRuleSaturday'),
            'So, ' : document.getElementById('checkNewRuleSunday'),
        }
    
    checkboxRepeatNewRule.addEventListener('change', function(){
            if(checkboxRepeatNewRule.checked == true){
                for (const [key, value] of Object.entries(dict_weekdays)){
                    value.disabled = false;
                }
            } else{
                for (const [key, value] of Object.entries(dict_weekdays)){
                    value.disabled = true;
                }
            }
    })
    
})

function get_all_devices(){
    deviceList = [];
    groupList = [];
    document.getElementById('new-rule-device-list').innerHTML = '';
    //document.getElementById('edit-rule-device-list').innerHTML = '';   #TODO
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
                    url: './kit/device-item-new-rule',
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
                        document.getElementById('new-rule-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                    }
            });
            // #TODO
            //
            //$.ajax({        
                //url: './kit/device-item-edit-rule',
                //type: 'get',
                //data: {
                    //"csrfmiddlewaretoken": getCookie('csrftoken'),
                    //"device-id2": entry['id'].toString(),
                    //"device-name2": entry['name'].toString(),
                    //"device-type2": entry['type'].toString(),
                //},
                //headers: {
                    //'Content-type': 'application/json', 'Accept': 'text/plain',
                    //'X-CSRFToken': getCookie('csrftoken')
                //},
                //dataType: 'json',
                //mode: 'same-origin'
            //}).always((data) => {
                //if (data.readyState === 4 && data.status === 200) {
                    //document.getElementById('edit-rule-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                    
                //}
            //});
        }
        }
    });
    $.ajax({
        url: '../groups/group_info/all',
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
            console.log(data);
            for (let entry of data["groupsCollection"]) {
                groupList.push(entry["id"].toString());
                let tmp_name = entry['name'];
                if (tmp_name.startsWith('room_')){
                    tmp_name = tmp_name.split('_').pop();
                }
                
                
                $.ajax({
                    url: './kit/group-item-new-rule',
                    type: 'get',
                    data: {
                        "csrfmiddlewaretoken": getCookie('csrftoken'),
                        "group-id": entry['id'].toString(),
                        "group-name": tmp_name,
                        
                    },
                    headers: {
                        'Content-type': 'application/json', 'Accept': 'text/plain',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    dataType: 'json',
                    mode: 'same-origin'
                }).always((data) => {
                    if (data.readyState === 4 && data.status === 200) {
                        document.getElementById('new-rule-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                    }
            });
            // #TODO
            //
            //$.ajax({        
                //url: './kit/device-item-edit-rule',
                //type: 'get',
                //data: {
                    //"csrfmiddlewaretoken": getCookie('csrftoken'),
                    //"device-id2": entry['id'].toString(),
                    //"device-name2": entry['name'].toString(),
                    //"device-type2": entry['type'].toString(),
                //},
                //headers: {
                    //'Content-type': 'application/json', 'Accept': 'text/plain',
                    //'X-CSRFToken': getCookie('csrftoken')
                //},
                //dataType: 'json',
                //mode: 'same-origin'
            //}).always((data) => {
                //if (data.readyState === 4 && data.status === 200) {
                    //document.getElementById('edit-rule-device-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                    
                //}
            //});
        }
        }
    });
    
}

function set_background_color_transparend(){
     for (let element in deviceList){
            try {document.getElementById('deviceCheckInNewRule-' + deviceList[element]).style.backgroundColor = "transparent";}
            catch{}
        }
    for (let element in groupList){
            try {document.getElementById('groupCheckInNewRule-' + groupList[element]).style.backgroundColor = "transparent";}
            catch{}
        }   
}


function set_background_color(id){
    if (document.getElementById(id).style.backgroundColor == 'var(--tertiary-color)'){
        document.getElementById(id).style.backgroundColor = "transparent";
        
    } else{
        if (id.startsWith('deviceCheckInNewRule-') || id.startsWith('groupCheckInNewRule-')){
            set_background_color_transparend();
        }
        document.getElementById(id).style.backgroundColor = 'var(--tertiary-color)';
        
    }  
}

function createNewRule(){
    selectedDeviceNewRule = "";
    newRuleName = "";
    savedTimeNewRule = "";
    selectedDaysNewRule = "";
    
    newRuleName = document.getElementById('inputRuleName').value;
    for (let element in deviceList){
        try{
            if (document.getElementById('deviceCheckInNewRule-' + deviceList[element]).style.backgroundColor == 'var(--tertiary-color)'){
                selectedDeviceNewRule = "device_" + deviceList[element];
            }
        } catch{}
    }
    for (let element in groupList){
        try{
            if (document.getElementById('groupCheckInNewRule-' + groupList[element]).style.backgroundColor == 'var(--tertiary-color)'){
                selectedDeviceNewRule = "group_" + groupList[element];
            }
        } catch{}
    }
    
    savedTimeNewRule = timePickerNewRule.getDate(true);
    
    for (const [key, value] of Object.entries(dict_weekdays)){
        if (value.style.backgroundColor == 'var(--tertiary-color)'){
            selectedDaysNewRule += '1';
        } else if (value.style.backgroundColor == '' || value.style.backgroundColor == 'transparent'){
            selectedDaysNewRule += '0';
        }
    }
    
    
    
    console.log(newRuleName);
    console.log(selectedDeviceNewRule);
    console.log(savedTimeNewRule);
    console.log(selectedDaysNewRule);
    
    
    $.ajax({
        url: './create_rule',
        type: 'get',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            'rule-name': newRuleName,
            'rule-device': selectedDeviceNewRule,
            'rule-time': savedTimeNewRule,
            'rule-days': selectedDaysNewRule,
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.log(data);
        }
        
    });
    
    
    
    
}
