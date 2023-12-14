import boto3
import os
import json
from datetime import time , datetime, timedelta

class AwsManager:   
    def __init__(self):
        self.AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')
        
    def create_wake_up_rule(self,wake_up_rules):
        
        #接続情報を参照 
        client = boto3.client(
            'events',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.AWS_DEFAULT_REGION
        )
        
        
        # 日付を取得
        today = datetime.now().strftime('%Y%m%d')
        
        for key,value in wake_up_rules.items():
            
            response = client.put_rule(
                Name=str(today) + "_{}_tree_rule".format(key),
                ScheduleExpression = self.convert_time_to_cron(value),
                State='ENABLED',
                Description='description'
            )
            
            response = client.put_targets(
                Rule=str(today) + "_{}_tree_rule".format(key),
                Targets=[
                    {
                        'Id': '1',
                        'Arn': "rule['arn']",
                        'Input': {"tree_index":key}
                    }
                ]
            )
        
    # def create_rule(self):  # Added 'self' here
    #     client = boto3.client(
    #         'events',
    #         aws_access_key_id=self.AWS_ACCESS_KEY_ID,
    #         aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
    #         region_name=self.AWS_DEFAULT_REGION
    #     )
    #     response = client.put_rule(
    #         Name='my-rule',
    #         ScheduleExpression='cron(0 12 * * ? *)',
    #         State='ENABLED',
    #         Description='This is a one-time rule'
    #     )

    #     # response = client.put_targets(
    #     #     Rule='my-rule',
    #     #     Targets=[
    #     #         {
    #     #             'Id': '1',
    #     #             'Arn': 'arn:aws:lambda:us-west-2:123456789012:function:my-function',
    #     #             'Input': '{ "key1": "value1", "key2": "value2" }'
    #     #         }
    #     #     ]
    #     # )
    def convert_time_to_cron(self,time_str):
        
        # Split the time string into hours, minutes, and seconds
        parts = time_str.split(':')

        # Check if the time string is valid
        if len(parts) != 3:
            raise ValueError("Time must be in HH:MM:SS format")

        # Extract hours and minutes
        hours, minutes, _ = parts

        # Create the cron expression (seconds are ignored in standard cron format)
        cron_expr = f"cron({minutes} {hours} * * ? *)"

        return cron_expr
