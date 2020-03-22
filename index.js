const { app, BrowserWindow } = require('electron')

var commandlineArguments = process.argv.slice(2);

function createWindow () {
  // Create the browser window.
  let win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false
    }
  })

  // and load the index.html of the app.
  win.loadURL(commandlineArguments[0])
}

app.whenReady().then(createWindow)