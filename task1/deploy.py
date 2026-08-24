import boto3
import zipfile

REGION = "eu-north-1"
s3 = boto3.client("s3", region_name=REGION)
cloudformation = boto3.client("cloudformation", region_name=REGION)

STACK_NAME = "s3-lambda-stack-01"

DEPLOY_BUCKET = "sksh-deploymentbucket-2026"

ZIP_FILE = "lambda_function.zip"


# 1. Create deployment bucket
try:
    s3.create_bucket(
        Bucket=DEPLOY_BUCKET,
        CreateBucketConfiguration={
            "LocationConstraint": REGION
        }
    )
    print("Deployment bucket created.")

except s3.exceptions.BucketAlreadyOwnedByYou:
    print("Deployment bucket already exists.")


# 2. Create ZIP file
with zipfile.ZipFile(ZIP_FILE, "w") as zip_file:
    zip_file.write("lambda_function.py")


# 3. Upload ZIP to deployment bucket
s3.upload_file(
    ZIP_FILE,
    DEPLOY_BUCKET,
    ZIP_FILE
)

print("Lambda ZIP uploaded.")


# 4. Read CloudFormation template
with open("template.yaml", "r") as file:
    template = file.read()


# 5. Create CloudFormation stack
cloudformation.create_stack(
    StackName=STACK_NAME,
    TemplateBody=template,

    Parameters=[
        {
            "ParameterKey": "LambdaCodeBucket",
            "ParameterValue": DEPLOY_BUCKET
        },
        {
            "ParameterKey": "LambdaCodeKey",
            "ParameterValue": ZIP_FILE
        },
        {
            "ParameterKey": "SourceBucketName",
            "ParameterValue": "sksh-sourcebucket-2026"
        },
        {
            "ParameterKey": "DestinationBucketName",
            "ParameterValue": "sksh-destinationbucket-2026"
        }
    ],

    Capabilities=["CAPABILITY_NAMED_IAM"]
)
print("CloudFormation stack creation started.")