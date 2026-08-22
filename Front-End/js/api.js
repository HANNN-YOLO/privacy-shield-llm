/* ======================================================
API CONFIGURATION
====================================================== */

// localhost
// const API_BASE_URL = "http://127.0.0.1:8000";

// IPv4
const API_BASE_URL = "http://10.182.106.226:8000";

/* ======================================================
HEALTH CHECK
====================================================== */

async function checkAPIHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    if (!response.ok) {
      throw new Error("Server Error");
    }
    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
}

/* ======================================================
REDACT TEXT
====================================================== */
async function redactText(text) {
  try {
    const response = await fetch(`${API_BASE_URL}/redact`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: text,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP Error : ${response.status}`);
    }
    const json = await response.json();
    return json;
  } catch (error) {
    console.error("API Error", error);
    throw error;
  }
}

/* ======================================================
RESTORE TEXT
====================================================== */
async function restoreText(text) {
  try {
    const response = await fetch(`${API_BASE_URL}/restore`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: text,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP Error : ${response.status}`);
    }
    const json = await response.json();
    return json;
  } catch (error) {
    console.error("API Error", error);
    throw error;
  }
}

/* ======================================================
TEST CONNECTION
====================================================== */
async function testConnection() {
  const online = await checkAPIHealth();
  updateAPIStatus(online);
}
