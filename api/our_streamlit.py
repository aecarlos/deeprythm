import streamlit as st
from PIL import Image
import requests
import io
import openai
import base64

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

height = st.sidebar.slider('Your height (in cm)', min_value=0, max_value=220)
st.sidebar.write("You selected ", height)

weight = st.sidebar.slider('Your weight (in KG)', min_value=0, max_value=200)
st.sidebar.write("You selected ", weight)

# Importante elegir el tipo de reloj
watch = st.sidebar.selectbox('Your watch is', options=['Samsung', 'Apple'])
st.sidebar.write("You selected ", watch) # to use this in the API
pdf_path = None
# Subir archivo PDF
pdf_path = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
# Functions to cut the pdf and remove the grid
#with fitz.open(stream=uploaded_file.getvalue(), filetype="pdf") as pdf_file:
ecg_path = None
ecg_path = st.sidebar.file_uploader("Upload an ECG", type=["pdf"])

data = None
if pdf_path is not None:
    # Read the contents of the uploaded file
    pdf_data = pdf_path.read()

    # Create a file-like object from the bytes data
    pdf_file = io.BytesIO(pdf_data)

    # Create a dictionary containing the file to be uploaded
    files = {'file': pdf_file,
             'device': watch}

    # Upload the PDF and get a response with images and predictions
    response = requests.post('https://deeprhythm-2lapr5ij4q-od.a.run.app/upload', files=files)

    if response.status_code != 400:
        data = response.json()
        sub_cr = 'Cropped image'
        sub_gl = 'Grid removed image'
        title_cr = 'Image cropped from the .pdf'
        title_gl = 'Grid removed from the image to pass through the model'

        st.subheader(f"{title_cr}")
        image1_data = base64.b64decode(data['image'])
        image1 = Image.open(io.BytesIO(image1_data))
        st.image(image1, caption=f"{sub_cr}", use_column_width=True)

        st.subheader(f"{title_gl}")
        image2_data = base64.b64decode(data['image_nogrid'])
        image2 = Image.open(io.BytesIO(image2_data))
        st.image(image2, caption=f"{sub_gl}", use_column_width=True)

        st.success(f"Prediction: {data['prediction']}")

        # Streamlit app layout
        st.title("Health tips and recommendations")
        # Set up OpenAI API key
        openai.api_key = st.secrets["api"]


        # Function to generate GPT response
        def generate_response(prompt):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Specify the chat-based GPT model here
                messages=[{"role": "system", "content": "Prompt: " + prompt}],
                max_tokens=1000  # Adjust based on desired length of the response
            )
            return response.choices[0].message['content']

        # User input prompt
        prompt = f"My heart is classified with this rythm {data['prediction']}.I am a {gender} and I have {age} years old. Could you give me some basic health and lifestyle recommendations according to my characteristics?"
        # Generate GPT response
        response = generate_response(prompt)
        # Display response
        st.write("Take into consideration:")
        st.write(response)
    else:
        st.error("Failed to fetch images and prediction from API")
