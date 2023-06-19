import matplotlib.pyplot as plt
import albumentations as albu

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
    plt.savefig(filename)

# Funktion, die eine Pipeline für die training augmentation bereitstellt
# (Mehrere zufällige Transformationen)
def get_training_augmentation():
    train_transform = [
        albu.HorizontalFlip(p=0.5),
        albu.ShiftScaleRotate(scale_limit=0.5, rotate_limit=0, shift_limit=0.1, p=1, border_mode=0),
        albu.PadIfNeeded(min_height=320, min_width=320, always_apply=True, border_mode=0),
        albu.RandomCrop(height=320, width=320, always_apply=True),
        albu.IAAAdditiveGaussianNoise(p=0.2),
        albu.IAAPerspective(p=0.5),
        albu.OneOf([albu.CLAHE(p=1), albu.RandomBrightness(p=1), albu.RandomGamma(p=1)], p=0.9),
        albu.OneOf([albu.IAASharpen(p=1), albu.Blur(blur_limit=3, p=1), albu.MotionBlur(blur_limit=3, p=1)], p=0.9),
        albu.OneOf([albu.RandomContrast(p=1), albu.HueSaturationValue(p=1)],p=0.9)
    ]
    return albu.Compose(train_transform)