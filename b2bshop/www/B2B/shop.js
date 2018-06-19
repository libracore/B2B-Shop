// Accordion controls:
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        /* Toggle between adding and removing the "active" class,
        to highlight the button that controls the panel */
        this.classList.toggle("active");

        /* Toggle between hiding and showing the active panel */
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}
//----------------------------------------------------------------

// Tab controls:
function findAndOpen(pageName) {
	// Hide all elements with class="tabcontent" by default */
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove border of all tablinks/buttons
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("bottomline");
    }
	// Show the specific tab content
	document.getElementById("order " + pageName).style.display = "block";
	
	// Add border to the button used to open the tab content
	document.getElementById(pageName).classList.add("bottomline");
}

function openPage(pageName, elmnt) {
    // Hide all elements with class="tabcontent" by default */
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove border of all tablinks/buttons
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("bottomline");
    }

    // Show the specific tab content
    document.getElementById(pageName).style.display = "block";

    // Add border to the button used to open the tab content
    elmnt.classList.add("bottomline");
}

// Get the element with id="defaultOpen" and click on it
//document.getElementById("defaultOpen").click();
//-----------------------------------------------------------------------------

// Place Order:

// Get the modal
var modal = document.getElementById('empty');
	
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function placeOrder() {
	var items = document.getElementsByClassName('item-qty');
	
	for (i = 0; i < items.length; i++) {
        if (items[i].value > 0) {
			_placeOrder(items[i].id, items[i].value);
			modal = document.getElementById('goToCart');
		}
    }
	modal.style.display = "block";
}

function _placeOrder(_item_code, _qty) {
	frappe.provide('erpnext.shopping_cart');

	erpnext.shopping_cart.update_cart({
		item_code: _item_code,
		qty: _qty,
		callback: function(r) {
			if(!r.exc) {
								
			} else {
					window.alert("oops");
			}
		},
		btn: this,
	});
}
//------------------------------------------------------------------------------

//spec modal:
function open_spec_modal(_modal) {
	modal = document.getElementById(_modal);
	modal.style.display = "block";
}