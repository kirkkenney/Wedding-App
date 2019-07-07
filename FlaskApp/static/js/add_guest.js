const guestNamesField = document.getElementById('addGuestNames')
const guestField = document.getElementById('addGuests')


function fieldDisplay() {
    if (guestField.value == '0') {
        guestNamesField.style.display = "none"
    } else {
        guestNamesField.style.display = "block"
    }
}


guestField.addEventListener('change', fieldDisplay)
