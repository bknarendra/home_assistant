from bs4 import BeautifulSoup
import requests
import os
import commands
import re


class MusicIntentHandler():

    def __init__(self, intent):
        self.intent = intent
        self.mplayer_control_file = "/tmp/mplayer-control"
        if os.path.exists(self.mplayer_control_file):
            os.remove(self.mplayer_control_file)

        self.music_dir = "~/songs/*.mp3"

        os.mkfifo(self.mplayer_control_file)

    def handle(self):
        if self.intent["MusicVerb"] == 'stop':
            os.system(
                "kill -9 `ps aux | grep mplayer | grep -v grep | awk '{print $2}'`"  # NoQA
            )
            return

        print self.intent

        if "MusicKeyword" in self.intent and self.intent["MusicKeyword"] == 'music':
            self.play_music_from_local_store()
        else:
            self.play_stream(self.intent["Media"])

    def search(self, query):
        print("query = " + query)
        resp = requests.get(
            'https://www.youtube.com/results?search_query=' + query
        )
        return self.extract(resp.content)

    def extract(self, html):
        page = BeautifulSoup(html, 'html.parser')
        found = page.find_all(
            'a',
            'yt-uix-tile-link',
            href=re.compile(r'/watch\?v=')
        )
        if found:
            return found[0].get("href")

    def play_stream(self, query):
        print("searching on youtube %s" % (query))
        url = self.search(query)
        if not url:
            return

        cmd = "youtube-dl https://www.youtube.com%s -g" % url
        print(url)
        try:
            download_urls = commands.getstatusoutput(cmd)
            audio_url = download_urls[1].split("\n")[1]
            cmd = 'wget -q "%s" -O - | mplayer -cache 1024 - >/dev/null 2>&1 &' % (  # NoQA
                audio_url
            )
            print("streaming the audio")
            os.system(cmd)
        except Exception as e:
            print(e)

    def play_music_from_local_store(self):
        cmd = "mplayer -quiet -shuffle -slave -input file=%s %s >/dev/null 2>&1 &" % (  # NoQA
                self.mplayer_control_file,
                self.music_dir
            )
        print cmd
        os.system(cmd)

# MusicPlayer({}).play_stream(sys.argv[1])
