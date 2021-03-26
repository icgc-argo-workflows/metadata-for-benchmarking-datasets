#!/usr/bin/env python3

import sys
import os
import argparse
import csv

base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

WGS_DONOR_METADATA_DIR = os.path.join(base_dir, "targeted-deep-seq-validation", "wgs")

"""
OUTPUT directory structure:
    DONOR_ID
    ├── N.SAMPLE_ID.json
    └── T.SAMPLE_ID.json

    with json file structure defined as:
"""
PARAMS_JSON = '''{{
  "study_id": "{study_id}",
  "experiment_info_tsv": "{sample_dir}/sequencing_experiment/experiment.tsv",
  "read_group_info_tsv": "{sample_dir}/sequencing_experiment/read_group.tsv",
  "file_info_tsv": "{sample_dir}/sequencing_experiment/file.tsv",
  "extra_info_tsv": "{sample_dir}/extra_info.tsv",
  "sequencing_files": "{bam_path}",
  "ref_genome_fa": "{reference_genome_fasta}",
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

def generate_params(donor_list_with_paths, reference_genome_fasta):
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
                    formatted_json = PARAMS_JSON.format(**locals())
                    donor_json['normal'] = {
                        'json': formatted_json,
                        'id': sample
                    }
                elif sample.startswith("T"):
                    bam_path=tumour_bam
                    formatted_json = PARAMS_JSON.format(**locals())
                    donor_json['tumour'] = {
                        'json': formatted_json,
                        'id': sample
                    }
                else:
                    sys.exit(f'Unexpected sample "{sample}" without T or N in donor folder: {donor_wgs_dir}')               
            json_strings.append(donor_json)

    return json_strings


def output(json_strings, output_dir):
    """ writes json parms files to specified outdir """

    for donor_json in json_strings:
        # create subdir for each donor
        donor_id = donor_json['donor']
        donor_output_dir = os.path.join(output_dir, donor_id)
        os.makedirs(donor_output_dir)

        for sample_type in ['normal', 'tumour']:
            sample = donor_json[sample_type]
            if not donor_json[sample_type]:
                print(f'Missing {sample} data for {donor_id}', file=sys.stderr)
            else:
                f = open(f'{os.path.join(donor_output_dir, sample["id"])}.json', "w")
                f.write(sample["json"])
                f.close()

    return


def main(donor_list_with_paths, reference_genome_fasta, output_dir):

    json_strings = generate_params(donor_list_with_paths, reference_genome_fasta)
    # all donors processed with no errors raised; create and write output
    output(json_strings, output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='donor_list_with_paths', required=True,
                        help='TSV file containing: ICGC Project ID, Donor ID, Normal Bam Path, Tumour Bam Path')
    parser.add_argument('-g', dest='reference_genome_fasta', required=True,
                        help='Path to GRCh38_hla_decoy_ebv.fa file')
    parser.add_argument('-o', dest='output_dir', required=True,
                        help='Path for output directory')
    args = parser.parse_args()

    if not os.path.isfile(args.donor_list_with_paths):
        sys.exit(f'Specified donor list does not exist: {args.donor_list_with_paths}')

    if os.path.isdir(args.output_dir):
        sys.exit(f'Specified output directory already exists: {args.output_dir}')

    main(
        donor_list_with_paths=args.donor_list_with_paths,
        reference_genome_fasta=args.reference_genome_fasta,
        output_dir=args.output_dir
    )