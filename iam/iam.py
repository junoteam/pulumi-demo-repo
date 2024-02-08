import pulumi_aws as aws
from pulumi_aws import iam
import json


# Func to create an IAM role for SSM
def create_iam_role_ssm():
    # Create custom IAM Role for EC2
    ec2_role = aws.iam.Role(
        "ec2Role",
        assume_role_policy=json.dumps({
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
            ],
        }),
    )

    # Attach existing service policy for newly created role
    aws.iam.RolePolicyAttachment("rolePolicyAttachment",
                                 policy_arn="arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
                                 role=ec2_role.name)

    # Create Instance Profile
    instance_profile = aws.iam.InstanceProfile("instanceProfile",
                                               role=ec2_role.name)

    return instance_profile


def eks_cluster_role_and_node_role():
    # # EKS Cluster Role
    # Purpose: This role is assumed by the EKS service to manage resources on your behalf,
    # such as creating or managing AWS resources that the cluster might need, like Elastic Load Balancers.
    eks_role = iam.Role(
        'eks-iam-role',
        assume_role_policy=json.dumps({
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'sts:AssumeRole',
                    'Principal': {
                        'Service': 'eks.amazonaws.com'
                    },
                    'Effect': 'Allow',
                    'Sid': ''
                }
            ],
        }),
    )

    iam.RolePolicyAttachment(
        'eks-service-policy-attachment',
        role=eks_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEKSServicePolicy',
    )

    iam.RolePolicyAttachment(
        'eks-cluster-policy-attachment',
        role=eks_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEKSClusterPolicy',
    )

    # # EC2 NodeGroup Role
    # Purpose: This role is for the EC2 instances that will serve as worker nodes in your EKS
    # cluster. It grants these instances permissions needed to join the cluster, operate within it, and interact with
    # AWS services that your applications might use (e.g., pulling images from ECR).
    ec2_role = iam.Role(
        'ec2-nodegroup-iam-role',
        assume_role_policy=json.dumps({
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'sts:AssumeRole',
                    'Principal': {
                        'Service': 'ec2.amazonaws.com'
                    },
                    'Effect': 'Allow',
                    'Sid': ''
                }
            ],
        }),
    )

    iam.RolePolicyAttachment(
        'eks-workernode-policy-attachment',
        role=ec2_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy',
    )

    iam.RolePolicyAttachment(
        'eks-cni-policy-attachment',
        role=ec2_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy',
    )

    iam.RolePolicyAttachment(
        'ec2-container-ro-policy-attachment',
        role=ec2_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly',
    )

    print("Defining IAM roles...")

    # Let's return the rule from the function
    return eks_role, ec2_role

