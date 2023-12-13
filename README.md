# CIS-024-Final_Project
Final Project for Python Class at SJCC

This project relies on REST API's from the following Azure Cognitive Services from Microsoft:
  Translation
  Speech (specifically "Text to Speech", or TTS)

Access to Azure (free, if need be) may be acquired at the Azure Portal:
  https://portal.azure.com/

Each service will require the creation of a corresponding Resource, and each Resource will create various Endpoints, Keys, etc...

For this application,  use of the Translation Service will require:
  LOCATION
  KEY
  ENDPOINT

For this application , use of The Speech Service will require:
  LOCATION
  SPEECH_KEY
  ENDPOINT
  ISSUETOKEN_ENDPOINT
  NEURAL_VOICE_ENDPOINT

NOTE: The LOCATION and KEYS for each service are independent of on another!  Thus they may not be the same, and have meaning whose semantics are contextualized by each individual service.

Information about acquiring and configuring Azure Translation may be found here:
  https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation-overview

Information about acquiring and configuring Azure TTS may be found here:
  https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text?tabs=macos%2Cterminal&pivots=programming-language-csharp

This application uses flask and thus dotenv, so a .env file in the launch directory (the Root Directory of the Project) is required.  The variables defined in this file correspond to the endpoints, keys, etc.. for the different services previously mentioned.  .env should look like the following snippet, where YOUR_XXXX corresponds to what you have received after accessing and configuring the corresponding Azure service.

TRANSLATION_LOCATION=YOUR_LOCATION
TRANSLATION_KEY=YOUR_KEY
TRANSLATION_ENDPOINT=YOUR_ENDPOINT

SPEECH_LOCATION=YOUR_LOCATION
SPEECH_KEY=YOUR_KEY
SPEECH_ENDPOINT=YOUR_ENDPOINT
TTS_ISSUETOKEN_ENDPOINT=YOUR_ISSUETOKEN_ENDPOINT
TTS_ENDPOINT=NEURAL_VOICE_ENDPOINT

Install required pyton modules in {PROJECT_ROOT}/requirements.txt:
  pip install -r requirements.txt

This a flask application is run by the command 'flask run' which will open the application in a web server on your machine which, as indicated by the return of the command (if issued on the command line), should be http://127.0.0.1:5000
Consult the documentation for flask for details.
