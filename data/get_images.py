import os
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
import pandas as pd

# Function to create folders and save images
def get_images_and_targets(df):
    parent_folder = 'class_pics'
    folder_names = df['Rhythm'].unique()
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    # Iterate through the list of names and create folders
    for name in folder_names:
        folder_path = os.path.join(parent_folder, name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{name}' created at '{folder_path}'")
        else:
            print(f"Folder '{name}' already exists at '{folder_path}'")

    # Save images to the folders
    X, y = [], []
    plt.figure(figsize=(80,10))
    for i in range(df.shape[0]):
        plt.clf()  # Clear the current figure
        plt.plot(df.iloc[i,1:5001])
        plt.axis('off')
        plt.savefig(f"class_pics/{df.loc[i,'Rhythm']}/tabpic{i}.jpg", bbox_inches='tight')  # Save as JPEG image with tight bounding box


def get_smote_images(df):
    '''The input has to be the combined.csv. This function will create a folder with subfolders for each class and save the images'''
    df.dropna(axis=0, inplace=True)

    X, y = df.iloc[:,1:5001], df.loc[:,'Rhythm']
    smote = SMOTE(sampling_strategy='not majority', k_neighbors=3, random_state=42)

    X_res, y_res = smote.fit_resample(X, y) # Resample the data

    parent_folder = 'smote_class_pics'
    folder_names = df['Rhythm'].unique()

    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    # Iterate through the list of names and create folders
    for name in folder_names:
        folder_path = os.path.join(parent_folder, name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{name}' created at '{folder_path}'")
        else:
            print(f"Folder '{name}' already exists at '{folder_path}'")

    plt.figure(figsize=(80,10))
    for i in range(X_res.shape[0]):
        plt.clf()  # Clear the current figure
        plt.plot(X_res.iloc[i,:])
        plt.axis('off')
        plt.savefig(f"smote_class_pics/{y_res[i]}/tabpic{i}.jpg", bbox_inches='tight')  # Save as JPEG image with tight bounding box
