# Data credits and licences

This folder holds only the potato images of two public datasets, re-encoded for the CS 4140 demo.

## Lab photos: PlantVillage (potato classes)

* Source: https://github.com/spMohanty/PlantVillage-Dataset (folder `raw/color`, classes `Potato___Early_blight`, `Potato___Late_blight`, `Potato___healthy`) and its leaf-grouping metadata (`leaf_grouping/filtered_leafmaps`).
* Licence: CC BY-SA 3.0 (as listed on https://huggingface.co/datasets/mohanty/PlantVillage). Share-alike: redistributions of these images keep the same licence.
* Paper: Mohanty, S. P., Hughes, D. P., and Salathé, M. (2016). Using deep learning for image-based plant disease detection. *Frontiers in Plant Science* 7:1419. https://doi.org/10.3389/fpls.2016.01419
* Files were renamed `<class>_<number>.jpg`; `lab_index.csv` keeps the original file name and the leaf number (4 photos per leaf).

## Field photos: PlantDoc (potato classes)

* Source: https://github.com/pratikkayal/PlantDoc-Dataset (folders `Potato leaf early blight`, `Potato leaf late blight`, train and test).
* Licence: CC BY 4.0 (LICENSE.txt of the repository).
* Paper: Singh, D., Jain, N., Jain, P., Kayal, P., Kumawat, S., and Batra, N. (2020). PlantDoc: A Dataset for Visual Plant Disease Detection. CoDS-COMAD 2020.
* Images were resized so that their shorter side is 256 pixels; `field_index.csv` keeps the original path.
