from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
from pulumi_kubernetes import Provider, core
import pulumi
import yaml


def deploy_basic_services(eks_cluster):

    # Set a custom Kubeconfig
    custom_kubeconfig_path = "./config"
    k8s_provider = Provider("k8s-provider", kubeconfig=custom_kubeconfig_path)
    opts = pulumi.ResourceOptions(provider=k8s_provider, depends_on=[eks_cluster])

    # Create a List of namespaces
    namespace_names = ["ingress-nginx",
                       "argocd",
                       "monitoring",
                       "production",
                       "staging",
                       "dev"
                       ]

    for name in namespace_names:
        core.v1.Namespace(
            name,
            metadata={
                "name": name,
            },
            opts=opts
        )

    def metrics_server(opts):
        # Load values from the metrics_server/values.yaml file
        with open('eks_services/metrics_server/values.yaml', 'r') as file:
            values = yaml.safe_load(file)

        # Deploy the metrics_server Helm chart using the loaded values
        metrics_server_chart = Release(
            "metrics-server",
            ReleaseArgs(
                chart="metrics-server",
                version="3.12.0",
                repository_opts=RepositoryOptsArgs(
                    repo="https://kubernetes-sigs.github.io/metrics-server",
                ),
                values=values,
                namespace="monitoring"
            ),
            opts=opts,
        )

    def ingress_nginx(opts):
        # Load values from the nginx_ingress/values.yaml file
        with open('eks_services/nginx_ingress/values.yaml', 'r') as file:
            values = yaml.safe_load(file)

        nginx_ingress_chart = Release(
            "ingress-nginx",
            ReleaseArgs(
                chart="ingress-nginx",
                version="4.9.1",
                repository_opts=RepositoryOptsArgs(
                    repo="https://kubernetes.github.io/ingress-nginx",
                ),
                values=values,
                namespace="ingress-nginx",
            ),
            opts=opts
        )

    metrics_server(opts)
    ingress_nginx(opts)
