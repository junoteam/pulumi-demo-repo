import pulumi
from pulumi_aws import s3
import random, string

# Generate random postfix string to make names of AWS S3 buckets random
def random_string(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# Create AWS S3 buckets
def create_s3_buckets():
    bucket_names = ["apple", "banana", "cherry"] #TO DO: move hardcoded names (not really hardcoded) of s3 buckets to Pulumi.dev.yaml
    bucket_ids = []

    for bucket_name in bucket_names:
        full_bucket_name = f"{bucket_name}-{random_string(8)}"
        bucket = s3.Bucket(full_bucket_name, versioning={"enabled": True})
        pulumi.log.info(f"Created bucket with name: {full_bucket_name}")
        bucket_ids.append(bucket.id)

    return bucket_ids
