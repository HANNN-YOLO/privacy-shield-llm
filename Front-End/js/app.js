document.addEventListener(
    "DOMContentLoaded",
    initializeApplication
);


/* ======================================================
MAIN INITIALIZATION
====================================================== */

function initializeApplication() {

    console.log(
        "Privacy Shield LLM Started"
    );

    testConnection();

    initializeTheme();

    initializeDashboard();

    initializeUI();

    initializeLogger();

    registerEvents();

    addLog(
        "Application Started"
    );
}


/* ======================================================
REGISTER ALL EVENTS
====================================================== */

function registerEvents() {

    const redactButton =
        document.getElementById(
            "redact-btn"
        );

    const restoreButton =
        document.getElementById(
            "restore-btn"
        );

    const clearButton =
        document.getElementById(
            "clear-btn"
        );

    const uploadButton =
        document.getElementById(
            "upload-btn"
        );

    const copyButton =
        document.getElementById(
            "copy-btn"
        );

    const downloadButton =
        document.getElementById(
            "download-btn"
        );

    const clinicalNote =
        document.getElementById(
            "clinical-note"
        );

    const fileInput =
        document.getElementById(
            "file-input"
        );

    const themeButton =
        document.getElementById(
            "theme-toggle"
        );


    /* ==================================================
    TEXT TYPING
    ================================================== */

    if (clinicalNote) {

        clinicalNote.addEventListener(
            "input",
            handleTextInput
        );

    }


    /* ==================================================
    REDACT
    ================================================== */

    if (redactButton) {

        redactButton.addEventListener(
            "click",
            handleRedaction
        );

    }


    /* ==================================================
    RESTORE
    ================================================== */

    if (restoreButton) {

        restoreButton.addEventListener(
            "click",
            handleRestore
        );

    }


    /* ==================================================
    CLEAR
    ================================================== */

    if (clearButton) {

        clearButton.addEventListener(
            "click",
            clearClinicalNote
        );

    }


    /* ==================================================
    UPLOAD BUTTON
    ================================================== */

    if (uploadButton) {

        uploadButton.addEventListener(
            "click",
            openFileDialog
        );

    }


    /* ==================================================
    FILE INPUT
    ================================================== */

    if (fileInput) {

        fileInput.addEventListener(
            "change",
            handleFileUpload
        );

    }


    /* ==================================================
    COPY
    ================================================== */

    if (copyButton) {

        copyButton.addEventListener(
            "click",
            copyResult
        );

    }


    /* ==================================================
    DOWNLOAD
    ================================================== */

    if (downloadButton) {

        downloadButton.addEventListener(
            "click",
            downloadResult
        );

    }


    /* ==================================================
    THEME
    ================================================== */

    if (themeButton) {

        themeButton.addEventListener(
            "click",
            toggleTheme
        );

    }

}


/* ======================================================
HANDLE USER INPUT
====================================================== */

function handleTextInput() {

    updateDashboard();

}


/* ======================================================
HANDLE REDACTION
====================================================== */

async function handleRedaction() {

    const text =
        getClinicalText();


    if (text.trim() === "") {

        showToast(
            "Clinical Note cannot be empty",
            "error"
        );

        addLog(
            "Empty Input"
        );

        return;

    }


    showLoading(
        "Redacting Text",
        "Detecting PHI / PII..."
    );


    addLog(
        "Sending Request to FastAPI"
    );


    try {

        const response =
            await redactText(text);


        console.log(
            response
        );


        displayRedactedText(
            response
        );


        updateDashboard();


        updateEntityMetrics(
            response
        );


        addLog(
            "Redaction Success"
        );


        showToast(
            "Redaction Completed",
            "success"
        );

    }

    catch (error) {

        console.error(
            error
        );


        addLog(
            "Connection Failed"
        );


        showToast(
            "FastAPI Connection Failed",
            "error"
        );

    }

    finally {

        hideLoading();

    }

}


/* ======================================================
HANDLE RESTORE
====================================================== */

async function handleRestore() {

    const text =
        getClinicalText();


    if (text.trim() === "") {

        showToast(
            "Clinical Note cannot be empty",
            "error"
        );

        addLog(
            "Empty Input"
        );

        return;

    }


    showLoading(
        "Restoring Text",
        "Restoring original data..."
    );


    addLog(
        "Sending Restore Request to FastAPI"
    );


    try {

        const response =
            await restoreText(text);


        console.log(
            response
        );


        displayRestoredText(
            response
        );


        updateDashboard();


        updateEntityMetrics(
            response
        );


        addLog(
            "Restore Success"
        );


        showToast(
            "Restore Completed",
            "success"
        );

    }

    catch (error) {

        console.error(
            error
        );


        addLog(
            "Restore Failed"
        );


        showToast(
            "Restore Failed",
            "error"
        );

    }

    finally {

        hideLoading();

    }

}