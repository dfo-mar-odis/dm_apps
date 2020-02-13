function popitup(url, windowName, hgt = 500, wdt = 500, top = 50, left = 200) {
    console.log(strWindowFeatures);
    console.log(hgt);
    console.log(wdt);
    var strWindowFeatures = "height=" + hgt + ",width=" + wdt + ",top=" + top + ",left=" + left;
    newwindow = window.open(url, windowName, strWindowFeatures);
    if (window.focus) {
        newwindow.focus()
    }
    return false;
}

$("a").click(function functionName() {
    if ($(this)[0].hasAttribute("pop-href")) {
        // var t = new Date();
        href = $(this)[0].getAttribute("pop-href");
        popitup(href, 'popoutWindow'  + Date.now());
    }
});