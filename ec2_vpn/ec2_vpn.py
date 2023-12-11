import pulumi
import pulumi_aws as aws
from iam import iam

# Retrieve configuration values from Pulumi configuration
config_ec2 = pulumi.Config("pulumi-ec2")
instance_type = config_ec2.require("instance_type_vpn")

def launch_vpn_instance(vpc, public_subnets, iam_instance_profile):
    # Create a security group allowing traffic on ports 80, 443, and 22 from anywhere
    security_group = aws.ec2.SecurityGroup("web-ssh-sg",
                                           vpc_id=vpc.id,
                                           description='Enable HTTP, Wireguard (UDP), HTTPS, SSH access',
                                           ingress=[
                                               {"protocol": "tcp", "from_port": 8080, "to_port": 8080, "cidr_blocks": ["0.0.0.0/0"]},
                                               {"protocol": "tcp", "from_port": 443, "to_port": 443, "cidr_blocks": ["0.0.0.0/0"]},
                                               {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]},
                                               {"protocol": "udp", "from_port": 51820, "to_port": 51820, "cidr_blocks": ["0.0.0.0/0"]}
                                           ],
                                           egress=[
                                               {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
                                           ])

    # Read your public SSH key from a file
    ssh_key_path = config_ec2.require("sshKeyPath")
    with open(ssh_key_path, "r") as f:
        ssh_public_key = f.read()

    # Retrieve AMI from Amazon
    ami = aws.ec2.get_ami(most_recent=True,
                          owners=["amazon"],
                          filters=[aws.GetAmiFilterArgs(name="name", values=["al2023-ami-2023*-x86_64"])])
    # Get AMI id
    ami_id = ami.id

    # Setup user data
    user_data=f"""#!/bin/bash
                    echo '{ssh_public_key}' >> /home/ec2_generic-user/.ssh/authorized_keys
                    sleep 30
                    dnf update && dnf install python3-pip git -y
                    pip install ansible
                    git clone https://github.com/junoteam/wg-ansible-playbook.git wg-ansible-playbook/
                    ansible-playbook wg-ansible-playbook/playbooks/enable_iptables.yml
                    ansible-playbook wg-ansible-playbook/playbooks/wireguard_server.yml
                    """

    # Create an EC2 instance in one of the public subnets with SSM Role attached
    ec2_instance = aws.ec2.Instance("pulumi-ec2_generic",
                                    instance_type=instance_type,
                                    ami=ami_id,
                                    subnet_id=public_subnets[0].id,
                                    vpc_security_group_ids=[security_group.id],
                                    user_data=user_data,
                                    iam_instance_profile=iam_instance_profile.name,
                                    associate_public_ip_address=True,
                                    tags={'Name': 'pulumi-wg-instance'}
                                    )
    return ec2_instance
