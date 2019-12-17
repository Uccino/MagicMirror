import subprocess
import sys
import os 

class Webserver():

    def __init__(self, host, port):
        self.Host = host
        self.Port = port
        self.platform = sys.platform

    def StartServer(self):
        """Starts the flask webserver

        Returns:

            [bool] -- [True if server was started]

        """

        print("[x] Starting the webserver server.")
        
        # If we're running on windows
        if self.platform == "win32":
            try:
                serverCommand = f"python ./Core/FlaskServer/app.py {self.Host} {self.Port}"
                subprocess.run(serverCommand)
            except Exception:
                print("Help")
                return False
        # Linux variant
        elif self.platform == "linux":
            try:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                serverCommand = f"python3 {dir_path}/FlaskServer/app.py {self.Host} {self.Port}"
                subprocess.call(serverCommand, shell=True)
            except Exception as e:
                print(e)
                return False


if __name__ == '__main__':
    x = Webserver('127.0.0.1', 8080)
    x.StartServer()
