import boto3

def check_security_groups():
    ec2 = boto3.client("ec2",
                       endpoint_url="http://localhost:4566",
                       aws_access_key_id="test",
                       aws_secret_access_key="test",
                       region_name="us-east-1")
    
    result = []
    response = ec2.describe_security_groups()["SecurityGroups"]
    for sg in response:
        open_ports = []
        for perm in sg["IpPermissions"]:
            if "IpRanges" in perm:
                for ip in perm["IpRanges"]:
                    if ip["CidrIp"] == "0.0.0.0/0":
                        open_ports.append(perm.get("FromPort", "All"))
        result.append({"Group": sg["GroupName"], "OpenToWorld": open_ports})
    
    return result
