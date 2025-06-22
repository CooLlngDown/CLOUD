import boto3

def check_s3_buckets():
    s3 = boto3.client("s3",
                      endpoint_url="http://localhost:4566",
                      aws_access_key_id="test",
                      aws_secret_access_key="test",
                      region_name="us-east-1")
    
    result = []
    buckets = s3.list_buckets()["Buckets"]
    for b in buckets:
        name = b["Name"]
        acl = s3.get_bucket_acl(Bucket=name)
        grants = acl["Grants"]
        public = any("AllUsers" in g["Grantee"].get("URI", "") for g in grants)
        result.append({"Bucket": name, "Public": public})
    
    return result
