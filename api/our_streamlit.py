import streamlit as st
from PIL import Image
import requests
import io
import openai
import base64

excluded_classes = [
    "Sinus Bradycardia",
    "Sinus Rhythm",
    "Sinus Tachycardia",
    "Sinus Irregularity",
    "Sinus Atrium to Atrial Wandering Rhythm",
    "Atrial Tachycardia"
]


# Configurar la página
st.set_page_config(layout="wide", page_title="ElectroCardiogram Classifier")

# Título principal y texto introductorio
st.title("Classify your ECG 🫀🧑🏼‍⚕️")
st.write("<br>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)
st.write(":dog: Try uploading an ElectroCardiogram PDF. This code is open source and available [here](https://github.com/ivanmarim/deeprythm) on GitHub")
st.write('Special thanks to the [Physionet Dataset](https://physionet.org/content/ptb-xl/1.0.3/) :grin:')
st.write("*This app takes into consideration only the II-Lead. This app is for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis or treatment. For any medical questions, please consult a medical professional.")
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
ecg_path = st.sidebar.file_uploader("Upload an ECG", type=["jpeg", "jpg", 'png'])

data_r = None
if pdf_path is not None:
    # Read the contents of the uploaded file
    pdf_data = pdf_path.read()

    # Create a file-like object from the bytes data
    pdf_file = io.BytesIO(pdf_data)

    # Create a dictionary containing the file to be uploaded
    files = {'file': pdf_file}

    data = {'device': watch}

    # Upload the PDF and get a response with images and predictions
    response = requests.post('https://deeprhythm-2lapr5ij4q-od.a.run.app/upload', data = data, files=files)
    if response.status_code != 400:
        data_r = response.json()
        sub_cr = 'Cropped image'
        sub_gl = 'Real-time Cardiac Analysis: ECG Visualization from Smartwatch Data'
        title_cr = 'Image cropped from the .pdf'
        title_gl = 'Real-time Cardiac Analysis: ECG Visualization from Smartwatch Data'

        #st.subheader(f"{title_cr}")
        #image1_data = base64.b64decode(data_r['image'])
        #image1 = Image.open(io.BytesIO(image1_data))
        #st.image(image1, caption=f"{sub_cr}", use_column_width=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.markdown(f"#### {title_gl}")
        image2_data = base64.b64decode(data_r['image_nogrid'])
        image2 = Image.open(io.BytesIO(image2_data))
        st.image(image2, caption=f"{sub_gl}", use_column_width=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.markdown(f"## Your Deeprhythm: ")
        if data_r['prediction'] not in excluded_classes:
            st.markdown(f"## ❤️‍🩹🩺 {data_r['prediction']} 🩺❤️‍🩹")
        else:
            st.markdown(f"## ❤️🩺 {data_r['prediction']} 🩺❤️")
        # Streamlit app layout
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.subheader("General Health Insights and Suggestions:")
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
        #prompt = f"My heart is classified with this rythm {data_r['prediction']}.I am a {gender}, I have {age} years old and my weight is {weight}. Could you give me some basic health and lifestyle recommendations specific and really related to my characteristics? And can you send me those in Streamlit Markdown format with font size of 18 so it is shown fancy in my streamlit app."
        prompt = f"My heart is classified with the following rhythm: **{data_r['prediction']}**. I am a {gender} of {age} years old, weighing {weight} kilograms and with height {height}. Could you please provide me with personalized health and lifestyle recommendations based on my characteristics? It would be great if you could format the recommendations using Streamlit Markdown for an elegant display in my Streamlit app."
        # Generate GPT response
        response = generate_response(prompt)
        # Display response
        st.markdown(response)
    else:
        st.error("Failed to fetch images and prediction from API")

if ecg_path is not None:
    # Read the contents of the uploaded file
    ecg_data = ecg_path.read()

    # Create a file-like object from the bytes data
    ecg_file = io.BytesIO(ecg_data)

    # Create a dictionary containing the file to be uploaded
    files = {'file': ecg_file}

    # Upload the ECG and get a response with images and predictions
    response = requests.post('https://deeprhythm-2lapr5ij4q-od.a.run.app/uploadecg', files=files)
    if response.status_code != 400:
        data_r = response.json()
        sub_gl = 'Cardiac Rhythm Visualization: An ECG Snapshot'
        title_cr = 'Image cropped from the .pdf'
        title_gl = 'Cardiac Rhythm Visualization: An ECG Snapshot'

        st.subheader(f"{title_gl}")
        image2_data = base64.b64decode(data_r['image'])
        image2 = Image.open(io.BytesIO(image2_data))
        st.image(image2, caption=f"{sub_gl}", use_column_width=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.markdown(f"## Your Deeprhythm: ")
        if data_r['prediction'] not in excluded_classes:
            st.markdown(f"## ❤️‍🩹🩺 {data_r['prediction']} 🩺❤️‍🩹")
        else:
            st.markdown(f"## ❤️🩺 {data_r['prediction']} 🩺❤️")
        # Streamlit app layout
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)

        # Streamlit app layout
        st.title("General Health Insights and Suggestions")
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
        # User input prompt
        #prompt = f"My heart is classified with this rythm {data_r['prediction']}.I am a {gender}, I have {age} years old and my weight is {weight}. Could you give me some basic health and lifestyle recommendations specific and really related to my characteristics? And can you send me those in Streamlit Markdown format with font size of 18 so it is shown fancy in my streamlit app."
        prompt = f"My heart is classified with the following rhythm: **{data_r['prediction']}**. I am a {gender} of {age} years old, weighing {weight} kilograms and with height {height}. Could you please provide me with personalized health and lifestyle recommendations based on my characteristics? It would be great if you could format the recommendations using Streamlit Markdown for an elegant display in my Streamlit app."
        # Generate GPT response
        response = generate_response(prompt)
        # Display response
        st.markdown(response)
    else:
        st.error("Failed to fetch images and prediction from API")
