import boto3
import os
from dataclasses import dataclass

AWS_REGION = os.getenv('AWS_REGION')
AWS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET = os.getenv('AWS_SECRET_ACCESS_KEY')


@dataclass
class AWSConnection:
    aws_region = os.getenv('AWS_REGION')
    aws_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_default_region = os.getenv('AWS_DEFAULT_REGION')

    def _create_session(self):
        if not all([self.aws_region, self.aws_key_id, self.aws_secret]):
            raise ValueError(
                "As variáveis de ambiente AWS_REGION, AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY devem estar configuradas.")

        session = boto3.Session(
            region_name=self.aws_region,
            aws_access_key_id=self.aws_key_id,
            aws_secret_access_key=self.aws_secret
        )
        return session

    def get_resource(self, service_name: str):
        session = self._create_session()
        resource_client = session.resource(service_name, region_name=self.aws_default_region)
        return resource_client

    def get_client(self, service_name: str):
        session = self._create_session()
        client = session.client(service_name, region_name=self.aws_default_region)
        return client