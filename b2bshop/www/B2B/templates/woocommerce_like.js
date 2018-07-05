

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
    if (x[i].className.indexOf(c) > -1) {
		w3AddClass(x[i], "show");
		w3RemoveClass(x[i].parentNode.parentNode, "hidden");
	}
  }
}

// Show filtered elements
function w3AddClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {
      element.className += " " + arr2[i];
    }
  }
}

// Hide elements that are not selected
function w3RemoveClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}

// Add active class to the current control button (highlight it)
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("filterdiv-btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}
/*----------------------------------------------------------------------------------*/
/* modal section */
/*------------------------------------------------------------------------------------*/
function open_order_modal(item) {
	order_modal = document.getElementById(item);
	order_modal.style.display = "block";
	
	/* disabled magnify function */
	/*magnify("myimage-"+item, 2);*/
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

/* disabled magnify section */
/*----------------------------------------------------------------------------------*/

/*function magnify(imgID, zoom) {
  var img, glass, w, h, bw;
  img = document.getElementById(imgID);*/

  /*create magnifier glass:*/
  /*glass = document.createElement("DIV");
  glass.setAttribute("class", "img-magnifier-glass");*/

  /*insert magnifier glass:*/
 /* img.parentElement.insertBefore(glass, img);*/

  /*set background properties for the magnifier glass:*/
  /*glass.style.backgroundImage = "url('" + img.src + "')";
  glass.style.backgroundRepeat = "no-repeat";
  glass.style.backgroundSize = (img.width * zoom) + "px " + (img.height * zoom) + "px";
  bw = 3;
  w = glass.offsetWidth / 2;
  h = glass.offsetHeight / 2;*/

  /*execute a function when someone moves the magnifier glass over the image:*/
  /*glass.addEventListener("mousemove", moveMagnifier);
  img.addEventListener("mousemove", moveMagnifier);*/

  /*and also for touch screens:*/
 /* glass.addEventListener("touchmove", moveMagnifier);
  img.addEventListener("touchmove", moveMagnifier);
  function moveMagnifier(e) {
    var pos, x, y;*/
    /*prevent any other actions that may occur when moving over the image*/
   /* e.preventDefault();*/
    /*get the cursor's x and y positions:*/
  /*  pos = getCursorPos(e);
    x = pos.x;
    y = pos.y;*/
    /*prevent the magnifier glass from being positioned outside the image:*/
   /* if (x > img.width - (w / zoom)) {x = img.width - (w / zoom);}
    if (x < w / zoom) {x = w / zoom;}
    if (y > img.height - (h / zoom)) {y = img.height - (h / zoom);}
    if (y < h / zoom) {y = h / zoom;}*/
    /*set the position of the magnifier glass:*/
   /* glass.style.left = (x - w) + "px";
    glass.style.top = (y - h) + "px";*/
    /*display what the magnifier glass "sees":*/
   /* glass.style.backgroundPosition = "-" + ((x * zoom) - w + bw) + "px -" + ((y * zoom) - h + bw) + "px";
  }

  function getCursorPos(e) {
    var a, x = 0, y = 0;
    e = e || window.event;*/
    /*get the x and y positions of the image:*/
   /* a = img.getBoundingClientRect();*/
    /*calculate the cursor's x and y coordinates, relative to the image:*/
   /* x = e.pageX - a.left;
    y = e.pageY - a.top;*/
    /*consider any page scrolling:*/
   /* x = x - window.pageXOffset;
    y = y - window.pageYOffset;
    return {x : x, y : y};
  }
}*/
/*-------------------------------------------------------------------------------------------*/

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
			_order_item.push(items[i].value);
			order_item.push(_order_item);
			check_order = true;
		}
	}
	if (check_order) {
		_placeOrder(order_item[0][0], order_item[0][1]);
		for (var i = 1; i < order_item.length; i++) {
			if (i != order_item.length - 1){
				doPlaceOrderWithTimeout(order_item[i][0], order_item[i][1], i);
			} else {
				doPlaceOrderWithTimeout(order_item[i][0], order_item[i][1], i, true);
			}
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
//var slideIndex = 1;
//showSlides(slideIndex);

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
  /*var captionText = document.getElementById("caption");*/
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
  /*captionText.innerHTML = dots[slideIndex-1].alt;*/
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