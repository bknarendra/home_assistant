from gtts import gTTS
import os
from processor import Processor
import cherrypy


class AppServer(object):

    def __init__(self):
        self.processor = Processor()

    @cherrypy.expose
    def process(self, cmd):
        print("cmd = %s" % (cmd))
        if cmd is None:
            tts = gTTS(text="Sorry I could not understand that", lang='en')
            tts.save("resources/temp.mp3")
            os.system("mplayer -quiet resources/temp.mp3 >/dev/null 2>&1")
        else:
            self.processor.process(cmd)

        return {"success": True}


cherrypy.config.update(
    {'server.socket_host': '0.0.0.0'})

cherrypy.quickstart(AppServer())
