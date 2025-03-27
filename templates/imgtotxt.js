<div class="container">
        <h1 class="text-center">Image to Text Converters</h1>

        <div class="row">
            <div class="col-md-6">
                <label for="file" class="btn btn-primary btn-block">Choose Image</label>
                <input id="file" type="file" style="display: none;">
            </div>
            <div class="col-md-6">
                <button id="openCameraBtn" class="btn btn-primary btn-block">Open Camera</button>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12 text-center">
                <video id="previewVideo" class="img-preview" style="display: none;"></video>
                <p id="previewText">No image selected</p>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <h2>Extracted Text:</h2>
                <p id="extractedText">Text will appear here...</p>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <button id="captureBtn" class="btn btn-primary btn-block" style="display: none;">Capture Image</button>
            </div>
        </div>
    </div>
    <div id="carouselExampleIndicators" class="carousel slide">
        <div class="carousel-indicators">
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
        </div>
        <div class="carousel-inner">
            <div class="carousel-item active">
                <img src="car1.png" class="d-block mx-auto" width="100" height="100"  alt="..."/>
            </div>
            <div class="carousel-item">
                <img src="car2.png" class="d-block mx-auto w-30" alt="..."/>
            </div>
            <div class="carousel-item">
                <img src="car3.png" class="d-block mx-auto w-30" alt="..."/>
            </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
        </button>
    </div>
    <script>
        let videoStream;
        let videoElement;

        document.getElementById('file').addEventListener('change', function () {
            const file = this.files[0];
            const formData = new FormData();
            formData.append('image', file);

            fetch('/capture_text', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('extractedText').innerText = data.text;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });

        document.getElementById('openCameraBtn').addEventListener('click', function () {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    videoStream = stream;
                    videoElement = document.createElement('video');
                    videoElement.srcObject = stream;
                    videoElement.autoplay = true;
                    videoElement.classList.add('img-preview');
                    document.getElementById('previewText').innerText = 'Camera Preview';
                    document.getElementById('previewVideo').replaceWith(videoElement);
                    document.getElementById('captureBtn').style.display = 'block';
                })
                .catch(err => {
                    console.error('Error accessing the camera:', err);
                });
        });

        document.getElementById('captureBtn').addEventListener('click', function () {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = videoElement.videoWidth;
            canvas.height = videoElement.videoHeight;
            context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

            const imgDataUrl = canvas.toDataURL('image/png');

            fetch('/capture_text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imgDataUrl })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('extractedText').innerText = data.text;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    </script>