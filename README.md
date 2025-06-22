Cloud Security Builder

Cloud Security Builder là một ứng dụng Python đơn giản giúp kiểm tra nhanh các cấu hình bảo mật cơ bản trên AWS — nhưng chạy hoàn toàn trên local bằng [LocalStack](https://localstack.cloud/), không cần tài khoản AWS thật.


- Phát hiện bucket S3 public
- Kiểm tra Security Group mở cổng SSH ra toàn thế giới
- Kiểm tra IAM user chưa bật MFA
- Hiển thị kết quả bằng web UI Flask

Cài đặt yêu cầu
- Python 3.8+
- Docker (để chạy LocalStack)
pip install -r requirements.txt
pip install localstack awscli-local
localstack start
python init_localstack_data.py
python app.py

http://localhost:5000

Để chạy trên Aws
Aws configure
Nhập vào:
AWS Access Key
AWS Secret Key
Region 
Output: json

sửa lại hàm boto3.client thành boto3.client('s3')
