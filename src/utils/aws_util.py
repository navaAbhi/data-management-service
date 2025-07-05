import boto3
from src.core.config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
from src.utils.constants import SERVICE_FILES_BUCKET_REGION


class AwsUtil:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=SERVICE_FILES_BUCKET_REGION,
    )

    def upload_file_to_s3(self, bucket_name, object_name, file_path, region):
        self.s3_client.upload_file(file_path, bucket_name, object_name)
        return object_name

    def get_presigned_post(self, bucket_name, object_name, content_type, expires_in, acl="private"):
        presigned_post = self.s3_client.generate_presigned_post(
            Bucket=bucket_name,
            Key=object_name,
            Fields={
                "Content-Type": content_type,
                "acl": acl
            },
            Conditions=[
                {"Content-Type": content_type},
                {"acl": acl}
            ],
            ExpiresIn=expires_in
        )
        return presigned_post
