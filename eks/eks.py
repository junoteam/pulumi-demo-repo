import pulumi
import pulumi_eks as eks
import pulumi_aws as aws

# Retrieve configuration values from Pulumi configuration
config_eks = pulumi.Config("pulumi-dev-env")
eks_instance_type = config_eks.require("eks-cluster_instance_type")
eks_cluster_version = config_eks.require("eks-cluster_version")
eks_cluster_name = config_eks.require("eks-cluster_name")


# Create an EKS cluster
def create_eks_cluster(private_subnets, public_subnets, vpc_id):
    eks_cluster = eks.Cluster(eks_cluster_name,
                              vpc_id=vpc_id,
                              name=eks_cluster_name,
                              private_subnet_ids=[subnet.id for subnet in private_subnets],
                              public_subnet_ids=[subnet.id for subnet in public_subnets],
                              skip_default_node_group=False,
                              # instance_role=eks_worker_role,  # check
                              # service_role=eks_cluster_role, # check
                              # instance_profile_name=iam_instance_profile, # check
                              # role_mappings=[
                              #     {
                              #         'groups': ['system:bootstrappers', 'system:nodes'],
                              #         'rolearn': eks_worker_role.arn,
                              #         'username': 'system:node:{{EC2PrivateDNSName}}',
                              #     }
                              # ],
                              # vpc_cni_options=eks.VpcCniOptionsArgs(
                              #     warm_ip_target=5,
                              # ),
                              instance_type=eks_instance_type,
                              node_associate_public_ip_address=False,
                              desired_capacity=3,
                              min_size=1,
                              max_size=3,
                              endpoint_public_access=True,
                              version=eks_cluster_version,
                              enabled_cluster_log_types=[
                                  "api",
                                  "audit",
                                  "authenticator"],
                              tags={
                                  'Name': f'{eks_cluster_name}',
                                  'ManagedBy': 'Pulumi',
                                  'Environment': 'dev',
                              })

    # Deploy EKS addons after cluster creation
    deploy_eks_addons(eks_cluster)

    # Output the cluster's kubeconfig and name.
    pulumi.export("kubeconfig", eks_cluster.kubeconfig)
    pulumi.export('cluster-name', eks_cluster.eks_cluster.name)

    return eks_cluster, eks_cluster.kubeconfig


# Deploy addons to EKS
def deploy_eks_addons(eks_cluster): # or aws-efs-csi-driver or aws-ebs-csi-driver leading to DependencyViolation and not removed ENI
    addons = [
        {
            "name": "aws-efs-csi-driver",
            "addon_version": "v1.7.4-eksbuild.1",
            "resolve_conflicts_on_create": "OVERWRITE",
        },
        {
            "name": "aws-ebs-csi-driver",
            "addon_version": "v1.27.0-eksbuild.1",
            "resolve_conflicts_on_create": "OVERWRITE",
        },
        {
            "name": "coredns",
            "addon_version": "v1.11.1-eksbuild.6",
            "resolve_conflicts_on_update": "OVERWRITE",
        },
    ]

    # Configure opts
    opts = pulumi.ResourceOptions(depends_on=[eks_cluster])

    for addon in addons:
        addon_name = addon["name"]
        aws.eks.Addon(addon_name,
                      cluster_name=eks_cluster.name,
                      addon_name=addon_name,
                      addon_version=addon["addon_version"],
                      resolve_conflicts_on_create=addon.get("resolve_conflicts_on_create", "NONE"),
                      opts=opts)

    """
    - Install addons / ebs-csi driver
    - Add nodepool
    - Add users via https://www.pulumi.com/registry/packages/aws/api-docs/eks/accessentry/
    """
