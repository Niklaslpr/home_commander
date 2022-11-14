function setData(id, key, value) {
    let element = document.querySelector("#" + id);

    if (element != null) {
        element.dataset[key] = value;
        return true;
    }

    return false;
}

function getData(id, key) {
    let element = document.querySelector("#" + id);

    if (element != null) {
        return element.dataset[key];
    }

    return null;
}
