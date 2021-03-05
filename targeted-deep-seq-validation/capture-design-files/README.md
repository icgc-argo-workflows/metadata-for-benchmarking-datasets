# Capturing Chip Design Files

This folder contains sample metadata and capturing chip design files for the PCAWG validation dataset.
The files are provided by our PCAWG colleague Matthew Bailey at Washington University in St. Louis where
the validation experiments were carried out.

**NOTE**: all genomic coordinates are GRCh37.

| file/folder | content | note |
|-------------|---------|------|
| ICGCValidationSamples.csv | basic info of tumour samples and mapping to specific capture array | column `Tumour Analysis ID` is GNOS ID which can be used to get more sample info from this file: pcawg-published-original-metadata/release_may2016.v1.4.tsv.gz |
| TCGA-1_42870_29jul2015_design_deliverables | design files, `primary_targets` BED file contains intended regions to capture | array 1 |
| ICGC_OID42722_hg19_08jun2015_design_deliverables | design files, `primary_targets` BED file contains intended regions to capture | array 2 |
| TCGA-3_42869_29jul2015_design_deliverables | design files, `primary_targets` BED file contains intended regions to capture | array 3 |
| TCGA-4_42868_29jul2015_design_deliverables | design files, `primary_targets` BED file contains intended regions to capture | array 4 |
