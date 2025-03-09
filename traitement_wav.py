import wave
import struct
import os

def lire_wav(fichier):
    """Lit un fichier WAV et retourne l'en-tête et les données audio."""
    with wave.open(fichier, "rb") as wav_file:
        params = wav_file.getparams()  # Récupérer les métadonnées (nb canaux, échantillonnage, etc.)
        frames = wav_file.readframes(wav_file.getnframes())  # Lire les données audio
    return params, frames

def verifier_wav(params):
    """Vérifie si le fichier WAV est bien au format PCM 16 bits."""
    if params.sampwidth != 2:
        raise ValueError("Le fichier WAV doit être en 16 bits PCM.")
    if params.nchannels not in [1, 2]:  # Mono ou Stéréo
        raise ValueError("Le fichier WAV doit être mono ou stéréo.")
    if params.comptype != "NONE":
        raise ValueError("Le fichier WAV doit être non compressé (PCM).")
    return True

def ecrire_wav(fichier, params, donnees):
    """Écrit un fichier WAV valide."""
    try:
        with wave.open(fichier, "wb") as wav_file:
            wav_file.setparams(params)  # Appliquer les mêmes paramètres que le fichier original
            wav_file.writeframes(donnees)  # Écrire les données audio
    except IOError as e:
        raise RuntimeError(f"Erreur lors de l'écriture du fichier WAV : {e}")

# Exemple d'utilisation :
# amplifier_wav("input.wav", "output.wav", 1.5)
