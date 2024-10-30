from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_s3_deployment as s3deploy,
)
from constructs import Construct

class StaticWebsiteStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Create the S3 Bucket for static site hosting
        website_bucket = s3.Bucket(
            self, 
            "WebsiteBucket",
            bucket_name="jasonteixeira-blog",
            website_index_document="index.html",
            website_error_document="404.html",
            public_read_access=True,
            removal_policy=s3.RemovalPolicy.DESTROY  # Optional: clean up bucket on stack deletion
        )

        # 2. Request ACM Certificate for HTTPS
        domain_name = "jasonteixeira.com"
        cert = acm.Certificate(
            self, 
            "SiteCertificate",
            domain_name=domain_name,
            subject_alternative_names=[f"www.{domain_name}"],
            validation=acm.CertificateValidation.from_dns()
        )

        # 3. Set up CloudFront Distribution
        distribution = cloudfront.Distribution(
            self, 
            "WebsiteDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(website_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            domain_names=[domain_name, f"www.{domain_name}"],
            certificate=cert
        )

        # 4. Configure Route 53 Hosted Zone and DNS Records
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone", domain_name=domain_name
        )

        # A Record for root domain
        route53.ARecord(
            self,
            "AliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(distribution)
            ),
            record_name=domain_name
        )

        # A Record for www subdomain
        route53.ARecord(
            self,
            "WWWAliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(distribution)
            ),
            record_name=f"www.{domain_name}"
        )

        # 5. Deploy static website content to S3
        s3deploy.BucketDeployment(
            self,
            "DeployWebsiteContent",
            sources=[s3deploy.Source.asset("./website-content")],
            destination_bucket=website_bucket,
        )
