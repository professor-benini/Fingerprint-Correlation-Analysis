import shutil
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def open_image_to_matrix(image_path):
    try:
        with open(image_path) as f:
            image = plt.imread(image_path)
    except FileNotFoundError:
        print("The following file does not exist: " + image_path)
        image = np.zeros((356, 328), dtype=np.uint8)
    return image

def cross_correlation(img1,img2):
    # Applying the shift to centralize the zero frequency
    img1_fft = np.fft.ifft2(img1)
    img1 = img1_fft/np.abs(img1_fft)
    img1_fft = np.fft.fftshift(img1)
    img2_fft = np.fft.ifft2(img2)
    img2 = img2_fft/np.abs(img2_fft)
    img2_fft = np.fft.fftshift(img2)

    # Performing the cross-correlation in the frequency spectrum
    correlation = np.fft.ifftshift(np.fft.ifft2(img1_fft * np.conj(img2_fft)))
    correlation = np.abs(correlation)
    return correlation

def get_central_region(matrix):
    row_sums = np.sum(matrix, axis=1)
    col_sums = np.sum(matrix, axis=0)
    max_row_index = np.argmin(row_sums)
    max_col_index = np.argmin(col_sums)

    row_mean = int(np.mean(max_row_index))
    col_mean = int(np.mean(max_col_index))
    center_row = min(max(int(row_mean), 128), 227)
    center_col = min(max(int(col_mean), 128), 200)
    center_col = 164

    start_row = center_row - 128
    end_row = center_row + 128
    start_col = center_col - 128
    end_col = center_col + 128
    
    return matrix[start_row:end_row, start_col:end_col]

def threshold_min(matrix):
    threshold_value = 120
    new_matrix = np.where(matrix >= threshold_value, 255, matrix)
    new_matrix = new_matrix.astype(np.uint8)
    return new_matrix

# create directories variable
BASE_DIR = "<path_to_base_directory>" # where is CASIA-FingerprintV5 database directory. ex.: os.path.join('G:\\Meu Drive', 'IFSP', 'Pesquisa e Extensão', 'Iniciação Científica', 'SEAID')
DESTINE_DIR = "<path_to_target_subdirectory>" # where data base subdirectory will be constructed. ex.: os.path.join('C:\\Users', 'IFSP', 'OneDrive - ifsp.edu.br', 'Fingerprint-Correlation-Analysis')
DATA_DIR = "<path_to_fingerprint_base_data>"   # CASIA-FingerprintV5 database. ex.: 'Amostras Impressão Digital'
TARGET_DIR = "<path_to_selected_fingerprint_base_directory>"  # selected fingerprint base directory. ex.: 'selected samples'
SUB_DIR = ['L', 'R']  # Left and Right directory
MAX_DIR = 500  # Number max + 1 of directories fingerprint (usually 499)
correlationCoefficient = 0.07
NUMBER_MATCH = 10
target_dir_path = os.path.join(DESTINE_DIR, TARGET_DIR)
data_dir_path = os.path.join(BASE_DIR, DATA_DIR)
os.chdir(target_dir_path)
##number_dir = 323
while (correlationCoefficient > 0):
    number_dir = 0  # Current directory number
    while (number_dir < MAX_DIR):
        person_number = str(number_dir).zfill(3)
        person_dir = os.path.join(data_dir_path, person_number)
        for side_dir in SUB_DIR:
            side_finger_dir = os.path.join(person_dir, side_dir)
            for finger in range(4):
                count_match = 0
                set_finger = str(finger)
                for set1_5 in range(4):
                    if count_match == -1:
                        break
                    fingerprint_file1 = person_number + "_" + side_dir + set_finger + "_" + str(set1_5) + ".bmp"
                    fingerprint1 = get_central_region(threshold_min(open_image_to_matrix(os.path.join(side_finger_dir, fingerprint_file1))))
                    for set2_5 in range(set1_5 + 1, 5):
                        fingerprint_file2 = person_number + "_" + side_dir + set_finger + "_" + str(set2_5) + ".bmp"
                        fingerprint2 = get_central_region(threshold_min(open_image_to_matrix(os.path.join(side_finger_dir, fingerprint_file2))))
                        correlation = cross_correlation(fingerprint1, fingerprint2)
                        if correlation.max() > correlationCoefficient:
                            count_match = count_match + 1
                        else:
                            count_match = -1
                            break
                if count_match == NUMBER_MATCH:
                    destination_dir = os.path.join(DESTINE_DIR, TARGET_DIR, str(int(correlationCoefficient * 1000)).zfill(3))
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir)
                    for set1_5 in range(5):
                        fingerprint_file1 = person_number + "_" + side_dir + set_finger + "_" + str(set1_5) + ".bmp"
                        destination_dir = os.path.join(DESTINE_DIR, TARGET_DIR, str(int(correlationCoefficient * 1000)).zfill(3), fingerprint_file1)
                        fingerprint1 = get_central_region(threshold_min(open_image_to_matrix(os.path.join(side_finger_dir, fingerprint_file1))))
                        imagem = Image.fromarray(fingerprint1, mode="L")
                        imagem.save(destination_dir)
                        print(destination_dir)

        print("correlation coefficient " + str(correlationCoefficient) + " - directory " + str(number_dir))
        number_dir = number_dir + 1
    correlationCoefficient = correlationCoefficient - 0.01
