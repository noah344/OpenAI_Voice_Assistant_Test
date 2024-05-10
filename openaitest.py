from os import environ
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import play, Voice, VoiceSettings
import speech_recognition as sr

# You need to set an environment variable named VOICEKEY with your ElevenLabs API Key.
voiceclient = ElevenLabs(api_key=environ['VOICEKEY'])

# You need to set an environment variable named OPENAI_API_KEY with your OPENAI Key.
client = OpenAI(api_key=environ['OPENAI_API_KEY'])
# Initializes an array to store chat history so OpenAI can use the context of previous questions/responses.
chat_history = []

# Initializes voice to text.
r = sr.Recognizer() 

# This is the first message that OpenAI will receive basically telling it how it should respond in the future.
FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are an AI assistant.  You help out by answering various questions.
                        
While responding, you must obey the following rules:
1) Provide short responses, 1 paragraph maximum unless told otherwise.
2) You will do your best to attempt to respond how a human would by emulating emotions, feelings, and preferences.
Okay, let the conversation begin!'''}

chat_history.append(FIRST_SYSTEM_MESSAGE)
while True:
    print("Speak Now")
    # Uses the microphone as an audio source, it'll auto-remove ambient noise and then translate the audio into text.
    with sr.Microphone() as source2:
        r.adjust_for_ambient_noise(source2, duration=0.2)
        audio2 = r.listen(source2)

        # The speech to text module uses google here to convert it to text.
        MyText = r.recognize_google(audio2)
        MyText = MyText.lower()

    chat_history.append({"role": "user", "content": MyText})
    print(MyText)

    # Here's where we query OpenAI, I'm using gpt-3.5-turbo cause it's cheaper.
    completion = client.chat.completions.create(
    messages=chat_history,
        model="gpt-3.5-turbo"
    )

    chat_history.append({"role": completion.choices[0].message.role, "content": completion.choices[0].message.content})

    # Here's where we get the response from OpenAI.
    response = completion.choices[0].message.content
    print(response)
    # Now we convert the tex to speech using ElevenLabs AI Voice generation.
    audio = voiceclient.generate(
    text=response, 
    voice=Voice(
        # This is the ID of a voice I generated on ElevenLabs.
        voice_id='LO5Q2kacZa9OdAJdHb6o',
        settings=voiceclient.voices.get_settings("LO5Q2kacZa9OdAJdHb6o")
    ),
    model="eleven_multilingual_v2"
    )
    # Finally the voice audio is played.
    play(audio)