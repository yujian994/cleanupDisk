import os
import string
import ConfigParser
import time
from shutil import copy


def GetPathSize(strPath):
    if not os.path.exists(strPath):
        return 0
    if os.path.isfile(strPath):
        return os.path.getsize(strPath)

    nTotalSize = 0
    for strRoot, lsDir, lsFiles in os.walk(strPath):
        for strDir in lsDir:
            nTotalSize = nTotalSize + GetPathSize(os.path.join(strRoot, strDir))
        for strFile in lsFiles:
            nTotalSize = nTotalSize + os.path.getsize(os.path.join(strRoot, strFile))
            return nTotalSize


def ChangePathMode(strPath, mode):
    if not os.path.exists(strPath):
        exit()
    for strRoot, lsDir, lsFiles in os.walk(strPath):
        for strDir in lsDir:
            dirpath = os.path.join(strRoot, strDir)
            os.chmod(dirpath, mode)
        for strFile in lsFiles:
            filepath = os.path.join(strRoot, strFile)
            os.chmod(filepath, mode)


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('cleanupDiskConfig.ini')
    section_list = config.sections()
    root_section_name = 'root_file'

    if os.geteuid() == 0:
        if root_section_name not in section_list:
            exit()

        option_list = config.options(root_section_name)
        item_list = config.items(root_section_name)

        for item in item_list:
            rpath = item[1]
            ChangePathMode(rpath, 0777)

    else:
        for section in section_list:
            if section == root_section_name:
                continue

            path = "backup"
            if not os.path.exists(path):
                os.makedirs(path, 0777)

            delpath = config.get(section, 'directory')
            day = config.get(section, 'days')
            res = config.get(section, 'reserve')

            dirSize = GetPathSize(delpath)

            if dirSize > string.atoi(res) * (2 ** 30):
                for rdirpath, dirnames, filenames in os.walk(delpath):
                    for dirname in dirnames:
                        dirpath = os.path.join(rdirpath, dirname)
                        copy(dirpath, os.path.join(path, dirname))
                        if GetPathSize(dirpath) == 0:
                            os.removedirs(dirpath)

                    for filename in filenames:
                        filepath = os.path.join(rdirpath, filename)
                        statinfo = os.stat(filenme)
                        if (statinfo.st_mtime - time.time()) > (day * 86400):
                            copy(filepath, os.path.join(path, filename))
                            os.remove(filepath)