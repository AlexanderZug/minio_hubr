import configparser

from s3_service import s3_bucket_service_factory

config = configparser.ConfigParser()
config.read("default.ini")


def test_object_is_created():
    s3 = s3_bucket_service_factory(config)
    objects_to_upload = [1, 2, 3]

    for obj in objects_to_upload:
        s3.upload_file_object("test", f"{obj}.txt", "")

    objects_in_bucket = s3.list_objects("test")
    assert len(objects_in_bucket) == len(objects_to_upload)


def test_object_is_deleted():
    s3 = s3_bucket_service_factory(config)
    objects_to_upload = [1, 2, 3]

    for obj in objects_to_upload:
        s3.delete_file_object("test", f"{obj}.txt")

    objects_in_bucket = s3.list_objects("test")
    assert len(objects_in_bucket) == 0
