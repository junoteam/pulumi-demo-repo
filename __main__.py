import pulumi
from vpc.vpc import create_vpc
from ec2_vpn.ec2_vpn import launch_vpn_instance
from ec2_generic.ec2_generic import launch_generic_instance
from iam.iam import create_iam_role_ssm, eks_worker_role, eks_cluster_role
from s3.s3 import create_s3_buckets
from eks.eks import create_eks_cluster
from rds.rds import create_rds_subnet_group, create_rds_instance
from ecr.ecr import create_ecr

# Get Pulumi project name
project_name = pulumi.get_project()

# Create VPC and related resources
vpc_resources = create_vpc()

# Create SSM IAM role
#iam_instance_profile = create_iam_role_ssm()

# Create VPN EC2 instance
#vpn_instance = launch_vpn_instance(vpc_resources['vpc'],
                                   #vpc_resources['public_subnets'],
                                   #iam_instance_profile)

# Create Generic EC2 instances (3)
#generic_instances = launch_generic_instance(vpc_resources['vpc'],
                                            #vpc_resources['public_subnets'],
                                            #iam_instance_profile, 3)

# Rds subnet group
#rds_subnet_group = create_rds_subnet_group(vpc_resources['private_subnets'])

# RDS instance
#rds_instance = create_rds_instance(vpc_resources['vpc'].id, rds_subnet_group)

# Create S3 Buckets
#buckets = create_s3_buckets()

# Create ECR Registry
ecr_reg = create_ecr()

# Create EKS cluster
eks_worker_role = eks_worker_role()
eks_cluster_role = eks_cluster_role()
eks_cluster = create_eks_cluster(vpc_resources['private_subnets'],
                                 vpc_resources['public_subnets'],
                                 vpc_resources['vpc'].id,
                                 eks_worker_role,
                                 eks_cluster_role)

# Export diff data about Cloud Resources
#pulumi.export("public_ip", vpn_instance.public_ip)
#pulumi.export('instance_url', vpn_instance.public_dns)
#pulumi.export("private_ip", vpn_instance.private_ip)
#pulumi.export("buckets", buckets)
pulumi.export("projectName", project_name)

# Export details for each Generic EC2 instance
#for i, instance in enumerate(generic_instances):
#    pulumi.export(f"generic_instance_{i}_public_ip", instance.public_ip)
#    pulumi.export(f"generic_instance_{i}_public_dns", instance.public_dns)
#    pulumi.export(f"generic_instance_{i}_private_ip", instance.private_ip)

