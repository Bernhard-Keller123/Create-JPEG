import os
import streamlit as st
from PIL import Image

def load_and_convert_images(uploaded_files):
    if not uploaded_files:
        st.write("Keine Dateien ausgewählt.")
        return

    # Wähle den Zielordner auf dem lokalen Dateisystem (Optional: Kann durch die Cloud ersetzt werden)
    output_folder = st.text_input("Gib den Pfad des Zielordners ein, um die Bilder zu speichern:", value="")

    if not output_folder:
        st.warning("Kein Zielordner ausgewählt.")
        return

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

            # Erstelle einen neuen Dateinamen für den Zielordner und speichere als JPG
            filename, _ = os.path.splitext(uploaded_file.name)  # Dateiname ohne Erweiterung
            new_file_path = os.path.join(output_folder, f"{filename}.jpg")  # Immer .jpg speichern

            # Konvertiere das Bild, falls nötig, und speichere es als JPEG
            rgb_img = img.convert('RGB')  # Konvertiere das Bild zu RGB, um es als JPG zu speichern
            rgb_img.save(new_file_path, 'JPEG')  # Speichere es als .jpg

            if rotated:
                st.write(f"Bild gespeichert unter: {new_file_path} (umgewandelt und in JPG gespeichert)")
            else:
                st.write(f"Bild gespeichert unter: {new_file_path} (unverändert und in JPG gespeichert)")

        except Exception as e:
            st.error(f"Fehler beim Verarbeiten des Bildes {uploaded_file.name}: {e}")

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
        if st.button("Bilder verarbeiten und als JPG speichern"):
            load_and_convert_images(uploaded_files)
