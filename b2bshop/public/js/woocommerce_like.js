if (window.location.href.indexOf("orders") > -1) {
    try {
        var btn = document.getElementById("pay-for-order");
        btn.classList.add("hidden");
    } catch {}
}

if (window.location.href.indexOf("invoices") > -1) {
    try {
        var btn = document.getElementById("pay-for-order");
        btn.classList.add("hidden");
        
    } catch {}
}

if (window.location.href.indexOf("me") > -1) {
    try {
        $("[href='/third_party_apps']").parent().remove();
        
    } catch {}
}

frappe.ready(function() {
    if (frappe.is_user_logged_in()) {
        setTimeout(function(){ $(".cart-icon").show(); }, 500);
    }
    if (window.location.href.indexOf("cart") > -1) {
        try {
            frappe.call({
                "method": "b2bshop.utils.get_weiter_btn",
                "args": {},
                "async": false,
                "callback": function(response) {
                    var btn_txt = response.message;
                    console.log(btn_txt);
                    var weiter_btn = $('<button class="btn btn-secondary" type="button">' + btn_txt + '</button>')
                    weiter_btn.on("click", function() {
                        window.location.href = "/B2B/shop";
                    });
                    var btn_area = $('.page-header-actions-block');
                    btn_area.append(weiter_btn);
                }
            });
            
        } catch {}
    }
});


/* Filter section */
/*---------------------------------------------------------*/
show_all_elements();

function show_all_elements() {
    hide_all_elements();
    elemente = document.getElementsByClassName("filterDiv");
    for (var i = 0; i < elemente.length; i++) {
        addFilterClass(elemente[i], "show");
        removeFilterClass(elemente[i].parentNode.parentNode, "hidden");
    }
}

function hide_all_elements() {
    elemente = document.getElementsByClassName("filterDiv");
    for (var i = 0; i < elemente.length; i++) {
        removeFilterClass(elemente[i], "show");
        addFilterClass(elemente[i].parentNode.parentNode, "hidden");
    }
}

function reset_all_filters() {
    var filter_doms = document.getElementsByClassName("filterContainer");
    for (var i = 0; i < filter_doms.length; i++) {
        if (filter_doms[i].dataset.filtertype == "Size") {
            $(filter_doms[i].childNodes[1]).text("Show all");
        } else if (filter_doms[i].dataset.filtertype == "Color") {
            $(filter_doms[i].childNodes[1]).text("Show all");
        } else if (filter_doms[i].dataset.filtertype == "SoleColor") {
            $(filter_doms[i].childNodes[1]).text("Show all");
        } else if (filter_doms[i].dataset.filtertype == "Group") {
            $(filter_doms[i].childNodes[1]).text("Show all");
        }
    }
    show_all_elements();
}

function show_based_on_filter(self, value) {
    if (['sole-color-all', 'color-all', 'size-all', 'Show-all'].includes(value)) {
        $($(self)[0].parentNode.parentNode.childNodes[1]).text('Show all')
    } else {
        value = value.replace("size-", "").replace("color-", "").replace("sole-", "");
        $($(self)[0].parentNode.parentNode.childNodes[1]).text(value);
    }
    
    var filter_doms = document.getElementsByClassName("filterContainer");
    var filters = []
    
    for (var i = 0; i < filter_doms.length; i++) {
        if (!['show all'].includes(filter_doms[i].childNodes[1].innerText.toLowerCase())) {
            if (filter_doms[i].dataset.filtertype == "Size") {
                filters.push("size-" + filter_doms[i].childNodes[1].innerText.toLowerCase());
            } else if (filter_doms[i].dataset.filtertype == "Color") {
                filters.push("color-" + filter_doms[i].childNodes[1].innerText.toLowerCase());
            } else if (filter_doms[i].dataset.filtertype == "SoleColor") {
                filters.push("sole-color-" + filter_doms[i].childNodes[1].innerText.toLowerCase());
            } else {
                // group
                filters.push(filter_doms[i].childNodes[1].innerText.toLowerCase());
            }
        }
    }
    
    hide_all_elements();
    
    if (filters.length < 2) {
        for (var filterValue = 0; filterValue < filters.length; filterValue++) {
            elemente = document.getElementsByClassName("filterDiv");
            for (var elmnt = 0; elmnt < elemente.length; elmnt++) {
                if (elemente[elmnt].className.indexOf(filters[filterValue]) > -1) {
                    addFilterClass(elemente[elmnt], "show");
                    removeFilterClass(elemente[elmnt].parentNode.parentNode, "hidden");
                }
            }
        }
        
        if (filters.length < 1) {
            show_all_elements();
        }
    } else {
        elemente = document.getElementsByClassName("filterDiv");
        for (var elmnt = 0; elmnt < elemente.length; elmnt++) {
            var not_found = false;
            for (var filterValue = 0; filterValue < filters.length; filterValue++) {
                if (elemente[elmnt].className.indexOf(filters[filterValue]) > -1) {
                    //filter found, all good
                } else {
                    not_found = true;
                }
            }
            if (!not_found) {
                addFilterClass(elemente[elmnt], "show");
                removeFilterClass(elemente[elmnt].parentNode.parentNode, "hidden");
            }
        }
    }
    
}

// Show filtered elements
function addFilterClass(element, name) {
    element.classList.add(name);
}

// Hide elements that are not selected
function removeFilterClass(element, name) {
    element.classList.remove(name);
}

/*----------------------------------------------------------------------------------*/
/* modal section */
/*------------------------------------------------------------------------------------*/
function open_order_modal(item) {
    order_modal = document.getElementById(item);
    order_modal.style.display = "block";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    modals = document.getElementsByClassName("modal")
    for (var i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        }
    }
}
/*---------------------------------------------------------------------------------*/

/* place order section */
/*----------------------------------------------------------------------------------------------*/
function placeOrder(ref_item) {
    openNav();
    var ref_container = document.getElementById(ref_item);
    var items = ref_container.getElementsByClassName('item-qty');
    var check_order = false;

    var order_item = [];
    for (i = 0; i < items.length; i++) {
        if (items[i].value > 0) {
            _order_item = [];
            _order_item.push(items[i].id);
            _order_item.push($(items[i]).val());
            order_item.push(_order_item);
            check_order = true;
        }
    }
    if (check_order) {
        if (order_item.length > 1 ) {
            _placeOrder(order_item[0][0], order_item[0][1]);
            for (var i = 1; i < order_item.length; i++) {
                if (i != order_item.length - 1){
                    doPlaceOrderWithTimeout(order_item[i][0], order_item[i][1], i);
                } else {
                    doPlaceOrderWithTimeout(order_item[i][0], order_item[i][1], i, true);
                }
            }
        } else {
            _placeOrder(order_item[0][0], order_item[0][1], true);
        }
    } else {
        modal = document.getElementById('empty');
        modal.style.display = "block";
        closeNav();
    }
}

function _placeOrder(_item_code, _qty, last=false) {
    frappe.provide('erpnext.shopping_cart');

    erpnext.shopping_cart.update_cart({
        item_code: _item_code,
        qty: _qty,
        callback: function(r) {
            if(!r.exc) {
                frappe.call({
                    method:"b2bshop.utils.check_and_update_warehouse_in_quotation",
                    args:{
                        item: _item_code,
                        qty: _qty
                    }
                });				
            } else {
                    window.alert("oops");
            }
        },
        btn: this,
    });
    if (last) {
        modal = document.getElementById('goToCart');
        modal.style.display = "block";
        closeNav();
    }
}
function doPlaceOrderWithTimeout(item, value, i, last=false) {
    setTimeout(function(){ _placeOrder(item, value, last); }, i * 1000);
}

/*------------------------------------------------------------------------------------------------------*/

/* slideshow section */
/*-------------------------------------------------------------------------------------------------------*/

// Next/previous controls
function plusSlides(n, item) {
    var slideIndex = 0;
    var slide_parent = document.getElementsByClassName("slideshow-container-" + item);
    var slides = slide_parent[0].getElementsByClassName("mySlides");
    var dots = slide_parent[0].getElementsByClassName("demo");
    for (i = 0; i < dots.length; i++) {
        if ($(dots[i]).hasClass("active")) {
            slideIndex = i + 1;
        }
    }
    slideIndex += n;
    showSlides(slideIndex, item);
}

// Thumbnail image controls
function currentSlide(n, item) {
    var slideIndex = n;
    showSlides(slideIndex, item);
}

function showSlides(n, item) {
    var slideIndex = n;
    var i;
    var slide_parent = document.getElementsByClassName("slideshow-container-" + item);
    var slides = slide_parent[0].getElementsByClassName("mySlides");
    var dots = slide_parent[0].getElementsByClassName("demo");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
}
/*--------------------------------------------------------------------------------------------------------------*/


/* Open */
function openNav() {
    document.getElementById("myNav").style.display = "block";
}

/* Close */
function closeNav() {
    document.getElementById("myNav").style.display = "none";
} 

function close_modal(modal_ref) {
    modal = document.getElementById(modal_ref);
    modal.style.display = "none";
}
