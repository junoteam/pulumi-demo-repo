import pulumi
import pulumi_aws as aws

config_ec2 = pulumi.Config("pulumi-ec2")
instance_type = config_ec2.require("instance_type")

def create_iam_role_ssm():
    # Create custom IAM Role for EC2
    ec2_role = aws.iam.Role("ec2Role",
        assume_role_policy={
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                    },
                    "Effect": "Allow",
                    "Sid": ""
                }
            ]
        })

    # TO DO
    # AmazonEC2RoleforSSM
    # This policy will soon be deprecated.
    # Please use AmazonSSMManagedInstanceCore policy to enable AWS Systems Manager service core functionality on EC2 instances.
    # For more information see https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-instance-profile.html

    # Attach existing service policy for newly created role
    aws.iam.RolePolicyAttachment("rolePolicyAttachment",
         policy_arn="arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM",
         role=ec2_role.name)

    # Create Instance Profile
    instance_profile = aws.iam.InstanceProfile("instanceProfile",
         role=ec2_role.name)

    return instance_profile
