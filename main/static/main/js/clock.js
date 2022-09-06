function datumanzeige() {
    function datumErzeugen() {
        a = new Date();
        b = a.getFullYear();
        c = a.getMonth() + 1;
        d = a.getDate();
        e = a.getDay();
        if (c < 10) {
            c = "0" + c;
        }
        if (d < 10) {
            d = "0" + d;
        }
        datum = d + "." + c + "." + b;

        if (e == 0){tag = "Sonntag";};
        if (e == 1){tag = "Montag";};
        if (e == 2){tag = "Dienstag";};
        if (e == 3){tag = "Mittwoch";};
        if (e == 4){tag = "Donnerstag";};
        if (e == 5){tag = "Freitag";};
        if (e == 6){tag = "Samstag";};

        return tag + ", " + datum;

    }

    document.getElementById("datum").innerHTML = datumErzeugen();
}
setInterval(datumanzeige, 100);

function uhrzeitanzeige() {
    function uhrzeitErzeugen() {
        a = new Date();
        b = a.getHours();
        c = a.getMinutes();
        d = a.getSeconds();
        if (b < 10) {
            b = "0" + b;
        }
        if (c < 10) {
            c = "0" + c;
        }
        uhrzeit = b + ":" + c;
        return uhrzeit;


    }

    document.getElementById("uhrzeit").innerHTML = uhrzeitErzeugen() + " Uhr";
}
setInterval(uhrzeitanzeige, 100);