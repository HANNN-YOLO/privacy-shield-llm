/*
Privacy Shield LLM

Utility Module

Author : Reyhan Rafaidhil

Berisi helper function yang dapat digunakan
oleh seluruh module.

Tidak ada UI.
Tidak ada API.
Tidak ada HTML.
*/


/* ======================================================
WORD COUNTER
====================================================== */

function countWords(
    text
) {

    if (
        !text ||
        !text.trim()
    ) {

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

function countEmail(
    text
) {

    const regex =
        /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g;


    const result =
        text.match(
            regex
        );


    return result
        ? result.length
        : 0;

}


/* ======================================================
PHONE COUNTER
====================================================== */

function countPhone(
    text
) {

    const regex =
        /(?:\+62|62|0)[0-9]{8,13}/g;


    const result =
        text.match(
            regex
        );


    return result
        ? result.length
        : 0;

}


/* ======================================================
DATE COUNTER
====================================================== */

function countDate(
    text
) {

    const regex =
        /\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b/g;


    const result =
        text.match(
            regex
        );


    return result
        ? result.length
        : 0;

}


/* ======================================================
EMPTY VALIDATION
====================================================== */

function isEmpty(
    text
) {

    return (
        !text ||
        text.trim() === ""
    );

}


/* ======================================================
FORMAT PROCESSING TIME
====================================================== */

function formatMilliseconds(
    ms
) {

    return `${ms.toFixed(0)} ms`;

}


/* ======================================================
COPY TEXT
====================================================== */

async function copyToClipboard(
    text
) {

    if (
        !text ||
        text.trim() === ""
    ) {

        return false;

    }


    /* ==================================================
    METHOD 1
    MODERN CLIPBOARD API
    ================================================== */

    try {

        if (
            navigator.clipboard &&
            window.isSecureContext
        ) {

            await navigator.clipboard.writeText(
                text
            );


            return true;

        }

    }

    catch (error) {

        console.warn(
            "Clipboard API failed:",
            error
        );

    }


    /* ==================================================
    METHOD 2
    FALLBACK
    Untuk HTTP / LAN IP
    ================================================== */

    try {

        const textarea =
            document.createElement(
                "textarea"
            );


        textarea.value =
            text;


        textarea.style.position =
            "fixed";

        textarea.style.left =
            "-9999px";

        textarea.style.top =
            "-9999px";

        textarea.style.opacity =
            "0";


        document.body.appendChild(
            textarea
        );


        textarea.focus();

        textarea.select();


        textarea.setSelectionRange(
            0,
            textarea.value.length
        );


        const successful =
            document.execCommand(
                "copy"
            );


        document.body.removeChild(
            textarea
        );


        return successful;

    }

    catch (error) {

        console.error(
            "Fallback copy failed:",
            error
        );


        return false;

    }

}


/* ======================================================
DOWNLOAD TEXT FILE
====================================================== */

function downloadTextFile(
    filename,
    content
) {

    const blob =
        new Blob(
            [
                content
            ],
            {
                type:
                    "text/plain;charset=utf-8"
            }
        );


    const url =
        URL.createObjectURL(
            blob
        );


    const link =
        document.createElement(
            "a"
        );


    link.href =
        url;


    link.download =
        filename;


    document.body.appendChild(
        link
    );


    link.click();


    document.body.removeChild(
        link
    );


    setTimeout(
        () => {

            URL.revokeObjectURL(
                url
            );

        },
        100
    );

}


/* ======================================================
GET FILE EXTENSION
====================================================== */

function getFileExtension(
    filename
) {

    if (
        !filename ||
        !filename.includes(".")
    ) {

        return "";

    }


    return filename
        .split(".")
        .pop()
        .toLowerCase();

}


/* ======================================================
FORMAT FILE SIZE
====================================================== */

function formatFileSize(
    bytes
) {

    if (
        bytes === 0
    ) {

        return "0 Bytes";

    }


    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];


    const index =
        Math.floor(
            Math.log(bytes) /
            Math.log(1024)
        );


    return (
        parseFloat(
            (
                bytes /
                Math.pow(
                    1024,
                    index
                )
            ).toFixed(2)
        ) +
        " " +
        units[index]
    );

}


/* ======================================================
FORMAT CURRENT TIME
====================================================== */

function getFormattedTime() {

    return new Date()
        .toLocaleTimeString();

}


/* ======================================================
RANDOM ID
====================================================== */

function generateID() {

    return Math
        .random()
        .toString(36)
        .substring(
            2,
            10
        );

}