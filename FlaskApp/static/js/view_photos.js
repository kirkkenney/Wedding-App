var modal = document.getElementById('photoModal');
var closeModalBtn = document.getElementById('closePhotoModal');
var imageTiles = document.getElementsByClassName('imageTile');
var modalPhoto = document.getElementById('photoModalView');
var gallery = document.getElementById('photoGallery');
var imgIndex;
var next = document.getElementById('nextPhoto');
var prev = document.getElementById('prevPhoto');

// get all image tile divs and apply onclick event to them to open modal
for (var i = 0, len = gallery.children.length; i < len; i++) {
    (function(index) {
        gallery.children[i].onclick = function() {
            // imgIndex set as a global variable for use in modal image slideshow
            // starting with the image tile that was clicked
            imgIndex = index;
            // open modal
            modal.style.display = "block";
            // get background image from clicked tile
            imgSrc = this.style.backgroundImage.slice(4, -1).replace(/"/g, "");
            // set image src property of modal
            modalPhoto.src = imgSrc;
        }
    })(i);
}

function nextPhoto() {
    // increment imgIndex value to get background image of next image tile
    imgIndex++;
    if (imgIndex >= imageTiles.length) {
        imgIndex = 0;
    }
    // set image src property of modal
    modalPhoto.src = imageTiles[imgIndex].style.backgroundImage.slice(4, -1).replace(/"/g, "");
}

function prevPhoto() {
    // decrement imgIndex value to get background image of previous image tile
    imgIndex--;
    if (imgIndex < 0) {
        imgIndex = imageTiles.length-1;
    }
    modalPhoto.src = imageTiles[imgIndex].style.backgroundImage.slice(4, -1).replace(/"/g, "");
}


closeModalBtn.addEventListener("click", function() {
    // reset modal image src
    modalPhoto.src = "";
    // close modal window
    modal.style.display = "none";
})


next.addEventListener("click", nextPhoto)
prev.addEventListener("click", prevPhoto)
