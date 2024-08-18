import configparser
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from botocore.response import StreamingBody


class S3BucketService:
    def __init__(
        self,
        bucket_name: str,
        endpoint: str,
        access_key: str,
        secret_key: str,
    ) -> None:
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key

    def create_s3_client(self) -> boto3.client:
        client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version="s3v4"),
        )
        return client

    def upload_file_object(
        self,
        prefix: str,
        source_file_name: str,
        content: Union[str, bytes],
    ) -> None:
        client = self.create_s3_client()
        destination_path = str(Path(prefix, source_file_name))

        if isinstance(content, bytes):
            buffer = BytesIO(content)
        else:
            buffer = BytesIO(content.encode("utf-8"))
        client.upload_fileobj(buffer, self.bucket_name, destination_path)

    def list_objects(self, prefix: str) -> list[str]:
        client = self.create_s3_client()

        response = client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        storage_content: list[str] = []

        try:
            contents = response["Contents"]
        except KeyError:
            return storage_content

        for item in contents:
            storage_content.append(item["Key"])

        return storage_content

    def get_file_object(self, object_name: str) -> Optional[StreamingBody]:
        client = self.create_s3_client()
        try:
            file_obj = client.get_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "NoSuchKey":
                return None
            raise ex
        return file_obj["Body"]

    def delete_file_object(self, prefix: str, source_file_name: str) -> None:
        client = self.create_s3_client()
        path_to_file = str(Path(prefix, source_file_name))
        client.delete_object(Bucket=self.bucket_name, Key=path_to_file)


def s3_bucket_service_factory(config: configparser.ConfigParser) -> S3BucketService:
    return S3BucketService(
        config["s3_storage"]["bucket_name"],
        config["s3_storage"]["endpoint"],
        config["s3_storage"]["access_key"],
        config["s3_storage"]["secret_key"],
    )