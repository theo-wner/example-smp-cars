import matplotlib.pyplot as plt
import albumentations as albu
import os
import stat
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors

# Hilfsfunktion, die mehrere Bilder in einem Subplot darstellt
# visualize(image_1=img1, image2=img2) kann dann über key und value iterieren
def visualize(filename='test', **images):
    """PLot images in one row."""
    n = len(images)
    plt.figure(figsize=(16, 5))
    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(' '.join(name.split('_')).title())
        plt.imshow(image)
        plt.legend()

    # Bild in Unterverzeichnis Abbildungen speichern
    directory = './Abbildungen/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(os.path.join(directory, filename))

# Hilfsfunktion, die ein Paar aus Bild und Maske darstellt
def visualize_img_mask(image, mask, filename='test'):
    # Bild
    plt.figure(figsize=(16, 5))
    plt.subplot(1, 2, 1)
    plt.xticks([])
    plt.yticks([])
    plt.title('Bild')
    plt.imshow(image)

    # Maske
    plt.subplot(1, 2, 2)
    plt.xticks([])
    plt.yticks([])
    plt.title('Maske')
    # Labels und dazugehörige Farben als dictionary definieren
    labels_and_colors = {'sky' : 'lightblue', 
            'building' : 'lightyellow',
            'pole' : 'orange', 
            'road' : 'gray',
            'pavement' : 'lightgray',
            'tree' : 'green',
            'signsymbol' : 'black',
            'fence' : 'brown',
            'car' : 'blue',
            'pedestrian' : 'red', 
            'bicyclist' : 'purple',
            'unlabelled' : 'white'}
    # Eigene Colomap erstellen
    cmap = mcolors.ListedColormap(list(labels_and_colors.values()))

    plt.imshow(mask, cmap=cmap)

    # Legende erstellen
    legend_patches = [mpatches.Patch(color=color, label=label) for label, color in labels_and_colors.items()]
    plt.legend(handles=legend_patches, title='Classes', loc='upper left', bbox_to_anchor=(1.02, 1))
   
    # Bild in Unterverzeichnis Abbildungen speichern
    directory = './Abbildungen/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(os.path.join(directory, filename))

# Funktion, die eine Pipeline für die training augmentation bereitstellt
# (Mehrere zufällige Transformationen)
def get_training_augmentation():
    train_transform = [
        albu.HorizontalFlip(p=0.5),
        albu.ShiftScaleRotate(scale_limit=0.5, rotate_limit=0, shift_limit=0.1, p=1, border_mode=0),
        albu.PadIfNeeded(min_height=320, min_width=320, always_apply=True, border_mode=0),
        albu.RandomCrop(height=320, width=320, always_apply=True),
        albu.GaussNoise(p=0.2),
        albu.Perspective(p=0.5),
        albu.OneOf([albu.CLAHE(p=1), albu.RandomBrightnessContrast(p=1), albu.RandomGamma(p=1)], p=0.9),
        albu.OneOf([albu.Sharpen(p=1), albu.Blur(blur_limit=3, p=1), albu.MotionBlur(blur_limit=3, p=1)], p=0.9),
        albu.OneOf([albu.RandomBrightnessContrast(p=1), albu.HueSaturationValue(p=1)],p=0.9)
    ]
    return albu.Compose(train_transform)

# Funktion, die dasselbe für den Validierungdatensatz macht, aber hier sind die Trafos nicht 
# so wichtig. Es sollen nur alle Validierungsbilder auf dieselbe, durch 32 teilbare Größe gebracht werden
def get_validation_augmentation():
    test_transform = [
        albu.PadIfNeeded(384, 480)
    ]
    return albu.Compose(test_transform)

# Für einige Encoder müssen die Bilder vorverarbeitet werden, hierfür wird eine zum Encoder passende
# preprocesing function benötigt.
def get_preprocessing(preprocessing_fn):
    _transform = [
        albu.Lambda(image=preprocessing_fn),
        albu.Lambda(image=to_tensor, mask=to_tensor),
    ]
    return albu.Compose(_transform)

# Ehrlichgesagt keine Ahnung was hier passiert
def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype('float32')