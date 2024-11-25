document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const fileInput = document.querySelector('input[type="file"]');
    const preview = document.getElementById('imagePreview');
    const error = document.getElementById('error');
    const loading = document.querySelector('.loading');

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;

        if (!isValidFileType(file)) {
            showError('Please select a valid image file (JPG, JPEG, PNG)');
            fileInput.value = '';
            preview.innerHTML = '';
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
        error.style.display = 'none';
    });
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        if (!formData.get('image').size) {
            showError('Please select an image to upload');
            return;
        }

        try {
            loading.style.display = 'block';
            error.style.display = 'none';

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.error) {
                throw new Error(result.error);
            }

            // Redirect to results page
            window.location.href = '/result?' + new URLSearchParams({
                original: result.original_image,
                detected: result.detected_image
            });

        } catch (err) {
            showError(err.message || 'An error occurred during upload');
        } finally {
            loading.style.display = 'none';
        }
    });

    function showError(message) {
        error.textContent = message;
        error.style.display = 'block';
    }

    function isValidFileType(file) {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        return validTypes.includes(file.type);
    }
});