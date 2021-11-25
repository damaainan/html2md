#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import os
import re


def main():

    path = sys.argv[1]
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # 判断文件类型以及是否包含需要替换的字符
            if filename.split('.')[-1] != "html":
                continue
            newname = re.sub('[ 　\((]+', '_', filename)
            newname = re.sub('[\))*：:]+', '', newname)
            if filename != newname:
                print('rename> {}: {} => {}'.format(
                    dirpath, filename, newname))
                # os.rename(os.path.join(dirpath, filename),
                #           os.path.join(dirpath, newname))


if __name__ == '__main__':
    main()
