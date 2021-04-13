# WGS Metadata to Support Running ARGO Workflows

TSV files are generated using `scripts/gen-meta-tsv.py`.
TSV files are generated using commands:

```
cd targeted-deep-seq-validation/
../scripts/gen-meta-tsv.py -t wgs -d 50-donors-selected-for-validation.txt -o .
```

Note: metadata from two donors (DO21115, DO36352) are missed as they were excluded in PCAWG final analysis due to QC issues. Details can be found in this file: `pcawg-published-original-metadata/PCAWG_Excluded_Donors_Samples_-_Excluded_donors_2016_08_30.tsv`
