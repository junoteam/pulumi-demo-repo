## Description of what this Pulumi IaC code do [AWS Amazon Cloud]
![Alt text for the image](./pulumi-pic.png)

### Versions
Pulumi version: `3.86.0`  
Python version: `3.11`  
Pip version: `3.11`  

### Install additional Pulumi packages
EKS Package (https://github.com/pulumi/pulumi-eks)
```bash
cd <my-pulumi-project>
./venv/bin/pip install -r requirements.txt
```

Folder structure:
```bash
.
├── Pulumi.dev.yaml # main stack
├── Pulumi.prod.yaml
├── Pulumi.yaml
├── README.md
├── __main__.py
├── ec2
│   ├── __init__.py
│   └── ec2.py
├── eks
│   ├── __init__.py
│   └── eks.py
├── iam
│   ├── __init__.py
│   └── iam.py
├── rds
│   ├── __init__.py
│   └── rds.py
├── requirements.txt
├── s3
│   ├── __init__.py
│   └── s3.py
├── venv
└── vpc
    ├── __init__.py
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
    Last updated: 1 week ago (2023-09-26 16:03:04.543055 +0300 IDT)
    Pulumi version used: v3.85.0
Current stack resources (0):
    No resources currently in this stack

More information at: https://app.pulumi.com/<user>/pulumi-ec2/dev

Use `pulumi stack select` to change stack; `pulumi stack ls` lists known ones
```

### Preview changes
```bash
pulumi preview

     Type                              Name                          Plan       Info
 +   pulumi:pulumi:Stack               pulumi-ec2-dev                create     3 messages
 +   ├─ aws:ec2:Vpc                    pulumi-vpc                    create
 +   ├─ aws:ec2:Subnet                 public-subnet-0               create
 +   ├─ aws:ec2:Subnet                 public-subnet-1               create
 +   ├─ aws:ec2:Subnet                 public-subnet-2               create
 +   ├─ aws:ec2:InternetGateway        pulumi-igw                    create
 +   ├─ aws:ec2:RouteTable             public-route-table            create
 +   ├─ aws:ec2:RouteTable             private-route-table           create
 +   ├─ aws:ec2:Subnet                 private-subnet-0              create
 +   ├─ aws:ec2:Subnet                 private-subnet-1              create
 +   ├─ aws:ec2:Subnet                 private-subnet-2              create
 +   ├─ aws:ec2:SecurityGroup          web-ssh-sg                    create
 +   ├─ aws:ec2:Route                  public-route                  create
 +   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-0   create
 +   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-1   create
 +   ├─ aws:ec2:RouteTableAssociation  private-subnet-association-0  create
 +   ├─ aws:ec2:RouteTableAssociation  private-subnet-association-1  create
 +   ├─ aws:ec2:RouteTableAssociation  private-subnet-association-2  create
 +   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-2   create
 +   ├─ aws:iam:Role                   ec2Role                       create
 +   ├─ aws:s3:Bucket                  apple-ofs1fjhf                create
 +   ├─ aws:s3:Bucket                  banana-qvh18ifm               create
 +   ├─ aws:s3:Bucket                  cherry-12r32j6c               create
 +   ├─ aws:ec2:SecurityGroup          pulumi-rds-sg                 create
 +   ├─ aws:rds:SubnetGroup            pulumi-rds-subnet-group       create
 +   ├─ aws:iam:RolePolicyAttachment   rolePolicyAttachment          create
 +   ├─ aws:iam:InstanceProfile        instanceProfile               create
 +   ├─ aws:rds:Instance               pulumi-rds-instance           create
 +   └─ aws:ec2:Instance               pulumi-ec2                    create


Diagnostics:
  pulumi:pulumi:Stack (pulumi-ec2-dev):
    Created bucket with name: apple-ofs1fjhf
    Created bucket with name: banana-qvh18ifm
    Created bucket with name: cherry-12r32j6c

Outputs:
    buckets     : [
        [0]: output<string>
        [1]: output<string>
        [2]: output<string>
    ]
    instance_url: output<string>
    private_ip  : output<string>
    projectName : "pulumi-ec2"
    public_ip   : output<string>

Resources:
    + 29 to create
```

### Launch cloud resources deployment
```bash
pulumi up

     Type                              Name                         Status
 +   pulumi:pulumi:Stack               pulumi-ec2-dev               created (65s)
 +   ├─ aws:ec2:Vpc                    pulumi-vpc                   created (14s)
 +   ├─ aws:ec2:InternetGateway        pulumi-igw                   created (1s)
 +   ├─ aws:ec2:RouteTable             public-route-table           created (2s)
 +   ├─ aws:ec2:Subnet                 public-subnet-1              created (12s)
 +   ├─ aws:ec2:Subnet                 public-subnet-2              created (13s)
 +   ├─ aws:ec2:Subnet                 public-subnet-0              created (13s)
 +   ├─ aws:ec2:SecurityGroup          web-ssh-sg                   created (5s)
 +   ├─ aws:ec2:Route                  public-route                 created (1s)
 +   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-1  created (1s)
 +   ├─ aws:ec2:Instance               pulumi-ec2                   created (33s)
 +   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-0  created (1s)
 +   └─ aws:ec2:RouteTableAssociation  public-subnet-association-2  created (1s)


Outputs:
    instance_url: "ec2-54-82-174-84.compute-1.amazonaws.com"
    private_ip  : "10.0.0.202"
    public_ip   : "54.82.174.84"

Resources:
    + 13 created

Duration: 1m8s
``` 

### Destroy cloud resources
```bash
pulumi destroy

     Type                              Name                         Status
 -   pulumi:pulumi:Stack               pulumi-ec2-dev               deleted
 -   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-0  deleted (2s)
 -   ├─ aws:ec2:Route                  public-route                 deleted (2s)
 -   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-1  deleted (2s)
 -   ├─ aws:ec2:Instance               pulumi-ec2                   deleted (32s)
 -   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-2  deleted (2s)
 -   ├─ aws:ec2:Subnet                 public-subnet-1              deleted (1s)
 -   ├─ aws:ec2:Subnet                 public-subnet-2              deleted (1s)
 -   ├─ aws:ec2:RouteTable             public-route-table           deleted (2s)
 -   ├─ aws:ec2:Subnet                 public-subnet-0              deleted (2s)
 -   ├─ aws:ec2:SecurityGroup          web-ssh-sg                   deleted (3s)
 -   ├─ aws:ec2:InternetGateway        pulumi-igw                   deleted (1s)
 -   └─ aws:ec2:Vpc                    pulumi-vpc                   deleted (1s)


Outputs:
  - instance_url: "ec2-54-82-174-84.compute-1.amazonaws.com"
  - private_ip  : "10.0.0.202"
  - public_ip   : "54.82.174.84"

Resources:
    - 13 deleted

Duration: 41s
```
