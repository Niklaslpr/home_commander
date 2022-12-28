
let favoritedevices;

$(document).ready(() => {
    createFavoriteGroup();
})

function createFavoriteGroup(){
    let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrftoken);

        let http = new XMLHttpRequest();

        http.onreadystatechange = function (){
             if (this.readyState === 4 && this.status === 200){
                 favoritedevices = this.response;
                 if (favoritedevices == ""){
                     document.getElementById("favoritedevices").innerHTML = "Es wurde noch kein Gerät als Favorit gesetzt.";
                 }
                 else{
                     document.getElementById("favoritedevices").innerHTML = favoritedevices;
                 }
             }
        }

        http.open('POST', '/createFavoriteGroup/');
        http.send(formData);

}
