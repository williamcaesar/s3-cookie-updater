import os
import json

from minio import Minio
from compare import make_hashs, has_changed, PATH, is_new


class CookieUpdater:
    def __init__(self):
        with open('/home/credentials.json', 'r') as file:
            self.credentials = json.load(file)
        self.bucket = self.credentials['bucket']
        self.client = Minio(self.credentials['url'],
                            access_key=self.credentials['key_id'],
                            secret_key=self.credentials['key'],
                            region=self.credentials['region'])

    def upload_file(self, filename):
        print('file to upload: {}'.format(filename))
        new_filename = filename

        if 'cookies/' in new_filename:
            new_filename = new_filename.replace('cookies/', '')

        if '/home/' in new_filename:
            new_filename = new_filename.replace('/home/', '')

        file = open(filename, 'rb')
        print('file: {} filename: {}'.format(new_filename, filename))
        length = os.path.getsize(filename)
        try:
            buk = self.client.put_object(self.bucket, new_filename, file, length)
            print('successfully uploaded {} '.format(buk))
        except Exception as e:
            print('error uploading {}:\n{}'.format(filename, e))

    def check_new_cookies(self):
        pass

    def run(self):
        changed_files = list()
        new_cookies = list()

        for path, subdirs, files in os.walk(PATH):
            print(path, subdirs, files)
            for filename in files:
                filename = '{}{}'.format(PATH, filename)
                if '.sha256' not in filename:
                    if is_new(filename):
                        new_cookies.append(filename)
                    elif has_changed(filename):
                        print('FILE: {}'.format(filename))
                        changed_files.append(os.path.join(filename))
                    else:
                        print('not new neither has changed')

        print('changed: {}'.format(changed_files))
        print('new: {}'.format(new_cookies))

        for new_cookie in new_cookies:
            self.upload_file(new_cookie)

        for cookie in changed_files:
            self.upload_file(cookie)
        make_hashs(PATH)
        print('\n' + '*' * 20 + '\n')



