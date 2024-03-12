import streamlit as st
from PIL import Image
import PyPDF2
import fitz
from data.pdf_proc import crop_pdf, remove_grid
import requests
from PIL import Image
import io


# Configurar la página
st.set_page_config(layout="wide", page_title="ElectroCardiogram Classifier")

# Título principal y texto introductorio
st.title("Classify your ECG :heart:")
st.markdown(":dog: Try uploading an ElectroCardiogram PDF. This code is open source and available [here](https://github.com/ivanmarim/deeprythm) on GitHub")
st.markdown('Special thanks to the [Physionet Dataset](https://physionet.org/content/ptb-xl/1.0.3/) :grin:')
st.sidebar.header("Upload :gear:")

age = st.sidebar.slider('Your age', min_value=0, max_value=100)
st.sidebar.write("You selected ", age)

gender = st.sidebar.selectbox('Your gender', options=['Male', 'Female'])
st.sidebar.write("You selected ", gender)

# Importante elegir el tipo de reloj
watch = st.sidebar.selectbox('Your watch is', options=['Samsung', 'Apple'])
st.sidebar.write("You selected ", watch)

pdf_path = None
# Subir archivo PDF
pdf_path = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
# Functions to cut the pdf and remove the grid
#with fitz.open(stream=uploaded_file.getvalue(), filetype="pdf") as pdf_file:

if pdf_path is not None:
    with open(pdf_path, 'rb') as file:
        files = {'pdf_file': file}
        #Upload pdf and get a response with images and predictions
        response = requests.post('http://nuesta_api/upload',files=files)
        if response.status_code == 200:
            data = response.json()
            sub_cr = 'Cropped image'
            sub_gl = 'Grid removed image'
            title_cr = 'Image cropped from the .pdf'
            title_gl = 'Grid removed from the image to pass through the model'

            st.subheader(f"{title_cr}")
            image1_data = base64.b64decode(response.json()['image'])
            image1 = Image.open(io.BytesIO(image1_data))
            st.image(image1, caption=f"{sub_cr}", use_column_width=True)

            st.subheader(f"{title_gl}")
            image1_data = base64.b64decode(response.json()['image_nogrid'])
            image1 = Image.open(io.BytesIO(image1_data))
            st.image(image1, caption=f"{sub_gl}", use_column_width=True)
            st.success(f"Prediction: {data['prediction']}")
        else:
            st.error("Failed to fetch images and prediction from API")
