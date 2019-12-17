const wsUrl = "ws://192.168.2.13:8000";
websocket = new WebSocket(wsUrl);
const getConfigJson = {
    "message": "get_config"
}

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

// Event listener for when a connection has been opened
websocket.addEventListener('open', function (event) {
    // Send GET/Config message to the server    
    console.log("Connection opened!");
    //websocket.send(JSON.stringify(getConfigJson));
});

// Event listener for when a message has been send
websocket.addEventListener('message', function (event) {
    ParseMessage(event.data);
});

// Event listener for when there is an error
websocket.addEventListener('error', function (event) {
    console.log("Websocket error! Unable to connect...");
});

// Event listener for when the server connection has been closed
websocket.addEventListener('close', function (event) {
    // sleep(5000).then(() => {
    //     location.reload();  
    // })    
});

function base64DecodeUnicode(str) {
    // Convert Base64 encoded bytes to percent-encoding, and then get the original string.
    percentEncodedStr = atob(str).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join('');


    return decodeURIComponent(percentEncodedStr);
}

function ParseMessage(message)
{    
    jsonObject = JSON.parse(base64DecodeUnicode(message));
    if(jsonObject.type == "mirror_page")
    {
        document.getElementById("module").innerHTML = jsonObject.data;
    }
    else if(jsonObject.type == "mirror_notification")
    {
        document.getElementById("mirror-notification").innerHTML = jsonObject.data;
    }
}