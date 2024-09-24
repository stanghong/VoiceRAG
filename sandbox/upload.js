document.getElementById('audioForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('audioFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select an audio file.');
        return;
    }

    const formData = new FormData();
    formData.append('audio', file, file.name);

    try {
        const response = await fetch('http://184.73.60.223:8000/api/voicebot/', {
            method: 'POST',
            body: formData
        });

        const responseText = await response.text();
        document.getElementById('response').innerText = `Response: ${responseText}`;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').innerText = 'An error occurred while uploading the file.';
    }
});