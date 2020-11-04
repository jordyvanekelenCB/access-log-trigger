import logging
from io import BytesIO
import gzip
from connection.aws_connection import AWSConnection

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class AWSS3:

    def __init__(self, aws_event):
        self.aws_event = aws_event
        self.boto_s3_client = AWSConnection().get_connection('s3')

    def get_aws_log_file(self):

        # Retrieve gzip file
        encoded_gzip_file = self.retrieve_gzip_file_from_bucket();

        # Decode gzip file
        decoded_gzip_file = self.decode_gzip_file(encoded_gzip_file);

        return decoded_gzip_file.decode("utf-8")

    def retrieve_gzip_file_from_bucket(self):

        # Retrieve bucket name and file-key from the Lambda event
        bucket_name = self.aws_event['Records'][0]['s3']['bucket']['name']
        file_key = self.aws_event['Records'][0]['s3']['object']['key']
        logger.info('Reading {} from {}'.format(file_key, bucket_name))

        # Retrieve the ALB log file from the bucket by file-key
        log_obj = self.boto_s3_client.get_object(Bucket=bucket_name, Key=file_key)

        # get encoded gzip file
        gzip_file = log_obj['Body'].read()

        return gzip_file

    def decode_gzip_file(self, gzip_lines):

        # Convert gzip file to buffer
        gzip_file_buffer = BytesIO(gzip_lines)

        # Compress and decode buffer
        gzip_file_compressed = gzip.GzipFile(fileobj=gzip_file_buffer)
        gzip_file_decoded = gzip_file_compressed.read()

        return gzip_file_decoded
