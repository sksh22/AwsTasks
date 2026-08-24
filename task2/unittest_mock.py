import unittest
from unittest.mock import Mock, patch

from s3_operations import S3Operations


class TestS3Operations(unittest.TestCase):

    @patch("s3_operations.boto3.client")
    def test_add_s3_objects(self, mock_client):

        operations = S3Operations("test-bucket")
        operations.add_s3_objects(6)

        mock_s3 = mock_client.return_value
        self.assertEqual(mock_s3.put_object.call_count, 6)


    @patch("s3_operations.boto3.client")
    def test_fetch_s3_objects_by_tags(self, mock_client):

        mock_s3 = mock_client.return_value

        paginator = Mock()
        mock_s3.get_paginator.return_value = paginator

        paginator.paginate.return_value = [{
            "Contents": [
                {"Key": "image_1.txt"},
                {"Key": "audio_2.txt"},
                {"Key": "image_4.txt"}
            ]
        }]

        mock_s3.get_object_tagging.side_effect = [
            {"TagSet": [{"Key": "Type", "Value": "image"}]},
            {"TagSet": [{"Key": "Type", "Value": "audio"}]},
            {"TagSet": [{"Key": "Type", "Value": "image"}]}
        ]

        operations = S3Operations("test-bucket")

        result = operations.fetch_s3_objects_by_tags("image")

        self.assertEqual(
            sorted(result),
            ["image_1.txt", "image_4.txt"]
        )
        


    @patch("s3_operations.boto3.client")
    def test_fetch_s3_objects_by_metadata(self, mock_client):

        mock_s3 = mock_client.return_value

        paginator = Mock()
        mock_s3.get_paginator.return_value = paginator

        paginator.paginate.return_value = [{
            "Contents": [
                {"Key": "image_1.txt"},
                {"Key": "audio_2.txt"},
                {"Key": "video_3.txt"}
            ]
        }]

        mock_s3.head_object.side_effect = [
            {"Metadata": {"source": "mobile"}},
            {"Metadata": {"source": "camera"}},
            {"Metadata": {"source": "mobile"}}
        ]

        operations = S3Operations("test-bucket")

        result = operations.fetch_s3_objects_by_metadata("mobile")

        self.assertEqual(
            sorted(result),
            ["image_1.txt", "video_3.txt"]
        )


    @patch("s3_operations.boto3.client")
    def test_delete_s3_objects_by_tags(self, mock_client):

        mock_s3 = mock_client.return_value
        operations = S3Operations("test-bucket")

        operations.fetch_s3_objects_by_tags = Mock(
            return_value=["image_1.txt", "image_4.txt"]
        )

        result = operations.delete_s3_objects_by_tags("image")

        self.assertEqual(
            result,
            ["image_1.txt", "image_4.txt"]
        )
        self.assertEqual(mock_s3.delete_object.call_count, 2)


    @patch("s3_operations.boto3.client")
    def test_delete_s3_objects_by_metadata(self, mock_client):

        mock_s3 = mock_client.return_value
        operations = S3Operations("test-bucket")

        operations.fetch_s3_objects_by_metadata = Mock(
            return_value=["audio_2.txt", "image_4.txt", "video_6.txt"]
        )

        result = operations.delete_s3_objects_by_metadata("camera")

        self.assertEqual(
            result,
            ["audio_2.txt", "image_4.txt", "video_6.txt"]
        )
        self.assertEqual(mock_s3.delete_object.call_count, 3)


if __name__ == "__main__":
    unittest.main()