# TEXAS Open Access Benchmark Datasets

## Introduction
These benchmarks are data from Texas sample TCRBOA7 of the [Baylor college
open access pilot](https://www.nature.com/articles/sdata201610). 

## Usage Notes
By downloading or utilizing any part of this dataset, end users must agree to the following conditions of use:

- No attempt to identify any specific individual represented by these data or any derivatives of these data will be made.
- No attempt will be made to compare and/or link this public data set or derivatives in part or in whole to private health information.
- These data in part or in whole may be freely downloaded, used in analyses and repackaged in databases.
- Redistribution of any part of these data or any material derived from the data will include a copy of this notice.
- The data are intended for use as learning and/or research tools only.
- This data set is not intended for direct profit of anyone who receives it and may not be resold
- Users are free to use the data in scientific publications if the providers of the data (Texas Cancer Research Biobank and Baylor College of Medicine Human Genome Sequencing Center) are properly acknowledged.

## Donor metadata 


## Raw datasets info
**ExperimentStrategy**|**analysisType**|**DataCategory**|**TumourNormalDesination**|**FileType**|**OpenBucketURL**
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
RNA-Seq|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/RNA-Seq/sequencing_experiment/tumour/TCRBOA7-T-RNA.read1.fastq.gz
RNA-Seq|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/RNA-Seq/sequencing_experiment/tumour/TCRBOA7-T-RNA.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/normal/TCRBOA7-N-WGS.lane1.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/normal/TCRBOA7-N-WGS.lane1.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/normal/TCRBOA7-N-WGS.lane2.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/normal/TCRBOA7-N-WGS.lane2.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane1.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane1.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane2.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane2.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane3.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane3.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane4.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane4.read2.fastq.gz
WXS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WXS/sequencing_experiment/normal/TCRBOA7-N-WEX.read1.fastq.gz
WXS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WXS/sequencing_experiment/normal/TCRBOA7-N-WEX.read2.fastq.gz
WXS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WXS/sequencing_experiment/tumour/TCRBOA7-T-WEX.read1.fastq.gz
WXS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.genomeinformatics.org/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WXS/sequencing_experiment/tumour/TCRBOA7-T-WEX.read2.fastq.gz

## ARGO Pipelines Processed Datasets
```
benchmark-datasets/TCRB-CA/
├── DO262483
    ├── RNA-Seq
    ├── WXS    
    ├── WGS
    ├── minified
        ├── minimal
        ├── minimal_multi_chr
        ├── small_crop
        ├── small_slice
        ├── tiny_crop
        ├── tiny_slice
        ├── TCRB-CA.DO262483.minimal.tgz
        ├── TCRB-CA.DO262483.minimal_multi_chr.tgz
        ├── TCRB-CA.DO262483.small_crop.tgz
        ├── TCRB-CA.DO262483.small_slice.tgz
        ├── TCRB-CA.DO262483.tiny_crop.tgz
        └── TCRB-CA.DO262483.tiny_slice.tgz
```
