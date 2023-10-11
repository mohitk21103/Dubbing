import moviepy.editor as mp
import speech_recognition as sr
from gtts import gTTS
import os
from googletrans import Translator

# Load the input video
input_video_path = 'Never Give Up.mp4'  # Replace with your video file path
output_audio_path = 'temp_audio.wav'  # Temporary audio file path

# Load the video and extract the audio
video_clip = mp.VideoFileClip(input_video_path)
audio_clip = video_clip.audio
audio_clip.write_audiofile(output_audio_path)

# Initialize the recognizer
recognizer = sr.Recognizer()

# Recognize speech from the audio file
with sr.AudioFile(output_audio_path) as source:
    audio_data = recognizer.record(source)  # Record the audio data
    audio_text = recognizer.recognize_google(audio_data)

# Print the recognized text
print("Recognized Text:")
print(audio_text)

# Define the target languages and their corresponding language codes
target_languages = {'Hindi': 'hi', 'Tamil': 'ta', 'Telugu': 'te', 'Marathi': 'mr'}

# Process each target language and generate audio
for lang, lang_code in target_languages.items():
    # Create an instance of the Translator class
    translator = Translator()

    # Translate the recognized English text to the target language
    translated_text = translator.translate(audio_text, src='en', dest=lang_code).text

    # Create a Text-to-Speech object for the translated text
    tts = gTTS(text=translated_text, lang=lang_code)

    # Save the TTS audio to a temporary file
    temp_audio_path = f'temp_audio_{lang}.mp3'
    tts.save(temp_audio_path)

    # Load the generated audio
    generated_audio_clip = mp.AudioFileClip(temp_audio_path)

    # Combine the generated audio with the video
    video_with_audio = video_clip.set_audio(generated_audio_clip)

    # Define the output video file path
    output_video_path = f'output_{lang}.mp4'

    # Write the video to the output file with compatible codecs
    video_with_audio.write_videofile(output_video_path, codec='libx264', audio_codec='aac', threads=4)

    # Clean up temporary audio file
    os.remove(temp_audio_path)
