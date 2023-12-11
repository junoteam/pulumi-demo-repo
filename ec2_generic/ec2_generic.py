import pulumi
import pulumi_aws as aws

# Retrieve configuration values from Pulumi configuration
config_ec2 = pulumi.Config("pulumi-ec2")
instance_type = config_ec2.require("instance_type_generic")
ssh_key_path = config_ec2.require("sshKeyPath")


def launch_generic_instance(vpc, public_subnets, iam_instance_profile, instance_count):
    instances = []

    # Create a security group allowing traffic on port 22 from anywhere
    security_group = aws.ec2.SecurityGroup("generic-ssh-sg",
                                           vpc_id=vpc.id,
                                           description='Enable SSH access',
                                           ingress=[
                                               {"protocol": "tcp", "from_port": 22, "to_port": 22,
                                                "cidr_blocks": ["0.0.0.0/0"]},
                                           ],
                                           egress=[
                                               {"protocol": "-1", "from_port": 0, "to_port": 0,
                                                "cidr_blocks": ["0.0.0.0/0"]}
                                           ])

    # Read your public SSH key from a file
    with open(ssh_key_path, "r") as f:
        ssh_public_key = f.read()

    # Retrieve AMI from Amazon
    ami = aws.ec2.get_ami(most_recent=True,
                          owners=["amazon"],
                          filters=[aws.GetAmiFilterArgs(name="name", values=["al2023-ami-2023*-x86_64"])])
    # Get AMI id
    ami_id = ami.id

    # Setup example user data
    user_data = f"""#!/bin/bash
                    echo '{ssh_public_key}' >> /home/ec2-user/.ssh/authorized_keys
                    sleep 30
                    dnf update
                    """

    # Create an (count) of EC2 instances in one of the public subnets with SSM Role attached
    for i in range(instance_count):
        instance_name = f"pulumi-ec2_generic-{i}"
        ec2_generic = aws.ec2.Instance(instance_name,
                                       instance_type=instance_type,
                                       ami=ami_id,
                                       subnet_id=public_subnets[0].id,
                                       vpc_security_group_ids=[security_group.id],
                                       user_data=user_data,
                                       iam_instance_profile=iam_instance_profile.name,
                                       associate_public_ip_address=True,
                                       tags={'Name': f'pulumi-generic-instance-{i}'}
                                       )
        instances.append(ec2_generic)

    return instances
