/*
==========================================================
Privacy Shield LLM

Dashboard Controller

Author : Reyhan Rafaidhil

Mengatur seluruh Dashboard.

Tidak ada komunikasi API.

Tidak ada manipulasi Backend.

Hanya menghitung statistik.
==========================================================
*/

/* ======================================================
DASHBOARD STATE
====================================================== */
let processingStart = 0;

/* ======================================================
INITIALIZE DASHBOARD
====================================================== */
function initializeDashboard() {
    updateDashboard();
}

/* ======================================================
UPDATE DASHBOARD
====================================================== */
function updateDashboard() {
    const text = getClinicalText();
    updateWordCount(text);
    updateCharacterCount(text);
    updateEstimatedPHI(text);
}

/* ======================================================
WORD COUNT
====================================================== */
function updateWordCount(text) {
    const totalWords = countWords(text);
    document.getElementById("word-count").innerHTML = totalWords;
}

/* ======================================================
CHARACTER COUNT
====================================================== */
function updateCharacterCount(text) {
    document.getElementById("character-count").innerHTML = text.length;
}

/* ======================================================
ESTIMATED PHI
====================================================== */
function updateEstimatedPHI(text) {
    let total = 0;
    total += countEmail(text);
    total += countPhone(text);
    total += countDate(text);
    document.getElementById("phi-count").innerHTML = total;
}

/* ======================================================
PROCESSING TIMER
====================================================== */
function startProcessingTimer() {
    processingStart = performance.now();
}

/* ======================================================
STOP TIMER
====================================================== */
function stopProcessingTimer() {
    const processingTime = performance.now() - processingStart;
    document.getElementById("processing-time").innerHTML =
        processingTime.toFixed(0) + " ms";
}

/* ======================================================
RESET DASHBOARD
====================================================== */
function resetDashboard() {
    document.getElementById("word-count").innerHTML = 0;
    document.getElementById("character-count").innerHTML = 0;
    document.getElementById("phi-count").innerHTML = 0;
    document.getElementById("processing-time").innerHTML = "0 ms";
}