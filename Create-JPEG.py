import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image


def load_and_convert_images():
    # Öffne einen Dateidialog, um mehrere Bild-Dateien auszuwählen (alle Bildformate)
    file_paths = filedialog.askopenfilenames(
        title="Wähle Bild-Dateien aus",
        filetypes=[("Image files", "*.jpeg *.jpg *.png *.bmp *.gif *.tiff"), ("All files", "*.*")]
    )

    if not file_paths:
        print("Keine Dateien ausgewählt.")
        return

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
