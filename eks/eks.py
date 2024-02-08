import pulumi
import pulumi_eks as eks

# TODO: Create 3 nodes AWS EKS Cluster
# Install there metrics-server, cluster-autoscaler
# Check how to install Helm3 charts
# Examples: https://github.com/pulumi/examples/blob/master/aws-py-eks/__main__.py
# Module docs: https://www.pulumi.com/docs/clouds/aws/guides/eks/ &
# https://www.pulumi.com/registry/packages/eks/api-docs/cluster/#inputs &
# https://www.pulumi.com/registry/packages/kubernetes/api-docs/

# Create an EKS cluster with the pretty default configuration.
def create_eks_cluster(private_subnets, public_subnets, vpc_id):
    private_subnet_ids = [subnet.id for subnet in private_subnets]
    public_subnet_ids = [subnet.id for subnet in public_subnets]
    eks_cluster = eks.Cluster("eks-cluster",
                          vpc_id=vpc_id,
                          private_subnet_ids=private_subnet_ids,
                          public_subnet_ids=public_subnet_ids,
                          instance_type="t2.medium",
                          node_associate_public_ip_address=False,
                          desired_capacity=3,
                          min_size=1,
                          max_size=3,
                          endpoint_public_access=True,
                          version="1.28",
                          enabled_cluster_log_types=[
                              "api",
                              "audit",
                              "authenticator",
                          ],
                          tags={'Name': 'pulumi-eks-cluster'})

    # Export the cluster's kubeconfig.
    pulumi.export("kubeconfig", eks_cluster.kubeconfig)
    pulumi.export('cluster-name', eks_cluster.name)
