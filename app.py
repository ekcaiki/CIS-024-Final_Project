import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

from misc_tts import get_issue_token, get_speak_ssml, send_text
import logging
from threading import Thread, Timer

# Load the values from .env
speech_resource_key = os.environ['SPEECH_KEY']
token_generater_url = os.environ['TTS_ISSUETOKEN_ENDPOINT']
token_issue_freq = int(os.environ['ISSUETOKEN_FREQUENCY'])

# Other Variables with Module Scope
# Directory which holds static output served to users
static_dir = os.environ['MP3_DIR']
# Hold value of token used for Text to Speech
token_dict = {"issued_token": ""}

# Retrieves and caches a new token, sets timer to repeat every period of seconds
def get_token_and_set_timer(seconds, foo, key, url):
    token = get_issue_token(key, url)
    token_dict["issue_token"] = token
    t = Timer(seconds, foo, (seconds, foo, key, url))
    t.start()

# Thread retrieves a new token from token_generater_url every token_issue_freq seconds
issue_token_thread = Thread(target=get_token_and_set_timer,
                            args=(token_issue_freq,
                                  get_token_and_set_timer,
                                  speech_resource_key,
                                  token_generater_url
                                  ))
issue_token_thread.start()

from flask import Flask, redirect, url_for, request, render_template, session
app = Flask(__name__, static_folder=static_dir)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values for Translation from .env
    key = os.environ['TRANSLATION_KEY']
    endpoint = os.environ['TRANSLATION_ENDPOINT']
    location = os.environ['TRANSLATION_LOCATION']

    # fetch Translated Text
    cur_uuid = str(uuid.uuid4()) # use for both Transation and TTS
    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': cur_uuid
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]

    # Make the call using post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']

    # Load the value for TTS from .env
    tts_endpoint= os.environ['TTS_ENDPOINT']

    # Fetch mp3 for text to speech
    mp3_file = f"tr-{cur_uuid}.mp3" #  Hold binary data retur ned from TTS
    # Fetch SSML to send to TTS REST API
    ssml = get_speak_ssml(target_language,translated_text)
    #logging.warning(f"POST ssml : {ssml}")
    # send_text, writing binary file to static_dir
    send_text(token_dict["issue_token"],tts_endpoint,
              cur_uuid,ssml, f"{static_dir}/{mp3_file}")

    # FINALLY, Render response
    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language,
        mp3_file=mp3_file
    )
