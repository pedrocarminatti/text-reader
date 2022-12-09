import requests
import base64
import json
import os
from gtts import gTTS
from playsound import playsound

def detect_text(frame):
    my_base64 = base64.b64encode(frame)

    # url = google cloud vision api url
    data = {
        "requests": [
            {
                "image": {
                    "content": my_base64.decode("utf-8")
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }

    r = requests.post(url=url, data=json.dumps(data))

    texts = r.json()["responses"][0]["textAnnotations"][0]["description"]
    print(texts)
    speak(texts)

    return texts


def speak(text):
    synth = gTTS(text, lang='pt')
    file = os.path.join(os.getcwd(), 'audio.mp3')
    synth.save(file)
    playsound(file)
    os.remove('audio.mp3')