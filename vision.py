import requests
import base64
import json
import os
from gtts import gTTS
from playsound import playsound

def detect_text(frame):
    my_base64 = base64.b64encode(frame)

    url = "https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDfECYjAV2dVwIgUEcEucuUFcFpKC4BwCA"
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
    synth = gTTS(text, lang='pt', slow=False)
    file = os.path.join(os.getcwd(), 'audio.mp3')
    synth.save(file)
    playsound(file)
    os.remove('audio.mp3')


# def text_to_speech(text):
#     url = "https://texttospeech.googleapis.com/v1/text:synthesize?key=AIzaSyDfECYjAV2dVwIgUEcEucuUFcFpKC4BwCA"
#     data = {
#         "input": {
#             "text": text
#         },
#         "voice": {
#             "languageCode": "pt-BR",
#             "name": "pt-BR-Standard-B",
#             "ssmlGender": "MALE"
#         },
#         "audioConfig": {
#             "audioEncoding": "MP3"
#         }
#     }

#     r = requests.post(url=url, data=json.dumps(data))

#     texts = r.json()["audioContent"]

#     results = base64.b64decode(texts)
#     print(texts)

#     with open("output/audio.wav", "wb") as output:
#         output.write(results)
        
#     speak(results)
