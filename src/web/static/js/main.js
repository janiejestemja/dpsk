"use strict";
function toggleNavbar() {
    var navLinks = document.getElementById("nav-links");
    navLinks?.classList.toggle("nav-open");
}
function showBelow(btn) {
    const target = btn.nextElementSibling;
    target?.classList.toggle("shown");
}
