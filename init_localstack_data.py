import boto3

CONFIG = {
    "endpoint_url": "http://localhost:4566",
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
    "region_name": "us-east-1"
}

def create_s3_buckets():
    s3 = boto3.client("s3", **CONFIG)

    # Bucket public
    s3.create_bucket(Bucket="public-bucket")
    s3.put_bucket_acl(Bucket="public-bucket", ACL="public-read")

    # Bucket private
    s3.create_bucket(Bucket="private-bucket")

    print("[+] Created 2 buckets: public-bucket (public), private-bucket (private)")

def create_iam_users():
    iam = boto3.client("iam", **CONFIG)

    # User without MFA
    iam.create_user(UserName="user-no-mfa")

    # User with MFA device (giả lập)
    iam.create_user(UserName="user-with-mfa")
    iam.create_virtual_mfa_device(VirtualMFADeviceName="mfa-device")
    iam.enable_mfa_device(
        UserName="user-with-mfa",
        SerialNumber="arn:aws:iam::000000000000:mfa/mfa-device",
        AuthenticationCode1="123456",  # Dummy
        AuthenticationCode2="654321"   # Dummy
    )

    print("[+] Created IAM users: user-no-mfa (❌), user-with-mfa (✅)")

def create_security_groups():
    ec2 = boto3.client("ec2", **CONFIG)
    vpc_id = ec2.describe_vpcs()["Vpcs"][0]["VpcId"]

    # SG mở SSH (22) toàn cầu
    sg1 = ec2.create_security_group(
        GroupName="sg-ssh-open", Description="SSH open", VpcId=vpc_id
    )
    ec2.authorize_security_group_ingress(
        GroupId=sg1["GroupId"],
        IpPermissions=[{
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
        }]
    )

    # SG mở RDP (3389)
    sg2 = ec2.create_security_group(
        GroupName="sg-rdp-open", Description="RDP open", VpcId=vpc_id
    )
    ec2.authorize_security_group_ingress(
        GroupId=sg2["GroupId"],
        IpPermissions=[{
            "IpProtocol": "tcp",
            "FromPort": 3389,
            "ToPort": 3389,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
        }]
    )

    # SG chỉ mở HTTP (80) cho nội bộ
    sg3 = ec2.create_security_group(
        GroupName="sg-http-internal", Description="HTTP internal only", VpcId=vpc_id
    )
    ec2.authorize_security_group_ingress(
        GroupId=sg3["GroupId"],
        IpPermissions=[{
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [{"CidrIp": "10.0.0.0/8"}]
        }]
    )

    print("[+] Created 3 security groups: ssh-open, rdp-open, http-internal")

if __name__ == "__main__":
    create_s3_buckets()
    create_iam_users()
    create_security_groups()
    print("\n✅ Done creating diverse test data in LocalStack.")
