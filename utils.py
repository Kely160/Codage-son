import tkinter as tk
from tkinter import filedialog, messagebox
import winsound


def selectionner_fichier():
    """Ouvre une boîte de dialogue pour sélectionner un fichier WAV."""
    return filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])

def afficher_message(type_message, titre, message):
    """Affiche un message d'information ou d'erreur."""
    if type_message == "info":
        messagebox.showinfo(titre, message)
    elif type_message == "erreur":
        messagebox.showerror(titre, message)

def lire_wav(fichier):
    """Joue un fichier WAV."""
    try:
        winsound.PlaySound(fichier, winsound.SND_FILENAME)
    except Exception as e:
        afficher_message("erreur", "Erreur", f"Impossible de lire le fichier : {e}")
