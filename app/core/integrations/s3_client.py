from typing import BinaryIO

import aioboto3
from botocore.exceptions import ClientError

from app.core.config import settings
from app.core.exceptions import FailedToUploadFileToS3Exception

__all__ = ["S3Client"]

from app.core.loggers import logger


class S3Client:
    def __init__(self):
        self._boto_session = aioboto3.Session()

    async def upload_file(
        self,
        file: BinaryIO,
        file_path: str,
        bucket_name: str,
    ) -> None:
        logger.info(
            "Uploading file %s to %s bucket in S3", file_path, bucket_name
        )
        async with self._boto_session.client(
            "s3", endpoint_url=settings.AWS_ENDPOINT_URL_CUSTOM
        ) as s3_client:
            try:
                await s3_client.upload_fileobj(
                    file,
                    bucket_name,
                    file_path,
                )
            except ClientError as err:
                logger.error(
                    "Failed to upload file %s to S3: %s", file_path, err
                )
                raise FailedToUploadFileToS3Exception from err
        logger.info(
            "Successfully uploaded file %s to %s bucket in S3",
            file_path,
            bucket_name,
        )
