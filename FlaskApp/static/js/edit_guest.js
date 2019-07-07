guestsField = document.getElementById('guestsField')
guestsNames = document.getElementById('guestsNamesField')
guestsNamesField = document.getElementById('guestsNamesField').querySelector('input')


// Set default display property of input field for additional guests names
// if field is empty (called from the databased), then field is hiddden

function toggleDefaultDisplay() {
    if (guestsNamesField.value.length > 0) {
        guestsNames.style.display = "block";
    }
}


// change display property of additional guest names if guest is edited to
// include additional guests


function toggleDisplay() {
    if (guestsField.innerHTML != '0') {
    guestsNames.style.display = "block"
    } else {
    guestsNames.style.display = "none"
}
}


guestsField.addEventListener('change', toggleDisplay)


toggleDefaultDisplay()
