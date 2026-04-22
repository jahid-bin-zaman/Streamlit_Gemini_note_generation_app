from google import genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import io

# loading the environment variable
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# initializing a client
client = genai.Client(api_key=api_key)



# note generator
def note_generator(images):
    
    prompt = """Summarize the picture in note format at max 100 words in Bangla language and
    make sure to add necessary markdown to differentiate different section"""
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[images, prompt]
    )
    
    return response.text

def audio_generator(text):
    speech = gTTS(text, lang='bn', slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)

    return audio_buffer

def quiz_generator(images, difficulty):
    prompt = f"""Generate 3 quizzes based on the difficulty {difficulty}.
    Make sure to add markdown to differentiate the options.
    Add correct options bellow"""
    
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents = [images, prompt]
    )
    
    return response.text
    
    