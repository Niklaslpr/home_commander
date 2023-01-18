let date;
let time;
let inputTimeNewRule;
let inputTimeEditRule;
let timeRule;
let dict_weekdays;
let savedTimeNewRule;
let savedTimeEditRule;
let selectedDaysNewRule;
let selectedDaysEditRule;
let checkboxRepeatNewRule;
let checkboxRepeatEditRule;
let createNewRuleButton;
let newRuleName;
let ruleControlModalLabel;
let ruleControlModal;
let editRuleName;
let selectedDeviceNewRule;
let selectedDeviceEditRule;
let timePickerNewRule;
let timePickerEditRule;
let groupListAll;
let currentRule;

$(document).ready(() => {
    
    get_all_devices();
    date = new Date();
    time = date.getHours() + ':' + (date.getMinutes()<10?'0':'') + date.getMinutes();
    inputTimeNewRule = document.getElementById('inputTimeNewRule');
    inputTimeEditRule = document.getElementById('inputTimeEditRule');
    timeRule = document.getElementById('timeRule');
    checkboxRepeatNewRule = document.getElementById('checkboxRepeatNewRule');
    checkboxRepeatEditRule = document.getElementById('checkboxRepeatEditRule');
    inputTimeNewRule.value = time;
    ruleControlModalLabel = document.getElementById('rule-control-modal-label');
    ruleControlModal = document.getElementById('rule-control-modal');
    editRuleName = document.getElementById('editRuleName');
    
    ruleControlModal.addEventListener('hide.bs.modal', function(){
            for (let x of groupList){
                document.getElementById("groupCheckInEditRule-" + x).style.backgroundColor = "transparent";
            }
            document.getElementById('rule-control-modal-label').hidden = false; 
            document.getElementById('editRuleName').hidden = true; 
            document.getElementById('modal-body-edit').hidden = true; 
            document.getElementById('modal-body-normal').hidden = false;
        })
    
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
    groupListAll = {};
    document.getElementById('new-rule-device-list').innerHTML = '';
    document.getElementById('edit-rule-group-list').innerHTML = ''; 
   
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
            groupListAll = data["groupsCollection"];
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
                $.ajax({
                    url: './kit/group-item-edit-rule',
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
                        document.getElementById('edit-rule-group-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                    }
                });
        }
        }
    });
    
}

function set_background_color_transparend_new(){
    
    for (let element in groupList){
            try {document.getElementById('groupCheckInNewRule-' + groupList[element]).style.backgroundColor = "transparent";}
            catch{}
        }   
}

function set_background_color_transparend_edit(){
    
    for (let element in groupList){
            try {document.getElementById('groupCheckInEditRule-' + groupList[element]).style.backgroundColor = "transparent";}
            catch{}
        }   
}

function set_background_color(id){
    if (document.getElementById(id).style.backgroundColor == 'var(--tertiary-color)'){
        document.getElementById(id).style.backgroundColor = "transparent";
        
    } else{
        if (id.startsWith('deviceCheckInNewRule-') || id.startsWith('groupCheckInNewRule-')){
            set_background_color_transparend_new();
        }
        if (id.startsWith('groupCheckInEditRule-')){
            set_background_color_transparend_edit();
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
                selectedDeviceNewRule = groupList[element];
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
            'rule-group': selectedDeviceNewRule,
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
            location.reload();
        }
        
    });
}

function loadRuleDataToModal(ruleId) {
    let rules = JSON.parse(window.localStorage.getItem("rules"));
    
    if (rules.hasOwnProperty(ruleId)) {
        currentRule = rules[ruleId];
        console.log(currentRule);
        timeRule.value = currentRule["localtime"];
        inputTimeEditRule.value = currentRule["localtime"];
        ruleControlModalLabel.innerHTML = currentRule["name"];
        editRuleName.value = currentRule["name"];
        console.log(currentRule["group_id"]);
        console.log(groupListAll);
        document.getElementById('rule-control-group-list').innerHTML = '';
        
        for (let element in groupListAll){
            if (groupListAll[element]["id"] == currentRule["group_id"]){
                $.ajax({
                    url: './kit/group-item-control-rule',
                    type: 'get',
                    data: {
                        "csrfmiddlewaretoken": getCookie('csrftoken'),
                        "group-id": groupListAll[element]["id"].toString(),
                        "group-name": groupListAll[element]["name"],
                        
                    },
                    headers: {
                        'Content-type': 'application/json', 'Accept': 'text/plain',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    dataType: 'json',
                    mode: 'same-origin'
                }).always((data) => {
                    if (data.readyState === 4 && data.status === 200) {
                        document.getElementById('rule-control-group-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                    }
                });
            }
        }
        
        
        } else {
            return null;
        }
}

function deleteRule(){
    console.log("Lösche: ",currentRule["id"]);
    $.ajax({
        url: './delete_rule',
        type: 'get',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            'rule-id': currentRule["id"],
        },
        headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
            console.log(data);
            location.reload();
        }
        
    });
}
