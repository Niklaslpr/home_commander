function loadLogs() {
	$.ajax({
		url: './load_logs',
		type: 'post',
		data: {
			csrfmiddlewaretoken: getCookie('csrftoken'),
			'a': 0,
			'b': 10,
		},
		headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
		dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
			console.log(data)
		}
	})
}



//function loadLogs() {
    //$.ajax({
        //url: './group_info/all',
        //type: 'get',
        //data: {
            //csrfmiddlewaretoken: getCookie('csrftoken'),
        //},
        //headers: {
            //'Content-type': 'application/json', 'Accept': 'text/plain',
            //'X-CSRFToken': getCookie('csrftoken')
        //},
        //dataType: 'json',
        //mode: 'same-origin',
        //success: function (data) {
            //console.info(data);

            //let groupsJson = {};
            //for (let entry of data.groupsCollection.reverse()) {
                //groupsJson[entry['id']] = entry;
                //if (entry['name'].startsWith('room_')){
                    
                //} else{    
                    //$.ajax({
                        //url: './kit/group-tile',
                        //type: 'get',
                        //data: {
                            //"csrfmiddlewaretoken": getCookie('csrftoken'),
                            //"group-id": entry['id'].toString(),
                            //"group-name": entry['name'].toString(),
                            //"group-state": entry['on'].toString(),
                        //},
                        //headers: {
                            //'Content-type': 'application/json', 'Accept': 'text/plain',
                            //'X-CSRFToken': getCookie('csrftoken')
                        //},
                        //dataType: 'json',
                        //mode: 'same-origin'
                    //}).always((data) => {
                        //if (data.readyState === 4 && data.status === 200) {
                            //document.getElementById('group-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                        //}
                    //});
                //}
            //}

            //window.localStorage.setItem('groups', JSON.stringify(groupsJson));
        //}
    //});
//}

$(document).ready(() => {
  
});


