# WGS Metadata to Support Running ARGO Workflows

## Generate metadata TSV files

Metadata TSV files (under each sample directory) are generated using commands:

```
cd targeted-deep-seq-validation/
../scripts/gen-meta-tsv.py -t wgs -d 50-donors-selected-for-validation.txt -o .
```

Note: metadata from two donors (DO21115, DO36352) are missed as they were excluded in PCAWG final analysis due to QC issues. Details can be found in this file: `pcawg-published-original-metadata/PCAWG_Excluded_Donors_Samples_-_Excluded_donors_2016_08_30.tsv`

## Generate Nextflow params files for running alignment and variant calling workflows

Nextflow params files are generated using `gen-params-json.py` script, see the examples blow.

Note that the donor list input file (with `-d` option) consists of four columns: `study_id`, `donor_id`,
`normal_seq`, `tumour_seq`. Example donor list files provided:
* [dummy-test.donor.unaligned-wgs-seq.for-generating-alignment-job-files.tsv](https://github.com/icgc-argo-workflows/metadata-for-benchmarking-datasets/blob/main/targeted-deep-seq-validation/wgs/dummy-test.donor.unaligned-wgs-seq.for-generating-alignment-job-files.tsv)
* [dummy-test.donor.aligned-wgs-crams.for-generating-variant-calling-job-files.tsv](https://github.com/icgc-argo-workflows/metadata-for-benchmarking-datasets/blob/main/targeted-deep-seq-validation/wgs/dummy-test.donor.aligned-wgs-crams.for-generating-variant-calling-job-files.tsv)

Example of generating 'DNA Seq Alignment' params files:
```
cd targeted-deep-seq-validation/wgs/
../../scripts/gen-params-json.py -d dummy-test.donor.unaligned-wgs-seq.for-generating-alignment-job-files.tsv -r /home/ubuntu/references/reference_genome -m . -o .
```

Example of generating 'GATK Mutect2 Variant Calling' params files generated using commands:
```
cd targeted-deep-seq-validation/wgs/
../../scripts/gen-params-json.py -d dummy-test.donor.aligned-wgs-crams.for-generating-variant-calling-job-files.tsv -t mutect2 -r /home/ubuntu/references/gatk-resources -m . -o .
```

Example of generating 'Sanger WGS Variant Calling' params files generated using commands:
```
cd targeted-deep-seq-validation/wgs/
../../scripts/gen-params-json.py -d dummy-test.donor.aligned-wgs-crams.for-generating-variant-calling-job-files.tsv -t sanger-wgs -r /home/ubuntu/references/sanger-variant-calling -m . -o .
```
