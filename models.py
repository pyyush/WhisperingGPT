from pydantic import BaseModel


class SpeechTranscribeRequest(BaseModel):
    """
    Defines the input schema for the /transcribe endpoint. 
    It requires a file path.
    """
    file: str

class SpeechTranscribeResponse(BaseModel):
    """
    Defines the output schema for the /transcribe endpoint.
    It returns the transcription of the input audio file.
    """
    transcript: str

class TextTranslateRequest(BaseModel):
    """
    Defines the input schema for the /translate endpoint.
    It requires text to be translated and a target language.
    """
    text: str
    target_language: str

class TextTranslateResponse(BaseModel):
    """
    Defines the output schema for the /translate endpoint.
    It returns the translated text in the target language.
    """
    translated_text: str

class SpeechTranslateRequest(BaseModel):
    """
    Defines the input schema for the /translate_speech endpoint.
    It requires an audio file path and a target language.
    """
    file: str
    target_language: str

class SpeechTranslateResponse(BaseModel):
    """
    Defines the output schema for the /translate_speech endpoint.
    It returns the translated text in the target language.
    """
    translated_text: str


