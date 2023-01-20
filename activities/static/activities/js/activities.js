let x;
let z;
function loadLogs() {
	
	$.ajax({
		url: './load_logs',
		type: 'get',
		data: {
			csrfmiddlewaretoken: getCookie('csrftoken'),
			'a': x,
			'b': x+10,
		},
		headers: {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken')
        },
		dataType: 'json',
        mode: 'same-origin',
        success: function (data) {
			console.log(data);
			
			if (data["timestamp0"] == "stop"){
				document.getElementById("show-next-logs").innerHTML = "Keine weiteren Einträge";
				document.getElementById("show-next-logs").disabled = true;
				document.getElementById("show-next-logs").style.backgroundColor = "";
				document.getElementById("show-next-logs").classList.add("btn-secondary");
			}
			z = 0;
			while (z < 10){
				document.getElementById("timestamp" + z).innerHTML = data["timestamp"+z];
				document.getElementById("message" + z).innerHTML = data["message"+z];
				z += 1;
			}
		}
	})
	x += 10;
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
	x = 10;
});


