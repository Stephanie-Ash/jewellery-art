// Listen for change in review product select box
document.getElementById("review-sel").addEventListener("change", function () {
    let selectedProduct = this.value;
    let addForm = document.getElementById("add-review-form");
    let addButton = document.getElementById("add-review-button");
    if (selectedProduct) {
        // Display add review button when product selected
        addButton.style.display = "initial";
        // Set url for form action based on selected product
        let url = "/products/add_review/123/";
        addForm.action = url.replace('123', selectedProduct);
    } else {
        // If no product remove add button and form action url
        addButton.style.display = "none";
        addForm.action = '#';
    }
});

let edits = document.getElementsByClassName("review-edit");
    // Dispaly review edit form when edit button selected
    for (let edit of edits) {
        edit.addEventListener("click", function () {
            this.style.display = "none";
            let form = this.parentNode.getElementsByTagName('form')[0];
            let deleteBtn = this.nextElementSibling;
            let review = this.previousElementSibling;
            form.style.display = "initial";
            deleteBtn.style.display = "none";
            review.style.display = "none";
        });
    }
