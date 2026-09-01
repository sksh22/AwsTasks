import boto3
import urllib.parse    #Python module used for working with URLs and encoded text

s3 = boto3.client("s3")

def lambda_handler(event, context):

    # Get source bucket name
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]

    # Get uploaded file name
    object_key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])

    # Get destination bucket
    destination_bucket = "sksh-destinationbucket-2026"

    # Copy the file to destination bucket
    s3.copy_object(
        Bucket=destination_bucket,
        Key=object_key,
        CopySource={
            "Bucket": source_bucket,
            "Key": object_key
        }
    )
