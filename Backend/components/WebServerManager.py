import subprocess

class Webserver():

    # Constructor
    def __init__(self, host, port):
        self.Host = host
        self.Port = port

    # Starts the webserver
    def StartServer(self):
        print("[x] Starting the server.")
        try:
            # I don't like flask's messages, so I pipe all output to this so it won't show up. 
            std = open("NUL", 'w')

            serverCommand =f"python ./components/FlaskNews/app.py {self.Host} {self.Port}"            
            subprocess.run(serverCommand, stdout=std, stderr=std)
        except:
            return False

if __name__ == '__main__':
    x = Webserver('127.0.0.1', 8080)
    x.StartServer()