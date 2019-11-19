const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

var mainWindow = null;

app.on('window-all-closed', function() {  
    app.quit();  
});

app.on('ready', function() {  
  var pythonProcess = require('child_process').spawn('python', ['Python/main.py']);  
  var request = require('request-promise');
  pagePath = "mirror_page/index.html";

  // Function to handle the window opening
  var openWindow = function(){

    mainWindow = new BrowserWindow({width: 800, height: 600, frame:false});
    mainWindow.setFullScreen(true);    
    mainWindow.loadFile(pagePath);

    mainWindow.on('closed', function() {
      mainWindow = null;
      pythonProcess.kill('SIGINT');
    });
  };

  // Function to handle startup of the server
  var startUp = function(){
    request(mainAddr)
      .then(function(htmlString){
        console.log('Server started!');
        openWindow();
      })
      .catch(function(err){
        console.log("Waiting for the python process to start the flask server");
        startUp();
      });
  };

  // fire!
  startUp();
});