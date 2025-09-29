#!/bin/bash
export AWS_REGION=eu-west-2
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_ENDPOINT_URL_CUSTOM=http://localstack:4566
awslocal s3api create-bucket --bucket weather --create-bucket-configuration LocationConstraint=$AWS_REGION --endpoint-url $AWS_ENDPOINT_URL_CUSTOM
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers $1 --log-level info --no-server-header
