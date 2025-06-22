from s3_checker import get_public_s3_buckets
from sg_checker import check_insecure_security_groups
from iam_checker import check_users_without_mfa
import json

if __name__ == "__main__":
    print("[*] Checking S3 buckets...")
    public_buckets = get_public_s3_buckets()

    print("[*] Checking Security Groups...")
    insecure_sgs = check_insecure_security_groups()

    print("[*] Checking IAM users without MFA...")
    users_without_mfa = check_users_without_mfa()

    report = {
        "public_s3_buckets": public_buckets,
        "insecure_security_groups": insecure_sgs,
        "users_without_mfa": users_without_mfa
    }

    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("[+] Report saved to report.json")
