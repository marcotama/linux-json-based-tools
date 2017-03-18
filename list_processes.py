import argparse
import os
import json
import platform
import re

# TODO add other info available in /proc ?


kernel_version = tuple(int(n) for n in re.match(r'Linux-(\d+)\.(\d+)\.(\d+)', platform.platform()).groups())


def get_proc_info(pid):
    proc_info = {}
    try:
        proc_info['cmdline'] = open(os.path.join('/proc', pid, 'cmdline'), 'r').read()[:-1].replace('\u0000',' ')
        stat = open(os.path.join('/proc', pid, 'stat'), 'r').read()
        match = re.search('\(([^)]+)\)', stat)
        proc_info['comm'] = match.group(1)
        tokens = stat.strip().replace("\n", '').replace(proc_info['comm'], '').split(' ')
        proc_info['pid'] = int(tokens[0])
        proc_info['state'] = tokens[2]
        proc_info['ppid'] = int(tokens[3])
        proc_info['pgrp'] = int(tokens[4])
        proc_info['session'] = int(tokens[5])
        proc_info['tty_nr'] = int(tokens[6])
        proc_info['tpgid'] = int(tokens[7])
        proc_info['flags'] = int(tokens[8])
        proc_info['minflt'] = int(tokens[9])
        proc_info['cminflt'] = int(tokens[10])
        proc_info['majflt'] = int(tokens[11])
        proc_info['cmajflt'] = int(tokens[12])
        proc_info['utime'] = int(tokens[13])
        proc_info['stime'] = int(tokens[14])
        proc_info['cutime'] = int(tokens[15])
        proc_info['cstime'] = int(tokens[16])
        proc_info['priority'] = int(tokens[17])
        proc_info['nice'] = int(tokens[18])
        proc_info['num_threads'] = int(tokens[19])
        proc_info['itrealvalue'] = int(tokens[20])
        proc_info['starttime'] = int(tokens[21])
        proc_info['vsize'] = int(tokens[22])
        proc_info['rss'] = int(tokens[23])
        proc_info['rsslim'] = int(tokens[24])
        proc_info['startcode'] = int(tokens[25])
        proc_info['endcode'] = int(tokens[26])
        proc_info['startstack'] = int(tokens[27])
        proc_info['kstkesp'] = int(tokens[28])
        proc_info['kstkeip'] = int(tokens[29])
        proc_info['signal'] = int(tokens[30])
        proc_info['blocked'] = int(tokens[31])
        proc_info['sigignore'] = int(tokens[32])
        proc_info['sigcatch'] = int(tokens[33])
        proc_info['wchan'] = int(tokens[34])
        proc_info['nswap'] = int(tokens[35])
        proc_info['cnswap'] = int(tokens[36])
        proc_info['exit_signal'] = int(tokens[37])
        proc_info['processor'] = int(tokens[38])
        proc_info['rt_priority'] = int(tokens[39])
        proc_info['policy'] = int(tokens[40])
        proc_info['delayacct_blkio_ticks'] = int(tokens[41])
        proc_info['guest_time'] = int(tokens[42])
        proc_info['cguest_time'] = int(tokens[43])
        proc_info['start_data'] = int(tokens[44])
        proc_info['end_data'] = int(tokens[45])
        proc_info['start_brk'] = int(tokens[46])
        proc_info['arg_start'] = int(tokens[47])
        proc_info['arg_end'] = int(tokens[48])
        proc_info['env_start'] = int(tokens[49])
        proc_info['env_end'] = int(tokens[50])
        proc_info['exit_code'] = int(tokens[51])
        statm = open(os.path.join('/proc', pid, 'statm'), 'r').read()
        tokens = statm.split(' ')
        proc_info['size'] = int(tokens[0])
        proc_info['resident'] = int(tokens[1])
        proc_info['shared'] = int(tokens[2])
        proc_info['text'] = int(tokens[3])
        proc_info['lib'] = int(tokens[4])
        proc_info['data'] = int(tokens[5])
        proc_info['dt'] = int(tokens[6])
        status = open(os.path.join('/proc', pid, 'status'), 'r').readlines()
        for line in status:
            match = re.match(r'Uid:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
            if match:
                proc_info['real_uid'] = match.group(1)
                proc_info['effective_uid'] = match.group(2)
                proc_info['saved_uid'] = match.group(3)
                proc_info['set_uid'] = match.group(4)

            match = re.match(r'Gid:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
            if match:
                proc_info['real_gid'] = match.group(1)
                proc_info['effective_gid'] = match.group(2)
                proc_info['saved_gid'] = match.group(3)
                proc_info['set_gid'] = match.group(4)
        return proc_info
    except IOError: # proc has already terminated
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Lists details of processes.'
                    'Specifically, every entry will be encoded in its own line as a shallow JSON object.'
                    'This format is sometimes called "JSON lines".'
                    'http://man7.org/linux/man-pages/man5/proc.5.html'
    )

    parser.add_argument(
        'directory',
        type=str,
        nargs='?',
        help='The directory whose content is to be listed'
    )

    args = parser.parse_args()

    dir_path = args.directory if args.directory else '.'
    for pid in os.listdir('/proc'):
        if not pid.isdigit():
            continue
        info = get_proc_info(pid)
        print(json.dumps(info))
