import os
import numpy as np
import matplotlib.pyplot as plt
import csv

def cross_correlation(img1,img2):
    # Applying the shift to center the zero frequency
    img1_fft = np.fft.ifft2(img1)
    img1 = img1_fft/np.abs(img1_fft)
    img1_fft = np.fft.fftshift(img1)
    img2_fft = np.fft.ifft2(img2)
    img2 = img2_fft/np.abs(img2_fft)
    img2_fft = np.fft.fftshift(img2)

    # Performing cross-correlation on the frequency spectrum
    correlation = np.fft.ifftshift(np.fft.ifft2(img1_fft * np.conj(img2_fft)))
    correlation = np.abs(correlation)
    return correlation

def peak_percentages(correlation):
    # Flatten the correlation matrix and sort in descending order
    sorted_correlation = np.sort(correlation.flatten())[::-1]

    # Get the highest peak
    highest_peak = sorted_correlation[0]

    # Calculate the percentages of the second to sixth highest peaks relative to the highest peak
    percentages = [(sorted_correlation[i] / highest_peak) * 100 for i in range(1, 6)]

    return percentages

def open_image_to_matrix(image_path):
    try:
        with open(image_path) as f:
            image = plt.imread(image_path)
    except FileNotFoundError:
        print("The following file does not exist: " + image_path)
        image = np.zeros((356, 328), dtype=np.uint8)
    return image

threshold = 0.03
flag1 = 0
flag2 = 0
flag3 = 0
directory = os.path.join('C:\\Users', 'IFSP', 'OneDrive - ifsp.edu.br', 'Fingerprint-Correlation-Analysis', 'selected samples', str(int(threshold*1000)).zfill(3)) #"<path_to_selected_fingerprint_base_directory>"  # Replace with your selected fingerprint base directory. Ex.: 
filecsv = str(int(threshold*1000)).zfill(3)+' peaks.csv'

archives = os.listdir(directory)

# Open csv file in write mode
with open(filecsv, mode='a', newline='') as file:
    # Create a csv.writer object and set the delimiter to ','
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Write the file header
    writer.writerow(['fingerprint1', 'fingerprint2', 'correlation max', 'peak2', 'peak3', 'peak4', 'peak5', 'peak6', 'same'])
    for k, archive_ext in enumerate(archives):
        for archive_int in archives[k+1:]:
            flag = ''
            archive1 = os.path.join(directory,archive_ext)
            archive2 = os.path.join(directory,archive_int)
            fingerprint1 = ((open_image_to_matrix(archive1)))
            fingerprint2 = ((open_image_to_matrix(archive2)))
            correlation = cross_correlation(fingerprint1,fingerprint2)
            maxvalue = correlation.max()
            peaks = peak_percentages(correlation)
            if archive_ext[:7] == archive_int[:7]:
                flag = '1' # Positive
                flag1 = flag1 + 1
        
            # Create a csv.writer object and set the delimiter to ','
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Write the variables in the csv file
            writer.writerow([archive_ext, archive_int, maxvalue, peaks[0], peaks[1], peaks[2], peaks[3], peaks[4], flag])
