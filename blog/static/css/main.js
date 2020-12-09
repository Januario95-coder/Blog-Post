"use strict";

window.addEventListener('resize', e => {
    if (window.innerWidth <= 640) {
        $(".list-item").attr({'display': 'block'});
    } else {
        $('.ul-header').attr({'display': 'inline-block'});
    }
});
function documentReady() {
    // console.log('Document is ready');


    var toggle_menu = $(".toggle-menu");
    var list_item = $(".list-item");
    toggle_menu.click(() => {
        list_item.attr({'display': 'none'});
        list_item.toggle(1000);
    });

}
$(document).ready(documentReady);
