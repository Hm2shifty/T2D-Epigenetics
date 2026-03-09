# Epigenetics Notebook
Datasets:
GSE272137 --> Main data site --> baraitic surgery --> n = 52, 850k sites
GSE38291 --> Twins Dataset - 27k sites --> n = 11 x 2 (Twins) 
GSE114763 --> Excersise Dataset 



## March 7 2026

### Phase 1: Foundation
- Set up conda environment `epi`
- Downloaded GSE272137 from GEO database
- Dataset: 52 samples, 13 OB + 13 T2D × 2 timepoints (w0, w52)
- Files: metadata_final.csv, GSE272137_processed_data_methylation.tsv.gz

### Key decisions made:
- Using processed beta values not raw IDAT files (reason: no minfi on Windows easily)
- Decided to run two analyses for sex confounding (reason: OB group all female, T2D mixed)

### Issues hit:
- None Today

### Questions to come back to:
- None Today

## March 8 2026

### Issues hit:
AUC went down --> meaning the orignal 52 set sample was being mmorized, running multi test code

