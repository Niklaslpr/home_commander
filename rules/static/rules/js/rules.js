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
let repeatRule;

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
    
    timePickerEditRule = new Picker(inputTimeEditRule, {
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
    dict_weekdays_edit = {
            'Mo, ' : document.getElementById('checkEditRuleMo'),
            'Di, ' : document.getElementById('checkEditRuleDi'),
            'Mi, ' : document.getElementById('checkEditRuleMi'),
            'Do, ' : document.getElementById('checkEditRuleDo'),
            'Fr, ' : document.getElementById('checkEditRuleFr'),
            'Sa, ' : document.getElementById('checkEditRuleSa'),
            'So, ' : document.getElementById('checkEditRuleSo'),
        }
    
    checkboxRepeatEditRule.addEventListener('change', function(){
            if(checkboxRepeatEditRule.checked == true){
                for (const [key, value] of Object.entries(dict_weekdays_edit)){
                    value.disabled = false;
                }
            } else{
                for (const [key, value] of Object.entries(dict_weekdays_edit)){
                    value.style.backgroundColor = "transparent";
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
    repeatRule = false;
    
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
    
    repeatRule = document.getElementById('checkboxRepeatNewRule').checked;
    
    
    console.log(newRuleName);
    console.log(repeatRule);
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
            'repeat-rule': repeatRule,
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
    
    for (const [key, value] of Object.entries(dict_weekdays_edit)){
                    value.style.backgroundColor = 'transparent';
                }
    
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
        document.getElementById('groupCheckInEditRule-'+ currentRule["group_id"]).style.backgroundColor = 'var(--tertiary-color)';
        
        for (let element in groupListAll){
            if (groupListAll[element]["id"] == currentRule["group_id"]){
                
                let tmp = groupListAll[element]["name"];
                if (tmp.startsWith('room_')){
                    tmp = tmp.split('_').pop();
                }
                
                
                
                $.ajax({
                    url: './kit/group-item-control-rule',
                    type: 'get',
                    data: {
                        "csrfmiddlewaretoken": getCookie('csrftoken'),
                        "group-id": groupListAll[element]["id"].toString(),
                        "group-name": tmp,
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
        document.getElementById('ruleWeekdays-modal').innerHTML = currentRule["weekdays"];
        if (typeof(currentRule['weekdays']) == 'string'){
            checkboxRepeatEditRule.checked = false;
            
        } else if (typeof(currentRule['weekdays']) == 'object'){
            checkboxRepeatEditRule.checked = true;
            
            for (const [key, value] of Object.entries(dict_weekdays_edit)){
                    value.disabled = false;
            }
            
            for (let z in currentRule['weekdays']){
                day = currentRule['weekdays'][z]
                day = day.replace(" ", "");
                document.getElementById('checkEditRule' + day).style.backgroundColor = 'var(--tertiary-color)';
            
            }
            
        }
        
        
        
        } else {
            return null;
        }
}

function deleteRule(){
    if (confirm('Bist Du sicher?')) {
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
}

function updateRule(){
    let updateRuleName, updateRuleGroup, updateRuleTime, updateRuleDays, updateRuleRepeat;
    updateRuleName = document.getElementById('editRuleName').value;
    updateRuleGroup = "";  
    updateRuleTime = document.getElementById("inputTimeEditRule").value;
    updateRuleDays = ""
    for (const [key, value] of Object.entries(dict_weekdays_edit)){
        if (value.style.backgroundColor == 'var(--tertiary-color)'){
            updateRuleDays += '1';
        } else if (value.style.backgroundColor == '' || value.style.backgroundColor == 'transparent'){
            updateRuleDays += '0';
        }
    }
    updateRuleRepeat = document.getElementById('checkboxRepeatEditRule').checked;
    for (thing in groupListAll){
        
        if (document.getElementById('groupCheckInEditRule-' + groupListAll[thing]["id"]).style.backgroundColor == "var(--tertiary-color)"){
            updateRuleGroup = groupListAll[thing]["id"];
        }
    }
     console.log("Change Rule: ", updateRuleName, updateRuleGroup, updateRuleTime, updateRuleDays, updateRuleRepeat);
     
     $.ajax({
        url: './update_rule',
        type: 'get',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            'rule-name': updateRuleName,
            'rule-group': updateRuleGroup,
            'rule-time': updateRuleTime,
            'rule-days': updateRuleDays,
            'repeat-rule': updateRuleRepeat,
            'rule-id': currentRule['id'],
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
