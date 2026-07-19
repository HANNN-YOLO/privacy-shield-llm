/* ======================================================
INITIALIZE UI
====================================================== */
function initializeUI() {
    console.log("Initialize UI");
    hideLoading();
}

// * ======================================================
// Cek Fast API
// ====================================================== */
function updateAPIStatus(online){
    const badge =
        document.getElementById("api-status");
    if(online){
        badge.innerHTML="🟢 Fast API Online";
    }
    else{
        badge.innerHTML="🔴 Fast API Offline";
    }
}

/* ======================================================
GET CLINICAL NOTE
====================================================== */
function getClinicalText() {
    return document
        .getElementById("clinical-note")
        .value;
}

/* ======================================================
DISPLAY REDACTED RESULT
====================================================== */
function displayRedactedText(response) {
    const resultBox = document.getElementById("redacted-result");
    resultBox.value = response.redacted_text;
    // resultBox.value = text
}

/* ======================================================
DISPLAY ENTITY
====================================================== */
function displayEntities(response) {
    document.getElementById("entity-name").innerHTML =
        response.entities.name.join(", ");
    document.getElementById("entity-email").innerHTML =
        response.entities.email.join(", ");
    document.getElementById("entity-phone").innerHTML =
        response.entities.phone.join(", ");
    document.getElementById("entity-address").innerHTML =
        response.entities.address.join(", ");
    document.getElementById("entity-date").innerHTML =
        response.entities.date.join(", ");
}

/* ======================================================
CLEAR INPUT
====================================================== */
function clearClinicalNote() {
    document.getElementById("clinical-note").value = "";
    document.getElementById("redacted-result").value = "";
    updateDashboard();
    addLog("Clinical Note Cleared");
}

/* ======================================================
LOADING
====================================================== */
function showLoading() {
    document
        .getElementById("loading-overlay")
        .style.display = "flex";
}

function hideLoading() {
    document
        .getElementById("loading-overlay")
        .style.display = "none";
}

/* ======================================================
TOAST
====================================================== */
function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    toast.innerHTML = message;
    toast.className = "toast";
    toast.classList.add(type);
    toast.style.display = "block";
    setTimeout(() => {
        toast.style.display = "none";
    }, 3000);
}

/* ======================================================
COPY RESULT
====================================================== */
function copyResult() {
    const text =
        document.getElementById("redacted-result").value;
    navigator.clipboard.writeText(text);
    showToast("Copied");
    addLog("Copy Result");
}

/* ======================================================
DOWNLOAD RESULT
====================================================== */
function downloadResult() {
    const result =
        document.getElementById("redacted-result").value;
    const blob =
        new Blob([result], {
            type: "text/plain"
        });
    const url =
        URL.createObjectURL(blob);
    const link =
        document.createElement("a");
    link.href = url;
    link.download = "redacted_result.txt";
    link.click();
    URL.revokeObjectURL(url);
    showToast("Downloaded");
    addLog("Download Result");
}

/* ======================================================
FILE UPLOAD
====================================================== */
function openFileDialog() {
    document
        .getElementById("file-input")
        .click();
}

function handleFileUpload(event) {
    const file =
        event.target.files[0];
    if (!file) return;
    const reader =
        new FileReader();
    reader.onload = function(e) {
        document
            .getElementById("clinical-note")
            .value = e.target.result;
        updateDashboard();
        addLog("TXT Uploaded");
    }
    reader.readAsText(file);
}