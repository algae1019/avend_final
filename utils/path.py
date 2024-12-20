'''
경로 자동화
'''

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_path(*subdirs):
    base_path = getattr(sys, '_MEIPASS', PROJECT_ROOT)
    return os.path.join(base_path, *subdirs)