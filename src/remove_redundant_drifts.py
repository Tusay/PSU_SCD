def read_dat(filename):
    """Read a turboseti .dat file
    Args:
      filename(str): Name of .dat file to open
    Returns:
        pandas dataframe of hits
    """

    file_dat = open(filename.strip())
    hits = file_dat.readlines()

    # Get info from the .dat file header
    FileID = hits[1].strip().split(':')[-1].strip()
    Source = hits[3].strip().split(':')[-1].strip()

    MJD = hits[4].strip().split('\t')[0].split(':')[-1].strip()
    RA = hits[4].strip().split('\t')[1].split(':')[-1].strip()
    DEC = hits[4].strip().split('\t')[2].split(':')[-1].strip()

    DELTAT = hits[5].strip().split('\t')[0].split(':')[-1].strip()  # s
    DELTAF = hits[5].strip().split('\t')[1].split(':')[-1].strip()  # Hz

    # Get info from individual hits (the body of the .dat file)
    all_hits = [hit.strip().split('\t') for hit in hits[9:]]

    # Now reorganize that info to be grouped by column (parameter)
    # not row (individual hit)
    if all_hits:
        TopHitNum = list(zip(*all_hits))[0]
        DriftRate = [float(df) for df in list(zip(*all_hits))[1]]
        SNR = [float(ss) for ss in list(zip(*all_hits))[2]]
        Freq = [float(ff) for ff in list(zip(*all_hits))[3]]
        ChanIndx = list(zip(*all_hits))[5]
        FreqStart = list(zip(*all_hits))[6]
        FreqEnd = list(zip(*all_hits))[7]
        CoarseChanNum = list(zip(*all_hits))[10]
        FullNumHitsInRange = list(zip(*all_hits))[11]

        data = {'TopHitNum': TopHitNum,
                'DriftRate': DriftRate,
                'SNR': SNR,
                'Freq': Freq,
                'ChanIndx': ChanIndx,
                'FreqStart': FreqStart,
                'FreqEnd': FreqEnd,
                'CoarseChanNum': CoarseChanNum,
                'FullNumHitsInRange': FullNumHitsInRange
                }

        # Creating pandas dataframe from data we just read in
        df_data = pd.DataFrame(data)
        df_data = df_data.apply(pd.to_numeric)

    else:
        df_data = pd.DataFrame()

    # Matching column information from before to the .dat data we read in
    df_data['FileID'] = FileID
    df_data['Source'] = Source.upper()
    df_data['MJD'] = MJD
    df_data['RA'] = RA
    df_data['DEC'] = DEC
    df_data['DELTAT'] = DELTAT
    df_data['DELTAF'] = DELTAF

    # Adding extra columns that will be filled out by this program
    df_data['Hit_ID'] = ''
    df_data['status'] = ''
    df_data['in_n_ons'] = ''
    df_data['RFI_in_range'] = ''

    return df_data
