from .ChromaBinary import ChromaBcaHandler
from .ChromaDatatypes import Heartbeat, ChromaAppInfo
from .ChromaDevices import Keyboard, Mouse, Mousepad, ChromaLink, Headset
from sys import platform

if platform == "linux" or platform == "linux2":
    from .LinuxDevices import LinuxDevices

    class ChromaApp:
        def __init__(self, Info: ChromaAppInfo):
            try:
                self._Handler = LinuxDevices()
                self.Keyboard = self._Handler._keyboard
                self.BcaHandler = ChromaBcaHandler()
            except:
                # TODO Add proper exception handling
                print('Unexpected Error!')
                raise


elif platform == "win32":
    import requests

    class ChromaApp:
        def __init__(self, Info: ChromaAppInfo):
            try:
                url = 'http://localhost:54235/razer/chromasdk'

                data = {
                    "title": Info.Title,
                    "description": Info.Description,
                    "author": {
                        "name": Info.DeveloperName,
                        "contact": Info.DeveloperContact
                    },
                    "device_supported": Info.SupportedDevices,
                    "category": Info.Category
                }
                response = requests.post(url=url, json=data)
                self.SessionID, self.URI = response.json()['sessionid'], response.json()['uri']
                self.heartbeat = Heartbeat(self.URI)
                self.Keyboard = Keyboard(self.URI)
                self.Mouse = Mouse(self.URI)
                self.Mousepad = Mousepad(self.URI)
                self.Headset = Headset(self.URI)
                self.ChromaLink = ChromaLink(self.URI)
                self.BcaHandler = ChromaBcaHandler()
            except:
                # TODO Add proper exception handling
                print('Unexpected Error!')
                raise

        def Version(self):
            try:
                return requests.get(url='http://localhost:54235/razer/chromasdk').json()['version']
            except:
                # TODO Add proper exception handling
                print('Unexpected Error!')
                raise

        def __del__(self):
            print('Im dying')
            self.heartbeat.stop()
