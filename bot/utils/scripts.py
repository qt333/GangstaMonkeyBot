import os
import glob

# from fake_useragent import UserAgent


def get_session_names():
    """Return session_names list"""
    names = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob('sessions/*.json')]

    return names

def get_users_data_names():
    """Return session_names list"""
    names = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob('sessions/users_data/*.json')]

    return names