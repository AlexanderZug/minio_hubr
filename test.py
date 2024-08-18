import configparser

from s3_service import s3_bucket_service_factory

config = configparser.ConfigParser()
config.read('default.ini')

s3 = s3_bucket_service_factory(config)
s3.upload_file_object("test", "test.txt", "test")
