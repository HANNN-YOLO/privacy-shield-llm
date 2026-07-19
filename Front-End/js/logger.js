/*
==========================================================
Privacy Shield LLM

Logger Module

Author : Reyhan Rafaidhil

Logger digunakan untuk mencatat seluruh aktivitas
yang dilakukan user selama aplikasi berjalan.

Tidak ada komunikasi API.

Tidak ada manipulasi Backend.

Hanya mencatat aktivitas.
==========================================================
*/

/* ======================================================
LOGGER STATE
====================================================== */
let activityLogs = [];

/* ======================================================
INITIALIZE LOGGER
====================================================== */
function initializeLogger() {
    activityLogs = [];
    clearLogView();
    addLog("Logger Initialized");
}

/* ======================================================
GET CURRENT TIME
====================================================== */
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString();
}

/* ======================================================
ADD LOG
====================================================== */
function addLog(message) {
    const timestamp = getCurrentTime();
    const log = `[${timestamp}] ${message}`;
    activityLogs.push(log);
    renderLog(log);
}

/* ======================================================
RENDER LOG
====================================================== */
function renderLog(logMessage) {
    const container = document.getElementById("activity-log");
    if (!container) return;
    const item = document.createElement("div");
    item.className = "log-item";
    item.innerHTML = logMessage;
    container.appendChild(item);
    autoScroll();
}

/* ======================================================
AUTO SCROLL
====================================================== */
function autoScroll() {
    const container = document.getElementById("activity-log");
    if (!container) return;
    container.scrollTop = container.scrollHeight;
}

/* ======================================================
CLEAR LOGGER
====================================================== */
function clearLogger() {
    activityLogs = [];
    clearLogView();
    addLog("Logger Cleared");
}

/* ======================================================
CLEAR HTML
====================================================== */
function clearLogView() {
    const container = document.getElementById("activity-log");
    if (!container) return;
    container.innerHTML = "";
}

/* ======================================================
EXPORT LOG
====================================================== */
function exportLogs() {
    const blob = new Blob(
        [activityLogs.join("\n")],
        {
            type:"text/plain"
        }
    );
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "activity-log.txt";
    link.click();
    URL.revokeObjectURL(url);
    showToast("Log Exported");
}

/* ======================================================
GET TOTAL LOG
====================================================== */
function getTotalLogs() {
    return activityLogs.length;
}