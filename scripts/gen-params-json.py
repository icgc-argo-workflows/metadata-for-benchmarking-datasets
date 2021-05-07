#!/usr/bin/env python3

import sys
import os
import argparse
import csv

base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

WGS_DONOR_METADATA_DIR = os.path.join(base_dir, "targeted-deep-seq-validation", "wgs")

"""
OUTPUT directory structure for DNA-Seq alignment:
    DONOR_ID
    ├── N.SAMPLE_ID
    │   └── N.SAMPLE_ID.dna-seq-alignment.json
    └── T.SAMPLE_ID
        └── T.SAMPLE_ID.dna-seq-alignment.json

    with json file structure defined as:
"""
DNA_SEQ_ALIGNMENT_PARAMS_JSON = '''{{
  "study_id": "{study_id}",
  "experiment_info_tsv": "{sample_dir}/sequencing_experiment/experiment.tsv",
  "read_group_info_tsv": "{sample_dir}/sequencing_experiment/read_group.tsv",
  "file_info_tsv": "{sample_dir}/sequencing_experiment/file.tsv",
  "extra_info_tsv": "{sample_dir}/extra_info.tsv",
  "sequencing_files": "{bam_path}",
  "ref_genome_fa": "{reference_data_dir}/GRCh38_hla_decoy_ebv.fa",
  "cpus": 2,
  "mem": 2,
  "tempdir": "NO_DIR",
  "publish_dir": "dna-seq-alignment/outdir",
  "alignedSeqQC": {{
      "cpus": 4,
      "mem": 10
  }},
  "bamMergeSortMarkdup": {{
      "cpus": 4,
      "mem": 18
  }},
  "bwaMemAligner": {{
      "cpus": 7,
      "mem": 30
  }},
  "gatkCollectOxogMetrics": {{
      "cpus": 3,
      "mem": 6
  }},
  "readGroupUBamQC": {{
      "cpus": 3,
      "mem": 6
  }},
  "seqDataToLaneBam": {{
      "cpus": 4,
      "mem": 12
  }}
}}
'''


"""
OUTPUT directory structure for variant calling workflows:
    DONOR_ID
    └── T.SAMPLE_ID
        └── T.SAMPLE_ID.<workflow_type>.json

    with json file structure defined as:
"""
GATK_MUTECT2_PARAMS_JSON = '''{{
  "study_id": "{study_id}",
  "tumour_aln_metadata": "{tumour_sample_dir}/dna-seq-alignment/DnaAln_pGenDnaAln/{tumour_metadata_json}",
  "tumour_aln_cram": "{tumour_cram}",
  "tumour_extra_info": "{tumour_sample_dir}/extra_info.tsv",
  "normal_aln_metadata": "{normal_sample_dir}/dna-seq-alignment/DnaAln_pGenDnaAln/{normal_metadata_json}",
  "normal_aln_cram": "{normal_cram}",
  "normal_extra_info": "{normal_sample_dir}/extra_info.tsv",
  "publish_dir": "gatk-mutect2-variant-calling",
  "perform_bqsr": false,
  "ref_fa": "{reference_data_dir}/../reference_genome/GRCh38_hla_decoy_ebv.fa",
  "mutect2_scatter_interval_files": "{reference_data_dir}/mutect2.scatter_by_chr/chr*.interval_list",
  "germline_resource_vcfs": [
    "{reference_data_dir}/af-only-gnomad.pass-only.hg38.vcf.gz"
  ],
  "panel_of_normals": "{reference_data_dir}/1000g_pon.hg38.vcf.gz",
  "contamination_variants": "{reference_data_dir}/af-only-gnomad.pass-only.biallelic.snp.hg38.vcf.gz",
  "mem": 4,
  "cpus": 2,
  "mutect2": {{
    "mem": 12,
    "cpus": 4
  }}
}}
'''


SANGER_WGS_PARAMS_JSON = '''{{
  "study_id": "{study_id}",
  "tumour_aln_metadata": "{tumour_sample_dir}/dna-seq-alignment/DnaAln_pGenDnaAln/{tumour_metadata_json}",
  "tumour_aln_cram": "{tumour_cram}",
  "tumour_extra_info": "{tumour_sample_dir}/extra_info.tsv",
  "normal_aln_metadata": "{normal_sample_dir}/dna-seq-alignment/DnaAln_pGenDnaAln/{normal_metadata_json}",
  "normal_aln_cram": "{normal_cram}",
  "normal_extra_info": "{normal_sample_dir}/extra_info.tsv",
  "publish_dir": "sanger-wgs-variant-calling",
  "cpus": 2,
  "mem": 4,

  "generateBas": {{
    "ref_genome_fa": "{reference_data_dir}/../reference_genome/GRCh38_hla_decoy_ebv.fa"
  }},
  "sangerWgsVariantCaller": {{
    "cpus": 8,
    "mem": 72,
    "ref_genome_tar": "{reference_data_dir}/core_ref_GRCh38_hla_decoy_ebv.tar.gz",
    "vagrent_annot": "{reference_data_dir}/VAGrENT_ref_GRCh38_hla_decoy_ebv_ensembl_91.tar.gz",
    "ref_snv_indel_tar": "{reference_data_dir}/SNV_INDEL_ref_GRCh38_hla_decoy_ebv-fragment.tar.gz",
    "ref_cnv_sv_tar": "{reference_data_dir}/CNV_SV_ref_GRCh38_hla_decoy_ebv_brass6+.tar.gz",
    "qcset_tar": "{reference_data_dir}/qcGenotype_GRCh38_hla_decoy_ebv.tar.gz",
    "exclude": "chrUn%,HLA%,%_alt,%_random,chrM,chrEBV"
  }}
}}
'''


SANGER_WXS_PARAMS_JSON = '''{{
  "study_id": "{study_id}",
  "tumour_aln_metadata": "{tumour_sample_dir}/dna-seq-alignment/DnaAln_pGenDnaAln/{tumour_metadata_json}",
  "tumour_aln_cram": "{tumour_cram}",
  "tumour_extra_info": "{tumour_sample_dir}/extra_info.tsv",
  "normal_aln_metadata": "{normal_sample_dir}/dna-seq-alignment/DnaAln_pGenDnaAln/{normal_metadata_json}",
  "normal_aln_cram": "{normal_cram}",
  "normal_extra_info": "{normal_sample_dir}/extra_info.tsv",
  "publish_dir": "sanger-wxs-variant-calling",
  "cpus": 2,
  "mem": 4,

  "generateBas": {{
    "ref_genome_fa": "{reference_data_dir}/../reference_genome/GRCh38_hla_decoy_ebv.fa"
  }},
  "sangerWxsVariantCaller": {{
    "cpus": 4,
    "mem": 32,
    "ref_genome_tar": "{reference_data_dir}/core_ref_GRCh38_hla_decoy_ebv.tar.gz",
    "vagrent_annot": "{reference_data_dir}/VAGrENT_ref_GRCh38_hla_decoy_ebv_ensembl_91.tar.gz",
    "ref_snv_indel_tar": "{reference_data_dir}/SNV_INDEL_ref_GRCh38_hla_decoy_ebv-fragment.tar.gz",
    "exclude": "chrUn%,HLA%,%_alt,%_random,chrM,chrEBV"
  }}
}}
'''


def generate_variant_calling_params(
            donor_list_with_paths,
            reference_data_dir,
            workflow_type,
            metadata_dir
        ):
    """ returns json_strings list with structure:
    [
        {
            'donor': "DONOR_ID",
            'tumour': {
                'json': params_json,
                'id': "TUMOUR_SAMPLE_ID"
            }
        },
        ...
    ]
    """
    if workflow_type == 'mutect2':
        params_template = GATK_MUTECT2_PARAMS_JSON
    elif workflow_type == 'sanger-wgs':
        params_template = SANGER_WGS_PARAMS_JSON
    elif workflow_type == 'sanger-wxs':
        params_template = SANGER_WXS_PARAMS_JSON

    json_strings = []
    with open(donor_list_with_paths) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            try:
                study_id, donor_id, normal_cram, tumour_cram = line
            except ValueError:
                sys.exit(f'Line {"  ".join(line)} is malformed. Expecting TSV with study_id, donor_id, normal_cram, tumour_cram')

            donor_json = {'donor': donor_id}
            donor_dir = os.path.join(metadata_dir, donor_id)
            normal_sample_dir = None
            tumour_sample_dir = None
            tumour_sample = None
            for sample in [f.name for f in os.scandir(donor_dir) if os.path.isdir(f)]:
                sample_dir = os.path.join(donor_dir, sample)
                alignment_metadata_dir = os.path.join(sample_dir, 'dna-seq-alignment', 'DnaAln_pGenDnaAln')
                payloads = [f.name for f in os.scandir(alignment_metadata_dir) if f.name.endswith('.payload.json')]
                if len(payloads) == 1:
                    metadata_payload = payloads[0]
                else:
                    sys.exit(f"Please make sure one and only one metadata json exists and with filename ends with '.payload.json' in: {alignment_metadata_dir}")

                if sample.startswith("N"):
                    normal_sample_dir = sample_dir
                    normal_metadata_json = metadata_payload
                elif sample.startswith("T"):
                    tumour_sample_dir = sample_dir
                    tumour_sample = sample
                    tumour_metadata_json = metadata_payload
                else:
                    sys.exit(f'Unexpected sample "{sample}" without T or N in donor folder: {donor_dir}')

            donor_json['tumour'] = {
                'json': params_template.format(**locals()),
                'id': tumour_sample
            }

            json_strings.append(donor_json)

    return json_strings


def generate_params(donor_list_with_paths, reference_data_dir):
    """ returns json_strings list with structure:
    [
        {
            'donor': "DONOR_ID",
            'normal': {
                'json': normal_sample_json,
                'id': "NORMAL_SAMPLE_ID"
            },
            'tumour': {
                'json': tumour_sample_json,
                'id': "TUMOUR_SAMPLE_ID"
            }
        },
        ...
    ]
    """
    json_strings = []
    with open(donor_list_with_paths) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            try:
                study_id, donor_id, normal_bam, tumour_bam = line
            except ValueError:
                sys.exit(f'Line {"  ".join(line)} is malformed. Expecting TSV with study_id, donor_id, normal_bam, tumour_bam')

            donor_json = {'donor': donor_id}
            donor_wgs_dir = os.path.join(WGS_DONOR_METADATA_DIR, donor_id)
            for sample in [f.name for f in os.scandir(donor_wgs_dir) if os.path.isdir(f)]:
                sample_dir = os.path.join(donor_wgs_dir, sample)
                if sample.startswith("N"):
                    bam_path=normal_bam
                    formatted_json = DNA_SEQ_ALIGNMENT_PARAMS_JSON.format(**locals())
                    donor_json['normal'] = {
                        'json': formatted_json,
                        'id': sample
                    }
                elif sample.startswith("T"):
                    bam_path=tumour_bam
                    formatted_json = DNA_SEQ_ALIGNMENT_PARAMS_JSON.format(**locals())
                    donor_json['tumour'] = {
                        'json': formatted_json,
                        'id': sample
                    }
                else:
                    sys.exit(f'Unexpected sample "{sample}" without T or N in donor folder: {donor_wgs_dir}')
            json_strings.append(donor_json)

    return json_strings


def output(json_strings, output_dir, workflow_type='alignment'):
    """ writes json parms files to specified outdir """

    for donor_json in json_strings:
        # create subdir for each donor
        donor_id = donor_json['donor']
        donor_output_dir = os.path.join(output_dir, donor_id)
        os.makedirs(donor_output_dir, exist_ok=True)

        for sample_type in ['normal', 'tumour']:
            # create subdir for each sample
            if sample_type not in donor_json:
                if workflow_type == 'alignment':
                    print(f'Missing {sample_type} data for {donor_id}', file=sys.stderr)
                continue

            sample = donor_json[sample_type]
            sample_output_dir = os.path.join(donor_output_dir, sample["id"])
            os.makedirs(sample_output_dir, exist_ok=True)

            # FUTURE: could iterate through list of workflows here
            sample_json_params_file = f'{os.path.join(sample_output_dir, sample["id"])}.{workflow_type}.json'
            try:
                os.remove(sample_json_params_file)
            except FileNotFoundError:
                pass # file doesn't exist yet

            f = open(sample_json_params_file, "w")
            f.write(sample["json"])
            f.close()

    return


def main(donor_list_with_paths, reference_data_dir, output_dir, workflow_type, metadata_dir):
    cwd = os.getcwd()
    if not reference_data_dir.startswith('/'):
        reference_data_dir = os.path.realpath(os.path.join(cwd, reference_data_dir))

    if workflow_type == 'alignment':
        json_strings = generate_params(donor_list_with_paths, reference_data_dir)
    elif workflow_type in ['mutect2', 'sanger-wgs', 'sanger-wxs']:
        if not metadata_dir.startswith('/'):
            metadata_dir = os.path.realpath(os.path.join(cwd, metadata_dir))

        json_strings = generate_variant_calling_params(
            donor_list_with_paths,
            reference_data_dir,
            workflow_type,
            metadata_dir
        )
    else:
        sys.exit(f'Unknown workflow type: {workflow_type}')

    # all donors processed with no errors raised; create and write output
    output(json_strings, output_dir, workflow_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='donor_list_with_paths', required=True,
                        help='TSV file containing: ICGC Project ID, Donor ID, Normal Bam Path, Tumour Bam Path')
    parser.add_argument('-r', dest='reference_data_dir', required=True,
                        help='Path to reference data directory')
    parser.add_argument('-t', dest='workflow_type',
                        choices=['alignment', 'mutect2', 'sanger-wgs', 'sanger-wxs'],
                        default='alignment',
                        help='Path for metadata directory')
    parser.add_argument('-m', dest='metadata_dir',
                        help='Path for metadata directory')
    parser.add_argument('-o', dest='output_dir', required=True,
                        help='Path for output directory')
    args = parser.parse_args()

    if not os.path.isfile(args.donor_list_with_paths):
        sys.exit(f'Specified donor list does not exist: {args.donor_list_with_paths}')

    if args.workflow_type in ['mutect2', 'sanger-wgs', 'sanger-wxs'] and not args.metadata_dir:
        sys.exit(f"Argument for 'metadata_dir' is required for {args.workflow_type}")

    main(
        donor_list_with_paths=args.donor_list_with_paths,
        reference_data_dir=args.reference_data_dir,
        output_dir=args.output_dir,
        workflow_type=args.workflow_type,
        metadata_dir=args.metadata_dir
    )
