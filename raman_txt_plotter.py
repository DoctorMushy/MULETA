import numpy as np
import json
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# #/#/# Section One #/#/#

# Define the file directory HERE:
fileDir = r'C:\Users\mrmel\Desktop\Honours\data\MoS2' 
''  # Example directory for Raman data files

def open_raman_txt(path):
    """
    Reads a Raman .txt file where:
    - Line 1: Raman shifts (tab-separated)
    - Line 2: scan index, (possibly something else), then intensities (tab-separated, columns 3+)
    Returns a 2D numpy array: [[raman_shift, intensity], ...] for the first scan.
    """
    with open(path) as f:
        lines = [line.strip() for line in f if line.strip()]
        # Get Raman shifts from line 1
        raman_shifts = [float(val) for val in lines[0].split('\t')]
        # Get first set of intensities from line 2, columns 3+
        first_intensity_line = lines[1].split('\t')
        intensities = [float(val) for val in first_intensity_line[2:]]
        # Pair up as many as possible
        n = min(len(raman_shifts), len(intensities))
        data = np.column_stack((raman_shifts[:n], intensities[:n]))
        return data

def extract_all_scans(path):
    """
    Returns a list of (raman_shifts, intensities) for all scans in the file.
    """
    with open(path) as f:
        lines = [line.strip() for line in f if line.strip()]
        raman_shifts = [float(val) for val in lines[0].split('\t')]
        scans = []
        for line in lines[1:]:
            parts = line.split('\t')
            if len(parts) < 3:
                continue
            intensities = [float(val) for val in parts[2:]]
            n = min(len(raman_shifts), len(intensities))
            scans.append((raman_shifts[:n], intensities[:n]))
        return scans

# Load all .txt files in the directory
all_files = [f for f in os.listdir(fileDir) if f.endswith('.txt')]
data_list = []
for file in all_files:
    file_path = os.path.join(fileDir, file)
    data_array = open_raman_txt(file_path)
    metadata = {'filename': file}
    data_list.append((data_array, metadata))
    # --- Extract and print scan index from line 2, column 1 ---
    with open(file_path) as f:
        lines = [line.strip() for line in f if line.strip()]
        if len(lines) > 1:
            scan_index = lines[1].split('\t')[0]
            print(f"{file} scan index: {scan_index}")

print(f"Loaded {len(data_list)} files from {fileDir}")
if data_list:
    print("Example data array and metadata from the first file:")
    print('--> Data:')
    print(data_list[0][0])
    print('------> Metadata:')
    print(data_list[0][1])
else:
    print("No .txt files found in the directory.")

if data_list:
    # Use the first file as an example
    data_array, metadata = data_list[0]
    raman_shifts = data_array[:, 0]
    first_intensities = data_array[:, 1]

    plt.figure()
    plt.plot(raman_shifts, first_intensities, label=metadata['filename'])
    plt.xlabel('Raman Shift')
    plt.ylabel('Intensity (first column)')
    plt.title(f"Raman Spectrum: {metadata['filename']}")
    plt.legend()
    plt.show()
else:
    print("No .txt files found in the directory.")

if data_list:
    # Use the first file as an example
    file_path = os.path.join(fileDir, data_list[0][1]['filename'])
    scans = extract_all_scans(file_path)
    raman_shifts = scans[0][0]  # x-axis is always the same

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    line, = ax.plot(raman_shifts, scans[0][1], label=f"Scan 1")
    ax.set_xlabel('Raman Shift')
    ax.set_ylabel('Intensity')
    ax.set_title(f"Raman Spectrum: {data_list[0][1]['filename']}")
    ax.legend()

    ax_slider = plt.axes([0.15, 0.1, 0.7, 0.03])
    slider = Slider(
        ax=ax_slider,
        label='Scan Index',
        valmin=1,
        valmax=len(scans),
        valinit=1,
        valstep=1,
        valfmt='%0.0f'
    )

    def update(val):
        idx = int(slider.val) - 1
        line.set_ydata(scans[idx][1])
        line.set_label(f"Scan {idx+1}")
        ax.legend()
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()
else:
    print("No .txt files found in the directory.")

def average_region_and_plot(scans):
    """
    Prompts the user for a Raman shift region, averages intensity in that region for each scan,
    and plots average intensity vs scan index.
    """
    try:
        region_min = float(input("Enter minimum Raman shift for averaging: "))
        region_max = float(input("Enter maximum Raman shift for averaging: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    avg_intensities = []
    scan_indices = []

    for idx, (raman_shifts, intensities) in enumerate(scans):
        # Find indices within the region
        region_mask = [(region_min <= shift <= region_max) for shift in raman_shifts]
        region_intensities = [i for i, m in zip(intensities, region_mask) if m]
        if region_intensities:
            avg_intensity = np.mean(region_intensities)
        else:
            avg_intensity = np.nan  # No data in region
        avg_intensities.append(avg_intensity)
        scan_indices.append(idx + 1)

    plt.figure()
    plt.plot(scan_indices, avg_intensities, marker='o')
    plt.xlabel('Scan Index')
    plt.ylabel(f'Average Intensity ({region_min}-{region_max} cm⁻¹)')
    plt.title('Average Intensity vs Scan Index')
    plt.show()

# --- To use this function, call it after extracting scans, e.g.: ---
if data_list:
    file_path = os.path.join(fileDir, data_list[0][1]['filename'])
    scans = extract_all_scans(file_path)
    user_choice = input("Would you like to average a region and plot average intensity vs scan index? (y/n): ")
    if user_choice.lower().startswith('y'):
        average_region_and_plot(scans)
