import pulumi
from pulumi_aws import s3
import random, string

# Retrieve configuration values from Pulumi configuration
config_ec2 = pulumi.Config("pulumi-ec2")
bucket_names_str = config_ec2.require("bucket_names")

# Generate random postfix string to make names of AWS S3 buckets random
def random_string(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# Create AWS S3 buckets
def create_s3_buckets():
    bucket_names = [name.strip() for name in bucket_names_str.split(",")]
    print(bucket_names)
    bucket_ids = []

    for bucket_name in bucket_names:
        full_bucket_name = f"{bucket_name}-{random_string(8)}"
        bucket = s3.Bucket(full_bucket_name, versioning={"enabled": True})
        pulumi.log.info(f"Created bucket with name: {full_bucket_name}")
        bucket_ids.append(bucket.id)

    return bucket_ids
