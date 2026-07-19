/*
==========================================================
Privacy Shield LLM

Utility Module

Author : Reyhan Rafaidhil

Berisi helper function yang dapat digunakan
oleh seluruh module.

Tidak ada UI.

Tidak ada API.

Tidak ada HTML.
==========================================================
*/

/* ======================================================
WORD COUNTER
====================================================== */
function countWords(text) {
    if (!text.trim()) {
        return 0;
    }
    return text
        .trim()
        .split(/\s+/)
        .length;
}

/* ======================================================
EMAIL COUNTER
====================================================== */
function countEmail(text) {
    const regex =
        /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g;
    const result = text.match(regex);
    return result ? result.length : 0;
}

/* ======================================================
PHONE COUNTER
====================================================== */
function countPhone(text) {
    const regex =
        /(\+62|62|0)[0-9]{8,13}/g;
    const result = text.match(regex);
    return result ? result.length : 0;
}

/* ======================================================
DATE COUNTER
====================================================== */
function countDate(text) {
    const regex =
        /\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b/g;
    const result = text.match(regex);
    return result ? result.length : 0;
}

/* ======================================================
EMPTY VALIDATION
====================================================== */
function isEmpty(text) {
    return text.trim() === "";
}

/* ======================================================
FORMAT PROCESSING TIME
====================================================== */
function formatMilliseconds(ms) {
    return `${ms.toFixed(0)} ms`;
}

/* ======================================================
COPY TEXT
====================================================== */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    }
    catch {
        return false;
    }
}

/* ======================================================
DOWNLOAD TEXT FILE
====================================================== */
function downloadTextFile(filename, content) {
    const blob =
        new Blob(
            [content],
            {
                type:"text/plain"
            }
        );
    const url =
        URL.createObjectURL(blob);
    const link =
        document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}

/* ======================================================
FORMAT CURRENT TIME
====================================================== */
function getFormattedTime() {
    return new Date().toLocaleTimeString();
}

/* ======================================================
RANDOM ID
====================================================== */
function generateID() {
    return Math
        .random()
        .toString(36)
        .substring(2,10);
}