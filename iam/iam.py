import pulumi_aws as aws

# Func to create an IAM role for SSM
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

    # Attach existing service policy for newly created role
    aws.iam.RolePolicyAttachment("rolePolicyAttachment",
         policy_arn="arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
         role=ec2_role.name)

    # Create Instance Profile
    instance_profile = aws.iam.InstanceProfile("instanceProfile",
         role=ec2_role.name)

    return instance_profile
