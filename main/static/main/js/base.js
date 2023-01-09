let formData = new FormData();
formData.append('csrfmiddlewaretoken', csrftoken);

const http = new XMLHttpRequest();
http.onreadystatechange = function(){
    if (this.readyState === 4 && this.status === 200){
        let response_tmp = JSON.parse(this.response);

        let temp = response_tmp["temp"] + ' °C';

        let code = response_tmp["code"];

        document.getElementById("temperature").innerHTML = temp;

        if (code == 200 || code == 201 || code == 202 || code == 210 || code == 211 || code == 212 || code == 221 || code == 230 || code == 231 || code == 232){
            // 11d
            document.getElementById("cloud-lightning_img").hidden = false;
        }
        if (code == 300 || code == 301 || code == 302 || code == 310 || code == 311 || code == 312 || code == 313 || code == 314 || code == 321 || code == 520 || code == 521 || code == 522 || code == 531 || code == 500 || code == 501 || code == 502 || code == 503 || code == 504){
            // 09d
            document.getElementById("cloud-rain_img").hidden = false;
        }
        if(code == 511 || code == 600 || code == 601 || code == 602 || code == 611 || code == 612 || code == 613 || code == 615 || code == 616 || code == 620 || code == 621 || code == 622){
            // 13d
            document.getElementById("snow_img").hidden = false;
        }
        if (code == 701 || code == 711 || code == 721 || code == 731 || code == 741 || code == 751 || code == 761 || code == 762 || code == 771 || code == 781){
            // 50d
            document.getElementById("cloud-haze_img").hidden = false;
        }
        if (code == 800){
            // 01d
            document.getElementById("sun_img").hidden = false;
        }
        if (code == 801){
            // 02d
            document.getElementById("cloud-sun_img").hidden = false;
        }
        if (code == 802){
            // 03d
            document.getElementById("cloud_img").hidden = false;
        }
        if (code == 803 || code == 804){
            // 04d
            document.getElementById("clouds_img").hidden = false;
        }
    }
}

http.open('GET', '/weather/');
http.send(formData);

// let response_tmp = {"temp": 9, "code": 804};




















