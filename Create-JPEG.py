#importing required packages
import streamlit
from PIL import Image
import io
import zipfile

import os
from PIL import Image

import streamlit as st

st.title("Bilder hochladen")

# Datei-Upload-Komponente von Streamlit
uploaded_file = st.file_uploader("Wähle ein Bild aus", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Verwende den hochgeladenen Inhalt
    st.image(uploaded_file, caption="Hochgeladenes Bild", use_column_width=True)
    # Öffne einen Dialog, um einen Zielordner für die gespeicherten Bilder auszuwählen
    output_folder = filedialog.askdirectory(title="Wähle einen Zielordner für die Bilder aus")

    if not output_folder:
        print("Kein Zielordner ausgewählt.")
        return

    for file_path in file_paths:
        try:
            # Lade das Bild
            img = Image.open(file_path)
            width, height = img.size
            rotated = False  # Flag um festzustellen, ob das Bild gedreht wurde

            # Überprüfe, ob das Bild im Hochformat ist (Höhe > Breite)
            if height > width:
                # Drehe das Bild um 90 Grad, um es ins Querformat zu bringen
                img = img.rotate(90, expand=True)
                rotated = True
                print(f"Bild {file_path} wurde ins Querformat gedreht.")
            else:
                print(f"Bild {file_path} ist bereits im Querformat.")

            # Erstelle einen neuen Dateinamen für den Zielordner und speichere als JPG
            filename, _ = os.path.splitext(os.path.basename(file_path))  # Dateiname ohne Erweiterung
            new_file_path = os.path.join(output_folder, f"{filename}.jpg")  # Immer .jpg speichern

            # Konvertiere das Bild, falls nötig, und speichere es als JPEG
            rgb_img = img.convert('RGB')  # Konvertiere das Bild zu RGB, um es als JPG zu speichern
            rgb_img.save(new_file_path, 'JPEG')  # Speichere es als .jpg

            if rotated:
                print(f"Bild gespeichert unter: {new_file_path} (umgewandelt und in JPG gespeichert)")
            else:
                print(f"Bild gespeichert unter: {new_file_path} (unverändert und in JPG gespeichert)")

        except Exception as e:
            print(f"Fehler beim Verarbeiten des Bildes {file_path}: {e}")


if __name__ == "__main__":
    # Erstelle das Hauptfenster
    root = tk.Tk()
    root.withdraw()  # Versteckt das leere Tkinter-Fenster

    # Rufe die Funktion auf, um Dateien auszuwählen und Bilder zu laden und zu drehen
    load_and_convert_images()
