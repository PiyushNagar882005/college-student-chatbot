const username =
    localStorage.getItem(
        "username"
    );


if (!username) {

    window.location.href =
        "login.html";
}



/* ========================= */
/* SEND MESSAGE */
/* ========================= */

async function sendMessage() {

    const input =
        document.getElementById(
            "message"
        );

    const message =
        input.value.trim();

    if (!message) return;


    addMessage(
        message,
        "user"
    );

    input.value = "";


    try {

        const response =
            await fetch(
                "http://127.0.0.1:5000/chat",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({
                        username,
                        message
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `HTTP error! status: ${response.status}`
            );
        }


        const data =
            await response.json();

        console.log(data);


        if (data.response) {

            addMessage(
                data.response,
                "bot"
            );

        } else if (data.error) {

            addMessage(
                `Error: ${data.error}`,
                "bot"
            );
        }

    } catch(error) {

        console.log(error);

        addMessage(
            "Error generating response. Please try again.",
            "bot"
        );
    }
}



/* ========================= */
/* NEW CHAT */
/* ========================= */

function newChat() {

    const chatBox =
        document.getElementById(
            "chat-box"
        );

    const input =
        document.getElementById(
            "message"
        );

    chatBox.innerHTML = "";

    input.value = "";

    input.focus();
}



/* ========================= */
/* ADD MESSAGE */
/* ========================= */

function addMessage(text, sender) {

    const chatBox =
        document.getElementById(
            "chat-box"
        );

    // Remove welcome message on first message
    const welcome =
        chatBox.querySelector(
            ".welcome"
        );

    if (welcome) {

        welcome.remove();
    }

    const div =
        document.createElement(
            "div"
        );

    div.classList.add(
        "message",
        sender
    );

    div.innerText = text;

    chatBox.appendChild(div);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}



/* ========================= */
/* LOAD HISTORY */
/* ========================= */

async function loadHistory() {

    try {

        const response =
            await fetch(
                `http://127.0.0.1:5000/history/${username}`
            );

        const chats =
            await response.json();

        console.log(chats);


        const historyDiv =
            document.getElementById(
                "history"
            );

        historyDiv.innerHTML = "";


        chats.reverse().forEach(chat => {

            const container =
                document.createElement(
                    "div"
                );

            container.style.display =
                "flex";

            container.style.justifyContent =
                "space-between";

            container.style.alignItems =
                "center";

            container.style.gap =
                "10px";

            container.style.marginBottom =
                "5px";


            const p =
                document.createElement(
                    "p"
                );

            p.innerText =
                chat.user_message.length > 20
                ? chat.user_message.substring(0, 20) + "..."
                : chat.user_message;

            p.classList.add(
                "history-item"
            );

            p.style.flex = "1";

            p.onclick = () => {

                openChat(chat);
            };


            const deleteBtn =
                document.createElement(
                    "button"
                );

            deleteBtn.innerText = "✕";

            deleteBtn.style.background =
                "none";

            deleteBtn.style.border =
                "none";

            deleteBtn.style.color =
                "#ff4444";

            deleteBtn.style.cursor =
                "pointer";

            deleteBtn.style.fontSize =
                "16px";

            deleteBtn.style.padding =
                "2px 5px";

            deleteBtn.onclick = (e) => {

                e.stopPropagation();

                deleteChat(chat.id);
            };


            container.appendChild(p);

            container.appendChild(deleteBtn);

            historyDiv.appendChild(
                container
            );
        });

    } catch(error) {

        console.log(error);
    }
}



/* ========================= */
/* OPEN CHAT */
/* ========================= */

function openChat(chat) {

    const chatBox =
        document.getElementById(
            "chat-box"
        );

    chatBox.innerHTML = "";


    addMessage(
        chat.user_message,
        "user"
    );


    addMessage(
        chat.bot_response,
        "bot"
    );
}



/* ========================= */
/* DELETE CHAT */
/* ========================= */

async function deleteChat(chatId) {

    try {

        console.log(
            `Deleting chat with ID: ${chatId}`
        );

        const response =
            await fetch(
                `http://127.0.0.1:5000/delete-chat/${chatId}`,
                {

                    method: "DELETE"
                }
            );


        if (!response.ok) {

            throw new Error(
                `HTTP error! status: ${response.status}`
            );
        }


        const data =
            await response.json();

        console.log(data);

        alert("Chat deleted successfully");

        loadHistory();

    } catch(error) {

        console.error(error);

        alert(
            `Failed to delete chat: ${error.message}`
        );
    }
}



/* ========================= */
/* PDF UPLOAD */
/* ========================= */

async function uploadPDF() {

    const file =
        document.getElementById(
            "pdfFile"
        ).files[0];

    if (!file) {

        alert("Select PDF");

        return;
    }


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    try {

        const response =
            await fetch(
                "http://127.0.0.1:5000/upload-pdf",
                {

                    method: "POST",

                    body: formData
                }
            );


        const data =
            await response.json();

        console.log(data);

        alert(data.message);

    } catch(error) {

        console.log(error);

        alert("Upload failed");
    }
}



/* ========================= */
/* LOGOUT */
/* ========================= */

function logout() {

    localStorage.removeItem(
        "username"
    );

    window.location.href =
        "login.html";
}



/* ========================= */
/* PAGE LOAD */
/* ========================= */

window.onload = () => {

    loadHistory();

    // Add Enter key listener
    const input = document.getElementById(
        "message"
    );

    input.addEventListener(
        "keypress",
        (e) => {

            if (e.key === "Enter") {

                e.preventDefault();

                sendMessage();
            }
        }
    );
};

window.sendMessage = sendMessage;
window.newChat = newChat;
window.uploadPDF = uploadPDF;
window.logout = logout;