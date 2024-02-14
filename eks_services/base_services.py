from pulumi_kubernetes.helm.v3 import Chart, ChartOpts
from pulumi_kubernetes import Provider
import os, pulumi, yaml

print("Current path: ", os.getcwd())

def deploy_basic_services():
    # Load values from the metrics_server/values.yaml file
    with open('eks_services/metrics_server/values.yaml', 'r') as file:
        values = yaml.safe_load(file)

    custom_kubeconfig_path = "./config"
    k8s_provider = Provider("k8s-provider", kubeconfig=custom_kubeconfig_path)

    # Deploy the metrics_server Helm chart using the loaded values
    metrics_server_chart = Chart(
        "metrics-server",
        ChartOpts(
            chart="metrics-server",
            version="3.12.0",
            fetch_opts={
                "repo": "https://kubernetes-sigs.github.io/metrics-server",
            },
            values=values,
        ),
        opts=pulumi.ResourceOptions(provider=k8s_provider),
    )

    # pulumi.export("metrics_server-name", metrics_server_chart.resource_name)
