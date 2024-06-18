document.getElementById("image").addEventListener("change", function (event) {
	// Hide images and download link
	const downloadLink = document.getElementById("download-link");
	downloadLink.style.display = "none";

	const previewFigure = document.getElementById("image-preview-figure");
	previewFigure.style.display = "none";

	const base64PreviewFigure = document.getElementById("ascii-art-figure");
	base64PreviewFigure.style.display = "none";

	// Show Sliders
	const backgroundAlphaContainer = document.getElementById(
		"background_alpha_container"
	);
	backgroundAlphaContainer.style.display = "block";

	const fontSizeContainer = document.getElementById("font_size_container");
	fontSizeContainer.style.display = "block";

	imageFile = event.target.files[0];

	if (imageFile) {
		// Show Image dimensions
		const img = new Image();
		img.src = URL.createObjectURL(imageFile);
		img.onload = function () {
			// Set max font size for slider
			const fontSize = document.getElementById("font_size");
			fontSize.max = Math.floor(parseInt(img.width) / 2);

			// const fontSizeMax = document.getElementById("font_size_max")
			// fontSizeMax.textContent = fontSize.max

			// Set Image Preview Dimensions
			const preview = document.getElementById("image-preview");
			const previewFigure = document.getElementById(
				"image-preview-figure"
			);
			preview.src = URL.createObjectURL(imageFile);
			previewFigure.style.display = "block";
			preview.style.height = img.height;
			preview.style.width = img.width;
		};
	}
});

document
	.getElementById("upload-form")
	.addEventListener("submit", function (event) {
		// Show Loading Display
		const loading = document.getElementById("loading");
		loading.classList.remove("hidden");
		loading.classList.add("flex");

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
			.then((response) => response.json())
			.then((data) => {
				// console.log(data);
				if (data) {
					// Get Original Image Details
					const fileNameAndFormat = imageFile.name.split(".");
					const fileFormat = fileNameAndFormat.pop();
					const imageName = fileNameAndFormat.join("");

					// Update ASCII Art Dimensions
					const preview = document.getElementById("image-preview");
					const base64Preview = document.getElementById("ascii-art");
					const base64PreviewFigure =
						document.getElementById("ascii-art-figure");
					base64Preview.src = `data:image/${"png"};base64,${data}`;
					base64PreviewFigure.style.display = "block";
					base64Preview.style.height = preview.style.height;
					base64Preview.style.width = preview.style.width;

					// Update Download Button
					const downloadLink =
						document.getElementById("download-link");
					downloadLink.href = base64Preview.src;
					downloadLink.download = `${imageName}_ascii.${fileFormat}`;
					downloadLink.title = `${imageName}_ascii.${fileFormat}`;
					downloadLink.style.display = "block";
				}
			})
			.catch((error) => {
				console.error("Error:", error);
			})
			.finally(() => {
				// Hide Loading
				const loading = document.getElementById("loading");
				loading.classList.remove("flex");
				loading.classList.add("hidden");
			});
	});

document
	.getElementById("background_alpha")
	.addEventListener("dragstart", function (event) {
		event.preventDefault();
		event.stopPropagation();
	});

document
	.getElementById("font_size")
	.addEventListener("dragstart", function (event) {
		event.preventDefault();
		event.stopPropagation();
	});
