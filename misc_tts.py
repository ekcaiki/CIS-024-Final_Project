import xml.etree.ElementTree as ET
import copy
import requests, uuid

# Uses key to query url for a token valid for 10 minutes
def get_issue_token(subscription_key, token_generater_url):
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    max_attempts = 3
    while max_attempts > 0:
        try:
            response = requests.post(token_generater_url, headers=headers)
            access_token = str(response.text)
            return access_token
        except:
            max_attempts = max_attempts -1
    return ""

# POSTs token to endpoint, sending ssml and dumping response into mp3 file
def send_text(token,endpoint,uuid,ssml, mp3_file):
    headers = {
        'Authorization': 'Bearer '  + token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-48khz-96kbitrate-mono-mp3',
        'User-Agent': 'Application for Final',
# Optional
        'cache-control': 'no-cache',
        'X-ClientTraceId': uuid
    }
    try:
        vocalize_request = requests.post(endpoint, headers=headers, data=ssml)
        #print(vocalize_request.status_code)
        # Retrieve mp3 data andn write to file
        with open(f"{mp3_file}", "wb") as binary_file:
        #Write bytes to file
            binary_file.write(vocalize_request.content)
    except:
        with open(f"{mp3_file}", "w") as text_file:
        #Write bytes to file
            text_file.write("Request to generation mp3 for translation failed")

def init_lang_locale_dict():
    return {
        "en":"en-US",
        "it":"it-IT",
        "ja":"ja-JP",
        "ru":"ru-RU",
        "de":"de-AT"
    }

# Maps language to specific locale used to find Neural Voice
def init_lang_voice_dict(nv_xml_file):
    # Dictionary will populated and returned
    lang_voice_dict = {}
    # Name spaces for xpath to search xml file
    ns = {'default': 'http://www.w3.org/2001/10/synthesis',
          'x': 'http://www.w3.org/XML/1998/namespace'}
    tree = ET.parse(nv_xml_file)
    # Entries in dictionary: { lang:Speak_Element }
    for lang, encode in lang_locale_dict.items():
        speak_xml_tree = tree.find(f'.//default:speak[@x:lang="{encode}"]', ns)
        lang_voice_dict[lang] = copy.deepcopy(speak_xml_tree)
    return lang_voice_dict

# XML file containg voices used for Text To Speech
NEURAL_VOICES_XML_FILE = "neural_voices.xml"

# Init dictionaries used in module functions
lang_locale_dict = init_lang_locale_dict()
lang_voice_dict = init_lang_voice_dict(NEURAL_VOICES_XML_FILE)

# Returns a SSML elment "speak" node for language with voice element containg text speak
def get_speak_xml_node(lang, text):
    cpy = copy.deepcopy(lang_voice_dict[lang])
    cpy[0].text = text
    return cpy

# Returns SSML for language with voice element containg text speak
def get_speak_ssml(lang, text):
    return ET.tostring(get_speak_xml_node(lang, text), encoding='utf8')
