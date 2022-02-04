# TEXAS Open Access Benchmark Datasets

## Introduction
These benchmarks are data from Texas sample TCRBOA7 of the [Baylor college
open access pilot](https://www.nature.com/articles/sdata201610). 

## Donor metadata 


## Raw datasets info
**ExperimentStrategy**|**analysisType**|**DataCategory**|**TumourNormalDesination**|**FileType**|**OpenBucketURL**
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
RNA-Seq|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/RNA-Seq/sequencing_experiment/tumour/TCRBOA7-T-RNA.read1.fastq.gz
RNA-Seq|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/RNA-Seq/sequencing_experiment/tumour/TCRBOA7-T-RNA.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/normal/TCRBOA7-N-WGS.lane1.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/normal/TCRBOA7-N-WGS.lane1.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/normal/TCRBOA7-N-WGS.lane2.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/normal/TCRBOA7-N-WGS.lane2.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane1.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane1.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane2.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane2.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane3.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane3.read2.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane4.read1.fastq.gz
WGS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WGS/sequencing_experiment/tumour/TCRBOA7-T-WGS.lane4.read2.fastq.gz
WXS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WXS/sequencing_experiment/normal/TCRBOA7-N-WEX.read1.fastq.gz
WXS|sequencing_experiment|Sequencing Reads|normal|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WXS/sequencing_experiment/normal/TCRBOA7-N-WEX.read2.fastq.gz
WXS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WXS/sequencing_experiment/tumour/TCRBOA7-T-WEX.read1.fastq.gz
WXS|sequencing_experiment|Sequencing Reads|tumour|FASTQ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/WXS/sequencing_experiment/tumour/TCRBOA7-T-WEX.read2.fastq.gz

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
