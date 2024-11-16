
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    
}

function scrollToBottom() {
    const conversation = document.querySelector(".conversation");
    conversation.scrollTop = conversation.scrollHeight;
}

function scrollToEntry(entryId) {
    const entryElement = document.getElementById(entryId);
    if (entryElement) {
        entryElement.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}

function clearHistory() {
    const conversation = document.querySelector(".conversation");
    conversation.innerHTML = '';
}

document.addEventListener("DOMContentLoaded", function () {
    scrollToBottom();
});

function startVoiceRecognition() {
    const popup = document.getElementById("listening-popup");
    popup.style.display = "block";

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function (event) {
        popup.style.display = "none";
        document.getElementById("question").value = event.results[0][0].transcript;
    };

    recognition.onerror = function () {
        popup.style.display = "none";
        alert("Voice recognition failed. Please try again.");
    };
}