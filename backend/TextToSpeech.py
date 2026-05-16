import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

async def TextToAudioFile(text) → None:
    file_path = r"Data\Speech.mp3"

    if os.path.exists(file_path):
        os.remove(file_path)
    
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='13%')
    await communicate.save(r'Data\speech.mp3')

def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            asyncio.run(TextToAudioFile(Text))
            pygame.mixer.init()
            pygame.mixer.music.load(r"Data\Speech.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)
            return True
        except Exception as e:
            print(f"Error in TTS: {e}")
        finally:
            try:
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in finally block: {e}")