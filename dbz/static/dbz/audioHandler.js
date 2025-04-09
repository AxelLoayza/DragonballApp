document.addEventListener("DOMContentLoaded", function () {
    let audio = document.createElement("audio");
    audio.id = "bgMusic";
    audio.loop = true;
    audio.src = "/static/aud/dbz.mp3";

    document.body.appendChild(audio);
    console.log("✅ Audio agregado al documento.");

    audio.addEventListener("canplay", function () {
        audio.volume = 0.2;  
        console.log("🎵 Volumen establecido en 0.2");
    });

  
    let isPlaying = sessionStorage.getItem("musicPlaying");
    console.log("Estado recuperado:", isPlaying);

    if (isPlaying === "true") {
        audio.play();
        console.log("🎵 Audio restaurado correctamente.");
    }


    window.addEventListener("beforeunload", function () {
        sessionStorage.setItem("musicPlaying", audio.paused ? "false" : "true");
        console.log("🔄 Estado de música guardado:", sessionStorage.getItem("musicPlaying"));
    });
});
