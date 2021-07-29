# This is the sample code for uni-site weather generation.
# It allow batch simulation for multiple sites (without spatial correlation)

import MultiWG 
WD = r"C:\Users\Philip\Documents\GitHub\MultiWG\Sample_WD"

# =============================================================================
# Step 1: Create Task and prepare Setting file
# =============================================================================
Wth_obv, Wth_gen, Setting, Stat = MultiWG.CreateTask(wd = WD)
Setting["WDPath"] = WD
Setting["StnID"] = ["466920"]  
# Batch mode => ["466920", "467080", "467440"]  
Setting["WthObvCsvFile"] = {"466920":"466920.csv"}
# Batch mode => 
# {"466920":"466920.csv",
#  "467080":"467080.csv",
#  "467440":"467440.csv"} 
Setting["ClimScenCsvFile"] = {"466920":"466920_Scen.csv"} 
# Batch mode => 
# {"466920":"466920_Scen.csv",
#  "467080":"467080_Scen.csv",
#  "467440":"467440_Scen.csv"} 
Setting["Var"] = ['PP01', 'TX01', 'TX02', 'TX04']

# =============================================================================
# Step2: Read-in Weather Data
# =============================================================================
## Read in files (WthObvCsvFile and (ClimScenCsvFile))
# Wth_obv will be automatically preprocessed.
Wth_obv, Setting, Stat = MultiWG.ReadFiles(Wth_obv, Setting, Stat) 

# =============================================================================
# Step3: Run Statistical Analysis
# =============================================================================
Stat = MultiWG.HisAnalysis(Wth_obv, Setting, Stat)

# =============================================================================
# Step4: Generate RN Sets 
# =============================================================================
Stat = MultiWG.GenRN(Setting, Stat)

# =============================================================================
# Step5: Generate Weather Data
# =============================================================================
Wth_gen, Stat = MultiWG.Generate(Wth_gen, Setting, Stat, ParalCores = 1)
# Note if it is a batch mode, set ParalCores to -1 to run in parallel.


#%% Validation Test
## Checking first and second moments among weather variables 
CompareResult = MultiWG.MonthlyStatPlot(Wth_gen, Wth_obv, Setting)

## Checking precipitation distribution
KruskalDict = MultiWG.Kruskal_Wallis_Test(Wth_gen, Wth_obv, Setting)

## Checking Markov parameters for generating pricipitation events
MultiWG.MCplot(Wth_gen, Stat, Setting)
