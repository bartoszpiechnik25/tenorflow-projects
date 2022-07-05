import zipfile
import os
import sys
from PIL import Image
from random import sample
import matplotlib.pyplot as plt
import random
from shutil import move

def unzip_data(archive_path, unzip_path, delete_archive=False):
    """
    Unzip file to specified location

    Args:
      archive_path (string): archive location containing .zip name
      unzip_path (string): directory path to be used for unzipping files
      delete_archive (bool): wether .zip file will be delteted or not

    Returns:
      None 
    """
    #Check whether specified unzip path exists
    if not os.path.isdir(unzip_path):
        print(f"Specified path {unzip_path} does not exists so creating.")
        os.makedirs(unzip_path)
    
    #Check wether if specified zip path is a file
    if not os.path.isfile(archive_path):
        print(f"{os.path.basename(archive_path)} is not a file.")
        sys.exit()        

    #Load zip file and set for read
    zip_reference = zipfile.ZipFile(archive_path, 'r')

    #Unzip files to specified location
    zip_reference.extractall(unzip_path)
    zip_reference.close()

    if delete_archive:
        os.remove(archive_path)



def data_counter(path, name):
    """
    Counts images in each directory

    Args:
      path (string): directory path containing images
      name (string): name of specified directory to be printed
      
    Returns:
      Dictionary: containing directory names as keys and number of
      files in directory as values.
    """
    directory = os.listdir(path)
    values = {directory[i]: 0 for i in range(len(directory))}
    for folder in directory:
        folder_path = os.path.join(path, folder)
        for img in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img)
            if os.path.getsize(img_path) == 0:
                os.remove(img_path)
            else:
                values[folder] += 1

    print(f"Number of files in {name} is {sum(values.values())}")
    return values


def print_size(dir):
    """
    Print size of random image from each directory

    Args:
      dir (string): directory path containing images
    
    Returns:
      None
    """
    for directory in os.listdir(dir):
        directory_path = os.path.join(dir, directory)
        image_p = sample(os.listdir(directory_path), 1)[0]
        image = Image.open(os.path.join(directory_path, image_p))
        print(f"Random image size from {directory} directory is: {image.size, image.mode}")


def split_test_val(test_path, validation_path, split_size):
    """
    Split test set to train/validation set with specified size

    Args:
      test_path (string): directory path containing test samples
      validation_path (string): path to be validation directory
      split_size (float): portion of the dataset to be used for validation

    Returns:
      None
    """
    test_dirs = os.listdir(test_path)
    
    for dir in test_dirs:
        path = os.path.join(test_path, dir)
        samples_test = os.listdir(path)
        num_samples = int(len(samples_test) * split_size)
        shuffled_dir = random.sample(samples_test, len(samples_test))

        validation_dir = os.path.join(validation_path, dir)
        os.makedirs(validation_dir)
        for img in shuffled_dir[:num_samples]:
            img_path = os.path.join(path, img)
            img_val_path = os.path.join(validation_dir, img)
            move(img_path, img_val_path)


def plot_learning(model, train_param, val_param, xtitle, ytitle, plot_title, label_1, label_2):
    plt.figure(dpi=80, figsize=(10,6))
    plt.plot(model.history[train_param],
            label=label_1,
            color='darkorange')
    plt.plot(model.history[val_param],
            label=label_2,
            color='skyblue')
    plt.legend()
    plt.title(plot_title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)