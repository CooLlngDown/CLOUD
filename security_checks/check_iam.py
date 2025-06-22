import boto3

def check_iam_mfa():
    iam = boto3.client("iam",
                       endpoint_url="http://localhost:4566",
                       aws_access_key_id="test",
                       aws_secret_access_key="test",
                       region_name="us-east-1")

    users = iam.list_users()["Users"]
    result = []
    for user in users:
        name = user["UserName"]
        mfa = iam.list_mfa_devices(UserName=name)["MFADevices"]
        result.append({"User": name, "MFA_Enabled": len(mfa) > 0})
    
    return result
