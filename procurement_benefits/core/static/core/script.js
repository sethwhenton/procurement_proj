document.addEventListener("DOMContentLoaded", function() {
    // Handle item form submission
    const itemForm = document.getElementById("item-form");

    if (itemForm) { // Check if itemForm exists to avoid null error
        itemForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const itemId = document.getElementById("item-select").value;
            const quantity = document.getElementById("quantity").value;

            fetch("{% url 'add_to_cart' %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    item_id: itemId,
                    quantity: quantity
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    updateCart();
                }
            });
        });
    }

    function updateCart() {
        fetch("{% url 'summary_checkout' %}")
        .then(response => response.text())
        .then(html => {
            document.getElementById("cart").innerHTML = html;
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
