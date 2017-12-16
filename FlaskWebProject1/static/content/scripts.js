var increased = false;
var isHelping = false;
var maxImageNumber = 6;
var minImageNumber = 1;

function createHelpMsg() {
    var helpBody = "Click on preview to increase.";
    var modal =
        "<div id='help' onclick='closeHelp()'>" +
        "<div class='modal-content modal-sm center role='dialog'>" +
        "<div class='modal-dialog>" +
        "<div class='modal-header'>" +
        "<h4 class='modal-title'>Helping message</h4>" + "</div>" +
        "<div class='modal-body'>" +
        "<p>" + helpBody + "</p>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "</div>";
    var div = document.createElement("div");
    div.id = "helper";
    div.innerHTML += modal;
    isHelping = true;
    return div;
}

function remove(element) {
    if (element && element.parentNode)
        element.parentNode.removeChild(element);
}

function closeMax(flushHash) {
    remove(document.querySelector("#magnify"));
    remove(document.querySelector("#overlay"));
    increased = false;
    if (flushHash)
        document.location.hash = "";
};

function closeHelp() {
    remove(document.querySelector("#overlay"));
    remove(document.querySelector("#helper"));
    isHelping = false;
};

function showHelpMsg() {
    if (isHelping)
        return;
    var overlay = document.createElement('div');
    overlay.id = "overlay";
    overlay.onclick = closeHelp;
    document.body.appendChild(overlay);
    document.body.appendChild(createHelpMsg());
    isHelping = true;
};

function maximize(element){
    var overlay = document.createElement('div');
    overlay.id = "overlay";
    overlay.onclick = closeMax;
    var magnified = document.createElement('div');
    magnified.id = "magnify";
    var img = document.createElement('img');
    img.src = element.src;
    magnified.appendChild(img);
    document.body.appendChild(overlay);
    document.body.appendChild(magnified);
    var divWidth = document.getElementById("magnify").offsetWidth;
    document.querySelector('#magnify').style.left = (document.body.clientWidth - divWidth)/2 + 'px';
    document.querySelector('#magnify').style.top = (document.body.clientHeight - divWidth)/2 + 'px';
    increased = true;
    document.location.hash = 'number=' + element.id;
};

var keyHandler = function (event) {
    event = event || window.event;
    var direction = 0;
    if (event.keyCode === 112 && !increased) {
        showHelpMsg();
        event.preventDefault ? event.preventDefault() : event.returnValue = false;
    }
    else if (event.keyCode === 27 && increased)
        closeMax(true);
    else if (event.keyCode === 27 && isHelping)
        closeHelp(true);
    else if (event.keyCode === 37)
        direction = -1;
    else if (event.keyCode === 39)
        direction = 1;
    var hash = getHashValue();
    if (hash) {
        var wantedNumber = parseInt(getHashValue()) + direction;
        wantedNumber = wantedNumber % maxImageNumber;
        if (wantedNumber < minImageNumber)
            wantedNumber = maxImageNumber;
        document.location.hash = 'number=' + wantedNumber; 
    }
};

function getHashValue() {
    var url = window.location.hash.substr(1, window.location.hash.length);
    return url.split('=')[1] === 'NaN' ? "" : url.split('=')[1];
}

function checkIfZoomed() {
    var current = getHashValue();
    if (current) {
        if (increased) {
            closeMax(false);
        }
        var element = document.getElementById(current);
        maximize(element);
    }
    else {
        closeMax(true);
    }
};

window.onload = checkIfZoomed
if (document.addEventListener) {
    document.addEventListener("keydown", keyHandler);
    window.addEventListener("popstate", checkIfZoomed);
    window.addEventListener("hashchange", checkIfZoomed);
}
else if (document.attachEvent) {
    document.attachEvent("onkeydown", keyHandler);
    if (window.onpopstate)
        window.onpopstate = checkIfZoomed;
    else
        window.onhashchange = checkIfZoomed;
}
