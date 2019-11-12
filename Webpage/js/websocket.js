const wsUrl = "ws://localhost:8000";
websocket = new WebSocket(wsUrl);
const getConfigJson = {
    "message": "get_config"
}
window.onload = windowLoad();

function windowLoad() {
    startTime();
}

function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('time-text').innerHTML =
        h + ":" + m + ":" + s;
    var t = setTimeout(startTime, 500);
}

function checkTime(i) {
    if (i < 10) {
        i = "0" + i
    }; // add zero in front of numbers < 10
    return i;
}

// Event listener for when a connection has been opened
websocket.addEventListener('open', function (event) {
    // Send GET/Config message to the server    
    console.log("Connection opened!");
    //websocket.send(JSON.stringify(getConfigJson));
});

// Event listener for when a message has been send
websocket.addEventListener('message', function (event) {
    // Message will be in JSON form
    console.log("Message from the server: " + event.data);
});

// Event listener for when there is an error
websocket.addEventListener('error', function (event) {
    console.log("Websocket error! Unable to connect...");
});

// Event listener for when the server connection has been closed
websocket.addEventListener('close', function (event) {
    console.log("Websocket connection closed!");
});