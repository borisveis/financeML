from aws_cdk import core
from aws_cdk import aws_s3 as s3
class MyCdkProjectStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define an S3 bucket
        s3.Bucket(self,
                  "MyFirstBucket",
                  versioned=True,
                  removal_policy=core.RemovalPolicy.DESTROY)