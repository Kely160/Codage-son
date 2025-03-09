import tkinter as tk
import pygame.mixer
from amplification_wav import amplifier_wav
from reduction_bruit import reduire_bruit_wav
from utils import selectionner_fichier, afficher_message

pygame.mixer.init()
lecture_en_pause = False

def choisir_fichier():
    fichier = selectionner_fichier()
    if fichier:
        entree_fichier.delete(0, tk.END)
        entree_fichier.insert(0, fichier)

def traiter_fichier():
    fichier_entree = entree_fichier.get()
    try:
        facteur = float(entree_facteur.get())
        fichier_sortie = "output.wav"
        amplifier_wav(fichier_entree, fichier_sortie, facteur)
    except Exception as e:
        afficher_message("erreur", "Erreur", f"Problème : {e}")

def appliquer_reduction_bruit():
    fichier_entree = entree_fichier.get()
    reduire_bruit_wav(fichier_entree)

def lire_wav(fichier):
    global lecture_en_pause
    if fichier:
        pygame.mixer.music.load(fichier)
        pygame.mixer.music.play()
        lecture_en_pause = False

def pause_wav():
    global lecture_en_pause
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        lecture_en_pause = True

def reprendre_wav():
    global lecture_en_pause
    if lecture_en_pause:
        pygame.mixer.music.unpause()
        lecture_en_pause = False

def arreter_wav():
    pygame.mixer.music.stop()

# Interface Tkinter
fenetre = tk.Tk()
fenetre.title("Traitement de son WAV")
fenetre.geometry("400x600")

# Widgets
tk.Label(fenetre, text="Sélectionner un fichier WAV :").pack(pady=5)
entree_fichier = tk.Entry(fenetre, width=40)
entree_fichier.pack()
tk.Button(fenetre, text="Parcourir", command=choisir_fichier).pack(pady=5)

tk.Label(fenetre, text="Facteur d'amplification :").pack(pady=5)
entree_facteur = tk.Entry(fenetre)
entree_facteur.pack()

tk.Button(fenetre, text="Amplifier", command=traiter_fichier).pack(pady=10)
tk.Button(fenetre, text="Réduction de bruit", command=appliquer_reduction_bruit).pack(pady=10)

# Contrôles de lecture
tk.Label(fenetre, text="Contrôles de lecture :").pack(pady=10)

tk.Button(fenetre, text="Écouter Original", command=lambda: lire_wav(entree_fichier.get())).pack(pady=5)
tk.Button(fenetre, text="Écouter Amplifié", command=lambda: lire_wav("output.wav")).pack(pady=5)
tk.Button(fenetre, text="Écouter Sans Bruit", command=lambda: lire_wav("denoised.wav")).pack(pady=5)

tk.Button(fenetre, text="Pause", command=pause_wav).pack(pady=5)
tk.Button(fenetre, text="Reprendre", command=reprendre_wav).pack(pady=5)
tk.Button(fenetre, text="Arrêter", command=arreter_wav).pack(pady=5)

fenetre.mainloop()
