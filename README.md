Packages needed (and all dependencies)

1. SpeechRecognition
2. snowboydecoder
3. gTTS
4. wit
5. nanpy
6. nanpy firmware

sudo pip install --upgrade youtube-dl

install adapt
pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser
pip install beautifulsoup4

Compile snowboy for your respective OS (currently its compiled on Mac) from the snowboydecoder_full directory and copy the _snowboydetect.so file to app root (ie. current) directory.


To run app as standalone on raspberry pi do:
> python main.py

Watch the demo https://www.youtube.com/watch?v=-DLjnHr4Hu8 for more help on how to run and use the app.

To run the app in client server mode

Run server on raspberry pi by:
> python server.py

To run the client (other computer) edit `server_url` in the client.py and run
> python client.py
