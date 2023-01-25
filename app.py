# app.py
import json
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return "Plex <-> Supla WebHook Listener by Xmon <a href='https://Xmon.eu.org/' targen='_BLANK'>https://Xmon.eu.org/</a>"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = json.loads(request.form.get('payload', "invalid"))
        print("Player Plex Identyfikator ", data['Player']['uuid'])
        sendAction(
            data, #to zawsze takie samo
            'https://svr11.supla.org/direct/xxxxx', #url do bramki supli
            "xxxxxxxxx", #code od bramki supli (identyfikator)
            "turn-off", #akcja która ma się zrobić na urządzeniu supla Dostępne: turn-on, turn-off, read
            "media.play",#przy jakim evencie ma sie to wykonać. Dostępne eventy: media.pause, media.play, media.rate, media.resume, media.scrobble, media.stop
            "playerId" #na jakim urządzeniu plex ma to działać
        )
        return "🚀 Webhook received!"

app.run(host='0.0.0.0', port=8000)


def sendAction(json, suplaUrl, suplaCode, suplaAction, plexEvent, plexUser):
    if json['Player']['uuid'] == plexUser && json['event'] == plexEvent:
        data = {'code': suplaCode, 'action': suplaAction}
        header = {"Content-Type": "application/json"}
        requests.patch(suplaUrl, data, headers=header)