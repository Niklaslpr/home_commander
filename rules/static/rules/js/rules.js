    var date = new Date();
    var time = date.getHours() + ':' + (date.getMinutes()<10?'0':'') + date.getMinutes();
    var input = document.getElementById('input');
    input.value = time;

    var timePicker = new Picker(input, {
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


    document.getElementById('saveRule').addEventListener("click", function(){
        var savedTime = timePicker.getDate(true);
        document.getElementById('savedTimeRule1').innerHTML = savedTime;

        var checkMonday = document.getElementById('checkMonday');
        var checkTuesday = document.getElementById('checkTuesday');
        var checkWednesday = document.getElementById('checkWednesday');
        var checkThursday = document.getElementById('checkThursday');
        var checkFriday = document.getElementById('checkFriday');
        var checkSaturday = document.getElementById('checkSaturday');
        var checkSunday = document.getElementById('checkSunday');
        var savedDaysOutput = '';

        if (checkMonday.checked == true){
            savedDaysOutput += 'Mo, ';
        }
        if (checkTuesday.checked == true){
            savedDaysOutput += 'Di, ';
        }
        if (checkWednesday.checked == true){
            savedDaysOutput += 'Mi, ';
        }
        if (checkThursday.checked == true){
            savedDaysOutput += 'Do, ';
        }
        if (checkFriday.checked == true){
            savedDaysOutput += 'Fr, ';
        }
        if (checkSaturday.checked == true){
            savedDaysOutput += 'Sa, ';
        }
        if (checkSunday.checked == true){
            savedDaysOutput += 'So, ';
        }
        document.getElementById('savedDays1').innerHTML = savedDaysOutput;
    });