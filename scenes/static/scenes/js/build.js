function loadScenes() {
    $.ajax({
        url: './scene_info/all',
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

            let scenesJson = {};
            for (let group in data.scenes) {
                for (let entry of data.scenes[group]) {
                    scenesJson[entry['id']] = entry;
                    scenesJson[entry['id']]['group_id'] = group;

                    $.ajax({
                        url: './kit/scene-tile',
                        type: 'get',
                        data: {
                            "csrfmiddlewaretoken": getCookie('csrftoken'),
                            "scene-id": entry['id'].toString(),
                            "scene-name": entry['name'].toString(),
                            "scene-icon": entry['icon'].toString(),
                            "group-id": group.toString()
                        },
                        headers: {
                            'Content-type': 'application/json', 'Accept': 'text/plain',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        dataType: 'json',
                        mode: 'same-origin'
                    }).always((data) => {
                        if (data.readyState === 4 && data.status === 200) {
                            document.getElementById('scene-list').insertAdjacentHTML('afterbegin', data.responseText.toString());
                        }
                    });
                }
            }

            window.localStorage.setItem('scenes', JSON.stringify(scenesJson));
        }
    });
}

$(document).ready(() => {
    loadScenes();
});

function test() {
    console.log("yes sir i am working")
}
