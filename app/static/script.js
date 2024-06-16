let imageFile;
let imageWidth;
let imageHeight;

document.getElementById('image').addEventListener('change', function(event) {
    // Hide images and download link
    const downloadLink = document.getElementById('download-link');
    downloadLink.style.display = "none"

    const preview = document.getElementById('image-preview');
    preview.style.display = "none"

    const base64Preview = document.getElementById('ascii-art');
    base64Preview.style.display = "none"

    imageFile = event.target.files[0];

    // console.log("image file", imageFile)
    if (imageFile) {       
        // Show Image dimensions
        const img = new Image();
        img.src = URL.createObjectURL(imageFile);
        img.onload = function() {
            imageWidth = img.width;
            imageHeight = img.height;
            // console.log(`Image dimensions: ${imageWidth}x${imageHeight}`);
        };

        // Display Preview
        const preview = document.getElementById('image-preview');
        preview.src = URL.createObjectURL(imageFile);
        preview.style.display = 'block';
        preview.style.height = imageHeight
        preview.style.width = imageWidth

    }
});

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    // Clear output of both images
    // const downloadLink = document.getElementById('download-link');
    // downloadLink.style.display = "none"

    // const preview = document.getElementById('image-preview');
    // preview.style.display = "none"

    const form = event.target;
    // console.log("event.target", form)
    const formData = new FormData(form);
    // console.log("formData", formData)

    fetch(form.action, {
        method: form.method,
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data);
        if (data) {
            // Get Original Image Details
            const fileNameAndFormat = imageFile.name.split(".");
			const fileFormat = fileNameAndFormat.pop();
			const imageName = fileNameAndFormat.join("");

            // Update ASCII Art
            const base64Preview = document.getElementById('ascii-art');
            base64Preview.src = `data:image/${"png"};base64,${data}`;
            base64Preview.style.display = 'block';
            base64Preview.style.height = imageHeight
            base64Preview.style.width = imageWidth
            
            // Update Download Button
            const downloadLink = document.getElementById('download-link');
            downloadLink.href = base64Preview.src;
            downloadLink.download = `${imageName}_ascii.${fileFormat}`;
            downloadLink.title = `${imageName}_ascii.${fileFormat}`;
            downloadLink.style.display = "block"
        }
        
    }).catch(error => {
        console.error('Error:', error);
    });
});
