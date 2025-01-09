
// Connect to chat stream on load
window.addEventListener('load', function () {
    const chatStream = new EventSource("/api/v1/stream");
    const chatBox = this.document.getElementById("chatBox");

    chatStream.onmessage = (event) => {
        // Parse chat
        const chatData = JSON.parse(event.data);
        console.log(chatData);

        // Create chat
        const chat = document.createElement("div");
        chat.setAttribute("class", "chat");

        const sender = document.createElement("div");
        sender.setAttribute("class", "chat-sender");
        sender.innerHTML = chatData.sender;

        const message = document.createElement("div");
        message.setAttribute("class", "chat-message");
        message.innerHTML = chatData.message;

        // Delete old chat if chats are more than 100
        if (chatBox.children.length >= 100) {
            chatBox.removeChild(chatBox.children[0]);
        }

        // Create new chat
        chat.appendChild(sender);
        chat.appendChild(message);
        chatBox.appendChild(chat);
    }
});