import struct
from traitement_wav import lire_wav, verifier_wav, ecrire_wav

def amplifier_wav(fichier_entree, fichier_sortie, facteur):
    """Amplifie un fichier WAV en s'assurant qu'il est bien au format PCM 16 bits."""
    try:
        params, donnees = lire_wav(fichier_entree)
        
        # Vérifier que le format est correct
        verifier_wav(params)

        # Convertir les données audio en entiers 16 bits
        echantillons = list(struct.unpack("<" + "h" * (len(donnees) // 2), donnees))

        # Appliquer l'amplification avec saturation
        max_amp, min_amp = 32767, -32768
        echantillons_amplifies = [max(min(int(e * facteur), max_amp), min_amp) for e in echantillons]

        # Reconvertir en bytes
        donnees_amplifiees = struct.pack("<" + "h" * len(echantillons_amplifies), *echantillons_amplifies)

        # Sauvegarde du fichier amplifié
        ecrire_wav(fichier_sortie, params, donnees_amplifiees)

        print(f"✅ Amplification réussie : fichier sauvegardé sous {fichier_sortie}")

    except Exception as e:
        print(f"❌ Erreur : {e}")