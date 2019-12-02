import subprocess
import sys

class Webserver():
    # Constructor
    def __init__(self, host, port):
        self.Host = host
        self.Port = port
        self.platform = sys.platform

    # Starts the webserver
    def StartServer(self):
        print("[x] Starting the webserver server.")
        # If we're running on windows
        if self.platform == "win32":
            try:                
                serverCommand =f"python ./FlaskServer/app.py {self.Host} {self.Port}"            
                subprocess.run(serverCommand)
            except:                
                return False
        # Linux variant
        elif self.platform == "linux":
            try:
                serverCommand =f"python3 FlaskServer/app.py {self.Host} {self.Port}"            
                subprocess.run(serverCommand)
            except:
                return False

if __name__ == '__main__':
    x = Webserver('127.0.0.1', 8080)
    x.StartServer()