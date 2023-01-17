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
filterSelection("all")
function filterSelection(c) {
var x, i;
  x = document.getElementsByClassName("filterDiv");
  if (c == "all") c = "";
  // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
  for (i = 0; i < x.length; i++) {
    w3RemoveClass(x[i], "show");
	w3AddClass(x[i].parentNode.parentNode, "hidden")
    if (c == '') {
		if ((x[i].className.indexOf(c) > -1)&&(x[i].className.indexOf('PRE') <= -1)) {
			w3AddClass(x[i], "show");
			w3RemoveClass(x[i].parentNode.parentNode, "hidden");
		}
	} else {
		if (x[i].className.indexOf(c) > -1) {
			w3AddClass(x[i], "show");
			w3RemoveClass(x[i].parentNode.parentNode, "hidden");
		}
	}
  }
}

// Show filtered elements
function w3AddClass(element, name) {
	element.classList.add(name);
}

// Hide elements that are not selected
function w3RemoveClass(element, name) {
	element.classList.remove(name);
}

// Add active class to the current control button (highlight it)
try {
	var btnContainer = document.getElementById("myBtnContainer");
	var btns = btnContainer.getElementsByClassName("filterdiv-btn");
	for (var i = 0; i < btns.length; i++) {
	  btns[i].addEventListener("click", function() {
		var current = document.getElementsByClassName("active");
		current[0].className = current[0].className.replace(" active", "");
		this.className += " active";
	  });
	}
} catch {}
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
  showSlides(slideIndex += n, item);
}

// Thumbnail image controls
function currentSlide(n, item) {
  showSlides(slideIndex = n, item);
}

function showSlides(n, item) {
  var i;
  var slide_parent = document.getElementsByClassName("slideshow-container-" + item);
  console.log(item);
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
