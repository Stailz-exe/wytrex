const tg = window.Telegram.WebApp;
tg.expand();

const checkBtn = document.getElementById("checkLink");
const videoInfo = document.getElementById("videoInfo");
const formatSection = document.getElementById("formatSection");
const optionsSection = document.getElementById("optionsSection");
const downloadSection = document.getElementById("downloadSection");
const downloadBtn = document.getElementById("downloadBtn");
const dailyLimitText = document.getElementById("dailyLimit");
const BACKEND_URL = "https://wytrex.onrender.com";


let videoData = null;  // объект с данными видео
let downloadsToday = 0;
const maxDownloads = 5;

// Обработчик проверки ссылки
checkBtn.addEventListener("click", async () => {
    const link = document.getElementById("videoLink").value.trim();
    if(!link) return alert("Введите ссылку!");

    // Здесь можно сделать fetch на backend для получения данных видео
    // Пока тестовый пример:
    videoData = {
        title: "Пример видео",
        date: "2026-03-01",
        views: 12345,
        likes: 678,
        comments: 90,
        formats: ["480", "720", "1080"]
    }

    // Показываем данные
    document.getElementById("title").innerText = videoData.title;
    document.getElementById("date").innerText = videoData.date;
    document.getElementById("views").innerText = videoData.views;
    document.getElementById("likes").innerText = videoData.likes;
    document.getElementById("comments").innerText = videoData.comments;

    videoInfo.classList.remove("hidden");

    // Форматы
    const formatsDiv = document.querySelector(".formats");
    formatsDiv.innerHTML = "";
    videoData.formats.forEach(f => {
        formatsDiv.innerHTML += `<label><input type="radio" name="format" value="${f}"> ${f}p</label>`;
    });

    formatSection.classList.remove("hidden");
    optionsSection.classList.remove("hidden");
    downloadSection.classList.remove("hidden");

    // Обновляем лимит
    dailyLimitText.innerText = `Вы можете скачать ${maxDownloads - downloadsToday} видео сегодня.`;
});

// Обработчик кнопки скачать
downloadBtn.addEventListener("click", () => {
    if(downloadsToday >= maxDownloads){
        return alert("Вы достигли лимита 5 видео в сутки. Приобретите Premium.");
    }

    const selectedFormat = document.querySelector('input[name="format"]:checked');
    if(!selectedFormat) return alert("Выберите формат!");

    const desc = document.getElementById("desc").checked;
    const music = document.getElementById("music").checked;

    downloadsToday++;

    alert(`Скачиваем видео: ${videoData.title}\nФормат: ${selectedFormat.value}p\nОписание: ${desc}\nМузыка: ${music ? 'Да (Premium)' : 'Нет'}`);

    dailyLimitText.innerText = `Вы можете скачать ${maxDownloads - downloadsToday} видео сегодня.`;
});