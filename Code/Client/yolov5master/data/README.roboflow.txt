
<<<<<<< HEAD
NanoBug_Dataset - v2 2023-05-23 5:55pm
==============================

This dataset was exported via roboflow.com on May 23, 2023 at 3:57 PM GMT
=======
NanoBug_Dataset - v4 2023-05-23 8:21pm
==============================

This dataset was exported via roboflow.com on May 23, 2023 at 6:21 PM GMT
>>>>>>> 2eae211e76395baac8eaefa6a5f0fae5c9a585ce

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

<<<<<<< HEAD
The dataset includes 2400 images.
=======
The dataset includes 2260 images.
>>>>>>> 2eae211e76395baac8eaefa6a5f0fae5c9a585ce
Robot are annotated in YOLO v5 PyTorch format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 640x640 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* 50% probability of horizontal flip
* Random rotation of between -19 and +19 degrees
* Random shear of between -21° to +21° horizontally and -10° to +10° vertically
* Random brigthness adjustment of between -25 and +25 percent
* Random Gaussian blur of between 0 and 2.25 pixels


