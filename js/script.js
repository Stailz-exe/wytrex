const tg = window.Telegram.WebApp;
tg.expand();

if (tg.colorScheme === "dark") {
    document.body.classList.add("dark");
}

function toggleTheme() {
    document.body.classList.toggle("dark");
}

function openBot(type) {
    window.location.href = `loader.html?bot=${type}`;
}

const translations = {
    ru: { title: "Выберите бота" },
    en: { title: "Choose a bot" },
    de: { title: "Bot auswählen" }
};

function setLang(lang) {
    localStorage.setItem("lang", lang);
    document.getElementById("title").innerText = translations[lang].title;
}

const savedLang = localStorage.getItem("lang") || "ru";
setLang(savedLang);