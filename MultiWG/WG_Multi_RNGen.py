from MultiWG.WG_Multi_HisAnalysis import GenMultiRN, GenSimrV2UCurve
from MultiWG.WG_General import ToPickle
from tqdm import tqdm
import numpy as np
import pandas as pd

# TX Rn might encounter problem.
def MultiGenRn(Setting, Stat):
    """Generate spatial correlated random number for weather generation.

    Args:
        Stat (dict): Stat dictionary.
        Setting (dict): Setting dictionary.

    Returns:
        dict: Stat
    """
    MultiSiteDict = Stat["MultiSiteDict"]
    # Add prep event variable
    Var = Setting["Var"].copy() + ["P_Occurrence"] 
    GenYear = Setting["GenYear"]
    LeapYear = Setting["LeapYear"]
    Stns = Setting["StnID"] 
    DayInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    DayInMonthLeap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    Simr = MultiSiteDict["Simr"]
    V2UCurve = MultiSiteDict["V2UCurve"]
    # When MultiSiteDict (Stat) is loaded from out source since 
    # functions cannot be saved as pickle
    if type(V2UCurve) == str:  
        MultiSiteDict = GenSimrV2UCurve(MultiSiteDict, Setting)  
        Stat["MultiSiteDict"] = MultiSiteDict
        V2UCurve = MultiSiteDict["V2UCurve"]
    SpatialRnNum = {}
    
    if LeapYear: 
        if GenYear%4 != 0:
            print("GenYear has to be the multiple of 4 to generate leap year.")
            input()
            quit()
    
    # Simulate spatial correlated RN
    for v in tqdm(Var, desc = "Gen spatial correlated RN"):        
        # Gen 40 years for the size is greater than 1000 for each month,
        # which we consider as statistically robust
        Rn = 0
        for y in range(GenYear):
            dcount = 0
            for m in range(12):
                day_in_month = DayInMonth[m]
                if LeapYear and (y+1)%4 == 0:
                    day_in_month = DayInMonthLeap[m]
                    
                W = MultiSiteDict["Weight"][v][m+1]
                r = Simr.loc[dcount:dcount+day_in_month-1,v] 
                if v == "PP01" or v == "P_Occurrence":
                    rn = GenMultiRN(r, W, Type = "P", Size = day_in_month,
                                    TransformFunc = None, Warn = False) 
                else:
                    rn = GenMultiRN(r, W, Type = "T", Size = day_in_month,
                                    TransformFunc = None, Warn = False)
                # Gen Rn
                for d in range(day_in_month):
                    CovertCurve = V2UCurve.loc[dcount,v]
                    rn[:,d] = CovertCurve(rn[:,d])

                    if day_in_month == 29 and (d+1) == 29: #2/29 = 2/28
                        dcount -= 1
                    dcount += 1
                # Add up
                if type(Rn) is int: 
                    Rn = rn
                else:
                    Rn = np.concatenate((Rn,rn), axis = 1)
        SpatialRnNum[v] = Rn
    Stat["MultiSiteDict"]["SpatialRnNum"] = SpatialRnNum
        
    # Re-organize the Rn to each stn
    for i, s in enumerate(Stns):
        RnNum = pd.DataFrame()
        for v in Var:
            RnNum[v] = SpatialRnNum[v][i]         
        Stat[s]["RnNum"] = RnNum
    ToPickle(Setting, "Stat.pickle", Stat)
    return Stat