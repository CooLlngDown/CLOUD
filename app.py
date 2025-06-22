from flask import Flask, render_template
from security_checks import check_s3, check_iam, check_sg

app = Flask(__name__)

@app.route("/")
def index():
    s3_results = check_s3.check_s3_buckets()
    iam_results = check_iam.check_iam_mfa()
    sg_results = check_sg.check_security_groups()
    
    return render_template("index.html", s3=s3_results, iam=iam_results, sg=sg_results)

if __name__ == "__main__":
    app.run(debug=True)
