# Fingerprint-Correlation-Analysis
Fingerprint-Correlation-Analysis: Python scripts for fingerprint analysis using CASIA Fingerprint Image Database V5.0. Includes preprocessing, resizing, thresholding, and cross-correlation evaluation with TNR, IRR, GAR, FNR, and FPR metrics.
This repository contains the code for fingerprint image preprocessing, which is an essential step in fingerprint correlation analysis using the CASIA-FingerprintV5 database.

## Description

The `fingerprint_image_processing.py` script is designed to perform several preprocessing tasks on fingerprint images, including resizing, thresholding, and noise reduction. These steps are necessary to ensure that the images are in a suitable format for further analysis and to improve the performance of the fingerprint correlation algorithm.

## Features

The script includes the following functions:

- `open_image_to_matrix`: Reads an image file from a given path and converts it into a NumPy array.
- `cross_correlation`: Calculates the cross-correlation between two images in the frequency domain using the Fast Fourier Transform (FFT).
- `get_central_region`: Identifies the region with the highest pixel density, which corresponds to the area where the fingerprint is concentrated. It then calculates the center of this region and crops the image to a fixed size of 256x256 pixels, centered around the calculated center.
- `threshold_min`: Applies a thresholding technique on the input image matrix to reduce noise by converting pixel values below a certain threshold to white (255).

## Usage

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Update the directory paths in the `fingerprint_image_processing.py` script, as mentioned below in the Configuration section.
4. Run the script by executing `python fingerprint_image_processing.py`.

## Configuration

Make sure to update the following variables in the script to match your folder structure and preferences:

- `BASE_DIR`: Path to the base directory where the CASIA-FingerprintV5 database is located.
- `DESTINE_DIR`: Path to the directory where the processed fingerprint image subdirectory will be constructed.
- `DATA_DIR`: Path to the CASIA-FingerprintV5 database directory.
- `TARGET_DIR`: Path to the directory where the selected fingerprint images will be saved.

Please ensure that the specified directories exist before running the script.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
