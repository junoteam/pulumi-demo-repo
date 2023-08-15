### Export sensitive vars and set value via Pulumi CLI
```bash
export SSH_KEY_PATH="/<path_to_your_key>/.ssh/tf-cloud-init.pub"
pulumi config set pulumi-ec2:sshKeyPath $SSH_KEY_PATH
```

### Check your stack
```bash
pulumi stack ls
```

### Select `dev` stack (in my case)
```bash
pulumi select dev
```

### Preview changes
```bash
pulumi preview

     Type                              Name                         Plan
 +   pulumi:pulumi:Stack               pulumi-ec2-dev               create
 +   ├─ aws:ec2:Vpc                    pulumi-vpc                   create
 +   ├─ aws:ec2:InternetGateway        pulumi-igw                   create
 +   ├─ aws:ec2:RouteTable             public-route-table           create
 +   ├─ aws:ec2:Subnet                 public-subnet-0              create
 +   ├─ aws:ec2:Subnet                 public-subnet-1              create
 +   ├─ aws:ec2:Subnet                 public-subnet-2              create
 +   ├─ aws:ec2:SecurityGroup          web-ssh-sg                   create
 +   ├─ aws:ec2:Route                  public-route                 create
 +   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-0  create
 +   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-1  create
 +   ├─ aws:ec2:RouteTableAssociation  public-subnet-association-2  create
 +   └─ aws:ec2:Instance               pulumi-ec2                   create


Outputs:
    instance_url: output<string>
    private_ip  : output<string>
    public_ip   : output<string>

Resources:
    + 13 to create
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
