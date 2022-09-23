# This is the sample code for multi-site weather generation.
# It allow batch simulation for multiple sites (without spatial correlation)

import MultiWG 
WD = r"C:\Users\Philip\Documents\GitHub\MultiWG\Sample_WD"

# =============================================================================
# Step 1: Create Task and prepare Setting file
# =============================================================================
Wth_obv, Wth_gen, Setting, Stat = MultiWG.CreateTask(wd = WD)
Setting["WDPath"] = WD
Setting["StnID"] = ["466990", "467080", "467440"]  
   
Setting["WthObvCsvFile"] = {"466990":"466990.csv",
                            "467080":"467080.csv",
                            "467440":"467440.csv"} 
# Setting["ClimScenCsvFile"] = {"466990":"466990_Scen.csv",
#                               "467080":"467080_Scen.csv",
#                               "467440":"467440_Scen.csv"} 
# or (Baseline simulation)
Setting["ClimScenCsvFile"] = None

# Daily precipitation and daily mean temperature.
Setting["Var"] = ['PP01', 'TX01'] 
# =============================================================================
# Step2: Read-in Weather Data
# =============================================================================
## Read in files (WthObvCsvFile and (ClimScenCsvFile))
# Wth_obv will be automatically preprocessed.
Wth_obv, Setting, Stat = MultiWG.ReadFiles(Wth_obv, Setting, Stat) 

# =============================================================================
# Step3: Run Statistical Analysis
# =============================================================================
# MultiWG.HisAnalysis has to be run first before running MultiWG.MultiHisAnalysis
Stat = MultiWG.HisAnalysis(Wth_obv, Setting, Stat)  
Stat = MultiWG.MultiHisAnalysis(Stat, Setting, Wth_obv, Wth_gen, ParalCores=-1)

# =============================================================================
# Step4: Generate RN Sets 
# =============================================================================
Stat = MultiWG.MultiGenRn(Setting, Stat)

# =============================================================================
# Step5: Generate Weather Data
# =============================================================================
Wth_gen, Stat = MultiWG.Generate(Wth_gen, Setting, Stat, ParalCores=-1)


#%% Validation Test
# Only validate the model with baseline simulation that 
# Setting["ClimScenCsvFile"] = None

## Checking first and second moments among weather variables 
CompareResult = MultiWG.MonthlyStatPlot(Wth_gen, Wth_obv, Setting)

## Checking precipitation distribution
KruskalDict = MultiWG.Kruskal_Wallis_Test(Wth_gen, Wth_obv, Setting)

## Checking Markov parameters for generating pricipitation events
MultiWG.MCplot(Wth_gen, Stat, Setting)

## Spatial auticorrelation check
MultiWG.SpatialAutoCorrelationComparison(Setting, Stat, Wth_gen)
