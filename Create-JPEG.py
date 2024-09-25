#importing required packages
import streamlit
from PIL import Image
import io
import zipfile

#adding title of the streamlit app
streamlit.title('PNG to JPEG Converter')

# let user to upload multiple PNG files using File uploader
uploaded_files = streamlit.file_uploader("Choose PNG files", type="png", accept_multiple_files=True)

# adding a "Convert" button
if streamlit.button('Convert'):
    if uploaded_files:
        # Creating a BytesIO buffer to store the ZIP file
        zip_buff = io.BytesIO()
        with zipfile.ZipFile(zip_buff, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for uploaded_file in uploaded_files:
                # opening the image file usnig Image object of PIL package
                image = Image.open(uploaded_file)
                 #converting file/s to JPEG
                converted_image = io.BytesIO()
                image.convert("RGB").save(converted_image, format='JPEG')
                converted_image.seek(0)
                # Displaying the converted image
                streamlit.write(f"Original file: {uploaded_file.name}")
                streamlit.image(converted_image, caption='Converted JPEG image', use_column_width=True, output_format="JPEG")

                # Adding the converted image to the ZIP file we initialized in start
                zip_file.writestr(uploaded_file.name.replace(".png", ".jpeg"), converted_image.read())

        # ensuring the buffer is set to the beginning
        zip_buff.seek(0)
    
        if len(uploaded_files)>1:
            # Create a download button
            streamlit.download_button(
                label="Download Converted Images", data=zip_buff , file_name="converted_images.zip", mime="application/zip")
        else:
            streamlit.download_button(
                    label=f"Download {uploaded_file.name.rsplit('.', 1)[0]}.jpeg",
                    data=converted_image,
                    file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.jpeg", on_click=None,
                    mime="image/jpeg")
    else:
        streamlit.warning("Please upload a PNG file.")
