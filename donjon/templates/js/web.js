let currentSelection;
function toggleBorder(img) {
    if (currentSelection) { // pas la première utilisation
        currentSelection.style.border = "none"; // enlève la bordure de l'image précédente     
    }
    currentSelection = img; // change l'image sélectionnée
    currentSelection.style.border = "2px solid #3DC3C5";
}

function reset_border() {
    currentSelection.style.border = "none"
}