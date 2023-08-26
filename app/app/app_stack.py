from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_lambda as lambda_
)
from constructs import Construct

class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "yagr-cdk-serverless-demo-bucket", auto_delete_objects=True, removal_policy=RemovalPolicy.DESTROY)
        handler = lambda_.Function(self, "cdk-serverless-demo",
                    runtime=lambda_.Runtime.NODEJS_18_X,
                    code=lambda_.Code.from_asset("resources/code.zip"),
                    handler="index.handler",
                    environment=dict(
                    BUCKET=bucket.bucket_name)
                    )
        bucket.grant_read_write(handler)
        api = apigateway.RestApi(self, "yagr-cdk-serverless-demo-api",
                  rest_api_name="demo service",
                  description="This service serves widgets.")

        api_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", api_integration)   # GET /