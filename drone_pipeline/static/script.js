document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('imageInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const fileName = document.getElementById('fileName');
    const resultImage = document.getElementById('resultImage');
    const humanCount = document.getElementById('humanCount');
    const carCount = document.getElementById('carCount');
    const loader = document.getElementById('loader');
    const placeholderText = document.getElementById('placeholderText');

    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            fileName.textContent = file.name;
            analyzeBtn.disabled = false;
            
            // Preview
            const reader = new FileReader();
            reader.onload = (event) => {
                resultImage.src = event.target.result;
                placeholderText.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    });

    analyzeBtn.addEventListener('click', async () => {
        const file = imageInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('image', file);

        // Show loading state
        loader.classList.remove('loader-hidden');
        loader.classList.add('loader-visible');
        resultImage.style.opacity = '0.3';
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.error) {
                alert(data.error);
            } else {
                // Update UI
                resultImage.src = `data:image/png;base64,${data.image}`;
                humanCount.textContent = data.human_count;
                carCount.textContent = data.car_count;
                
                // Animate counts
                animateValue(humanCount, 0, data.human_count, 1000);
                animateValue(carCount, 0, data.car_count, 1000);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Analysis failed. Please check backend connection.');
        } finally {
            loader.classList.remove('loader-visible');
            loader.classList.add('loader-hidden');
            resultImage.style.opacity = '1';
            analyzeBtn.disabled = false;
        }
    });

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});
