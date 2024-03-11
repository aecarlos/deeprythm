from data.pdf_proc import crop_pdf, output_ecgs, convert_to_images, remove_grid
from data.params import smsng_crop_areas
from models.final_model import model_load_compile, predict


# Crop the Samsung ECG
output_ecgs('samsung_ecg.pdf', smsng_crop_areas)

# Convert the cropped PDFs to images
for i in range(3):
    convert_to_images(f'ecg{i + 1}.pdf', f'ecg{i + 1}.jpg')

# Remove the gridlines from the images
for i in range(3):
    remove_grid(f'ecg{i + 1}.jpg', f'ecg{i + 1}_no_grid.jpg')


# Load the model
#model_load_compile('base_model_backup.h5')

# Make predictions
#predict(model, 'ecg1_no_grid.jpg')
