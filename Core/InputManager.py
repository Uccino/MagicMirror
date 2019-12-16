class InputGetter():
    def __init__(self, pageManager):
        self.PageManager = pageManager

    def GetKeyboardInput(self):
        inp = None
        while inp != 'q':
            inp = input("Input: ")
            if inp == 'w':
                self.PageManager.ZoomIn()
            elif inp == 's':
                self.PageManager.ZoomOut()
            elif inp == 'a':
                self.PageManager.PreviousPage()
            elif inp == 'd':
                self.PageManager.NextPage()

            self.PageManager.DisplayMirrorPage()
