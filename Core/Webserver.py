import subprocess
import sys


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
            except BaseException:
                return False
        # Linux variant
        elif self.platform == "linux":
            try:
                serverCommand = f"python3 FlaskServer/app.py {self.Host} {self.Port}"
                subprocess.run(serverCommand)
            except BaseException:
                return False


if __name__ == '__main__':
    x = Webserver('127.0.0.1', 8080)
    x.StartServer()
