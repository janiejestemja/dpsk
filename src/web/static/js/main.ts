function toggleNavbar() {
    var navLinks = document.getElementById("nav-links");
    navLinks?.classList.toggle("nav-open");
}

function showBelow(btn: HTMLButtonElement) {
    const target = btn.nextElementSibling;
    target?.classList.toggle("shown");
}