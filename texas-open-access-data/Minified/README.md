Minified real tumor/normal benchmarks
=====================================

Introduction
------------

These benchmarks are derived from Texas sample TCRBOA7 of the [Baylor college
open access pilot](https://www.nature.com/articles/sdata201610). They are
minified versions that can be used for technical benchmarking. Their usefulness
for scientific benchmarking may be limited right now, since the regions
selected are not designed to capture any particular feature of interest.

Design
------

The WGS reads for the tumor and the normal samples where aligned to the hg38
reference by the official ARGO alignment pipeline. For each benchmark we
defined a BED file with regions of interest, which is used to fish-out all the
reads that overlap those regions along with their corresponding pairs. The
pairs need not fall inside these regions. This process has two steps, first
selecting the reads names that overlap the regions using samtools, and then
using GATK's FilterSamReads with that list. This ensures that the reads pairs
are respected, but it also means that some reads will fall outside of the
selected regions and may not align to the mini-reference.

Files provided
--------------

Each benchmark includes the following files

* *WGS/FASTQ*: the FASTQ files for the normal and tumor samples, each set in
  a directory
* *WGS/BAM*: the reads on their original alignments for the tumor and normal
  samples, in BAM format
* *WGS/CRAM*: the reads on their original alignments for the tumor and normal
  samples, in CRAM format, using the original hg38 reference
* *WGS/BAM-mini*: the reads re-aligned to the mini-reference, in BAM format
* *WGS/CRAM-mini*: the reads re-aligned to the mini-reference, in CRAM format
* *mini-reference*: a minified version of the reference including only the
  regions selected, used to produce the CRAM-mini files
* *inputs/regions.bed*: contains the BED file with the regions used to select the reads

The mini-reference is intended to be used in alignment and variant calling
pipelines to speed-up the process. It also contains minified versions of the
typical population resources that are used in these pipelines, which may have
the genomic locations of variants shifted to reflect the changes in the
reference.

Types of benchmarks
-------------------

We have two types of benchmarks: cropped and sliced. The cropped alternative
only takes the start of chromosomes. The beginning of chromosomes include
telomeric regions, which are not well characterized. However, they have
the benefit that the genomic elements that fall inside these regions do not
need to have their positions adjusted on the mini-reference. The sliced
alternative takes our a set regions spreads across the chromosomes, allowing to
target arbitrary regions across them. The mini-reference for the sliced
alternative is done by mushing together these regions and requires us to adjust
the positions of genomic elements like SNPs.

Here we provide a selection of benchmarks with different sizes and types, which
might be suitable in different scenarios.

Benchmark datasets info
----------------------

**FileName**|**FileSize**|**FileType**|**OpenBucketURL**
:-----:|:-----:|:-----:|:-----:
TCRB-CA.DO262483.minimal.tgz|20832323|TGZ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/minified/TCRB-CA.DO262483.minimal.tgz
TCRB-CA.DO262483.minimal_multi_chr.tgz|78414105|TGZ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/minified/TCRB-CA.DO262483.minimal_multi_chr.tgz
TCRB-CA.DO262483.small_crop.tgz|10662870245|TGZ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/minified/TCRB-CA.DO262483.small_crop.tgz
TCRB-CA.DO262483.small_slice.tgz|94020121|TGZ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/minified/TCRB-CA.DO262483.small_slice.tgz
TCRB-CA.DO262483.tiny_crop.tgz|6298466484|TGZ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/minified/TCRB-CA.DO262483.tiny_crop.tgz
TCRB-CA.DO262483.tiny_slice.tgz|12465449|TGZ|https://object.cancercollaboratory.org:9080/swift/v1/genomics-public-data/benchmark-datasets/TCRB-CA/DO262483/minified/TCRB-CA.DO262483.tiny_slice.tgz

