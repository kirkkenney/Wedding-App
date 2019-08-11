var fileBtn = document.getElementById("fileBtn");
var uploadBtn = document.getElementById("uploadBtn");
var submitBtn = document.getElementById("submitPhotoBtn");
var photoPreview = document.getElementById("photoPreview");


function preview() {
    fileBtn.click()
}

function showPreview() {
    photoPreview.src = window.URL.createObjectURL(this.files[0])
    if (photoPreview.src.length > 0) {
        submitBtn.style.display = "inline-block";
    } else {
        submitBtn.style.display = "none";
    }
}


uploadBtn.addEventListener("click", preview)
fileBtn.addEventListener("change", showPreview)
