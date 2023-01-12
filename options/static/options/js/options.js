let user_list;
let user_table;
let my_username;

$(document).ready(() => {
    get_all_users();
    user_table = document.getElementById('user_table');
    my_username = document.getElementById('my_username').innerHTML;
})

function get_all_users(){
    let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrftoken);
        let http = new XMLHttpRequest();
        http.onreadystatechange = function (){
             if (this.readyState === 4 && this.status === 200){
                 user_list = JSON.parse(this.response);
                 let x = user_list[0].split(", ");
                 if (my_username == x[0]) {
                     for (const x in user_list) {
                         const tmp = user_list[x].split(", ");
                         let row = user_table.insertRow(0);
                         let cell1 = row.insertCell(0);
                         let cell2 = row.insertCell(1);
                         let cell3 = row.insertCell(2);
                         cell1.innerHTML = tmp[0];
                         cell2.innerHTML = tmp[1];
                         cell3.align = 'Right';
                         let temp = " '" + tmp[0] + "'";
                         if (tmp[0] == 'admin') {
                             cell3.innerHTML = '';
                         } else {
                             cell3.innerHTML = '<button id="deleteUserButton' + tmp[0] + '" class="btn btn-danger" onclick="deleteUser(' + temp + ')">X</button>';
                         }
                     }
                 } else {
                     for (const x in user_list) {
                             const tmp = user_list[x].split(", ");
                         if (tmp[0] == my_username) {
                             let row = user_table.insertRow(0);
                             let cell1 = row.insertCell(0);
                             let cell2 = row.insertCell(1);
                             let cell3 = row.insertCell(2);
                             cell1.innerHTML = tmp[0];
                             cell2.innerHTML = tmp[1];
                             cell3.align = 'Right';
                             let temp = " '" + tmp[0] + "'";
                             if (tmp[0] == 'admin') {
                                 cell3.innerHTML = '';
                             } else {
                                 cell3.innerHTML = '<button id="deleteUserButton' + tmp[0] + '" class="btn btn-danger" onclick="deleteUser(' + temp + ')">X</button>';
                             }
                         }
                     }
                 }
             }
        }
        http.open('POST', './get_all_users/');
        http.send(formData);
}

function deleteUser(user){
    if ((confirm('Bist Du sicher?')) == true) {
        console.log(user + " wurde gelöscht");
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrftoken);
        formData.append('user', user);
        let http = new XMLHttpRequest();
        http.onreadystatechange = function (){
             if (this.readyState === 4 && this.status === 200){
                 location.reload();
             }
        }

        http.open('POST', './delete_user/');
        http.send(formData);
    }

}