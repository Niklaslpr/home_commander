let user_list
let user_table

$(document).ready(() => {
    get_all_users();

    user_table = document.getElementById('user_table');
})

function get_all_users(){
    let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrftoken);
        let http = new XMLHttpRequest();
        http.onreadystatechange = function (){
             if (this.readyState === 4 && this.status === 200){
                 user_list = JSON.parse(this.response);
                 for (const x in user_list){
                     const tmp = user_list[x].split(", ");
                     let row = user_table.insertRow(0);
                     let cell1 = row.insertCell(0);
                     let cell2 = row.insertCell(1);
                     cell1.innerHTML = tmp[0];
                     cell2.innerHTML = tmp[1];
                 }
             }
        }
        http.open('POST', '/get_all_users/');
        http.send(formData);
}