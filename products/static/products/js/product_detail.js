// JS for the product detail page

// Change the arrow on the accordian button to up when the accordian is open
$(".collapse").on('shown.bs.collapse', function () {
    let iElement = $(this).siblings(".card-header").find("i")[0];
    if (iElement.classList.contains("fa-chevron-down")) {
        iElement.classList.remove("fa-chevron-down");
        iElement.classList.add("fa-chevron-up");
    }
});

// Change the arrow on the accordian button to down when the accordian is closed
$(".collapse").on('hidden.bs.collapse', function () {
    let iElement = $(this).siblings(".card-header").find("i")[0];
    if (iElement.classList.contains("fa-chevron-up")) {
        iElement.classList.remove("fa-chevron-up");
        iElement.classList.add("fa-chevron-down");
    }
});

// Check the inventory when the quantity box is updated
let productInventory = $('#id_product_inventory').text();
let productId = $('#id_product_id').text();
let addQuantity = document.getElementById(`id_qty_${productId}`);
let addButton = document.getElementById("add-to-basket-btn");
let stock = parseInt(productInventory);
addQuantity.addEventListener('change', function () {
    // Disable the add to basket button when quantity greater than inventory
    // Already disabled in the html when inventory 0
    if (stock > 0 && this.value > stock) {
        addButton.setAttribute("aria-disabled", "true");
        document.getElementById("stock-notification").innerHTML = `Only ${stock} left in stock.`;
    } else if (stock > 0 && this.value <= stock) {
        // Reenable button when quantity less or equal to stock
        addButton.removeAttribute("aria-disabled");
        document.getElementById("stock-notification").innerHTML = ''
    }
})

// Prevent low stock product from being added to basket on pressing enter
addQuantity.addEventListener('keydown', function (event) {
    if (event.key === "Enter") {
        if (addButton.hasAttribute("aria-disabled")) {
            event.preventDefault();
        } else if (stock > 0 && this.value > stock) {
            document.getElementById("stock-notification").innerHTML = `Only ${stock} left in stock.`;
            event.preventDefault();
        }
    }
})
