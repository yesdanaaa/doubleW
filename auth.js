const API_BASE = "https://doublew.onrender.com";

/* ============================
   Получение токенов
============================ */
function getAccessToken() {
    return localStorage.getItem("access_token");
}

function getRefreshToken() {
    return localStorage.getItem("refresh_token");
}

/* ============================
   Выход
============================ */
function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

/* ============================
   Обновление Access Token
============================ */
async function refreshAccessToken() {
    const refreshToken = getRefreshToken();

    if (!refreshToken) {
        logout();
        return false;
    }

    try {
        const response = await fetch(`${API_BASE}/refresh`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${refreshToken}`
            }
        });

        if (!response.ok) {
            logout();
            return false;
        }

        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        return true;

    } catch (error) {
        console.error(error);
        logout();
        return false;
    }
}

/* ============================
   Универсальный fetch
============================ */
async function apiFetch(url, options = {}) {
    let accessToken = getAccessToken();

    options.headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${accessToken}`
    };

    let response = await fetch(
        `${API_BASE}${url}`,
        options
    );

    if (response.status !== 401) {
        return response;
    }

    const refreshed = await refreshAccessToken();

    // ВОТ ТУТ ИЗМЕНЕНИЕ: если обновить токен не удалось, 
    // мы просто сразу возвращаем битый ответ и не шлем повторный запрос
    if (!refreshed) {
        return response;
    }

    accessToken = getAccessToken();
    options.headers.Authorization = `Bearer ${accessToken}`;

    response = await fetch(
        `${API_BASE}${url}`,
        options
    );

    return response;
}