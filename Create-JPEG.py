import os
import zipfile
from io import BytesIO
import streamlit as st
from PIL import Image
from pathlib import Path

def load_and_convert_images(uploaded_files):
    if not uploaded_files:
        st.write("Keine Dateien ausgewählt.")
        return
    
    # Erstelle ein BytesIO-Objekt zum Erstellen des ZIP-Archivs im Speicher
    zip_buffer = BytesIO()
    
    # ZIP-Datei erstellen
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            try:
                # Lade das Bild
                img = Image.open(uploaded_file)
                width, height = img.size
                rotated = False  # Flag um festzustellen, ob das Bild gedreht wurde

                # Überprüfe, ob das Bild im Hochformat ist (Höhe > Breite)
                if height > width:
                    # Drehe das Bild um 90 Grad, um es ins Querformat zu bringen
                    img = img.rotate(90, expand=True)
                    rotated = True
                    st.write(f"Bild {uploaded_file.name} wurde ins Querformat gedreht.")
                else:
                    st.write(f"Bild {uploaded_file.name} ist bereits im Querformat.")

                # Konvertiere das Bild zu RGB, um es als JPG zu speichern
                rgb_img = img.convert('RGB')

                # Speichere das Bild im ZIP-Archiv unter einem neuen Dateinamen
                filename, _ = os.path.splitext(uploaded_file.name)  # Dateiname ohne Erweiterung
                new_file_name = f"{filename}.jpg"

                # Speichere das Bild in der ZIP-Datei
                img_byte_arr = BytesIO()  # Temporärer Speicher für das Bild
                rgb_img.save(img_byte_arr, format='JPEG')  # Speichere das Bild im BytesIO-Objekt
                zip_file.writestr(new_file_name, img_byte_arr.getvalue())  # Füge das Bild zum ZIP-Archiv hinzu

            except Exception as e:
                st.error(f"Fehler beim Verarbeiten des Bildes {uploaded_file.name}: {e}")

    # Rückgabe der ZIP-Datei zum Herunterladen
    zip_buffer.seek(0)
    return zip_buffer


if __name__ == "__main__":
    st.title("Bildverarbeitungs-App")

    # Lade mehrere Dateien hoch
    uploaded_files = st.file_uploader("Lade eine oder mehrere Bilddateien hoch", type=["jpeg", "jpg", "png", "bmp", "gif", "tiff"], accept_multiple_files=True)

    if uploaded_files:
        # Zeige hochgeladene Bilder an
        for uploaded_file in uploaded_files:
            img = Image.open(uploaded_file)
            st.image(img, caption=f"Hochgeladenes Bild: {uploaded_file.name}", use_column_width=True)
        
        # Button zur Verarbeitung der Bilder
        if st.button("Bilder verarbeiten und als ZIP herunterladen"):
            zip_buffer = load_and_convert_images(uploaded_files)
            
            # Speichere die ZIP-Datei im "Downloads"-Ordner und stelle sie zum Download bereit
            st.download_button(
                label="Download ZIP",
                data=zip_buffer,
                file_name="processed_images.zip",
                mime="application/zip"
            )
