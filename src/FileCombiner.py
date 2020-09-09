#to combine all targets into a single dat file of hits for plotting purposes

import pandas as pd

ColumnNames = ["HitNum", "Drift_Rate", "SNR", "Uncorrected_Frequency", "Corrected_Frequency", "Index",
    "freq_start", "freq_end", "SEFD", "SEFD_freq", "Coarse_Channel_Number" , "Full_number_of_hits"]
full_files = open('full_files.lst', 'r')
files_array = full_files.readlines()

output_file = '/datax/scratch/ssheikh/SCD/turboseti/trimmed_hit_lists/all_drifts/all_hits_full.dat'

original_hits_df = pd.read_csv(files_array[0].strip())

for file in files_array[1:]:
        addendum_hits_df = pd.read_csv(file.strip())
        frames = [original_hits_df, addendum_hits_df]
        original_hits_df = pd.concat(frames)
        print("original file name = " + file)

original_hits_df.to_csv(output_file)
print("Merge Complete")
