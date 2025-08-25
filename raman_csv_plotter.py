import numpy as np
import json
import os

# #/#/# Section One #/#/#

# Define the file directory HERE:
fileDir = r'C:\Users\mrmel\Desktop\Honours\data\7AugWS2WL'  # Example directory for Raman data files

'''Functions bundle code into discrete wrappers we can use again and again easily. They look like this:'''

def open_raman_csv(path):
    '''Open a Raman CSV file and return the data array and metadata. Designed for use with Raman spectroscopy data.
    
    Our Raman data is a more complex than just a simple CSV file. It has complex metadata that stores the state of the machine, type of scan, scan attributes, and the calibrated wavelength. We need to preserve this metadata when we load the data, so we can use it later for processing and analysis.
    
    Consequently, we need a special function to open the CSV file and extract the metadata and data array. The metadata is stored in the first few lines of the file, starting with a '#' character, and the data is stored in the remaining lines. We will parse this file to extract both the metadata and the data array.'''

    metadata = {}
    data_lines = []

    with open(path) as f:
        for line in f:
            if line.startswith('#'):
                key, json_str = line[2:].split(':', 1)
                metadata[key.strip()] = json.loads(json_str.strip())
            else:
                data = line.strip()
                data = data.split(',')
                data_lines.append(data)

    filename = os.path.basename(path)
    metadata['filename'] = filename  # Add the filename to the metadata for convenience later

    data_array = np.array(data_lines).astype(float)  # Convert the list of data lines to a NumPy array of floats. We need to convert the data to floats so we can do math on it later, and plot it.

    return data_array, metadata

''' They are defined with the keyword 'def', followed by the function name, and then the parameters in parentheses. The code inside the function is indented. When you call the function "function_name(...)", it will execute the code inside the function. You can pass arguments to the function by putting them in the parentheses when you call it.'''

'''We need to specify a directory to load the data from. We can do this one file at a time, or we can load all the files in a directory. Here we will load all the files in a directory. We can use the os module to list the files in a directory.'''

# Example directory containing Raman CSV files
# fileDir is defined above, so we can use it directly.
all_files = [f for f in os.listdir(fileDir) if f.endswith('.csv')] # make a list of all CSV files in the directory

data_list = [] # make an empty list to hold the data arrays and metadata
for file in all_files: # loop through each file in the directory
    file_path = os.path.join(fileDir, file) # make the filename for the file by joining the directory and the file name
    data_array, metadata = open_raman_csv(file_path) # open the file and get the data array and metadata
    data_list.append((data_array, metadata)) # append the data array and metadata to the list

print(f"Loaded {len(data_list)} files from {fileDir}")  # Print the number of files loaded and from where
print("Example data array and metadata from the first file:")
print('--> Data:')
print(data_list[0][0])  # Print the data array of the first file
print('------> Metadata:')
print(data_list[0][1])  # Print the metadata of the first file

# input("Press Enter to continue to Section Two...")  # Wait for user input before proceeding

# #/#/# Section Two #/#/#

'''Now we have a list of tuples, where each tuple contains a data array and metadata for that file. We can process this data as needed. For example, we can plot the data, export it to a different format, or perform some analysis on it.'''
import matplotlib.pyplot as plt

def plot_data(data_array, metadata):
    '''Plot the Raman data array. This is a simple example of how to visualize the data. You can customize this function to suit your needs.'''

    dataX = data_array[:, 0] # indexing starts at 0.  "[0:"  means we take all rows except the first one, and ", :0]" means the first column. So this will take all rows and the first column as the x-axis data.
    dataY = data_array[:, 1]  # take all rows and the second column as the y-axis data
    filename = metadata.get('filename', 'Raman Spectrum') # we can get the filename from the metadata, or use a default value if it is not present
    plt.plot(dataX, dataY, label=filename)

    plt.title('Raman Spectroscopy Data')
    plt.xlabel('Wavenumber (cm⁻¹)')
    plt.ylabel('Intensity (a.u.)')
    plt.legend() # need to add a legend to the plot
    plt.show()

# plot_data(data_list[1][0], data_list[1][1])  # Plot the second data array as an example (note the first is index 0, so we use index 1 to plot the second one)

'''and we can loop through the data_list to plot each data array.'''

def plot_all_data(data_list):

    for data_array, metadata in data_list:
        dataX = data_array[:, 0]
        dataY = data_array[:, 1]
        filename = metadata.get('filename', 'Raman Spectrum')  # Get the filename from metadata or use a default
        plt.plot(dataX, dataY, label=filename)

        plt.title('Raman Spectroscopy Data')
        plt.xlabel('Wavenumber (cm⁻¹)')
        plt.ylabel('Intensity (a.u.)')
        plt.legend()

    # drop the show function outside the loop to let all plots add to the same figure
    plt.show()

# plot_all_data(data_list)  # Plot all data arrays in the list

# input("Press Enter to continue to Section Three...")  # Wait for user input before proceeding

# #/#/# Section Three #/#/#

'''We can bundle these functions into a simple class to handle the dataset more cleanly.
A class is a blueprint for creating a thing that we can use to hold, manipulate, and process data. Think of it like a template for a car. We can put our bags in the trunk (metadata), and our data in the passenger seats (data_array). We can can then drive the car (process the data) and take the data out at those places (view/export the data).

Classes can be complex, but for now we'll keep it simple. We will create a class called RamanDataSet that will hold the data and metadata, and provide methods to load, process, and plot the data.'''

class RamanDataSet:
    def __init__(self, data_dir):
        '''All classes have an __init__ method that is called when the class is created. This is where we can set up the initial state of the class. Here we are setting the data_dir and initializing an empty list to hold the data arrays and metadata.'''
        self.data_dir = data_dir
        self.data_list = []  # List to hold tuples of (data_array, metadata)

    def load_data(self):
        '''Load all CSV files from the data directory.'''
        all_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
        for file in all_files:
            file_path = os.path.join(self.data_dir, file)
            data_array, metadata = open_raman_csv(file_path)
            self.data_list.append((data_array, metadata))

    def process_data(self):
        '''We can process the data in various ways.'''
        pass

    def process_flakescan(self):
        '''Asks for a Raman shift range, reads all csv to find intensities in that range, records and plots average intensity'''
        while True:
            try:
                shift_min = float(input("Enter the minimum Raman shift (cm⁻¹): "))
                shift_max = float(input("Enter the maximum Raman shift (cm⁻¹): "))
                if shift_min < shift_max and -100 <= shift_min <= 1327 and -100 <= shift_max <= 1327:
                    break
                else:
                    print("Please enter a valid range between -100 and 1327 cm⁻¹ (min < max).")
            except ValueError:
                print("Invalid input. Please enter numbers.")

        results = []
        for data_array, metadata in self.data_list:
            shifts = data_array[:, 0]
            mask = (shifts >= shift_min) & (shifts <= shift_max)
            intensities_in_range = data_array[mask, 1]
            if intensities_in_range.size > 0:
                avg_intensity = np.mean(intensities_in_range)
            else:
                avg_intensity = np.nan  # or 0, depending on your preference
            results.append((metadata['filename'], avg_intensity))
            print(f"{metadata['filename']}: Avg Intensity = {avg_intensity} a.u. in range {shift_min}-{shift_max} cm⁻¹")

        filenames = [r[0] for r in results]
        avg_intensities = [r[1] for r in results]
        plt.figure()
        plt.plot(filenames, avg_intensities)
        plt.xlabel('File')
        plt.ylabel(f'Average Intensity ({shift_min}-{shift_max} cm⁻¹)')
        plt.title('Flake Scan Average Intensities')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def plot_all_data(self):
        '''Plot all data arrays in the dataset.'''

        for data_array, metadata in self.data_list:
            dataX = data_array[:, 0]
            dataY = data_array[:, 1]
            filename = metadata.get('filename', 'Raman Spectrum')
            plt.plot(dataX, dataY, label=filename)
        plt.title('Raman Spectroscopy Data')
        plt.xlabel('Wavenumber (cm⁻¹)')
        plt.ylabel('Intensity (a.u.)')
        plt.legend()
        plt.show()

    def plot_data(self, index=1):
        '''Plot a single data array by index.'''

        if index < len(self.data_list):
            data_array, metadata = self.data_list[index]
            dataX = data_array[:, 0]
            dataY = data_array[:, 1]
            filename = metadata.get('filename', 'Raman Spectrum')
            plt.plot(dataX, dataY, label=filename)
            plt.title('Raman Spectroscopy Data')
            plt.xlabel('Wavenumber (cm⁻¹)')
            plt.ylabel('Intensity (a.u.)')
            plt.legend()
            plt.show()


'''Now to do the data processing, we can create an instance of the RamanDataSet class, load the data, and plot it.'''

fileDir = r'C:\Users\mrmel\Desktop\Honours\data\15AugWS2Defect'  # Example directory for Raman data files
raman_dataset = RamanDataSet(fileDir)
'''We call specific functions in the RamanDataSet class to load and plot the data using the .function_name() syntax.'''
raman_dataset.load_data()
raman_dataset.process_data()  # Placeholder for any processing we might want to do
# raman_dataset.process_flakescan()  # Process a flake scan based on user input
raman_dataset.plot_all_data()
raman_dataset.plot_data()

print("Data loaded and plotted successfully.")