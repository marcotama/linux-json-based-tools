import argparse
import os
import stat
import json

def get_file_info(file_path):
    file_stat = os.stat(file_path)
    mode = file_stat[stat.ST_MODE] # type: int
    file_info = {
        'name': os.path.basename(file_path),
        'parent': os.path.dirname(file_path),
        'access_rights': file_stat[stat.ST_MODE],
        'i-node': file_stat[stat.ST_INO],
        'device': file_stat[stat.ST_DEV],
        'number-of-links': file_stat[stat.ST_NLINK],
        'user-id': file_stat[stat.ST_UID],
        'group-id': file_stat[stat.ST_GID],
        'size': file_stat[stat.ST_SIZE],
        'last-accessed': file_stat[stat.ST_ATIME],
        'last-modified': file_stat[stat.ST_MTIME],
        'last-info-changed': file_stat[stat.ST_CTIME],
        'is-file': stat.S_ISREG(mode),
        'is-directory': stat.S_ISDIR(mode),
        'is-character-device': stat.S_ISCHR(mode),
        'is-block-device': stat.S_ISBLK(mode),
        'is-device': stat.S_ISCHR(mode) or stat.S_ISBLK(mode),
        'is-fifo': stat.S_ISFIFO(mode),
        'is-link': stat.S_ISLNK(mode),
        'is-socket': stat.S_ISSOCK(mode),
        'set-uid-bit': bool(mode & stat.S_ISUID),
        'set-gid-bit': bool(mode & stat.S_ISGID),
        'sticky-bit': bool(mode & stat.S_ISVTX),
        'access-rights': str((mode & stat.S_IRWXU) // stat.S_IXUSR) +
                         str((mode & stat.S_IRWXG) // stat.S_IXGRP) +
                         str((mode & stat.S_IRWXO) // stat.S_IXOTH),
        'user-rights': (mode & stat.S_IRWXU) // stat.S_IXUSR,
        'group-rights': (mode & stat.S_IRWXG) // stat.S_IXGRP,
        'others-rights': (mode & stat.S_IRWXO) // stat.S_IXOTH,
        'user-can-read': bool(mode & stat.S_IRUSR),
        'user-can-execute': bool(mode & stat.S_IXUSR),
        'user-can-write': bool(mode & stat.S_IWUSR),
        'group-can-read': bool(mode & stat.S_IRGRP),
        'group-can-execute': bool(mode & stat.S_IXGRP),
        'group-can-write': bool(mode & stat.S_IWGRP),
        'others-can-read': bool(mode & stat.S_IROTH),
        'others-can-execute': bool(mode & stat.S_IXOTH),
        'others-can-write': bool(mode & stat.S_IWOTH),
        'lock-enforcement': bool(mode & stat.S_ENFMT),
    }
    return file_info


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Lists details of the content of a directory using JSON format.'
                    'Specifically, every entry will be encoded in its own line as a shallow JSON object.'
                    'This format is sometimes called "JSON lines".'
    )

    parser.add_argument(
        'directory',
        type=str,
        nargs='?',
        help='The directory whose content is to be listed'
    )

    args = parser.parse_args()

    dir_path = args.directory if args.directory else '.'
    for file_name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, file_name)
        info = get_file_info(full_path)
        print(json.dumps(info))
