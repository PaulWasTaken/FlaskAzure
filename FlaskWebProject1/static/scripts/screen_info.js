function saveResolution() {
    document.cookie = "width=" + window.outerWidth + "; path=/";
    document.cookie = "height=" + window.outerHeight + "; path=/";
}

if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", saveResolution);
}
else if (document.attachEvent) {
    document.attachEvent("onreadystatechange", function () {
        if (document.readyState === "complete") {
            saveResolution();
        }
    });
}
