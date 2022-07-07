console.log("Sanity check from room.js.");

const roomName = window.location.pathname.split("/").filter(e=>e)[1];
console.log(roomName)

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

//async function postData(url = '', data = {}) {
//  // Default options are marked with *
//  const response = await fetch(url, {
//    method: 'POST', // *GET, POST, PUT, DELETE, etc.
//    mode: 'cors', // no-cors, *cors, same-origin
//    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
//    credentials: 'same-origin', // include, *same-origin, omit
//    headers: {
//      'Content-Type': 'application/json'
//      // 'Content-Type': 'application/x-www-form-urlencoded',
//    },
//    redirect: 'follow', // manual, *follow, error
//    referrerPolicy: 'no-referrer', // no-referrer, *client
//    body: JSON.stringify(data) // body data type must match "Content-Type" header
//  });
//  return await response.json(); // parses JSON response into native JavaScript objects
//}


// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    console.log("message SENT")
//    postData('http://localhost:8000/chat/room/message/send', {
//      "receiver_id": 1,
//      "sender_id": 9,
//      "text": "HELLO"
//    }).then((data) => {
//    console.log(data); // JSON data parsed by `response.json()` call
//    });
    chatSocket.send(JSON.stringify({
    "message": chatMessageInput.value,
}));
    chatMessageInput.value = "";
};

let chatSocket = null;

function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log(data.user);
        switch (data.type) {
            case "chat_message":
                chatLog.value += data.user + ": " + data.message + "\n";
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();