#to combine all targets into a single dat file of hits for plotting purposes

import pandas as pd
import os

# ColumnNames seems unnecessary, but will leave it in.
ColumnNames = ["HitNum", "Drift_Rate", "SNR", "Uncorrected_Frequency", "Corrected_Frequency", "Index",
    "freq_start", "freq_end", "SEFD", "SEFD_freq", "Coarse_Channel_Number" , "Full_number_of_hits"]

# Open the file list and make it into an array
full_files = open('full_files.lst', 'r')
files_array = full_files.read().splitlines()

# Name the output file
output_file = './all_hits_full.dat'

# Read the first .dat file in order to preserve the headers
original_hits_df = pd.read_csv(files_array[0], skipinitialspace=True)

# This for loop adds the extra .dat files onto the first one while skipping the headers
for file in files_array[1:]:
        addendum_hits_df = pd.read_csv(file.strip(), skiprows=8, skipinitialspace=True)
        frames = [original_hits_df, addendum_hits_df]

        # This next line forces the columns to match or else you get weird delimiter issues
        addendum_hits_df.columns = original_hits_df.columns

        # This line adds each .dat file onto the last
        original_hits_df = pd.concat(frames, ignore_index=True)
        print("original file name = " + file)

original_hits_df.to_csv(output_file)
print("Merge Complete")
