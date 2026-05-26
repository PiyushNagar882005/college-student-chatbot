async function sendMessage() {

    const input = document.getElementById("user-input");

    const chatBox = document.getElementById("chat-box");

    const userMessage = input.value;

    if(userMessage.trim() === ""){
        return;
    }

    // User Message

    chatBox.innerHTML += `
        <div class="message user">
            ${userMessage}
        </div>
    `;

    input.value = "";

    // Loading

    chatBox.innerHTML += `
        <div class="message bot" id="loading">
            Thinking...
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    try{

        const response = await fetch(
            `${BACKEND_URL}/chat`,
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    message:userMessage
                })
            }
        );

        const data = await response.json();

        document.getElementById("loading").remove();

        chatBox.innerHTML += `
            <div class="message bot">
                ${data.response}
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    }

    catch(error){

        console.log(error);

        document.getElementById("loading").remove();

        chatBox.innerHTML += `
            <div class="message bot">
                Error connecting to backend.
            </div>
        `;
    }
}



async function uploadPDF(){

    const fileInput = document.getElementById("pdf-file");

    const file = fileInput.files[0];

    if(!file){

        alert("Please select a PDF");

        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try{

        const response = await fetch(
            `${BACKEND_URL}/upload-pdf`,
            {
                method:"POST",
                body:formData
            }
        );

        const data = await response.json();

        alert(data.message);
    }

    catch(error){

        console.log(error);

        alert("Upload failed");
    }
}