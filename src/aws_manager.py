import boto3
import os
import json
from datetime import time , datetime, timedelta

class AwsManager:   
    def __init__(self):
        self.AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')
        
    def create_wake_up_rule(self,json):
        
        #接続情報を参照 
        client = boto3.client(
            'events',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.AWS_DEFAULT_REGION
        )
        
        #jsonをリストに変換 
        rules = json.loads(json)
        
        # 日付を取得
        today = datetime.now().strftime('%Y%m%d')
        
        for rule in rules:
            response = client.put_rule(
                Name=rule[str(today) + "_{}_tree".format(rule[0])],
                ScheduleExpression=rule['schedule_expression'],
                State='ENABLED',
                Description=rule['description']
            )
            
            response = client.put_targets(
                Rule=rule['name'],
                Targets=[
                    {
                        'Id': '1',
                        'Arn': rule['arn'],
                        'Input': rule['input']
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
