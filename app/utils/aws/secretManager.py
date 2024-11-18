import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Function to start the database, using AWS SECRET MANAGER for database controls and encryption in the application
class SecretManager:
    def get_secrets(secret:str):
        secret_name = secret
        region_name = 'us-east-1'

        # In this case, I prefer to use the credentials directly to facilitate access in this test
        # But, this profile only accesses the AWS SECRET MANAGER service to read credentials
        aws_access_key_id = 'AKIAY4SEKHGV2L5WAPHK'
        aws_secret_access_key = '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'

        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        client = session.client(service_name='secretsmanager', region_name=region_name)

        try:

            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"AWS credentials error: {e}")
            raise
        except ClientError as e:
            print(f"Error into AWS Secret Manager: {e}")
            raise

        secret = json.loads(get_secret_value_response['SecretString'])
        return secret