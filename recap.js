// Function triggered when client clicks [Verify]
function verifyCaptcha() {

    alert("Verified!");
    closeVerifyWindow();

}





let checkboxWindow = document.getElementById("fkrc-checkbox-window");
let checkboxBtn = document.getElementById("fkrc-checkbox");
let checkboxBtnSpinner = document.getElementById("fkrc-spinner");
let verifyWindow = document.getElementById("fkrc-verifywin-window");
let verifyWindowArrow = document.getElementById("fkrc-verifywin-window-arrow");
let verifyBtn = document.getElementById("fkrc-verifywin-verify-button");

function addCaptchaListeners() {
    if (checkboxBtn && verifyBtn) {
        document.addEventListener("click", function (event) {
            if (!event.path.includes(verifyWindow) && isVerifyWindowVisible()) {
                closeVerifyWindow();
            }
        });
        
