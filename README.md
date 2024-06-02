# gplotter
A package for plotting [ADMIXTURE]([https://www.cog-genomics.org/plink/](https://dalexander.github.io/admixture/) and [smartPCA](https://github.com/DReichLab/EIG) outputs. <br />

### ADMIXTURE
Unzip the repository and place "gplotter-admixture.py" in the same directory as your fam and Q files. This script will create two files, "<prefix>.csv" and "<prefix>.pdf" which will the Q estimates dataframe and a pdf of the bar plots. <br />

To do a dry run, you can use the input files provided in data directory of this repository to get bar plots of a supervised ADMIXTURE analysis.
``` r
python gplotter-admixture.py --fam admixture.fam -Q admixture.3s.Q --df_csv test.csv --out_pdf test.pdf
```

### smartPCA
Place "gplotter-PCA.R" in the same directory as your evec and poplist files (the file containing the population labels used to calculate the principle components of the PCA). <br />

An example of how to create PCA plots:
``` r
> setwd("path/to/your/input/files")
> source("gplotter-PCA.R")
Do you want to project samples? (yes/no): yes
Enter ancient population labels separated by commas: Steppe_MLBA,Steppe_EMBA,Steppe_Eneolithic,EHG,Europe_MNChL,WHG,Europe_LNBA,Europe_EN,SHG,Anatolia_N,Armenia_ChL,Armenia_EBA,Armenia_MLBA,Iran_N,Natufian,Levant_BA,Levant_N,Iran_ChL,Iran_LN,MA1,Ust_Ishim,Steppe_IA,Iran_recent,Anatolia_ChL,Iran_HotuIIIb,Iberia_BA,Kostenki14,Switzerland_HG,CHG,AG2,Altai,Denisovan,MezE,Vi_merge,Mota,Clovis,Kennewick,Mbuti.DG,Chimp,hg19ref
Enter the x-axis variable (PC1/PC2/PC3/PC3): PC1
Enter the y-axis variable (PC1/PC2/PC3/PC3): PC2
Enter the title for the PCA plot: Test
Do you want to save the plot? (yes/no): yes
Enter the file format (pdf/html/png): html
Enter the file name (without extension): test
Enter the units (in/px): in
Enter the width: 30
Enter the height: 20
Do you want to create a zoomed plot? (yes/no): yes
Enter Y-axis limits: -0.05, 0.05
Enter X-axis limits: -0.05, 0.016
Do you want to save the zoomed plot? (yes/no): yes
Enter the file format (pdf/html/png): pdf
Enter the file name for the zoomed plot (without extension): test_zoomed
Enter the units for the zoomed plot (in/px): in
Enter the width for the zoomed plot: 30
Enter the height for the zoomed plot: 20
```
