import unittest
import boto3
from moto import mock_aws
from s3_operations import S3Operations


class TestS3Operations(unittest.TestCase):

    def setUp(self):                                    #setup and cleanup for each test case
        self.mock = mock_aws()
        self.mock.start()

        self.bucket_name = "test-bucket"
        self.s3 = boto3.client("s3",region_name="us-east-1")
        self.s3.create_bucket(Bucket=self.bucket_name)

        self.operations = S3Operations(self.bucket_name)

    def tearDown(self):
        self.mock.stop()


    # Test 1
    def test_add_s3_objects(self):

        self.operations.add_s3_objects(6)

        result = self.s3.list_objects_v2(
            Bucket=self.bucket_name
        )

        objects = result.get("Contents", [])

        self.assertEqual(len(objects), 6)


    # Test 2
    def test_fetch_s3_objects_by_tags(self):

        self.operations.add_s3_objects(6)

        result = self.operations.fetch_s3_objects_by_tags("image")

        expected = ["image_1.txt", "image_4.txt"]

        self.assertEqual(sorted(result), sorted(expected))


    # Test 3
    def test_fetch_s3_objects_by_metadata(self):

        self.operations.add_s3_objects(6)

        result = self.operations.fetch_s3_objects_by_metadata("mobile")

        expected = ["image_1.txt", "video_3.txt","audio_5.txt"]

        self.assertEqual(sorted(result), sorted(expected))


    # Test 4
    def test_delete_s3_objects_by_tags(self):

        self.operations.add_s3_objects(6)

        deleted = self.operations.delete_s3_objects_by_tags("image")

        expected = ["image_1.txt", "image_4.txt"]

        self.assertEqual(sorted(deleted), sorted(expected))

        remaining_images = self.operations.fetch_s3_objects_by_tags("image")
        self.assertEqual(remaining_images, [])


    # Test 5
    def test_delete_s3_objects_by_metadata(self):

        self.operations.add_s3_objects(6)

        deleted = self.operations.delete_s3_objects_by_metadata("camera")

        expected = ["audio_2.txt","image_4.txt","video_6.txt"]

        self.assertEqual(sorted(deleted), sorted(expected))

        remaining_objects = self.operations.fetch_s3_objects_by_metadata("camera")
        self.assertEqual(remaining_objects, [])


if __name__ == "__main__":
    unittest.main()