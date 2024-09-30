// Log to verify the script is loaded
console.log("favorites.js loaded!");

// Wait for the document to load before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Select all heart buttons on the page
    const heartButtons = document.querySelectorAll('.heart-button');

    // Loop through each button
    heartButtons.forEach(function(button) {
        // Add an event listener for the click event
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent any default behavior

            const heartButton = event.currentTarget;
            const placeId = heartButton.dataset.placeId; // Get the place ID from the data attribute

            // Toggle the hearted class
            heartButton.classList.toggle('hearted');
            const isFavorited = heartButton.classList.contains('hearted'); // Check if it's favorited

            // Send an AJAX request to the server to update favorites
            fetch(`/add_to_favorites/${placeId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include the CSRF token
                },
                body: JSON.stringify({ favorited: isFavorited })
            })
            .then(response => {
                if (!response.ok) {
                    console.error('Failed to update favorites.');
                    return;
                }

                // Update the button text based on the favorited status
                if (isFavorited) {
                    heartButton.textContent = '❤️ Remove from Favorites';
                } else {
                    heartButton.textContent = '🤍 Add to Favorites';
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Function to get the CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
