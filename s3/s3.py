import pulumi
from pulumi_aws import s3

# Retrieve configuration values from Pulumi configuration
config_s3 = pulumi.Config("pulumi-dev-env")
bucket_names_str = config_s3.require("bucket_names")
bucket_suffix = config_s3.require("bucket_suffix")

def create_s3_buckets():
    bucket_names = [name.strip() for name in bucket_names_str.split(",")]
    bucket_ids = []

    for bucket_name in bucket_names:
        full_bucket_name = f"{bucket_name}-{bucket_suffix}"
        bucket = s3.Bucket(full_bucket_name, versioning={"enabled": True})
        pulumi.log.info(f"Created bucket with name: {full_bucket_name}")
        bucket_ids.append(bucket.id)

    return bucket_ids
