// Scroll to top of page on back to top button click event.
let toTopButton = document.getElementById("to-top-link");
toTopButton.addEventListener("click", function () {
    window.scrollTo(0, 0);
});

// Check whether designer images are portrait and if so
// add portrait class to ensure they display correctly.
let designerImages = document.getElementsByClassName("designer-img");

function checkImgSize(image) {
    let newImg = new Image();
    newImg.onload = function () {
        let height = newImg.height;
        let width = newImg.width;

        if (height > width) {
            image.classList.add("portrait");
        }
    };
    newImg.src = image.src;
}
for (let image of designerImages) {
    checkImgSize(image);
}
