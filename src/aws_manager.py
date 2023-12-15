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
                Description='プロセス開始用ルール'
            )
            
            response = client.put_targets(
                Rule=str(today) + "_{}_tree_rule".format(key),
                Targets=[
                    {
                        'Id': '1',
                        'Arn': "arn:aws:lambda:ap-northeast-1:087162124036:function:wake_up_user",
                        'Input': json.dumps({"tree_index": key})
                    }
                ]
            )
            
            # ルールを削除するためのルールを作成
            response = client.put_rule(
                Name=str(today) + "_{}_tree_rule_DELETE".format(key),
                ScheduleExpression = self.convert_time_to_cron_use_delete(value),
                State='ENABLED',
                Description='イベント削除用ルール'
            )
            
        return True
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
    def convert_time_to_cron(self, time_str):
        # 時間文字列を時、分、秒に分割
        parts = time_str.split(':')

        # 時間文字列の形式を確認
        if len(parts) != 3:
            raise ValueError("時間はHH:MM:SSの形式である必要があります")

        # 時と分を取り出す
        hours, minutes, _ = map(int, parts)

        # datetimeオブジェクトに変換
        jst_time = datetime.now().replace(hour=hours, minute=minutes, second=0, microsecond=0)

        # JSTからUTCへの変換（9時間引く）
        utc_time = jst_time - timedelta(hours=9)

        # 時間が負の数になった場合の調整
        utc_hours = utc_time.hour
        utc_minutes = utc_time.minute

        # Cron式を生成（秒は標準のCron形式では無視される）
        cron_expr = f"cron({utc_minutes} {utc_hours} * * ? *)"

        return cron_expr

    def convert_time_to_cron_use_delete(self, time_str):
        # 時間文字列を時、分、秒に分割
        parts = time_str.split(':')

        # 時間文字列の形式を確認
        if len(parts) != 3:
            raise ValueError("時間はHH:MM:SSの形式である必要があります")

        # 時と分を取り出す
        hours, minutes, _ = map(int, parts)

        # datetimeオブジェクトに変換
        jst_time = datetime.now().replace(hour=hours, minute=minutes, second=0, microsecond=0)

        # JSTからUTCへの変換（9時間引く）
        utc_time = jst_time - timedelta(hours=9)
        
        # 二時間足す
        utc_time = utc_time + timedelta(hours=2)

        # 時間が負の数になった場合の調整
        utc_hours = utc_time.hour
        utc_minutes = utc_time.minute

        # Cron式を生成（秒は標準のCron形式では無視される）
        cron_expr = f"cron({utc_minutes} {utc_hours} * * ? *)"

        return cron_expr
