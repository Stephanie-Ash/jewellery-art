// Scroll to top of page on back to top button click event.
let toTopButton = document.getElementById("to-top-link");
toTopButton.addEventListener("click", function () {
    window.scrollTo(0, 0)
});

// Update the quantity of product in the basket
$('.update-link').click(function (e) {
    let form = $(this).next('.update-form');
    form.submit();
})

// Remove product from basket
$('.remove-item').click(function (e) {
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    let itemId = $(this).attr('id').split('remove_')[1];
    let url = `/basket/remove/${itemId}/`;
    let data = {
        'csrfmiddlewaretoken': csrfToken
    };

    $.post(url, data)
        .done(function () {
            location.reload();
        });
})

// Check stock on quantity update
let quantityInputs = document.getElementsByClassName("qty-input")
for (let input of quantityInputs) {
    input.addEventListener('change', function () {
        let form = this.parentNode.parentNode;
        let updateLink = form.previousElementSibling;
        let inventory = parseInt(updateLink.previousElementSibling.innerHTML);
        // Disable update link if not enough in stock
        if (this.value > inventory) {
            updateLink.setAttribute("aria-disabled", "true");
        } else {
            // Enable update link if enough stock enabled
            updateLink.removeAttribute("aria-disabled");
        }
    })

    // Prevent pressing enter from updating basket if not enough inventory
    input.addEventListener('keydown', function (event) {
        if (event.key === "Enter") {
            let form = this.parentNode.parentNode;
            let updateLink = form.previousElementSibling;
            let inventory = parseInt(updateLink.previousElementSibling.innerHTML);
            if (updateLink.hasAttribute("aria-disabled")) {
                event.preventDefault();
            } else if (this.value > inventory) {
                event.preventDefault();
            }
        }
    })
}

// Select delivery country
let country = document.getElementById('id_country');
// Check if country box there to avoid errors on empty basket page
if (country) {
    // Enable country box which is disabled on the order form
    country.removeAttribute('disabled');
    country.classList.remove('checkout-country-dis');

    country.addEventListener('change', function () {
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        let countryCode = this.value.trim();
        let data = {
            'csrfmiddlewaretoken': csrfToken
        };
        // Submit the country value to set delivery country view
        // Will be saved in session allowing delivery price to be set
        if (countryCode) {
            let url = `/basket/set_delivery_country/${countryCode}/`;
            $.post(url, data).done(function () {
                location.reload();
            });
        } else {
            let url = '/basket/set_delivery_country/no_country/';
            $.post(url, data).done(function () {
                location.reload();
            });
        }
    })
}