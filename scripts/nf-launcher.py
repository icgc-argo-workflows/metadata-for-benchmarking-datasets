#!/usr/bin/env python3

import os
import sys
import glob
import time
import argparse
import yaml
import json
import subprocess


# configuration to be used when no config file exists in the batch dir
DEFAULT_CONFIG = {
  'max_parallel_runs': 3,
  'resume_failed_run': False,
  'nextflow_config': '/home/ubuntu/testing/argo-alignment-test-run/nextflow.config',
  'workflow_version': '1.5.5',
  'profile': 'slurm_docker',
  'reverse_order': False,
  'remove_input_bam': False
}


def get_config(batch_dir):
    # name of the config file: settings.conf, file format: YAML
    conf_file = os.path.join(batch_dir, 'settings.conf')

    if os.path.isfile(conf_file):
        with open(os.path.join(batch_dir, 'settings.conf')) as f:
            config = yaml.safe_load(f)
    else:
        config = DEFAULT_CONFIG

    return config


def cleanup(job_dir, config):
    if config.get('remove_input_bam'):
        job_file = os.path.join(job_dir, '%s.nf-job.json' % os.path.basename(job_dir))
        with open(job_file, 'r') as j:
            job = json.load(j)
        for bam in job['sequencing_files']:
            if os.path.exists(os.path.realpath(os.path.join(job_dir, bam))):
                print("remove input bam: %s" % os.path.realpath(os.path.join(job_dir, bam)))
                os.remove(os.path.realpath(os.path.join(job_dir, bam)))


def get_job_summary(batch_dir, config=DEFAULT_CONFIG):
    # go through the job dirs
    job_summary = {
        'new': [],
        'completed': [],
        'running': [],
        'failed': []
    }

    job_dirs = sorted(glob.glob(os.path.join(batch_dir, '*')))
    if config.get('reverse_order'):
        job_dirs = sorted(job_dirs, reverse=True)

    for job_dir in job_dirs:
        if not os.path.isdir(job_dir):  # skip if not dir
            continue

        job_file = os.path.join(job_dir, '%s.nf-job.json' % os.path.basename(job_dir))
        if not os.path.isfile(job_file):  # skip if no job json
            continue

        trace_file = os.path.join(job_dir, 'trace.txt')
        stdout_file = os.path.join(job_dir, 'stdout')
        # the logic below for different job status can be improved
        if os.path.isfile(stdout_file):
            # if 'stdout' exists but 'trace.txt' does not, the job has already been launched
            # it's in running state, but just not scheduled by slurm or have not got the time
            # to generate the 'trace.txt' file
            if not os.path.isfile(trace_file):
                job_summary['running'].append({
                    'job_dir': job_dir
                })

            else:  # now both trace.txt and stdout exist
                trace_lines = []
                with open(trace_file, 'r') as f:
                    trace_lines = f.read().split('\n')
                trace_lines = trace_lines[:-1]  # remove the last line which is empty 

                stdout_lines = []
                with open(stdout_file, 'r') as f:
                    stdout_lines = f.read().split('\n')

                completed_in_stdout = False
                for stdout_line in reversed(stdout_lines):  # loop backwards
                    if 'process > DnaAln:cleanup' in stdout_line and '[100%] 1 of 1' in stdout_line:
                        completed_in_stdout = True

                # we are conservative to call a run is completed, so require confirmation
                # from both trace and stdout
                if 'DnaAln:cleanup' == trace_lines[-1].split('\t')[3] and \
                        'COMPLETED' == trace_lines[-1].split('\t')[4] and \
                        completed_in_stdout:
                    job_summary['completed'].append({
                        'job_dir': job_dir
                    })

                    # cleanup the input BAM to free more space
                    cleanup(job_dir, config)

                else:  # now either running or failed
                    status = 'running'  # assume running
                    for trace_line in trace_lines:
                        if trace_line.startswith('task_id'):
                            continue

                        cols = trace_line.split('\t')
                        if cols[4] == 'FAILED' or cols[4] == 'ABORTED':  # treat the two same way
                            status = 'failed'
                            break

                    job_summary[status].append({
                        'job_dir': job_dir
                    })

        else:  # no stdout file, it's new job
            job_summary['new'].append({
                'job_dir': job_dir
            })

    return job_summary


def launch_job(job, config=DEFAULT_CONFIG, resume=False, launch=False):
    job_dir = job['job_dir']
    job_file = os.path.join(job_dir, '%s.nf-job.json' % os.path.basename(job_dir))
    if not os.path.isfile(job_file):
        raise Exception('Nextflow job JSON file not found under: %s' % job_dir)

    launch_command = 'cd %s && nextflow -C %s run icgc-argo/dna-seq-processing-wfs -r %s -params-file %s ' % \
                     (job_dir, config['nextflow_config'], config['workflow_version'], os.path.basename(job_file)) + \
                     '-profile %s -queue-size %s ' % (config['profile'], "2") + \
                     '-with-report -with-trace %s' % ('-resume ' if resume else '')

    launch_command += '2> stderr > stdout'

    if launch:
        time.sleep(8)  # sleep 8 seconds to avoid launching runs too close to each other
        system_call = subprocess.Popen(launch_command, shell=True)
        print('Launched run: %s' % job_file, file=sys.stderr)
    else:
        print('Launch flag (-l) not set. Otherwise, would have launched a run with command: %s' % launch_command, file=sys.stderr)


def main(batch_dir=None, launch=False):
    config = get_config(batch_dir)

    job_summary = get_job_summary(batch_dir, config=config)
    # print(json.dumps(job_summary))
    print("Job status, new: %s, running: %s, completed: %s, failed: %s" % (
             len(job_summary['new']), len(job_summary['running']), len(job_summary['completed']), len(job_summary['failed'])
         ))

    available_run_slots = config['max_parallel_runs'] - len(job_summary['running'])

    if available_run_slots > 0:
        if config['resume_failed_run']:  # resume failed jobs first if resume set to true
            for job in job_summary['failed']:
                launch_job(job, config, resume=True, launch=launch)
                available_run_slots -= 1

                if available_run_slots == 0:
                    break

        # still have run slots, then launch new jobs
        if available_run_slots > 0:
            for job in job_summary['new']:
                launch_job(job, config, resume=False, launch=launch)
                available_run_slots -= 1

                if available_run_slots == 0:
                    break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nextflow run monitor and launcher')
    parser.add_argument('-d', dest='batch_dir', required=True, help='A directory containing all job folders in one batch')
    parser.add_argument('-l', dest='launch', action='store_true', help='Flag for actual launch, otherwise informational only')
    args = parser.parse_args()

    main(batch_dir=args.batch_dir, launch=args.launch)

