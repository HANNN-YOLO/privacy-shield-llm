/*
==========================================================
Privacy Shield LLM

Theme Manager

Author : Reyhan Rafaidhil

Mengatur seluruh tema aplikasi.

Tidak ada komunikasi API.

Tidak ada manipulasi data.

Hanya mengatur tema UI.
==========================================================
*/

/* ======================================================
STORAGE KEY
====================================================== */
const THEME_KEY = "privacy-shield-theme";

/* ======================================================
INITIALIZE THEME
====================================================== */
function initializeTheme() {
    const savedTheme = localStorage.getItem(THEME_KEY);
    if (savedTheme === "dark") {
        applyDarkTheme();
    }
    else {
        applyLightTheme();
    }
}

/* ======================================================
TOGGLE THEME
====================================================== */
function toggleTheme() {
    const isDark = document.body.classList.contains("dark");
    if (isDark) {
        applyLightTheme();
    }
    else {
        applyDarkTheme();
    }
}

/* ======================================================
APPLY DARK THEME
====================================================== */
function applyDarkTheme() {
    document.body.classList.add("dark");
    localStorage.setItem(
        THEME_KEY,
        "dark"
    );
    updateThemeIcon();
    console.log("Dark Theme");
}

/* ======================================================
APPLY LIGHT THEME
====================================================== */
function applyLightTheme() {
    document.body.classList.remove("dark");
    localStorage.setItem(
        THEME_KEY,
        "light"
    );
    updateThemeIcon();
    console.log("Light Theme");
}

/* ======================================================
UPDATE BUTTON ICON
====================================================== */
function updateThemeIcon() {
    const button = document.getElementById(
        "theme-toggle"
    );
    if (!button) return;
    if (
        document.body.classList.contains("dark")
    ) {
        button.innerHTML = "☀️";
    }
    else {
        button.innerHTML = "🌙";
    }
}

/* ======================================================
GET CURRENT THEME
====================================================== */
function getCurrentTheme() {
    if (
        document.body.classList.contains("dark")
    ) {
        return "dark";
    }
    return "light";
}