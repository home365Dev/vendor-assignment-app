import boto3
import datetime
from dotenv import find_dotenv, load_dotenv
import os


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET")


class CloudWatchLogger:
    def __init__(self, log_group, log_stream):
        self.log_group = log_group
        self.log_stream = log_stream
        self.client = boto3.client('logs', aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET, region_name='us-east-1')

    def log(self, message):
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        try:
            response = self.client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
                logEvents=[{
                    'timestamp': timestamp,
                    'message': message
                }]
            )
        except Exception as e:
            print(f'Error logging to CloudWatch: {e}')


# logger = CloudWatchLogger(log_group='your-log-group', log_stream='your-log-stream')
# logger.log('This is a test log message')
