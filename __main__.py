import pulumi
from vpc.vpc import create_vpc
from ec2.ec2 import launch_instance
from s3.s3 import create_s3_buckets
from eks.eks import create_eks_cluster
from rds.rds import create_rds_subnet_group, create_rds_instance

# Get Pulumi project name
project_name = pulumi.get_project()

# Create VPC and related resources
vpc_resources = create_vpc()

# Launch EC2 instance
instance = launch_instance(vpc_resources['vpc'], vpc_resources['public_subnets'])

# Rds subnet group
rds_subnet_group = create_rds_subnet_group(vpc_resources['private_subnets'])

# RDS instance
rds_instance = create_rds_instance(vpc_resources['vpc'].id, rds_subnet_group)

# Create S3 Buckets
buckets = create_s3_buckets()

# Create EKS cluster
# cluster = create_eks_cluster()

# Export diff data about Cloud Resources
pulumi.export("public_ip", instance.public_ip)
pulumi.export('instance_url', instance.public_dns)
pulumi.export("private_ip", instance.private_ip)
pulumi.export("buckets", buckets)
pulumi.export("projectName", project_name)
