function disableButtons() {
    const buttons = document.getElementsByClassName("submitBtn");
    for (let button of buttons) {
        button.disabled = true;
    }
}