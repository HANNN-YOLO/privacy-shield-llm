/* ======================================================
INITIALIZE UI
====================================================== */

function initializeUI() {

    console.log(
        "Initialize UI"
    );

    hideLoading();

}


/* ======================================================
FAST API STATUS
====================================================== */

function updateAPIStatus(
    online
) {

    const badge =
        document.getElementById(
            "api-status"
        );


    if (!badge) {
        return;
    }


    if (online) {

        badge.innerHTML =
            "🟢 Fast API Online";

    }

    else {

        badge.innerHTML =
            "🔴 Fast API Offline";

    }

}


/* ======================================================
GET CLINICAL NOTE
====================================================== */

function getClinicalText() {

    const input =
        document.getElementById(
            "clinical-note"
        );


    if (!input) {
        return "";
    }


    return input.value;

}


/* ======================================================
DISPLAY REDACTED RESULT
====================================================== */

function displayRedactedText(
    response
) {

    const resultBox =
        document.getElementById(
            "redacted-result"
        );


    if (!resultBox) {
        return;
    }


    resultBox.value =
        response.redacted_text || "";

}


/* ======================================================
DISPLAY RESTORED RESULT
====================================================== */

function displayRestoredText(
    response
) {

    const resultBox =
        document.getElementById(
            "redacted-result"
        );


    if (!resultBox) {
        return;
    }


    resultBox.value =
        response.restored_text || "";

}


/* ======================================================
DISPLAY ENTITY
====================================================== */

function displayEntities(
    response
) {

    if (
        !response ||
        !response.entities
    ) {

        return;

    }


    const entities =
        response.entities;


    const entityMap = {

        name:
            "entity-name",

        email:
            "entity-email",

        phone:
            "entity-phone",

        address:
            "entity-address",

        date:
            "entity-date"

    };


    Object.keys(
        entityMap
    ).forEach(
        key => {

            const element =
                document.getElementById(
                    entityMap[key]
                );


            if (!element) {
                return;
            }


            const value =
                entities[key];


            if (
                Array.isArray(value)
            ) {

                element.innerHTML =
                    value.join(", ");

            }

            else {

                element.innerHTML =
                    value || "";

            }

        }
    );

}


/* ======================================================
CLEAR INPUT
====================================================== */

function clearClinicalNote() {

    const clinicalNote =
        document.getElementById(
            "clinical-note"
        );

    const resultBox =
        document.getElementById(
            "redacted-result"
        );


    if (clinicalNote) {

        clinicalNote.value = "";

    }


    if (resultBox) {

        resultBox.value = "";

    }


    updateDashboard();


    addLog(
        "Clinical Note Cleared"
    );


    showToast(
        "Clinical Note Cleared",
        "success"
    );

}


/* ======================================================
LOADING
====================================================== */

function showLoading(
    title = "Processing...",
    message = "Please wait..."
) {

    const overlay =
        document.getElementById(
            "loading-overlay"
        );


    const titleElement =
        document.getElementById(
            "loading-title"
        );


    const messageElement =
        document.getElementById(
            "loading-message"
        );


    if (!overlay) {
        return;
    }


    if (titleElement) {

        titleElement.textContent =
            title;

    }


    if (messageElement) {

        messageElement.textContent =
            message;

    }


    overlay.style.display =
        "flex";

}


function hideLoading() {

    const overlay =
        document.getElementById(
            "loading-overlay"
        );


    if (!overlay) {
        return;
    }


    overlay.style.display =
        "none";

}


/* ======================================================
TOAST
====================================================== */

function showToast(
    message,
    type = "success"
) {

    const toast =
        document.getElementById(
            "toast"
        );


    if (!toast) {
        return;
    }


    toast.innerHTML =
        message;


    toast.className =
        "toast";


    toast.classList.add(
        type
    );


    toast.style.display =
        "block";


    setTimeout(
        () => {

            toast.style.display =
                "none";

        },
        3000
    );

}


/* ======================================================
COPY RESULT
====================================================== */

async function copyResult() {

    const resultBox =
        document.getElementById(
            "redacted-result"
        );


    if (!resultBox) {
        return;
    }


    const text =
        resultBox.value;


    if (
        !text ||
        text.trim() === ""
    ) {

        showToast(
            "Nothing to copy",
            "error"
        );

        addLog(
            "Copy Failed: Empty Result"
        );

        return;

    }


    const success =
        await copyToClipboard(
            text
        );


    if (success) {

        showToast(
            "Copied to Clipboard",
            "success"
        );


        addLog(
            "Copy Result"
        );

    }

    else {

        showToast(
            "Copy Failed",
            "error"
        );


        addLog(
            "Copy Failed"
        );

    }

}


/* ======================================================
DOWNLOAD RESULT
====================================================== */

function downloadResult() {

    const resultBox =
        document.getElementById(
            "redacted-result"
        );


    if (!resultBox) {
        return;
    }


    const result =
        resultBox.value;


    if (
        !result ||
        result.trim() === ""
    ) {

        showToast(
            "Nothing to download",
            "error"
        );

        return;

    }


    downloadTextFile(
        "redacted_result.txt",
        result
    );


    showToast(
        "Downloaded",
        "success"
    );


    addLog(
        "Download Result"
    );

}


/* ======================================================
FILE DIALOG
====================================================== */

function openFileDialog() {

    const fileInput =
        document.getElementById(
            "file-input"
        );


    if (!fileInput) {

        console.error(
            "file-input not found"
        );

        return;

    }


    fileInput.value = "";


    fileInput.click();

}


/* ======================================================
FILE UPLOAD
====================================================== */

async function handleFileUpload(
    event
) {

    const file =
        event.target.files[0];


    if (!file) {
        return;
    }


    const allowedExtensions = [
        "txt",
        "md",
        "pdf",
        "docx"
    ];


    const extension =
        getFileExtension(
            file.name
        );


    if (
        !allowedExtensions.includes(
            extension
        )
    ) {

        showToast(
            "Unsupported file type",
            "error"
        );


        addLog(
            `Upload Rejected: .${extension}`
        );


        return;

    }


    try {

        showLoading(
            "Reading File",
            `Extracting text from ${file.name}...`
        );


        addLog(
            `Reading File: ${file.name}`
        );


        let text = "";


        /* ==============================================
        TXT
        ============================================== */

        if (
            extension === "txt"
        ) {

            text =
                await readTextFile(
                    file
                );

        }


        /* ==============================================
        MARKDOWN
        ============================================== */

        else if (
            extension === "md"
        ) {

            text =
                await readTextFile(
                    file
                );

        }


        /* ==============================================
        PDF
        ============================================== */

        else if (
            extension === "pdf"
        ) {

            text =
                await readPDFFile(
                    file
                );

        }


        /* ==============================================
        DOCX
        ============================================== */

        else if (
            extension === "docx"
        ) {

            text =
                await readDOCXFile(
                    file
                );

        }


        if (
            !text ||
            text.trim() === ""
        ) {

            throw new Error(
                "No readable text found in file"
            );

        }


        /* ==============================================
        PUT TEXT INTO CLINICAL NOTE
        ============================================== */

        const clinicalNote =
            document.getElementById(
                "clinical-note"
            );


        if (!clinicalNote) {

            throw new Error(
                "Clinical Note textarea not found"
            );

        }


        clinicalNote.value =
            text;


        /* ==============================================
        UPDATE UI
        ============================================== */

        updateDashboard();


        addLog(
            `File Loaded: ${file.name}`
        );


        showToast(
            `${file.name} loaded successfully`,
            "success"
        );

    }

    catch (error) {

        console.error(
            "File processing error:",
            error
        );


        addLog(
            `File Processing Failed: ${file.name}`
        );


        showToast(
            `Failed to read ${file.name}`,
            "error"
        );

    }

    finally {

        hideLoading();

    }

}


/* ======================================================
READ TXT / MD
====================================================== */

function readTextFile(
    file
) {

    return new Promise(
        (
            resolve,
            reject
        ) => {

            const reader =
                new FileReader();


            reader.onload =
                event => {

                    resolve(
                        event.target.result
                    );

                };


            reader.onerror =
                () => {

                    reject(
                        new Error(
                            "Unable to read text file"
                        )
                    );

                };


            reader.readAsText(
                file
            );

        }
    );

}


/* ======================================================
READ PDF
====================================================== */

async function readPDFFile(
    file
) {

    if (
        typeof pdfjsLib ===
        "undefined"
    ) {

        throw new Error(
            "PDF.js library is not loaded"
        );

    }


    const arrayBuffer =
        await file.arrayBuffer();


    const pdf =
        await pdfjsLib.getDocument(
            {
                data:
                    arrayBuffer
            }
        ).promise;


    let fullText = "";


    for (
        let pageNumber = 1;
        pageNumber <= pdf.numPages;
        pageNumber++
    ) {

        const page =
            await pdf.getPage(
                pageNumber
            );


        const content =
            await page.getTextContent();


        const pageText =
            content.items
                .map(
                    item =>
                        item.str
                )
                .join(" ");


        fullText +=
            pageText +
            "\n\n";


        updateLoadingMessage(
            `Reading PDF page ${pageNumber} of ${pdf.numPages}...`
        );

    }


    return fullText.trim();

}


/* ======================================================
READ DOCX
====================================================== */

async function readDOCXFile(
    file
) {

    if (
        typeof mammoth ===
        "undefined"
    ) {

        throw new Error(
            "Mammoth.js library is not loaded"
        );

    }


    const arrayBuffer =
        await file.arrayBuffer();


    updateLoadingMessage(
        "Extracting DOCX content..."
    );


    const result =
        await mammoth.extractRawText(
            {
                arrayBuffer:
                    arrayBuffer
            }
        );


    return (
        result.value || ""
    ).trim();

}


/* ======================================================
UPDATE LOADING MESSAGE
====================================================== */

function updateLoadingMessage(
    message
) {

    const element =
        document.getElementById(
            "loading-message"
        );


    if (element) {

        element.textContent =
            message;

    }

}