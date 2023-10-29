import pulumi
import pulumi_eks as eks

#TODO: Create 3 nodes AWS EKS Cluster
# Install there metrics-server, cluster-autoscaler
# Check how to install Helm3 charts
# Examples: https://github.com/pulumi/examples/blob/master/aws-py-eks/__main__.py
# Module docs: https://www.pulumi.com/docs/clouds/aws/guides/eks/ &
# https://www.pulumi.com/registry/packages/eks/api-docs/cluster/#inputs &
# https://www.pulumi.com/registry/packages/kubernetes/api-docs/

# Create an EKS cluster with the default configuration.
def create_eks_cluster():
    cluster = eks.Cluster("eks-cluster",
      # vpc_id=vpc.vpc_id,
      # public_subnet_ids=vpc.public_subnet_ids,
      # private_subnet_ids=vpc.private_subnet_ids,
      node_associate_public_ip_address=False,
      desired_capacity=5,
      min_size=3,
      max_size=5,
      enabled_cluster_log_types=[
          "api",
          "audit",
          "authenticator",
      ])

    # Export the cluster's kubeconfig.
    pulumi.export("kubeconfig", cluster.kubeconfig)
