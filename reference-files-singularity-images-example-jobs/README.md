# Reference files and Singularity images derived from Docker images

Reference files used by AROG workflows and Singularity images are hosted at [Cancer Genome Collaboratory](https://cancercollaboratory.org/). Please see the individual sections for the reference files and how
to download and stage them before running the workflows.

## BWA-MEM DNA-Seq Alignment Workflow

### GRCh38 reference genome sequencing and auxilary files

| file name | size | md5sum |
|--------------------------------|------------|----------------------------------|
| GRCh38_hla_decoy_ebv.dict      | 480732     | eea9d8e1d3a172362f4d16de7415bd79 |
| GRCh38_hla_decoy_ebv.fa        | 3263683042 | 64b32de2fc934679c16e83a2bc072064 |
| GRCh38_hla_decoy_ebv.fa.dict   | 480732     | eea9d8e1d3a172362f4d16de7415bd79 |
| GRCh38_hla_decoy_ebv.fa.fai    | 154196     | 5ccc91e56dc4a05448dd5b9507ec6bc6 |
| GRCh38_hla_decoy_ebv.fa.gz     | 918931038  | 9513ce08c458ac88f8411dcf01097a1f |
| GRCh38_hla_decoy_ebv.fa.gz.alt | 487553     | b07e65aa4425bc365141756f5c98328c |
| GRCh38_hla_decoy_ebv.fa.gz.amb | 20199      | e4dc4fdb7358198e0847106599520aa9 |
| GRCh38_hla_decoy_ebv.fa.gz.ann | 448319     | f228aeed2106bc6b0cf880317132ac2d |
| GRCh38_hla_decoy_ebv.fa.gz.bwt | 3217347004 | 7f0c8dcfc86b7c2ce3e3a54118d68fbd |
| GRCh38_hla_decoy_ebv.fa.gz.fai | 154196     | 5ccc91e56dc4a05448dd5b9507ec6bc6 |
| GRCh38_hla_decoy_ebv.fa.gz.gzi | 799928     | 11af7c4adcf5d2e211a4ed03a1a8c73e |
| GRCh38_hla_decoy_ebv.fa.gz.pac | 804336731  | 178862a79b043a2f974ef10e3877ef86 |
| GRCh38_hla_decoy_ebv.fa.gz.sa  | 1608673512 | 91a5d5ed3986db8a74782e5f4519eb5f |

The above files need to be staged under a path in the file system where workflow
jobs can access. The files can be downloaded using `wget`, one example is given as
below:

```
wget https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/reference-genome/GRCh38_hla_decoy_ebv/GRCh38_hla_decoy_ebv.dict
```

### Singularity image files for DNA-Seq Alignment Workflow (v1.8.1)
| file name | size | md5sum |
|--------------------------------|------------|----------------------------------|
| ghcr.io-icgc-argo-data-processing-utility-tools.payload-gen-dna-alignment-0.4.0.img   |    466771968    |     2c47868571e03c0e9a614e8b35ae6d65 |
| ghcr.io-icgc-argo-data-processing-utility-tools.payload-gen-dna-seq-qc-0.6.0.img    |      71360512    |      09188f09cd0a6b314a68891ac2182163 |
| quay.io-icgc-argo-aligned-seq-qc-aligned-seq-qc.0.2.2.1.img    |   436604928    |     0dc56cb4fd64d78108f0c8d1c616b7ec |
| quay.io-icgc-argo-bam-merge-sort-markdup-bam-merge-sort-markdup.0.1.11.0.img   |   459984896   |      beb4dd3be25f02f6060d1ffb642e579b |
| quay.io-icgc-argo-bwa-mem-aligner-bwa-mem-aligner.0.1.12.0.img  |  459984896    |     c7d436a9e1e367d763942aeab84a9d5b |
| quay.io-icgc-argo-gatk-collect-oxog-metrics-gatk-collect-oxog-metrics.4.1.8.0-3.0.img   |  1838567424   |     5839458c95e34d8b4fa70529322858cf |
| quay.io-icgc-argo-gatk-split-intervals-gatk-split-intervals.4.1.4.1-1.0.img   |    1429229568   |     164a607f74815da8329a071b82e77204 |
| quay.io-icgc-argo-metadata-parser-metadata-parser.0.1.0.0.img   |  71647232     |     4904869a0c91391c71d2e7d8883e782d |
| quay.io-icgc-argo-read-group-ubam-qc-read-group-ubam-qc.0.1.2.0.img   |    459984896   |      39b26626c0bd484bd730c5f7d6134e59 |
| quay.io-icgc-argo-seq-data-to-lane-bam-seq-data-to-lane-bam.0.3.3.0.img  | 459984896   |      91dc04f38f76fcb0b5d74c1e6437c872 |
| ubuntu-18.04.img     |     25853952     |     3e36f8d4e9c85803d56ef1cabc691f82 |

If you plan to run Sanger using Singularity, these image files need to be downloaded and transferred to
a path where is accessible to all compute nodes running Nextflow tasks. You would also need to set
the *singularity.cacheDir* to this path in the *nextflow.config* file.

To download the images, please follow the example below:

```
wget https://object.cancercollaboratory.org:9080/swift/v1/argo-singularity-images/quay.io-icgc-argo-bwa-mem-aligner-bwa-mem-aligner.0.1.12.0.img
```

## Sanger somatic variant calling workflow

### Reference genome and annotation files used by Sanger caller

| file name | size | md5sum |
|--------------------------------|------------|----------------------------------|
| CNV_SV_ref_GRCh38_hla_decoy_ebv_brass6+.tar.gz      | 4257793984 | 90a100d06dbde243c6e7e11e6a764374 |
| SNV_INDEL_ref_GRCh38_hla_decoy_ebv-fragment.tar.gz  | 1550158859 | 03ac504f1a2c0dbe34ac359a0f8ef690 |
| VAGrENT_ref_GRCh38_hla_decoy_ebv_ensembl_91.tar.gz  | 90122115   | 876657ce8d4a6dd69342a9467ef8aa76 |
| core_ref_GRCh38_hla_decoy_ebv.tar.gz                | 899142864  | 6448a15bcc8f91271b1870a3ecfcf630 |
| qcGenotype_GRCh38_hla_decoy_ebv.tar.gz              | 11472540   | 1956e28c1ff99fc877ff61e359e1020c |

The above files need to be staged under a path in the file system where workflow
jobs can access. The files can be downloaded using `wget`, one example is given as
below:

```
wget https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/sanger-variant-calling/qcGenotype_GRCh38_hla_decoy_ebv.tar.gz
```

### Singularity image files for Sanger WGS variant caller (v2.1.0-9.6.0)
| file name | size | md5sum |
|--------------------------------|------------|----------------------------------|
| ghcr.io-icgc-argo-data-processing-utility-tools.cleanup-workdir-1.0.0.img  |   27754496  |   af288fdac6358050eacf0be4e9e364f1 |
| ghcr.io-icgc-argo-data-processing-utility-tools.payload-add-uniform-ids-0.1.1.img  |   57327616  |   06fc2f3972d6fff8159da573a11e6ae4 |
| ghcr.io-icgc-argo-data-processing-utility-tools.payload-gen-variant-calling-0.6.0.img  |   304177152   |  dce06ee121749bf4e33f78ca8b636d45 |
| quay.io-icgc-argo-caveman-vcf-fix-caveman-vcf-fix.0.1.0.0.img  |   509239296  |   0c448debc2d1016e0d2d4fe2d6079127 |
| quay.io-icgc-argo-generate-bas-generate-bas.0.2.1.0.img   |  384573440   |  8d138b2a04632878646e561571f3a931 |
| quay.io-icgc-argo-prep-sanger-qc-prep-sanger-qc.0.1.3.0.img  |   57327616  |   f7adcca3c24ef017ce3dd4f82fe15bf2 |
| quay.io-icgc-argo-prep-sanger-supplement-prep-sanger-supplement.0.1.2.0.img  |   57327616  |   78904fe65a0a1d53a13b439efa385223 |
| quay.io-icgc-argo-repack-sanger-results-repack-sanger-results.0.2.0.0.img   |  459984896  |   ee755c08930ed6a7ae36115cb0db3a9a |
| quay.io-icgc-argo-sanger-wgs-variant-caller-sanger-wgs-variant-caller.2.1.0-9.img   |  384573440   |  a46a3e6059f4f769e4d6c67c87b0fe2d |
| ubuntu-18.04.img  |   25853952  |   3e36f8d4e9c85803d56ef1cabc691f82 |

If you plan to run Sanger using Singularity, these image files need to be downloaded and transferred to
a path where is accessible to all compute nodes running Nextflow tasks. You would also need to set
the *singularity.cacheDir* to this path in the *nextflow.config* file.

To download the images, please follow the example below:

```
wget https://object.cancercollaboratory.org:9080/swift/v1/argo-singularity-images/ghcr.io-icgc-argo-data-processing-utility-tools.payload-add-uniform-ids-0.1.1.img
```

### Input files for testing

| file name | size | md5sum |
|-----------|------|--------|
| N.dna_alignment.payload.json | 24761 | 785be595dfa6aec0dfb634835cf57be3 |
| N.extra_info.tsv | 111 | 0c86d86ae6479fb76438a0f8202d7591 |
| T.dna_alignment.payload.json | 35870 | bea284d1319e93ad41bac8b6ff382fe5 |
| T.extra_info.tsv | 105 | 79edd6437e02d7bb5c722597e4202d27 |
| TEST-PR.DO250183.SA610228.wgs.20200404.aln.cram | 6359358414 | 35d0f666a7f897dc7a12bb3a1fb8f04e |
| TEST-PR.DO250183.SA610228.wgs.20200404.aln.cram.crai | 308279 | eec86ac4f6561206dd8bdbb50a98e08d |
| TEST-PR.DO250183.SA610229.wgs.20200404.aln.cram | 9353098543 | 34c28db7b591f2bc5d0f4d91a0bdd194 |
| TEST-PR.DO250183.SA610229.wgs.20200404.aln.cram.crai | 430812 | 145a3452655003932c0a74ffea889c33 |

The the Nextflow params file is `sanger-wgs-example-job.json` in this folder of the git repo. Please
modify it to exclude more chromosomes so the test job will finish much quicker. The `exclude` param looks
like `"exclude":"chr1,chr2,chr3,chr4,chr5,chr6,chr7,chr8,chr9,chr10,chr11,chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19,chr20,chr22,chrX,chrY,chrUn%,HLA%,%_alt,%_random,chrM,chrEBV"`

To download the input files, please follow the example below:

```
wget https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/test-datasets/variant-calling/TEST-PR.DO250183.SA610228.wgs.20200404.aln.cram
```


## GATK Mutect2 somatic variant calling workflow

Reference files used by Mutect2 caller:

| file name | size | md5sum |
|--------------------------------|------------|----------------------------------|
| 1000g_pon.hg38.vcf.gz                                  | 17273497   | e236330d8d156d2aad2d0930a2440177 |
| 1000g_pon.hg38.vcf.gz.tbi                              | 1534802    | b95230d6634c3926fb0b4f104518a0f5 |
| af-only-gnomad.hg38.vcf.gz                             | 3184275189 | a4209be7fb4b5a5a8d3b778132cb7401 |
| af-only-gnomad.hg38.vcf.gz.tbi                         | 2443190    | a7efccb1519f046c19cdf9f28559d747 |
| af-only-gnomad.pass-only.biallelic.snp.hg38.vcf.gz     | 3529021364 | 6009ac7799419f69f19957a2ba1b3a16 |
| af-only-gnomad.pass-only.biallelic.snp.hg38.vcf.gz.tbi | 3121555    | 54bbff8e5637e5505eb06a0186d9b306 |
| af-only-gnomad.pass-only.hg38.vcf.gz                   | 4461091562 | 1c0240e5b752c8e414a86d204e4768fb |
| af-only-gnomad.pass-only.hg38.vcf.gz.tbi               | 3259267    | c537795d90d71e56279545e1682f5fdf |
| small_exac_common_3.hg38.vcf.gz                        | 1297183    | 4c75c1755a45c64e8af7784db7fde009 |
| small_exac_common_3.hg38.vcf.gz.tbi                    | 242095     | f650d1dda6bd68cba65d77f131147985 |


The above files need to be staged under a path in the file system where workflow
jobs can access. The files can be downloaded using `wget`, one example is given as
below:

```
wget https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/gatk-resources/1000g_pon.hg38.vcf.gz
```

Additional files needed for scatter/gather:

| file name | size | md5sum |
|--------------------------------|------------|----------------------------------|
| mutect2.scatter_by_chr/chr1.interval_list  | 180 | 24d9137f7ccd5c2803d58ef56b8b3f53 |
| mutect2.scatter_by_chr/chr10.interval_list | 182 | 512975027d78247fcb19166882fd51bf |
| mutect2.scatter_by_chr/chr11.interval_list | 182 | 4e51ed603da33710c7f1b8698f79649d |
| mutect2.scatter_by_chr/chr12.interval_list | 182 | 0f29b41613170edfca43fd27073c5079 |
| mutect2.scatter_by_chr/chr13.interval_list | 182 | d4dd4925e687cc9fce124dee7b063bb2 |
| mutect2.scatter_by_chr/chr14.interval_list | 182 | 17b4b3f0e549ed5acd1d4897bf8d0100 |
| mutect2.scatter_by_chr/chr15.interval_list | 182 | 9cfd133e2e3f90e37f8097048285e927 |
| mutect2.scatter_by_chr/chr16.interval_list | 180 | 9f4b5fb8db1493214d1aa540aecfc231 |
| mutect2.scatter_by_chr/chr17.interval_list | 180 | ff20b86a75cf9f329e2b935ea4edb2d3 |
| mutect2.scatter_by_chr/chr18.interval_list | 180 | 7607a18fa2a9ef98b4548c3d19e905c4 |
| mutect2.scatter_by_chr/chr19.interval_list | 180 | 2d95d0b4dc2282215c1981f759335ff4 |
| mutect2.scatter_by_chr/chr2.interval_list  | 180 | 9991a595530b6b06cafdb4ec62e6b419 |
| mutect2.scatter_by_chr/chr20.interval_list | 180 | 645342a858273248874e99acb29c50d5 |
| mutect2.scatter_by_chr/chr21.interval_list | 180 | 46907e8a00757980748c4a39864b8af5 |
| mutect2.scatter_by_chr/chr22.interval_list | 180 | fe4a33ce8693de2384ab447fb09f6f1b |
| mutect2.scatter_by_chr/chr3.interval_list  | 180 | 0548550722522719b2e4f0a1c8c3de42 |
| mutect2.scatter_by_chr/chr4.interval_list  | 180 | 191cdd70699c18d9fc68af035f00b0ef |
| mutect2.scatter_by_chr/chr5.interval_list  | 180 | f6e3b6b42e3f020c476aa89e7cbb32fc |
| mutect2.scatter_by_chr/chr6.interval_list  | 180 | e639558c71d116419dfcf41bbd2a4413 |
| mutect2.scatter_by_chr/chr7.interval_list  | 180 | b166ff8931a4ef196052b7cf961e71d3 |
| mutect2.scatter_by_chr/chr8.interval_list  | 180 | 86971574be70f3c6a38c8f6f8ad74f26 |
| mutect2.scatter_by_chr/chr9.interval_list  | 180 | b4aa7ed56e505cf6f9b0eca9ddc8c319 |
| mutect2.scatter_by_chr/chrXY.interval_list | 358 | bfef3db07d46c8d8d5c893c3cca827f3 |
| bqsr.sequence_grouping.grch38_hla_decoy_ebv.csv               | 89497 | 8ea70d26ffae94f8e14f321a7c0e7680 |
| bqsr.sequence_grouping_with_unmapped.grch38_hla_decoy_ebv.csv | 89509 | 1f6db058b2209485852059ecb69d7535 |

These files have been checked into [GitHub repository](https://github.com/icgc-argo/gatk-mutect2-variant-calling/tree/main/assets)
for the Mutect2 workflow. To get the files you may just clone the repo, or download using
`wget` using the URL pattern as in the following example:

```
wget https://raw.githubusercontent.com/icgc-argo/gatk-mutect2-variant-calling/main/assets/mutect2.scatter_by_chr/chr1.interval_list
```
