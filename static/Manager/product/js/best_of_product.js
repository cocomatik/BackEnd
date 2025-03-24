document.addEventListener("DOMContentLoaded", function () {
    const categoryLinks = document.querySelectorAll(".best-category-link");
    const productRows = document.querySelectorAll(".best-products-table tbody tr");
    const bestOfForm = document.getElementById("best-of-form");
    const successMessage = document.getElementById("success-message");

    // Function to filter products based on category selection
    function filterProducts(selectedCategory) {
        document.getElementById("best-category-title").innerText = selectedCategory + " Products";

        productRows.forEach(row => {
            row.style.display = row.getAttribute("data-category") === selectedCategory ? "table-row" : "none";
        });
    }

    // Highlight selected category and filter products
    categoryLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const selectedCategory = this.getAttribute("data-category");

            categoryLinks.forEach(link => link.classList.remove("active"));
            this.classList.add("active");

            filterProducts(selectedCategory);
        });
    });

    // Handle form submission with AJAX
    bestOfForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(bestOfForm);

        fetch(window.location.href, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                successMessage.style.display = "block";
                setTimeout(() => {
                    successMessage.style.display = "none";
                }, 3000);
            } else {
                // alert("Error updating products. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            // alert("An unexpected error occurred. Please try again.");
        });
    });

    // Automatically filter products if a category is pre-selected
    const activeCategory = document.querySelector(".best-category-link.active");
    if (activeCategory) {
        filterProducts(activeCategory.getAttribute("data-category"));
    }
});
