import pulumi_aws as aws
import pulumi


# Func to create ECR Registry
def create_ecr():
    ecr_repo = aws.ecr.Repository("pulumi-ecr-repo",
                                  image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
                                      scan_on_push=True),
                                  image_tag_mutability="MUTABLE",
                                  encryption_configurations=[{
                                      "encryptionType": "AES256",
                                  }],
                                  )

    lifecycle_policy = aws.ecr.LifecyclePolicy("lifecycle-policy",
                                               repository=ecr_repo.name,
                                               policy="""{
                                                "rules": [
                                                    {
                                                        "rulePriority": 1,
                                                        "description": "Expire images older than 30 days",
                                                        "selection": {
                                                            "tagStatus": "any",
                                                            "countType": "sinceImagePushed",
                                                            "countUnit": "days",
                                                            "countNumber": 30
                                                        },
                                                        "action": {
                                                            "type": "expire"
                                                        }
                                                    }
                                                ]
                                            }
                                         """)

    # Export the repository URL
    pulumi.export("ecr_repo_url", ecr_repo.repository_url)
