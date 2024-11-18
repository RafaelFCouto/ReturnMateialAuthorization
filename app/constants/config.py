from utils.aws.secretManager import SecretManager

class ConfigDatabase:
    # Get secrets on AWS
    secret = 'dev/rma/postegres'
    secrets = SecretManager.get_secrets(secret)

    DB_HOST = secrets['host']
    DB_NAME = secrets['dbname']
    DB_USER = secrets['username']
    DB_PASSWORD = secrets['password']
    DB_PORT = secrets['port']