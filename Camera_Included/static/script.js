document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const preview = document.getElementById('image-preview');
    const resultDiv = document.getElementById('result');

    // Show image preview
    const reader = new FileReader();
    reader.onload = function (e) {
        preview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`;
    };
    reader.readAsDataURL(file);

    // Show loading spinner
    resultDiv.innerHTML = `<div class="loader"></div>`;

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.prediction) {
                resultDiv.innerHTML = `
                    Prediction: <strong>${data.prediction}</strong><br>
                    Confidence: <strong>${data.confidence}%</strong>
                `;
            } else {
                resultDiv.innerHTML = `<span style="color: red;">${data.error}</span>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<span style="color: red;">Error: ${error}</span>`;
        });
});
