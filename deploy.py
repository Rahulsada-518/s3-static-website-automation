import boto3
import os
import json

REGION = "ap-south-1"
BUCKET_NAME = "rahul-static-site-sdk-518"

s3 = boto3.client("s3", region_name=REGION)

# Create bucket
s3.create_bucket(
    Bucket=BUCKET_NAME,
    CreateBucketConfiguration={"LocationConstraint": REGION}
)

# Disable block public access
s3.put_public_access_block(
    Bucket=BUCKET_NAME,
    PublicAccessBlockConfiguration={
        "BlockPublicAcls": False,
        "IgnorePublicAcls": False,
        "BlockPublicPolicy": False,
        "RestrictPublicBuckets": False
    }
)

# Enable static website hosting
s3.put_bucket_website(
    Bucket=BUCKET_NAME,
    WebsiteConfiguration={
        "IndexDocument": {"Suffix": "index.html"},
        "ErrorDocument": {"Key": "error.html"}
    }
)

# Add public read bucket policy
policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
    }]
}

s3.put_bucket_policy(
    Bucket=BUCKET_NAME,
    Policy=json.dumps(policy)
)

# Upload website files
for file in os.listdir("website"):
    file_path = os.path.join("website", file)

    content_type = "text/html" if file.endswith(".html") else "text/css"

    s3.upload_file(
        file_path,
        BUCKET_NAME,
        file,
        ExtraArgs={"ContentType": content_type}
    )

print("✅ Website deployed successfully!")
print(f"🌐 URL: http://{BUCKET_NAME}.s3-website.{REGION}.amazonaws.com")