import tensorflow as tf
from keras.optimizers import Adam
import matplotlib.pyplot as plt

# Specify the path to your saved model file (replace 'your_model.h5' with the actual filename)
#model_path = './base_model_3.h5'

def model_load_compile(model_path):
    # Load the model from the .h5 file
    model = tf.keras.models.load_model(model_path)
    optimizer = Adam(learning_rate=0.001)  # Use the same learning rate as during training
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model


#model = model_load_compile(model_path)

#img = tf.keras.preprocessing.image.load_img('../ecg1.jpg')
#print(model.predict(plt.imread('../ecg1_no_grid.jpg')))
