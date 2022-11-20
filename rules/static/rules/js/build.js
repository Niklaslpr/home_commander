function loadRules() {
    $.ajax({
        url: '/rule_info/all',
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
            console.info(data);

            let rulesJson = {};
            for (let entry of data.rules.reverse()) {
                rulesJson[entry['id']] = entry;

                $.ajax({
                    url: '/kit/rule-tile',
                    type: 'get',
                    data: {
                        "csrfmiddlewaretoken": getCookie('csrftoken'),
                        "rule-id": entry['id'].toString(),
                        "rule-name": entry['name'].toString(),
                    },
                    headers: {
                        'Content-type': 'application/json', 'Accept': 'text/plain',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    dataType: 'json',
                    mode: 'same-origin'
                }).always((data) => {
                    if (data.readyState === 4 && data.status === 200) {
                        document.getElementById('rule-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                        // document.getElementById('switchLight-' + entry['id'].toString()).checked = entry['on'];
                    }
                });
            }

            window.localStorage.setItem('rules', JSON.stringify(rulesJson));
        }
    });
}

$(document).ready(() => {
    loadRules();
});