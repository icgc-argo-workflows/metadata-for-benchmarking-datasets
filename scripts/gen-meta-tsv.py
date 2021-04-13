#!/usr/bin/env python3

import os
import re
import gzip
from io import TextIOWrapper
from glob import glob
import sys
import argparse
import csv
import json

script_dir = os.path.dirname(os.path.realpath(__file__))

DONOR_INFO = f'{script_dir}/../pcawg-published-original-metadata/pcawg_donor_clinical_August2016_v9.tsv'
PCAWG_JSONL = f'{script_dir}/../pcawg-published-original-metadata/release_may2016.v1.4.jsonl.gz'
WGS_META = f'{script_dir}/../pcawg-published-original-metadata/WGS.metadata.tsv.gz'
RNA_SEQ_META = f'{script_dir}/../pcawg-published-original-metadata/RNA-Seq.metadata.tsv.gz'
TARGET_SEQ_META = f'{script_dir}/../pcawg-published-original-metadata/Targeted-Seq.validation.metadata.tsv.gz'
TARGET_SEQ_BAM_HEADERS = f'{script_dir}/../targeted-deep-seq-validation/targeted-seq-bam-info/*.header.gz'
TARGET_SEQ_BAM_INFO = f'{script_dir}/../targeted-deep-seq-validation/targeted-seq-bam-info/bam_size_md5sum.tsv'
TARGET_SEQ_IDS = f'{script_dir}/../targeted-deep-seq-validation/targeted-seq-bam-info/ids.from_portal_keywords_endpoint.jsonl.gz'
TARGET_SEQ_META_JSONL = f'{script_dir}/../targeted-deep-seq-validation/targeted-seq-bam-info/targeted_seq_bam_info.from_portal_file_endpoint.jsonl.gz'

"""
    OUTPUT
    ==> experiment.v2.tsv <==
    type
    program_id
    submitter_sequencing_experiment_id
    submitter_donor_id
    gender
    submitter_specimen_id
    tumour_normal_designation
    specimen_type
    specimen_tissue_source
    submitter_sample_id
    sample_type
    submitter_matched_normal_sample_id
    sequencing_center
    platform
    platform_model
    experimental_strategy
    sequencing_date
    read_group_count

    ==> file.v2.tsv <==
    type
    name
    format
    size
    md5sum
    path

    ==> read_group.v2.tsv <==
    type
    submitter_read_group_id
    read_group_id_in_bam
    submitter_sequencing_experiment_id
    platform_unit
    is_paired_end
    file_r1
    file_r2
    read_length_r1
    read_length_r2
    insert_size
    sample_barcode
    library_name
"""


def get_donor_ids(donor_list_file):
    cols = []
    counts = []

    with open(donor_list_file, 'r') as f:
        for row in f:
            values = row.split('\t')
            for i in range(len(values)):
                if len(cols) <= i:
                    cols.append([])
                    counts.append(0)

                value = values[i].strip()
                cols[i].append(value)
                if re.match(r'^DO\d+$', value):
                    counts[i] += 1

    max_count = max(counts)
    max_index = counts.index(max_count)

    return [d for d in cols[max_index] if re.match(r'^DO\d+$', d)]  # this is needed to remove possible header


def get_donor_info(donor_ids=None):
    donor_info = dict()

    with open(DONOR_INFO, 'r') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            if row['icgc_donor_id'] not in donor_ids:
                continue

            donor_info[row['icgc_donor_id']] = {
                'project_code': row['project_code'],
                'icgc_donor_id': row['icgc_donor_id'],
                'submitter_donor_id': row['submitted_donor_id'],
                'gender': row['donor_sex']
            }

    return donor_info


def get_targeted_bam_info(donor_ids):
    targeted_bam_info = dict()

    # read info from TARGET_SEQ_BAM_INFO (for file size/md5sum) and TARGET_SEQ_META (for tumour/normal pairing)

    bam_info = dict()  # temporary use
    with open(TARGET_SEQ_BAM_INFO, 'r') as b:
        for row in b:
            row = row.strip()
            bam_name, bam_md5sum, bam_size = row.split('\t')

            bam_info[bam_name] = {
                'size': bam_size,
                'md5sum': bam_md5sum
            }

    with gzip.open(TARGET_SEQ_META, 'r') as j:
        for row in csv.DictReader(TextIOWrapper(j, 'utf-8'), delimiter='\t'):
            if row['icgc_donor_id'] not in donor_ids:
                continue

            normal_bam_name = row['normal_validation_alignment_bam_file_name']
            normal_gnos_id = row['normal_validation_alignment_gnos_id']
            normal_aliquot_id = row['normal_validation_aliquot_id']
            tumour_bam_name = row['tumor_validation_alignment_bam_file_name']
            tumour_gnos_id = row['tumor_validation_alignment_gnos_id']
            tumour_aliquot_id = row['tumor_validation_aliquot_id']

            # add normal bam
            targeted_bam_info[normal_bam_name] = {
                'size': bam_info[normal_bam_name]['size'],
                'md5sum': bam_info[normal_bam_name]['md5sum'],
                'submitter_matched_normal_sample_id': None,
                'aliquot_id': normal_aliquot_id,
                'gnos_id': normal_gnos_id
            }

            # add tumour bam
            targeted_bam_info[tumour_bam_name] = {
                'size': bam_info[tumour_bam_name]['size'],
                'md5sum': bam_info[tumour_bam_name]['md5sum'],
                'submitter_matched_normal_sample_id': normal_aliquot_id,
                'aliquot_id': tumour_aliquot_id,
                'gnos_id': tumour_gnos_id
            }

    return targeted_bam_info


def get_targeted_seq_meta(donor_ids=None, donors=None):
    read_groups = dict()
    # get RG info from TARGET_SEQ_BAM_HEADERS
    for bam_header_file in glob(TARGET_SEQ_BAM_HEADERS):
        bam_name = os.path.basename(bam_header_file).replace('.header.gz', '')
        read_groups[bam_name] = []

        with gzip.open(bam_header_file, 'r') as h:
            for row in TextIOWrapper(h, 'utf-8'):
                if not row.startswith('@RG'):
                    continue

                kv_paris = row.strip().split('\t')
                rg = dict()
                for kv in kv_paris:
                    if ':' not in kv:
                        continue

                    key = kv.split(':')[0]
                    rg[key] = ':'.join(kv.split(':')[1:])

                read_groups[bam_name].append(rg)

    targeted_bam_info = get_targeted_bam_info(donor_ids)
    targeted_seq_meta = dict()

    # read from TARGET_SEQ_META_JSONL
    with gzip.open(TARGET_SEQ_META_JSONL, 'r') as j:
        for row in TextIOWrapper(j, 'utf-8'):
            file_meta = json.loads(row)
            file_doc = file_meta['fileCopies'][0]
            donor_doc = file_meta['donors'][0]

            if donor_doc['donorId'] not in donor_ids:
                continue

            if file_doc['fileName'] not in targeted_seq_meta:
                bam_rgs = read_groups[file_doc['fileName']]
                targeted_seq_meta[file_doc['fileName']] = {
                    'project_code': donor_doc['projectCode'],
                    'icgc_donor_id': donor_doc['donorId'],
                    'gender': donors[donor_doc['donorId']]['gender'],
                    'submitter_donor_id': donor_doc['submittedDonorId'],
                    'aliquot_id': targeted_bam_info[file_doc['fileName']]['aliquot_id'],
                    'submitter_matched_normal_sample_id': targeted_bam_info[file_doc['fileName']]['submitter_matched_normal_sample_id'],
                    'submitter_specimen_id': donor_doc['submittedSpecimenId'][0],
                    'icgc_specimen_id': donor_doc['specimenId'][0],
                    'submitter_sample_id': donor_doc['submittedSampleId'][0],
                    'icgc_sample_id': donor_doc['sampleId'][0],
                    'dcc_specimen_type': donor_doc['specimenType'][0],
                    'submitter_sequencing_experiment_id': targeted_bam_info[file_doc['fileName']]['gnos_id'],  # use gnos_id as exp_id
                    'library_strategy': 'Targeted-Seq',
                    'object_id': file_doc['repoFileId'],
                    'file_name': file_doc['fileName'],
                    'file_size': targeted_bam_info[file_doc['fileName']]['size'],
                    'file_md5sum': targeted_bam_info[file_doc['fileName']]['md5sum'],
                    'read_group_count': len(bam_rgs),
                    'read_groups': [],
                }

                if targeted_seq_meta[file_doc['fileName']]['project_code'].endswith('-US'):
                    read_length = '125'
                else:
                    read_length = '100'

                for rg in bam_rgs:
                    targeted_seq_meta[file_doc['fileName']]['read_groups'].append(
                        {
                            'read_length_r1': read_length,
                            'read_length_r2': read_length,
                            'read_group_id_in_bam': rg['ID'],
                            'platform_unit': rg['PU'],
                            'is_paired_end': True,
                            'file_r1': file_doc['fileName'],
                            'file_r2': file_doc['fileName'],
                            'insert_size': int(rg['PI']) if ('PI' in rg and len(rg['PI'])) else '',
                            'sample_barcode': '',
                            'library_name': rg['LB'],
                        }
                    )

                    # all read groups from the same BAM should share the same value for the following fields
                    targeted_seq_meta[file_doc['fileName']]['platform'] = rg['PL']
                    targeted_seq_meta[file_doc['fileName']]['platform_model'] = rg['PM']
                    targeted_seq_meta[file_doc['fileName']]['sequencing_date'] = rg['DT'].split('T')[0]  # only need the date
                    targeted_seq_meta[file_doc['fileName']]['sequencing_center'] = rg['CN']
                    assert rg['SM'] == targeted_seq_meta[file_doc['fileName']]['aliquot_id']

    return targeted_seq_meta


def get_wgs_bam_info(donor_ids):
    wgs_bam_info = dict()

    with gzip.open(PCAWG_JSONL, 'r') as j:
        for row in TextIOWrapper(j, 'utf-8'):
            donor_centric = json.loads(row)
            if donor_centric['icgc_donor_id'] not in donor_ids:
                continue

            gnos_id = donor_centric['wgs']['normal_specimen']['bwa_alignment']['gnos_id']
            normal_aliquot_id = donor_centric['wgs']['normal_specimen']['bwa_alignment']['aliquot_id']
            files = []
            for f in donor_centric['wgs']['normal_specimen']['bwa_alignment']['files']:
                files.append(f)

            for t in donor_centric['wgs']['tumor_specimens']:
                for f in t['bwa_alignment']['files']:
                    files.append(f)

            for f in files:
                if f['file_name'].endswith('.bam'):
                    wgs_bam_info[f['file_name']] = {
                        'size': f['file_size'],
                        'md5sum': f['file_md5sum'],
                        'submitter_matched_normal_sample_id': normal_aliquot_id,
                        'gnos_id': gnos_id
                    }

    return wgs_bam_info


def get_wgs_meta(donor_ids=None, donors=None):
    """
        donor_unique_id
        donor_wgs_exclusion_white_gray
        submitter_donor_id
        icgc_donor_id
        dcc_project_code
        aliquot_id
        submitter_specimen_id
        icgc_specimen_id
        submitter_sample_id
        icgc_sample_id
        dcc_specimen_type
        library_strategy
        object_id
        file_name
        header_file_in_tar
        read_length_r1
        read_length_r2
        read_group_info
    """
    wgs_bam_info = get_wgs_bam_info(donor_ids)
    wgs_meta = dict()

    with gzip.open(WGS_META, 'r') as f:
        for row in csv.DictReader(TextIOWrapper(f, 'utf-8'), delimiter='\t'):
            if row['icgc_donor_id'] not in donor_ids:
                continue

            if row['file_name'] not in wgs_meta:
                wgs_meta[row['file_name']] = {
                    'project_code': row['dcc_project_code'],
                    'icgc_donor_id': row['icgc_donor_id'],
                    'gender': donors[row['icgc_donor_id']]['gender'],
                    'submitter_donor_id': row['submitter_donor_id'],
                    'donor_wgs_exclusion_white_gray': row['donor_wgs_exclusion_white_gray'],
                    'aliquot_id': row['aliquot_id'],
                    'submitter_matched_normal_sample_id': wgs_bam_info[row['file_name']]['submitter_matched_normal_sample_id'],
                    'submitter_specimen_id': row['submitter_specimen_id'],
                    'icgc_specimen_id': row['icgc_specimen_id'],
                    'submitter_sample_id': row['submitter_sample_id'],
                    'icgc_sample_id': row['icgc_sample_id'],
                    'dcc_specimen_type': row['dcc_specimen_type'],
                    'submitter_sequencing_experiment_id': wgs_bam_info[row['file_name']]['gnos_id'],  # use gnos_id as exp_id
                    'library_strategy': row['library_strategy'],
                    'object_id': row['object_id'],
                    'file_name': row['file_name'],
                    'file_size': wgs_bam_info[row['file_name']]['size'],
                    'file_md5sum': wgs_bam_info[row['file_name']]['md5sum'],
                    'read_group_count': 0,
                    'read_groups': [],
                }

            # ID:WTSI61808,PL:ILLUMINA,CN:WTSI,DT:2013-07-01T00:00:00.000+00:00,PI:457,LB:WGS:WTSI:33042,PM:Illumina HiSeq,SM:f82d213f-bc03-5b51-e040-11ac0c48687e,PU:WTSI:10078_7#10
            # parse RG info
            kv_paris = row['read_group_info'].split(',')
            rg = {}
            for kv in kv_paris:
                if ':' not in kv:
                    continue

                key = kv.split(':')[0]
                rg[key] = ':'.join(kv.split(':')[1:])

                if key == 'PL':
                    wgs_meta[row['file_name']]['platform'] = rg['PL']
                if key == 'PM':
                    wgs_meta[row['file_name']]['platform_model'] = rg['PM']
                if key == 'DT':
                    wgs_meta[row['file_name']]['sequencing_date'] = rg['DT'].split('T')[0]  # only need the date
                if key == 'CN':
                    wgs_meta[row['file_name']]['sequencing_center'] = rg['CN']

                if key == 'SM':  # make sure SM matches aliquot_id
                    assert rg['SM'] == wgs_meta[row['file_name']]['aliquot_id']

            wgs_meta[row['file_name']]['read_group_count'] += 1
            wgs_meta[row['file_name']]['read_groups'].append(
                {
                    'read_length_r1': int(row['read_length_r1']) if len(row['read_length_r1']) > 0 else '',
                    'read_length_r2': int(row['read_length_r2']) if len(row['read_length_r2']) > 0 else '',
                    'read_group_id_in_bam': rg['ID'],
                    'platform_unit': rg['PU'],
                    'is_paired_end': True if row['read_length_r2'] else False,
                    'file_r1': row['file_name'],
                    'file_r2': row['file_name'],
                    'insert_size': int(rg['PI']) if ('PI' in rg and len(rg['PI'])) else '',
                    'sample_barcode': '',
                    'library_name': rg['LB'],
                }
            )

    return wgs_meta


def migrate_specimen_type(old_specimen_type):
    specimen_type_mapping = {
        'Cell line - derived from tumour': ['Tumour', 'Cell line - derived from tumour', 'Other'],
        'Metastatic tumour - NOS': ['Tumour', 'Metastatic tumour', 'Other'],
        'Metastatic tumour - lymph node': ['Tumour', 'Metastatic tumour', 'Lymph node'],
        'Metastatic tumour - metastasis local to lymph node': ['Tumour', 'Metastatic tumour - metastasis local to lymph node', 'Lymph node'],
        'Metastatic tumour - metastasis to distant location': ['Tumour', 'Metastatic tumour - metastasis to distant location', 'Other'],
        'Normal - EBV immortalized': ['Normal', 'Normal', 'Other'],
        'Normal - blood derived': ['Normal', 'Normal', 'Blood derived'],
        'Normal - bone marrow': ['Normal', 'Normal', 'Bone marrow'],
        'Normal - buccal cell': ['Normal', 'Normal', 'Buccal cell'],
        'Normal - lymph node': ['Normal', 'Normal', 'Lymph node'],
        'Normal - other': ['Normal', 'Normal', 'Other'],
        'Normal - solid tissue': ['Normal', 'Normal', 'Solid tissue'],
        'Normal - tissue adjacent to primary': ['Normal', 'Normal - tissue adjacent to primary tumour', 'Solid tissue'],
        'Primary tumour - blood derived (bone marrow)': ['Tumour', 'Primary tumour', 'Blood derived - bone marrow'],
        'Primary tumour - blood derived (peripheral blood)': ['Tumour', 'Primary tumour', 'Blood derived - peripheral blood'],
        'Primary tumour - lymph node': ['Tumour', 'Primary tumour', 'Lymph node'],
        'Primary tumour - other': ['Tumour', 'Primary tumour', 'Other'],
        'Primary tumour - solid tissue': ['Tumour', 'Primary tumour', 'Solid tissue'],
        'Recurrent tumour - other': ['Tumour', 'Recurrent tumour', 'Other'],
        'Recurrent tumour - solid tissue': ['Tumour', 'Recurrent tumour', 'Solid tissue'],
    }

    if old_specimen_type in specimen_type_mapping:
        return specimen_type_mapping[old_specimen_type]
    else:
        return [None, None, None]


def output(metadata_info=None, output_dir=None, dataset_type=None):
    # write to different subfolders under output_dir

    exp_tsv_header = "type\tprogram_id\tsubmitter_sequencing_experiment_id\tsubmitter_donor_id\tgender\tsubmitter_specimen_id\ttumour_normal_designation\tspecimen_type\tspecimen_tissue_source\tsubmitter_sample_id\tsample_type\tsubmitter_matched_normal_sample_id\tsequencing_center\tplatform\tplatform_model\texperimental_strategy\tsequencing_date\tread_group_count\n"

    read_group_tsv_header = "type\tsubmitter_read_group_id\tread_group_id_in_bam\tsubmitter_sequencing_experiment_id\tplatform_unit\tis_paired_end\tfile_r1\tfile_r2\tread_length_r1\tread_length_r2\tinsert_size\tsample_barcode\tlibrary_name\n"

    file_tsv_header = "type\tname\tformat\tsize\tmd5sum\tpath\n"

    extra_info_tsv_header = "type\tsubmitter_id\tuniform_id\n"

    """
    OUTPUT directory structure:
    <data-type>
    └── DO50342
        ├── N.SA528891
        │   ├── extra_info.tsv
        │   └── sequencing_experiment
        │       ├── experiement.tsv
        │       ├── files.tsv
        │       └── read_groups.tsv
        └── T.SA528892
    """
    outdir = os.path.join(output_dir, dataset_type)

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    for bam_file in metadata_info:
        bam_meta = metadata_info[bam_file]

        uniform_donor_id = bam_meta['icgc_donor_id']
        uniform_specimen_id = bam_meta['icgc_specimen_id']
        specimen_type = bam_meta['dcc_specimen_type']
        uniform_sample_id = bam_meta['icgc_sample_id']
        t_or_n = 'T' if 'tumour' in specimen_type.lower() else 'N'

        submitter_sequencing_experiment_id = bam_meta['submitter_sequencing_experiment_id']

        tumour_normal_designation, specimen_type_new, specimen_tissue_source = migrate_specimen_type(specimen_type)

        donor_dir = os.path.join(outdir, uniform_donor_id)
        sample_dir = os.path.join(donor_dir, '.'.join([t_or_n, uniform_sample_id]))
        exp_dir = os.path.join(sample_dir, 'sequencing_experiment')

        if not os.path.isdir(exp_dir):
            os.makedirs(exp_dir)

        extra_info_tsv = os.path.join(sample_dir, 'extra_info.tsv')
        exp_tsv = os.path.join(exp_dir, 'experiment.tsv')
        file_tsv = os.path.join(exp_dir, 'file.tsv')
        read_group_tsv = os.path.join(exp_dir, 'read_group.tsv')

        with open(extra_info_tsv, 'w') as o:
            o.write(extra_info_tsv_header)
            o.write("\t".join(["donor", bam_meta["submitter_donor_id"], uniform_donor_id]) + "\n")
            o.write("\t".join(["specimen", bam_meta["submitter_specimen_id"], uniform_specimen_id]) + "\n")
            o.write("\t".join(["sample", bam_meta["submitter_sample_id"], uniform_sample_id]) + "\n")

        with open(exp_tsv, 'w') as o:
            o.write(exp_tsv_header)
            o.write("\t".join([
                'experiment', bam_meta['project_code'], submitter_sequencing_experiment_id,
                bam_meta['submitter_donor_id'], bam_meta['gender'],
                bam_meta['submitter_specimen_id'],
                tumour_normal_designation, specimen_type_new, specimen_tissue_source,
                bam_meta['submitter_sample_id'],
                'Total DNA' if dataset_type == 'wgs' else ('polyA+ RNA' if dataset_type == 'rna-seq' else 'Other DNA enrichments'),
                bam_meta['submitter_matched_normal_sample_id'] if tumour_normal_designation == 'Tumour' else '',
                bam_meta['sequencing_center'],
                bam_meta['platform'],
                bam_meta['platform_model'] if 'platform_model' in bam_meta else '',
                'WGS' if dataset_type == 'wgs' else ('RNA-Seq' if dataset_type == 'rna-seq' else 'Targeted-Seq'),
                bam_meta['sequencing_date'],
                str(bam_meta['read_group_count'])
            ]))
            o.write("\n")

        with open(file_tsv, 'w') as o:
            o.write(file_tsv_header)
            o.write("\t".join([
                'file', bam_file, 'BAM', str(bam_meta['file_size']), bam_meta['file_md5sum'], bam_file
            ]))
            o.write("\n")

        with open(read_group_tsv, 'w') as o:
            o.write(read_group_tsv_header)
            for rg in bam_meta['read_groups']:
                submitter_rg_id = rg['read_group_id_in_bam'].replace("'", "_").replace(":", "_")
                if len(submitter_rg_id) < 2:
                    submitter_rg_id += "_"

                o.write("\t".join([
                    'read_group',
                    submitter_rg_id,
                    rg['read_group_id_in_bam'],
                    submitter_sequencing_experiment_id,
                    rg['platform_unit'],
                    'true' if rg['is_paired_end'] else 'false',
                    bam_file,
                    bam_file,
                    str(rg['read_length_r1']),
                    str(rg['read_length_r2']),
                    str(rg['insert_size']),
                    rg['sample_barcode'],
                    rg['library_name']
                ]))
                o.write("\n")


def main(donor_list_file, output_dir, dataset_type='wgs'):
    donor_ids = get_donor_ids(donor_list_file)

    donors = get_donor_info(donor_ids)

    if dataset_type == 'wgs':
        wgs_meta = get_wgs_meta(donor_ids, donors)
        output(metadata_info=wgs_meta, output_dir=output_dir, dataset_type=dataset_type)

    elif dataset_type == 'targeted-seq':
        targeted_seq_meta = get_targeted_seq_meta(donor_ids, donors)
        output(metadata_info=targeted_seq_meta, output_dir=output_dir, dataset_type=dataset_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='donor_list_file', required=True,
                        help='A TSV file containing ICGC Donor IDs')
    parser.add_argument('-o', dest='output_dir', required=True,
                        help='A path for output directory')
    parser.add_argument('-t', dest='dataset_type', default='wgs',
                        choices=['wgs', 'rna-seq', 'targeted-seq'],
                        help='type of dataset to output')
    args = parser.parse_args()

    if not os.path.isdir(args.output_dir):
        sys.exit(f'Specified output directory does not exist: {output_dir}')

    main(
        donor_list_file=args.donor_list_file,
        output_dir=args.output_dir,
        dataset_type=args.dataset_type
    )
