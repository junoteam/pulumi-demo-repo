import pulumi
import pulumi_eks as eks

# Create an EKS cluster with the default configuration.
def create_eks_cluster():
    cluster = eks.Cluster("eks-cluster")

    print("test")

    # Export the cluster's kubeconfig.
    pulumi.export("kubeconfig", cluster.kubeconfig)
