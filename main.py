from data.pdf_proc import crop_pdf, output_ecgs, convert_to_images, remove_grid
from data.params import smsng_crop_areas
from models.final_model import model_load_compile
import tensorflow as tf
import os


# Crop the Samsung ECG
output_ecgs('samsung_ecg.pdf', smsng_crop_areas)

# Convert the cropped PDFs to images
for i in range(3):
    convert_to_images(f'ecg{i + 1}.pdf', f'ecg{i + 1}.jpg')

# Remove the gridlines from the imagesx
for i in range(3):
    remove_grid(f'ecg{i + 1}.jpg', f'ecg{i + 1}_no_grid.jpg')


# Load the model
model = model_load_compile('models/base_model_fulldata_2.h5')

for i in range(3):
    #Take one ecg picture to make a prediction
    img = tf.keras.preprocessing.image.load_img(f'ecg{i+1}_no_grid.jpg')

    # Resize the image to match the target shape
    new_height, new_width = 79, 622  # Specify the target height and width
    resized_img = tf.image.resize(img, (new_height, new_width))

    # Expand the dimensions to create a batch with a single image
    input_img = tf.expand_dims(resized_img/255, axis=0)

    # Make predictions
    predictions_list = model.predict(input_img).tolist()[0]
    print(predictions_list.index(max(predictions_list)))
