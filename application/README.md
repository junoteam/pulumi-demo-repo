### Deploy

```bash
cd app-chart
helm upgrade --install application ./app-chart --namespace production --kubeconfig ../config
```

List: 
```bash
helm list -A  --kubeconfig config
NAME                   	NAMESPACE    	REVISION	UPDATED                             	STATUS  	CHART                	APP VERSION
application            	production   	3       	2024-02-25 17:16:35.426993 +0200 IST	deployed	application-0.1.0    	1.16.0
ingress-nginx-8dd3aaee 	ingress-nginx	1       	2024-02-22 23:33:19.532731 +0200 IST	deployed	ingress-nginx-4.9.1  	1.9.6
metrics-server-c9c24aa9	monitoring   	1       	2024-02-22 23:33:21.737428 +0200 IST	deployed	metrics-server-3.12.0	0.7.0
```

Business logic should be deployed via ArgoCD in a GitOps way.
Here it's only example.

Remove this application from cluster before running `pulumi destroy`
```bash
helm uninstall application --namespace production --kubeconfig config
```
