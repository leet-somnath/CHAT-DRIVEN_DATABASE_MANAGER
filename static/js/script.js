
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    
}
document.addEventListener("DOMContentLoaded", function() {
    const conversation = document.querySelector(".conversation");
    const scrollDownBtn = document.getElementById("scroll-down-btn");

    conversation.addEventListener("scroll", function() {
        if (conversation.scrollTop < conversation.scrollHeight - conversation.offsetHeight - 50) {
            scrollDownBtn.style.display = "block";
        } else {
            scrollDownBtn.style.display = "none";
        }
    });

    // Ensure smooth scrolling when button is clicked
    function scrollToBottom() {
        conversation.scrollTo({
            top: conversation.scrollHeight,
            behavior: "smooth"
        });
    }

    // Attach the function globally for use in HTML
    window.scrollToBottom = scrollToBottom;
});
function deleteChat(entryId) {
    // Remove user message
    const userMessage = document.getElementById(entryId);
    if (userMessage) {
        userMessage.remove();
    }

    // Remove chatbot response (assume it immediately follows the user message)
    const botResponse = document.getElementById(`bot-response-${entryId}`);
    if (botResponse) {
        botResponse.remove();
    }

    // Remove from the sidebar
    const historyItem = document.getElementById(`history-item-${entryId}`);
    if (historyItem) {
        historyItem.remove();
    }

    // Optionally, make an AJAX request to the server to delete the entry permanently
    fetch(`/delete_chat/${entryId}`, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                console.log("Chat entry deleted successfully on the server.");
            } else {
                console.error("Failed to delete the chat entry on the server.");
            }
        })
        .catch(error => {
            console.error("Error deleting chat entry:", error);
        });
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