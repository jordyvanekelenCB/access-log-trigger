import logging
from io import BytesIO
import gzip

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class AWSS3:

    def __init__(self, aws_event, s3_client):
        self.aws_event = aws_event
        self.s3_client = s3_client

    # entry point
    def getAWSLogFile(self):
        encoded_gzip_lines = self.retrieve_gzip_lines_from_bucket();
        decoded_gzip_lines = self.decode_gzip_file(encoded_gzip_lines);

        return decoded_gzip_lines.decode("utf-8")


    def retrieve_gzip_lines_from_bucket(self):

        # retrieve bucket name and file_key from the S3 event
        bucket_name = self.aws_event['Records'][0]['s3']['bucket']['name']
        file_key = self.aws_event['Records'][0]['s3']['object']['key']

        logger.info('Reading {} from {}'.format(file_key, bucket_name))

        # get the object
        log_obj = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)

        # get encoded gzip file
        gzip_lines = log_obj['Body'].read()

        return gzip_lines

    def decode_gzip_file(self, gzip_lines):

        gzip_file = BytesIO(gzip_lines)

        gzip_file = gzip.GzipFile(fileobj=gzip_file)
        decoded_zip = gzip_file.read()

        return decoded_zip

    pass