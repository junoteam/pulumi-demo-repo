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
aws eks --region us-east-1 update-kubeconfig --kubeconfig ./config --name $(pulumi stack output cluster-name)
```

### EKS Required IAM Roles and Policies

Data plane  
Role name: `EKS_Worker_Role`
```bash
arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
```

Control plane  
Role name: `EKS_Cluster_Role`
```bash
arn:aws:iam::aws:policy/AmazonEKSServicePolicy
arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
```
