const BACKEND_URL = "https://YOUR_RENDER_URL"; // замените на URL Render

const checkBtn = document.getElementById("checkBtn");
const downloadBtn = document.getElementById("downloadBtn");
const videoInfoDiv = document.getElementById("videoInfo");
const formatsDiv = document.getElementById("formats");
const premiumOptionsDiv = document.getElementById("premiumOptions");
const buyPremiumBtn = document.getElementById("buyPremiumBtn");

checkBtn.addEventListener("click", async () => {
    const link = document.getElementById("videoLink").value.trim();
    if(!link) return alert("Вставьте ссылку!");
    const userId = Telegram.WebApp.initDataUnsafe.user.id;

    try {
        const res = await fetch(`${BACKEND_URL}/video_info`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({user_id: userId, url: link})
        });
        const data = await res.json();

        if(data.error){ alert(data.error); return; }

        videoInfoDiv.classList.remove("hidden");
        formatsDiv.classList.remove("hidden");
        premiumOptionsDiv.classList.remove("hidden");
        downloadBtn.classList.remove("hidden");

        document.getElementById("title").innerText = `Название видео: ${data.title}`;
        document.getElementById("views").innerText = `Просмотры: ${data.views}`;
        document.getElementById("likes").innerText = `Лайки: ${data.likes}`;
        document.getElementById("comments").innerText = `Комментарии: ${data.comments}`;
        document.getElementById("date").innerText = `Дата: ${data.date}`;

        if(data.limit_reached){
            downloadBtn.classList.add("hidden");
            buyPremiumBtn.classList.remove("hidden");
        } else {
            buyPremiumBtn.classList.add("hidden");
        }

    } catch(e){ alert("Ошибка сервера: " + e); }
});

downloadBtn.addEventListener("click", async () => {
    const link = document.getElementById("videoLink").value.trim();
    const selectedFormat = document.querySelector('input[name="format"]:checked').value;
    const extractDescription = document.getElementById("extractDescription").checked;
    const extractMusic = document.getElementById("extractMusic").checked;
    const userId = Telegram.WebApp.initDataUnsafe.user.id;

    try {
        const res = await fetch(`${BACKEND_URL}/download`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                user_id: userId,
                url: link,
                format: selectedFormat,
                extract_description: extractDescription,
                extract_music: extractMusic
            })
        });
        const data = await res.json();

        if(data.status === "OK"){
            alert("✅ Видео отправлено в Telegram!");
            Telegram.WebApp.close();
        } else if(data.error === "LIMIT_REACHED"){
            alert("Лимит 5 видео достигнут. Купите Premium!");
            downloadBtn.classList.add("hidden");
            buyPremiumBtn.classList.remove("hidden");
        } else {
            alert("Ошибка: " + data.error);
        }

    } catch(e){ alert("Ошибка сервера: " + e); }
});

buyPremiumBtn.addEventListener("click", () => {
    Telegram.WebApp.sendData("/buy_premium");
});