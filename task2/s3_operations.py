import boto3

class S3Operations:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")

    def add_s3_objects(self,n):
        types = ["image", "audio", "video"]
        sources = ["mobile", "camera"]

        for i in range(1, n+1):

            obj_type = types[(i - 1) % 3]
            source = sources[(i - 1) % 2]

            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=f"{obj_type}_{i}.txt",
                Body=f"This is {obj_type} number {i}",
                Metadata={
                    "source": source
                },
                Tagging=f"Type={obj_type}"
            )


    def fetch_s3_objects_by_tags(self, tag_value):

        result = []
        paginator = self.s3.get_paginator("list_objects_v2")              #object

        for page in paginator.paginate(Bucket=self.bucket_name):

            for obj in page.get("Contents", []):

                key = obj["Key"]

                tags = self.s3.get_object_tagging(
                    Bucket=self.bucket_name,
                    Key=key
                )

                for tag in tags["TagSet"]:
                    if tag["Key"] == "Type" and tag["Value"] == tag_value:
                        result.append(key)
                        break

        with open("filtered_by_tags.txt", "w") as file:
            for key in result:
                file.write(key + "\n")
        return result

    def fetch_s3_objects_by_metadata(self, metadata_value):
        result = []

        paginator = self.s3.get_paginator("list_objects_v2")

        for page in paginator.paginate(Bucket=self.bucket_name):
            for obj in page.get("Contents", []):

                key = obj["Key"]

                details = self.s3.head_object(
                    Bucket=self.bucket_name,
                    Key=key
                )

                if details["Metadata"].get("source") == metadata_value:
                    result.append(key)

        with open("filtered_by_metadata.txt", "w") as file:
            for key in result:
                file.write(key + "\n")
        return result

    def delete_s3_objects_by_tags(self, tag_value):

        objects = self.fetch_s3_objects_by_tags(tag_value)

        if objects:
            self.s3.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    "Objects": [
                        {"Key": key} for key in objects
                    ]
                }
            )

        return objects


    def delete_s3_objects_by_metadata(self, metadata_value):

        objects = self.fetch_s3_objects_by_metadata(metadata_value)

        if objects:
            self.s3.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    "Objects": [
                        {"Key": key} for key in objects
                    ]
                }
            )

        return objects



if __name__ == "__main__":
    bucket_name = "sksh-first-bucket"            

    operations = S3Operations(bucket_name)
    #operations.add_s3_objects(250)
    operations.fetch_s3_objects_by_tags("audio")