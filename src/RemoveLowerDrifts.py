import os
import numpy as np
import pandas as pd

try:
    ScriptDirectory = os.path.dirname(os.path.abspath(__file__))
except:
    ScriptDirectory = r"/home/shbhuk/PSU_SCD/src" # On the cluster
    # ScriptDirectory = r"C:\Users\shbhu\Documents\Git\PSU_SCD\src" # Local to SK's computer


# Folder where Data is stored
DataDirectory = r"/mnt_scratch/SCD/turboseti/hit_lists" # On the cluster
# DataDirectory = os.path.join(os.path.dirname(ScriptDirectory), 'OtherData', 'hit_lists')# Local to SK's computer

TrimmedDataDirectory = r"/mnt_scratch/SCD/turboseti/trimmed_hit_lists" # On the cluster
#TrimmedDataDirectory = os.path.join(os.path.dirname(ScriptDirectory), 'OtherData', 'trimmed_hit_lists')# Local to SK's computer
#TrimmedDataDirectory = r"/home/shbhuk/trimmed_hit_lists"

# Check which drift rates have been run in the data directory
# Save only those outputs that are directories
DriftRateRange = np.sort([float(f) for f in os.listdir(DataDirectory) if os.path.isdir(os.path.join(DataDirectory, f))])

ColumnNames = ["HitNum", "Drift_Rate", "SNR", "Uncorrected_Frequency", "Corrected_Frequency", "Index",
    "freq_start", "freq_end", "SEFD", "SEFD_freq", "Coarse_Channel_Number" , "Full_number_of_hits"]

for i, d in enumerate(DriftRateRange):
    HitListDirectory = os.path.join(DataDirectory, str(d))
    ListofHitFiles = np.array([f for f in os.listdir(HitListDirectory) if f[-4:]=='.dat'])

    if os.path.exists(os.path.join(TrimmedDataDirectory, str(d))):
        print("Trimmed directory already exists for drift = {} Hz/s".format(d))
    else:
        os.mkdir(os.path.join(TrimmedDataDirectory, str(d)))
        print("Trimmed directory created for drift = {} Hz/s".format(d))

    for j, fn in enumerate(ListofHitFiles):
        Hits_df = pd.read_csv(os.path.join(HitListDirectory, fn), delimiter="\t", skiprows=9)
        Hits_df = Hits_df.iloc[:,:-1]
        Hits_df.columns = ColumnNames

        DriftRateLowerBound = d/2
        Trimmed_df = Hits_df[np.abs(Hits_df.Drift_Rate) > DriftRateLowerBound]

        Trimmed_df.to_csv(os.path.join(TrimmedDataDirectory, str(d), fn))
        print("Finished running file = {} for drift rate = {} Hz/s".format(fn, d))
