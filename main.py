import os
import openai
import warnings
from fastapi import FastAPI, HTTPException
from config import MAX_TOKENS, TRANSCRIPTION_MODEL, TRANSLATION_MODEL, SUPPORTED_LANGS
from models import SpeechTranscribeRequest, SpeechTranscribeResponse, TextTranslateRequest, TextTranslateResponse, SpeechTranslateRequest, SpeechTranslateResponse

# raised all warnings as an error
warnings.filterwarnings('error')

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    # raise warning and stop the program
    warnings.warn("OPENAI_API_KEY environment variable is not set. Please set your OPENAI_API_KEY as follows: \033[1m\033[32mexport OPENAI_API_KEY=<your-api-key>\033[0m")
    
app = FastAPI()

@app.get("/")
async def status():
    """
    Returns the status of the API.
    """
    return {"api_status": "OK"}

@app.post("/transcribe", response_model=SpeechTranscribeResponse)
async def transcribe_audio(request: SpeechTranscribeRequest) -> SpeechTranscribeResponse:
    """
    Transcribes the audio file specified in the request using OpenAI's audio transcription API.
    
    Args:
    - request: An instance of SpeechTranscribeRequest.
    
    Returns:
    - An instance of SpeechTranscribeResponse containing the transcription of the audio file.
    """

    try:
        # Speech to Text Transciption aka Speech Recognition
        async with open(request.file, "rb") as audio_file:
            transcription = await openai.Audio.transcribe(TRANSCRIPTION_MODEL, audio_file)
    except:
        raise HTTPException(status_code=400, detail="Error transcribing audio file")

    return SpeechTranscribeResponse(transcript=transcription['text'])

@app.post("/translate", response_model=TextTranslateResponse)
async def translate_text(request: TextTranslateRequest) -> TextTranslateResponse:
    """
    Translates the input text into the target language specified in the request 
    using OpenAI's machine translation API.
    
    Args:
    - request: An instance of TextTranslateRequest.
    
    Returns:
    - An instance of TextTranslateResponse containing the translated text in the target language.
    """

    if request.target_language.lower() not in SUPPORTED_LANGS:
        raise HTTPException(status_code=400, detail="Unsupported target language")
    
    try:
      # Text to Text Translation aka Machine Translation
      translated_text = await openai.Completion.create(
          model = TRANSLATION_MODEL,
          prompt = f"Translate this text: {request.text} to {request.target_language}.",
          max_tokens = MAX_TOKENS
        )
      translated_text = translated_text['choices'][0]['text'].replace('\n', '')
    except:
        raise HTTPException(status_code=400, detail="Error translating text")
    
    return TextTranslateResponse(translated_text=translated_text)
    
@app.post("/translate_speech", response_model=SpeechTranslateResponse)
async def translate_speech(request: SpeechTranslateRequest) -> SpeechTranslateResponse:
    """
    Transcribes the audio file specified in the request using OpenAI's Whisper API,
    then translates the transcription into the target language specified in the request 
    using OpenAI's GPT-3.5 API.
    
    Args:
    - request: An instance of SpeechTranslateRequest.

    Returns:
    - An instance of SpeechTranslateResponse containing the translated text in the target language.
    """

    if request.target_language.lower() not in SUPPORTED_LANGS:
        raise HTTPException(status_code=400, detail="Unsupported target language")
    
    try:
        # Speech to Text Transciption aka Speech Recognition
        async with open(request.file, "rb") as audio_file:
            transcription = await openai.Audio.transcribe(TRANSCRIPTION_MODEL, audio_file)
    except:
        raise HTTPException(status_code=400, detail="Error transcribing audio file")
    
    try:
      # Text to Text Translation aka Machine Translation
      translated_text = await openai.Completion.create(
          model = TRANSLATION_MODEL,
          prompt = f"Translate this text: {transcription['text']} to {request.target_language}.",
          max_tokens = MAX_TOKENS
        )
      translated_text = translated_text['choices'][0]['text'].replace('\n', '')
    except:
        raise HTTPException(status_code=400, detail="Error translating text")
      
    return SpeechTranslateResponse(translated_text=translated_text)


