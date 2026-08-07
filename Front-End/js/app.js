document.addEventListener("DOMContentLoaded", initializeApplication);

/* ======================================================
MAIN INITIALIZATION
====================================================== */
function initializeApplication() {
    testConnection()
    checkAPIHealth()
    console.log("Privacy Shield LLM Started");
    initializeTheme();
    initializeDashboard();
    initializeUI();
    initializeLogger();
    registerEvents();
    addLog("Application Started");
}

/* ======================================================
REGISTER ALL EVENT
====================================================== */
function registerEvents() {
    const redactButton = document.getElementById("redact-btn");
    const restoreButton = document.getElementById("restore-btn");
    const clearButton = document.getElementById("clear-btn");
    const uploadButton =document.getElementById("upload-btn");
    const copyButton = document.getElementById("copy-btn");
    const downloadButton = document.getElementById("download-btn");
    const clinicalNote = document.getElementById("clinical-note");
    const themeButton =document.getElementById("theme-toggle");
    
    /* ==========================
    Text Typing
    ========================== */

    clinicalNote.addEventListener(
        "input",
        handleTextInput
    );


    /* ==========================
    Redact
    ========================== */

    redactButton.addEventListener(
        "click",
        handleRedaction
    );

    /* ==========================
    Restore
    ========================== */
    restoreButton.addEventListener(
        "click",
        handleRestore
    );


    /* ==========================
    Clear
    ========================== */

    clearButton.addEventListener(
        "click",
        clearClinicalNote
    );


    /* ==========================
    Upload
    ========================== */

    uploadButton.addEventListener(
        "click",
        openFileDialog
    );


    /* ==========================
    Copy
    ========================== */

    copyButton.addEventListener(
        "click",
        copyResult
    );


    /* ==========================
    Download
    ========================== */

    downloadButton.addEventListener(
        "click",
        downloadResult
    );


    /* ==========================
    Theme
    ========================== */

    themeButton.addEventListener(
        "click",
        toggleTheme
    );

}


/* ======================================================
HANDLE USER INPUT
====================================================== */

function handleTextInput(){
    updateDashboard();
}


/* ======================================================
HANDLE REDACTION
====================================================== */

async function handleRedaction(){
    const text = getClinicalText();
    if(text.trim()===""){
        showToast(
            "Clinical Note cannot be empty",
            "error"
        );
        addLog("Empty Input");
        return;
    }

    showLoading();

    addLog("Sending Request to FastAPI");

    try{
        const response = await redactText(text);
        console.log(response);

        displayRedactedText(response),

        updateDashboard();

        addLog(
            "Redaction Success"
        );

        showToast(
            "Redaction Completed",
            "success"
        );

    }

    catch(error){
        console.error(error);
        addLog(
            "Connection Failed"
        );

        showToast(
            "FastAPI Connection Failed",
            "error"
        );
    }
    finally{
        hideLoading();
    }
}

/* ======================================================
HANDLE RESTORE
====================================================== */
async function handleRestore(){
    const text = getClinicalText();
    if(text.trim()===""){
        showToast(
            "Clinical Note cannot be empty",
            "error"
        );
        addLog("Empty Input");
        return;
    }

    showLoading();

    addLog("Sending Request to FastAPI");

    try{
        const response = await restoreText(text);
        console.log(response);

        displayRedactedText(response),

        updateDashboard();

        addLog(
            "Restore Success"
        );

        showToast(
            "Restore Completed",
            "success"
        );

    }

    catch(error){
        console.error(error);
        addLog(
            "Connection Failed"
        );

        showToast(
            "FastAPI Connection Failed",
            "error"
        );
    }
    finally{
        hideLoading();
    }
}