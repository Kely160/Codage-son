import wave
import struct
import numpy as np
from utils import afficher_message

def estimate_noise(signal, frame_size=1024):
    """
    Estime la puissance du bruit en prenant les parties les plus silencieuses du signal.
    :param signal: Signal audio sous forme de tableau numpy.
    :param frame_size: Taille des blocs pour l'analyse.
    :return: Puissance moyenne du bruit.
    """
    num_frames = len(signal) // frame_size
    min_power = np.inf

    for i in range(num_frames):
        frame = signal[i * frame_size : (i + 1) * frame_size]
        power = np.mean(frame ** 2)
        min_power = min(min_power, power)

    return min_power


def wiener_filter(signal, noise_power):
    """
    Applique un filtre de Wiener amélioré en supprimant les fréquences parasites.
    :param signal: Signal audio sous forme de tableau numpy.
    :param noise_power: Niveau de bruit estimé.
    :return: Signal filtré.
    """
    signal = signal.astype(np.float32)

    # Transformée de Fourier pour analyse fréquentielle
    freq_signal = np.fft.rfft(signal)
    power_signal = np.abs(freq_signal) ** 2

    # Calcul du filtre Wiener en domaine fréquentiel
    wiener_gain = power_signal / (power_signal + noise_power)
    freq_filtered = wiener_gain * freq_signal

    # Retour au domaine temporel
    filtered_signal = np.fft.irfft(freq_filtered)

    return np.clip(filtered_signal, -32768, 32767).astype(np.int16)  # Éviter les débordements


def smooth_signal(signal, window_size=5):
    """
    Applique une moyenne glissante pour lisser le signal.
    :param signal: Signal audio sous forme de tableau numpy.
    :param window_size: Nombre d'échantillons à moyenner.
    :return: Signal lissé.
    """
    smoothed = np.convolve(signal, np.ones(window_size) / window_size, mode='same')
    return smoothed.astype(np.int16)


def reduire_bruit_wav(fichier_entree):
    """Réduction avancée du bruit avec Wiener + FFT + Lissage."""
    fichier_sortie = "denoised.wav"

    try:
        # Ouvrir le fichier WAV
        with wave.open(fichier_entree, 'rb') as wav_in:
            params = wav_in.getparams()
            num_channels, sample_width, frame_rate, num_frames = params[:4]

            # Lire les données audio
            raw_data = wav_in.readframes(num_frames)

        # Convertir en valeurs numériques
        fmt = f"{num_frames * num_channels}h"  # Format signé short
        audio_data = np.array(struct.unpack(fmt, raw_data), dtype=np.int16)

        # Estimer le bruit
        noise_power = estimate_noise(audio_data)

        # Appliquer le filtre de Wiener amélioré
        filtrage = wiener_filter(audio_data, noise_power)

        # Appliquer un lissage pour supprimer les artefacts
        filtrage = smooth_signal(filtrage)

        # Convertir en binaire pour écriture
        filtered_data = struct.pack(fmt, *filtrage)

        # Sauvegarder le fichier filtré
        with wave.open(fichier_sortie, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(filtered_data)

        afficher_message("info", "Succès", f"Fichier avec réduction de bruit enregistré sous {fichier_sortie}")

    except Exception as e:
        afficher_message("erreur", "Erreur", f"Problème lors de la réduction de bruit : {e}")
