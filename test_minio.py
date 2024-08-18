import configparser

from s3_service import s3_bucket_service_factory


OBJECTS_TO_UPLOAD = [1, 2, 3]
config = configparser.ConfigParser()
config.read("default.ini")
S3 = s3_bucket_service_factory(config)


def test_object_is_created():
    for obj in OBJECTS_TO_UPLOAD:
        S3.upload_file_object("test", f"{obj}.txt", "")

    objects_in_bucket = S3.list_objects("test")
    assert len(objects_in_bucket) == len(OBJECTS_TO_UPLOAD)


def test_object_is_deleted():
    for obj in OBJECTS_TO_UPLOAD:
        S3.delete_file_object("test", f"{obj}.txt")

    objects_in_bucket = S3.list_objects("test")
    assert len(objects_in_bucket) == 0
