import pulumi_aws as aws
from pulumi_aws import iam
from pulumi import log
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


def eks_cluster_role():
    log.info('[base.iam.eks_cluster_role]')
    eks_cluster_role = iam.Role(
        'eks-iam-role',
        name='EKS-Cluster-Role',
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
        role=eks_cluster_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEKSServicePolicy',
    )

    iam.RolePolicyAttachment(
        'eks-cluster-policy-attachment',
        role=eks_cluster_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEKSClusterPolicy',
    )

    # Let's return the role from the function
    return eks_cluster_role

def eks_worker_role():
    log.info('[base.iam.eks_worker_role]')
    eks_worker_role = iam.Role(
        'ec2-nodegroup-iam-role',
        name='EKS-Worker-Role',
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
        role=eks_worker_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy',
    )

    iam.RolePolicyAttachment(
        'eks-cni-policy-attachment',
        role=eks_worker_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy',
    )

    iam.RolePolicyAttachment(
        'ec2-container-ro-policy-attachment',
        role=eks_worker_role.id,
        policy_arn='arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly',
    )

    # Let's return the role from the function
    return eks_worker_role
