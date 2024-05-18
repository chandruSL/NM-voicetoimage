document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const imageContainer = document.getElementById('imageContainer');

    // Function to show loading spinner
    const showLoading = () => {
        imageContainer.innerHTML = '<div class="loader"></div>';
    };

    // Function to hide loading spinner
    const hideLoading = () => {
        imageContainer.innerHTML = '';
    };

    // Function to display generated image
    const displayImage = (imageData) => {
        imageContainer.innerHTML = `<img src="data:image/png;base64, ${imageData}" alt="Generated Image">`;
    };

    // Event listener for the start button
    startBtn.addEventListener('click', async () => {
        startBtn.disabled = true;
        showLoading();

        try {
            const recognition = new window.webkitSpeechRecognition(); // Create a new SpeechRecognition object
            recognition.lang = 'en-US'; // Set the language for speech recognition

            // Start speech recognition
            recognition.start();

            // Event listener for speech recognition result
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript; // Get the recognized speech transcript
                console.log('Transcript:', transcript);

                // Send the transcript to the backend for image generation
                fetch('/generate-image', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: transcript }), // Send the transcript as JSON data
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.image_base64) {
                        displayImage(data.image_base64);
                    } else {
                        imageContainer.innerHTML = '<p>Error generating image.</p>';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    imageContainer.innerHTML = '<p>Error generating image.</p>';
                })
                .finally(() => {
                    hideLoading();
                    startBtn.disabled = false;
                });
            };

            // Event listener for speech recognition error
            recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                imageContainer.innerHTML = '<p>Error recognizing speech.</p>';
                hideLoading();
                startBtn.disabled = false;
            };
        } catch (error) {
            console.error('Error:', error);
            imageContainer.innerHTML = '<p>Error recognizing speech.</p>';
            hideLoading();
            startBtn.disabled = false;
        }
    });
});
