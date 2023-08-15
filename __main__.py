import pulumi
from vpc.vpc import create_vpc
from ec2.ec2 import launch_instance

# Create VPC and related resources
vpc_resources = create_vpc()

# Launch EC2 instance
instance = launch_instance(vpc_resources['vpc'], vpc_resources['public_subnets'])

# Export the instance's public IP for easy access
pulumi.export("public_ip", instance.public_ip)
pulumi.export('instance_url', instance.public_dns)
pulumi.export("private_ip", instance.private_ip)
