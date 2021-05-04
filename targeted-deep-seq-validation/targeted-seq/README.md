# Targeted-seq Metadata to Support Running ARGO Workflows

TSV files are generated using commands:

```
cd targeted-deep-seq-validation/
../scripts/gen-meta-tsv.py -t targeted-seq -d 50-donors-selected-for-validation.txt -o .
```

Mutect2 params files generated using commands (as an example):
```
cd targeted-deep-seq-validation/targeted-seq/
../../scripts/gen-params-json.py -d donors.aligned_normal_tumour_crams.tsv -t mutect2 -r /home/ubuntu/references/gatk-resources -m . -o .
```

Sanger WXS params files generated using commands (as an example):
```
cd targeted-deep-seq-validation/targeted-seq/
../../scripts/gen-params-json.py -d donors.aligned_normal_tumour_crams.tsv -t sanger-wxs -r /home/ubuntu/references/sanger-variant-calling -m . -o .
```

