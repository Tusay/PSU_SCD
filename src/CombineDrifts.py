#for future reference

import pandas as pd

ColumnNames = ["HitNum", "Drift_Rate", "SNR", "Uncorrected_Frequency", "Corrected_Frequency", "Index",
    "freq_start", "freq_end", "SEFD", "SEFD_freq", "Coarse_Channel_Number" , "Full_number_of_hits"]
drift_array = [0.15, 0.3, 0.6, 1.2, 2.4, 4.8, 9.6, 19.2, 38.4, 76.8, 153.6, 307.2, 614.4]
prefixes = open('prefixes.lst', 'r')
prefix_array = prefixes.readlines()

for prefix in prefix_array:
        output_file = '/datax/scratch/ssheikh/SCD/turboseti/trimmed_hit_lists/all_drifts/' + prefix.strip() + 'full.0000.dat'
        for i in range(0, len(drift_array) - 1):
                print(i)
                if i == 0:
                        file_name = '/datax/scratch/ssheikh/SCD/turboseti/trimmed_hit_lists/0.15/' + prefix.strip() + '0000.dat'
                        original_hits_df = pd.read_csv(file_name)
                else:
                        file_name = '/datax/scratch/ssheikh/SCD/turboseti/trimmed_hit_lists/' + str(drift_array[i]) + '/' + prefix.strip() + '0000.s' + str(i) + '.dat' 
                        addendum_hits_df = pd.read_csv(file_name)
                        frames = [original_hits_df, addendum_hits_df]
                        original_hits_df = pd.concat(frames)
                print("original file name = " + file_name)
        original_hits_df.to_csv(output_file)
        print("Finished running file = " + output_file)
