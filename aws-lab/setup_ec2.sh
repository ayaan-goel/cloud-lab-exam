#!/bin/bash
# ─────────────────────────────────────────────────────────────
# EC2 Setup Script — Run this after SSH-ing into your EC2 instance
# Amazon Linux 2023 / Ubuntu 22.04 compatible
# ─────────────────────────────────────────────────────────────

# 1. Update system packages
sudo apt update -y && sudo apt upgrade -y          # Ubuntu
# sudo yum update -y                               # Amazon Linux — use this instead

# 2. Install Python and pip
sudo apt install -y python3 python3-pip git        # Ubuntu
# sudo yum install -y python3 python3-pip git      # Amazon Linux

# 3. Clone your project (replace with your GitHub URL or upload files via SCP)
# git clone https://github.com/yourusername/aws-lab.git
# cd aws-lab

# 4. Install Python dependencies
pip3 install -r requirements.txt

# 5. Set environment variables (replace with your actual values)
export DB_HOST="your-rds-endpoint.rds.amazonaws.com"
export DB_USER="admin"
export DB_PASSWORD="YourPassword123"
export DB_NAME="notesdb"
export S3_BUCKET="your-s3-bucket-name"
export AWS_REGION="us-east-1"

# 6. Run the Flask app on port 5000
python3 app.py

# ── To run persistently in background ────────────────────────
# nohup python3 app.py > app.log 2>&1 &
# echo "App running! PID: $!"
