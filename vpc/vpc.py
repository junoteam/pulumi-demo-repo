import pulumi
import pulumi_aws as aws

# Retrieve configuration values from Pulumi configuration
config_vpc = pulumi.Config("pulumi-ec2")
public_subnet_cidrs = config_vpc.require_object("public_subnet_cidrs")
private_subnet_cidrs = config_vpc.require_object("private_subnet_cidrs")
vpc_cidr = config_vpc.require("vpc_cidr")


def create_vpc():
    # Create the VPC
    vpc = aws.ec2.Vpc("pulumi-vpc",
                      cidr_block=vpc_cidr,
                      enable_dns_support=True,
                      enable_dns_hostnames=True,
                      tags={'Name': 'pulumi-vpc'})

    # Create an Internet Gateway
    igw = aws.ec2.InternetGateway("pulumi-igw",
                                  vpc_id=vpc.id,
                                  tags={'Name': 'pulumi-igw'})

    # Create a Route Table for the public subnet
    public_route_table = aws.ec2.RouteTable("public-route-table",
                                            vpc_id=vpc.id,
                                            tags={'Name': 'pulumi-public-rt'})

    # Add a route to the Route Table that points all traffic (0.0.0.0/0) to the Internet Gateway
    public_route = aws.ec2.Route("public-route",
                                 route_table_id=public_route_table.id,
                                 destination_cidr_block="0.0.0.0/0",
                                 gateway_id=igw.id)

    # Fetch the available AZs in the region
    azs = aws.get_availability_zones()

    # Create public subnets
    public_subnets = []
    for idx, cidr in enumerate(public_subnet_cidrs):
        az_name = azs.names[idx % len(azs.names)]
        public_subnet = aws.ec2.Subnet(f"public-subnet-{idx}",
                                       cidr_block=cidr,
                                       vpc_id=vpc.id,
                                       availability_zone=az_name,
                                       tags={'Name': f'pulumi-public-subnet-{idx}'},
                                       map_public_ip_on_launch=True)
        public_subnets.append(public_subnet)

    # Associate each public subnet with the public route table
    public_subnet_associations = []
    for idx, subnet in enumerate(public_subnets):
        association = aws.ec2.RouteTableAssociation(f"public-subnet-association-{idx}",
                                                    route_table_id=public_route_table.id,
                                                    subnet_id=subnet.id)
        public_subnet_associations.append(association)

    # Create a Route Table for the private subnets
    private_route_table = aws.ec2.RouteTable("private-route-table",
                                             vpc_id=vpc.id,
                                             tags={'Name': 'pulumi-private-rt'})

    # Create private subnets
    private_subnets = []
    for idx, cidr in enumerate(private_subnet_cidrs):
        az_name = azs.names[idx % len(azs.names)]
        private_subnet = aws.ec2.Subnet(f"private-subnet-{idx}",
                                        cidr_block=cidr,
                                        vpc_id=vpc.id,
                                        availability_zone=az_name,
                                        tags={'Name': f'pulumi-private-subnet-{idx}'})
        private_subnets.append(private_subnet)

    # Associate each private subnet with the private route table
    private_subnet_associations = []
    for idx, subnet in enumerate(private_subnets):
        association = aws.ec2.RouteTableAssociation(f"private-subnet-association-{idx}",
                                                    route_table_id=private_route_table.id,
                                                    subnet_id=subnet.id)
        private_subnet_associations.append(association)

    return {
        'vpc': vpc,
        'public_subnets': public_subnets,
        'private_subnets': private_subnets
    }
