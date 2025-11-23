function toggleNavbar() {
    var navLinks = document.getElementById("nav-links");
    navLinks?.classList.toggle("nav-open");
}

function showBelow(btn: HTMLButtonElement) {
    const target = btn.nextElementSibling;
    target?.classList.toggle("shown");
}

function deleteDB() {
    console.log("something");
    fetch("/delete-db", {
        method: "DELETE",
        body: JSON.stringify({ "": ""}),
          headers: { "Content-Type": "application/json" },
    }).then((_res) => {
        window.location.href="/";
    });
}