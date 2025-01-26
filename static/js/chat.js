
function isEmpty(v) {
    if (v === undefined || v === null) {
        return true;
    }

    return v.length === 0;
}

// Connect to chat stream on load
window.addEventListener('load', function () {
    const chatStream = new EventSource("/api/v1/stream");
    const chatBox = this.document.getElementById("chatBox");

    chatStream.onopen = () => {
        console.log("chat server connected");
    }

    chatStream.onerror = (event) => {
        console.log("error: ", event);
    }

    chatStream.onmessage = (event) => {
        console.log(event);
    }

    // Event listener: new chat
    chatStream.addEventListener("new_chat", (event) => {
        // Parse chat
        const chatData = JSON.parse(event.data);
        console.log("server event: ", event);

        // Create chat
        const chat = document.createElement("div");
        chat.setAttribute("class", "chat");

        const sender = document.createElement("div");
        sender.setAttribute("class", "chat-sender");
        sender.textContent = chatData.sender;

        const message = document.createElement("div");
        message.setAttribute("class", "chat-message");
        message.textContent = chatData.message;

        const timestamp = document.createElement("div");
        const messageDate = new Date(chatData.timestamp * 1000);
        timestamp.setAttribute("class", "chat-timestamp");
        timestamp.textContent = messageDate.toLocaleString(Intl.NumberFormat().resolvedOptions().locale);

        // Delete old chat if chats are more than 100
        if (chatBox.children.length >= 100) {
            chatBox.removeChild(chatBox.children[0]);
        }

        // Create new chat
        chat.appendChild(sender);
        chat.appendChild(message);
        chat.appendChild(timestamp);
        chatBox.appendChild(chat);

        // Move to bottom of chatbox
        chatBox.scrollTo(0, chatBox.scrollHeight);
    });

    // Event listener: new user
    chatStream.addEventListener("new_user", (event) => {
        const eventData = JSON.parse(event.data);

        console.log("new user is joined the room");
        console.log("server event: ", event);

        // Create chat
        const chat = document.createElement("div");
        chat.setAttribute("class", "event_new_user");

        const sender = document.createElement("div");
        sender.setAttribute("class", "message");
        sender.textContent = eventData.message;

        // Create new chat
        chat.appendChild(sender);
        chatBox.appendChild(chat);

        // Move to bottom of chatbox
        chatBox.scrollTo(0, chatBox.scrollHeight);
    });

    // Send chat to server
    document.querySelector("input[name='chatText']").addEventListener("keypress", function(e) {
        if (e.key !== 'Enter') {
            return;
        }

        e.preventDefault();

        // Get username
        const chatUser = document.querySelector("input[name='chatUser']");
        const username = !isEmpty(chatUser.value) ? chatUser.value : "Anonymous";
        const message = e.target.value;

        // Do nothing if no message entered
        if (isEmpty(message)) {
            return;
        }

        // Remove entered message
        e.target.value = "";

        // Send message
        fetch("/api/v1/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "sender": username,
                "message": message
            })
        })
        .then((response) => {
            // Move to bottom of chatbox
            chatBox.scrollTo(0, chatBox.scrollHeight);
        })
        .then((result) => {})
    })
});