// Load the toggle homepage featured view when featured checkbox clicked
// Changing the value of this model field
let checks = document.getElementsByClassName("home-featured");
for (let check of checks) {
    check.addEventListener("click", function () {
        let url = this.getAttribute("data-url");
        window.location.href = url;
    });
}