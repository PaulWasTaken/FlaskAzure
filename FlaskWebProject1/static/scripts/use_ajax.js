function firstComment(answer){
    var place = document.querySelectorAll(".container")[2];
    var sender = answer[0][0];
    var date = answer[0][1];
    var text = answer[0][2];
    place.insertAdjacentHTML("afterbegin",
        "<div class='feedback-content data-container'>" +
            "<div>" + sender + " " + date + "</div>" +
            "<div>" + text + "</div>" +
        "</div>"
    );
}

function ajaxUpdate() {
    try {
        ajax.post(
            window.location.pathname + window.location.search,
            {
                nickname: '',
                text_area: '',
            },
            function (rawResponse) {
                var answer = JSON.parse(rawResponse);
                var posts = document.querySelectorAll(".feedback-content");
                if (posts.length === 0 && answer.length !== 0)
                {
                    firstComment(answer);
                    return;
                }
                if (posts.length === answer.length)
                    return;
                var sender = answer[answer.length - 1][0];
                var date = answer[answer.length - 1][1];
                var text = answer[answer.length - 1][2];
                posts[posts.length - 1].insertAdjacentHTML("afterend",
                    "<div class='feedback-content data-container'>" +
                        "<div>" + sender + " " + date + "</div>" +
                        "<div>" + text + "</div>" +
                    "</div>"
                );
            }
        );
    }
    catch (e) {
    }
}


function postFeedback(event) {
    event.preventDefault();
    ajax.post(
        window.location.pathname + window.location.search,
        {
            nickname: event.target[0].value,
            text_area: event.target[1].value,
        },
        function(rawResponse) {
            event.target.reset();
            ajaxUpdate(rawResponse);
        }
    );
}

function updater() {
    setInterval(ajaxUpdate, 8000);
    document.querySelector("#form").onsubmit = postFeedback;
}

if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", updater);
}
else if (document.attachEvent) {
    document.attachEvent("onreadystatechange", function () {
        if (document.readyState === "complete") {
            updater();
        }
    });
}