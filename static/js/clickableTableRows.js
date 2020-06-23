// look through all table row
$("tr").each(function () {
    // if there is an href attr
    if ($(this)[0].getAttribute("href") != null) {
        // have the cursor change to a pointer on hover
        $(this)[0].style.cursor = "pointer"
        // add a click event listener to navigate to the specified url
        $(this).click(function () {
            href = $(this)[0].getAttribute("href")

            if ($(this)[0].hasAttribute("pop")) {
                popitup(href, 'popoutWindow' + Date.now());
            } else if ($(this)[0].hasAttribute("newtab")) {
                window.open(href, '_blank')
            } else {
                document.location.href = href
            }

        });
    }
});


$(".stop").click(function (e) {
    e.stopImmediatePropagation();
    e.stopPropagation();
});

$(".stop-pop").click(function (e) {
    e.stopImmediatePropagation();
    e.preventDefault();
    href = $(this).attr("href");
    popitup(href, 'popoutWindow' + Date.now());
});

$(".stop-blank").click(function (e) {
    e.stopImmediatePropagation();
    e.preventDefault();
    url = $(this).attr("href");
    var win = window.open(url, '_blank');
    win.focus();
});