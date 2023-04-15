import requests
import json
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
# Récupération de la clé d'API auprès de OpenAI
api_key = 'VOTRE-CLE-API'

# Définition de l'URL de l'API de ChatGPT
# url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
url = 'https://api.openai.com/v1/completions'

# Définition des paramètres pour l'API de ChatGPT
params = {
    'prompt': '',
    'temperature': 0.7,
    'max_tokens': 1024,
    'top_p': 1,
    'stop': None,
    'n': 1,
    'frequency_penalty': 0,
    'presence_penalty': 1,
    'model': 'text-davinci-003',
}


# Boucle infinie pour saisir continuellement des phrases et obtenir des réponses
# while True:
# Demande à l'utilisateur de saisir une phrase
# prompt = input('Vous: ')
def chat(prompt):
    # Met à jour les paramètres de l'API avec la phrase saisie
    params['prompt'] = f"fr: {prompt}"

    # Envoi de la requête à l'API de ChatGPT
    response = requests.post(url, headers={'Authorization': f'Bearer {api_key}'}, json=params)

    # Récupération de la réponse de l'API et extraction du texte généré
    data = json.loads(response.text)

    completions = data['choices'][0]['text']
    answer = completions.strip()

    # Affichage de la réponse de l'API
    print(f"ChatGPT: {answer}")

    # Convertir la réponse en audio avec gTTS
    tts = gTTS(text=answer, lang="fr")
    if os.path.isfile("C:/Maria/output.mp3"):
        os.remove("C:/Maria/output.mp3")
    tts.save("C:/Maria/output.mp3")

    # Jouer l'audio avec pygame
    pygame.mixer.init()
    pygame.mixer.music.load("C:/Maria/output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove("C:/Maria/output.mp3")


# Créer un objet recognizer pour la reconnaissance vocale
r = sr.Recognizer()

# Utiliser le microphone par défaut comme source audio
with sr.Microphone() as source:
    # Régler le niveau de bruit de fond pour améliorer la reconnaissance vocale
    r.adjust_for_ambient_noise(source)

    while True:
        # Demander à l'utilisateur de parler
        print("Dites quelque chose!")
        audio = r.listen(source)

        try:
            # Convertir l'audio en texte
            text = r.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit: {text}")

            # Envoyer la saisie utilisateur à l'API de ChatGPT
            chat(text)

        except sr.UnknownValueError:
            print("Impossible de comprendre la saisie vocale")
        except sr.RequestError as e:
            print(f"Erreur de la reconnaissance vocale: {e}")
