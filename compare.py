import os
import hashlib
PATH = '/home/cookies/'


def get_digest(name):
    digest = None
    with open('{}'.format(name), 'r') as file:
        content = file.readlines()
        hash_obj = hashlib.sha3_256()
        hash_obj.update(repr(content).encode('utf-8'))
        digest = hash_obj.hexdigest()
    return digest


def is_new(cookie_name):
    try:
        file = open('{}.sha256'.format(cookie_name))
        file.close()
        return False
    except FileNotFoundError:
        return True


def has_changed(cookie_name):
    # if not is_new(cookie_name):
    digest = get_digest('{}'.format(cookie_name))

    old_hash_file = open('{}.sha256'.format(cookie_name))
    old_hash = old_hash_file.readline()
    old_hash_file.close()

    print('old {} new {}'.format(old_hash, digest))
    if digest == old_hash:
        return False
    else:
        return True


def make_hashs(path_str):
    print(path_str)
    for path, subdirs, files in os.walk(path_str):
        print(path, subdirs, files)
        for filename in files:
            name = os.path.join(path, filename)
            if '.sha256'not in name:
                digest = get_digest('{}{}'.format(PATH, filename))
                with open('{}.sha256'.format(name), 'w') as file:
                    file.write(digest)
