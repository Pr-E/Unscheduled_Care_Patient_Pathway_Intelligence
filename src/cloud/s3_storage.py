import io
import json
import logging
import shutil
from pathlib import Path
from typing import Optional

import boto3
import pandas as pd
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

from src.utils.config import AWS_REGION, LOCAL_STORAGE_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class S3Storage:
    """
    S3 storage helper with local fallback.

    Local mode is useful during development.
    S3 mode is used when AWS credentials and bucket are available.
    """

    def __init__(self, bucket_name: str, use_local: bool = False):
        self.bucket_name = bucket_name
        self.local_base = LOCAL_STORAGE_DIR
        self.local_base.mkdir(parents=True, exist_ok=True)
        self.use_local = use_local

        if self.use_local:
            logging.info("S3Storage initialised in LOCAL mode.")
            self.s3 = None
            return

        try:
            self.s3 = boto3.client("s3", region_name=AWS_REGION.strip())
            self.s3.head_bucket(Bucket=self.bucket_name)
            logging.info(f"S3Storage using bucket: {self.bucket_name}")
        except (NoCredentialsError, PartialCredentialsError, ClientError) as error:
            logging.warning(f"S3 unavailable, falling back to local storage: {error}")
            self.use_local = True
            self.s3 = None

    # =====================================================
    # LOCAL HELPERS
    # =====================================================

    def _local_path(self, key: str) -> Path:
        clean_key = key.replace("\\", "/")
        return self.local_base / clean_key

    # =====================================================
    # UPLOAD
    # =====================================================

    def upload_bytes(self, data, key: str, content_type: str = "application/octet-stream") -> str:
        if isinstance(data, str):
            data = data.encode("utf-8")

        if self.use_local:
            path = self._local_path(key)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            logging.info(f"Written locally: {path}")
            return str(path)

        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=data, ContentType=content_type)
        uri = f"s3://{self.bucket_name}/{key}"
        logging.info(f"Uploaded to S3: {uri}")
        return uri

    def upload_file(self, local_path: str, key: str) -> str:
        if self.use_local:
            destination = self._local_path(key)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(local_path, destination)
            logging.info(f"Copied locally: {destination}")
            return str(destination)

        self.s3.upload_file(Filename=local_path, Bucket=self.bucket_name, Key=key)
        uri = f"s3://{self.bucket_name}/{key}"
        logging.info(f"Uploaded file to S3: {uri}")
        return uri

    def upload_dataframe(self, dataframe: pd.DataFrame, key: str) -> str:
        buffer = io.StringIO()
        dataframe.to_csv(buffer, index=False)
        return self.upload_bytes(data=buffer.getvalue(), key=key, content_type="text/csv")

    def upload_json(self, data: dict, key: str) -> str:
        json_string = json.dumps(data, ensure_ascii=False, indent=2)
        return self.upload_bytes(data=json_string, key=key, content_type="application/json")

    # =====================================================
    # LOAD
    # =====================================================

    def load_csv(self, key: str, parse_dates: Optional[list] = None) -> pd.DataFrame:
        if self.use_local:
            path = self._local_path(key)
            if not path.exists():
                raise FileNotFoundError(f"Local CSV not found: {path}")
            return pd.read_csv(path, parse_dates=parse_dates)

        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return pd.read_csv(io.BytesIO(response["Body"].read()), parse_dates=parse_dates)

    def load_json(self, key: str) -> dict:
        if self.use_local:
            path = self._local_path(key)
            if not path.exists():
                raise FileNotFoundError(f"Local JSON not found: {path}")
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)

        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return json.loads(response["Body"].read().decode("utf-8"))

    # =====================================================
    # DISCOVERY
    # =====================================================

    def file_exists(self, key: str) -> bool:
        if self.use_local:
            return self._local_path(key).exists()

        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False

    def get_latest_file(self, prefix: str, keyword: Optional[str] = None) -> str:
        if self.use_local:
            base = self.local_base / prefix
            if not base.exists():
                raise FileNotFoundError(f"Local prefix not found: {base}")

            files = [file for file in base.rglob("*") if file.is_file()]
            if keyword:
                files = [file for file in files if keyword in file.name]

            if not files:
                raise FileNotFoundError(f"No files found for prefix='{prefix}', keyword='{keyword}'")

            latest_file = max(files, key=lambda file: file.stat().st_mtime)
            return str(latest_file.relative_to(self.local_base)).replace("\\", "/")

        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        if "Contents" not in response:
            raise FileNotFoundError(f"No S3 objects found under prefix: {prefix}")

        files = response["Contents"]
        if keyword:
            files = [obj for obj in files if keyword in obj["Key"]]

        if not files:
            raise FileNotFoundError(f"No S3 files found for prefix='{prefix}', keyword='{keyword}'")

        latest_file = max(files, key=lambda obj: obj["LastModified"])
        return latest_file["Key"]