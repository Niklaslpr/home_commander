

$(document).ready(() => {
    
    get_all_devices();
    
})

function get_all_devices(){
    deviceList = [];
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
}
