### Get Kubeconfig

Get the name of the cluster from AWS Amazon console and run: 
```bash
aws eks --region us-east-1 update-kubeconfig --kubeconfig ./config --name eks-cluster-eksCluster-bc25c89
```

Or take a name of the EKS cluster from the `output` of your Pulumi stack.
For that in your code `eks.py` should be output defined: 
```python
...
pulumi.export('cluster-name', eks_cluster.name)
```
```bash
aws eks --region us-east-1 update-kubeconfig kubeconfig ./config --name $(pulumi stack output cluster-name)
```

