## Description of what this Pulumi IaC code do [AWS Amazon Cloud]
![Alt text for the image](./pulumi-pic.png)

### Versions
Pulumi version: `3.105.0`  
Python version: `3.11`  
Pip version: `24.0`

### Install additional Pulumi packages
EKS Package (https://github.com/pulumi/pulumi-eks)

### Pulumi plugins versions
```bash
pulumi plugin ls
NAME        KIND      VERSION  SIZE    INSTALLED       LAST USED
aws         resource  6.20.1   604 MB  52 seconds ago  46 seconds ago
eks         resource  2.2.1    87 MB   55 seconds ago  55 seconds ago
kubernetes  resource  4.7.1    92 MB   55 seconds ago  55 seconds ago
```

### Pulumi project name: `pulumi-ec2`
It's configured in `Pulumi.yaml` -> `name: pulumi-ec2`

Folder structure:
```bash
├── Pulumi.dev.yaml
├── Pulumi.prod.yaml
├── Pulumi.yaml
├── README.md
├── __main__.py
├── ec2_generic
│   ├── __init__.py
│   ├── __pycache__
│   └── ec2_generic.py
├── ec2_vpn
│   ├── __init__.py
│   ├── __pycache__
│   └── ec2_vpn.py
├── ecr
│   ├── __init__.py
│   ├── __pycache__
│   └── ecr.py
├── eks
│   ├── README.md
│   ├── __init__.py
│   ├── __pycache__
│   └── eks.py
├── iam
│   ├── __init__.py
│   ├── __pycache__
│   └── iam.py
├── pulumi-pic.png
├── rds
│   ├── __init__.py
│   ├── __pycache__
│   └── rds.py
├── s3
│   ├── __init__.py
│   ├── __pycache__
│   └── s3.py
└── vpc
    ├── __init__.py
    ├── __pycache__
    └── vpc.py
```

This is very simple Pulumi (Python 3.11) program which do next: 
1. In `us-east-1` region provision VPC, public subnets, IGW, routing table and does table associations and attach IGW to VPC.
2. Create AWS EC2 instance of type `t2.micro` in the VPC we created previously, create SG and configure it, and run `user-data` on the server after it's up & running.  
3. `user-data` Git clones repo (https://github.com/junoteam/wg-ansible-playbook.git) which contain simple Ansible playbooks to install and enable IPtables and then install Wireguard server.
4. Create 3 AWS S3 buckets for a demo purpose. 
5. Create AWS RDS Instance for a demo purpose. Including private subnets (`vpc.py` module), subnet group and security group for database.
6. It includes `iam.py` module which creates Instance Profile to attach SSM policy to EC2 instance, to have access to EC2 via SSM.

### Export `sensitive vars` and set value via Pulumi CLI
```bash
# SSH key for AWS EC2 instance
export SSH_KEY_PATH="/<path_to_your_key>/.ssh/<your_key>.pub"
pulumi config set --secret pulumi-ec2:sshKeyPath $SSH_KEY_PATH

# Secrets for AWS RDS Instance:
pulumi config set --secret pulumi-ec2:rds-password <db_password>
pulumi config set --secret pulumi-ec2:username <db_user>
```

### Check your `stack`
```bash
pulumi stack ls
```

### Select `dev` stack (in my case)
```bash
pulumi stack select dev
```

### Check currently active `stack`
```bash
pulumi stack
Current stack is dev:
    Owner: Alex
    Last updated: 38 minutes ago (2024-02-08 17:32:39.643438 +0200 IST)
    Pulumi version used: v3.105.0
Current stack resources (0):
    No resources currently in this stack
```

### Preview changes
```bash
pulumi preview
```

### Launch cloud resources deployment
```bash
pulumi up
``` 

### Destroy cloud resources
```bash
pulumi destroy
```
