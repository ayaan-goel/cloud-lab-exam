# ☁️ AWS Lab — Complete Step-by-Step Guide
### Flask Notes App | EC2 + RDS MySQL + S3

---

## 📋 Mock Exam Question

> **Design and deploy a simple web-based application on Amazon Web Services (AWS).**
> The application must be:
> - Hosted on an **Amazon EC2** instance (compute)
> - Connected to an **Amazon RDS (MySQL)** database to store application data
> - Configured to use **Amazon S3** for storing static files or user-uploaded content
> - **Publicly accessible** via the EC2 instance's public IP or DNS on port 5000
>
> Demonstrate the running application in the browser and show that data is being stored in RDS and files are uploaded to S3.

---

## 🔁 Docker Lab vs AWS Lab — Comparison

| Concept | Docker Lab | AWS Lab |
|---|---|---|
| **App Host** | Docker container | EC2 Instance |
| **Database** | MongoDB container | RDS MySQL (managed) |
| **File Storage** | Local container | S3 Bucket |
| **Networking** | Docker bridge network | AWS VPC / Security Groups |
| **Registry** | Docker Hub | (EC2 runs directly) |
| **Config** | `docker-compose.yml` | Environment variables + IAM |

---

## 📁 Project Structure

```
aws-lab/
├── app.py              ← Flask Notes app (EC2 + RDS + S3)
├── requirements.txt    ← Python dependencies
├── setup_ec2.sh        ← EC2 bootstrap script
└── README.md           ← This guide
```

---

## 🗺️ Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                         AWS Cloud                            │
│                                                              │
│   User Browser                                               │
│       │                                                      │
│       │  HTTP :5000                                          │
│       ▼                                                      │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              EC2 Instance (t2.micro)                 │    │
│  │         Amazon Linux / Ubuntu                        │    │
│  │                                                      │    │
│  │   Flask App (app.py)  ←── IAM Role                  │    │
│  │         │                     │                     │    │
│  │         │ SQL queries         │ boto3 SDK           │    │
│  │         ▼                     ▼                     │    │
│  │  ┌─────────────┐    ┌──────────────────┐            │    │
│  │  │  RDS MySQL  │    │   S3 Bucket      │            │    │
│  │  │ (Port 3306) │    │ (Image Uploads)  │            │    │
│  │  └─────────────┘    └──────────────────┘            │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│   Security Group: Inbound 5000 (HTTP) + 22 (SSH) open       │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔧 Step 1 — Prerequisites

- **AWS Account** (free tier at [aws.amazon.com](https://aws.amazon.com))
- AWS Console access (browser)
- A key pair `.pem` file for SSH

> [!NOTE]
> All services used (EC2 t2.micro, RDS db.t3.micro, S3) are **free tier eligible** for 12 months.

---

## 🪣 Step 2 — Create an S3 Bucket

1. Go to **AWS Console → S3 → Create Bucket**
2. **Bucket name**: `your-notes-app-bucket` *(must be globally unique)*
3. **Region**: `us-east-1` (or your preferred region)
4. Under **"Block Public Access"** settings:
   - **Uncheck** "Block all public access" *(so images can be viewed publicly)*
   - Confirm the warning checkbox
5. Click **Create Bucket**
6. After creation, go to **Permissions → Bucket Policy** and add:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-notes-app-bucket/*"
    }
  ]
}
```

> Replace `your-notes-app-bucket` with your actual bucket name.

---

## 🗄️ Step 3 — Create an RDS MySQL Database

1. Go to **AWS Console → RDS → Create Database**
2. **Engine**: MySQL
3. **Template**: Free Tier
4. Configure:
   - **DB Instance Identifier**: `notes-db`
   - **Master Username**: `admin`
   - **Master Password**: `YourPassword123` *(remember this!)*
5. **Instance type**: `db.t3.micro`
6. **Storage**: 20 GB (default)
7. **Connectivity**:
   - VPC: Default
   - **Public access**: Yes *(for exam simplicity)*
   - VPC Security group: Create new → name it `rds-sg`
8. Click **Create Database** (takes ~5 min)

### After RDS is created:
- Copy the **Endpoint** (looks like: `notes-db.xxxxxx.us-east-1.rds.amazonaws.com`)
- Edit the `rds-sg` Security Group:
  - Add **Inbound rule**: Type = MySQL/Aurora, Port = 3306, Source = **EC2 Security Group** (or `0.0.0.0/0` for exam)

### Create the database:
```sql
-- Connect via MySQL client or any DB tool:
-- mysql -h <RDS_ENDPOINT> -u admin -p
CREATE DATABASE notesdb;
```

> [!TIP]
> You can also create the database from inside EC2 after you launch it, or the Flask app's `init_db()` function will auto-create the **table** — but you must create the **database** `notesdb` manually first.

---

## 🖥️ Step 4 — Launch an EC2 Instance

1. Go to **AWS Console → EC2 → Launch Instance**
2. Configure:
   - **Name**: `notes-app-server`
   - **AMI**: Ubuntu Server 22.04 LTS (Free Tier)
   - **Instance Type**: `t2.micro` (Free Tier)
   - **Key pair**: Create new → download `notes-key.pem`
3. **Network Settings** → Edit:
   - **Security Group**: Create new → `web-sg`
   - Add rules:
     | Type | Port | Source |
     |---|---|---|
     | SSH | 22 | My IP |
     | Custom TCP | 5000 | 0.0.0.0/0 |
4. **IAM Instance Profile** → Create new role:
   - Go to IAM → Roles → Create Role → EC2
   - Attach policy: `AmazonS3FullAccess`
   - Name: `ec2-s3-role`
   - Back in EC2 launch: select this role
5. Click **Launch Instance**

> [!IMPORTANT]
> The IAM Role lets your EC2 access S3 **without any AWS keys in your code**. This is the correct, secure approach.

---

## 📡 Step 5 — SSH into EC2 and Deploy the App

### Connect from your machine (PowerShell):
```powershell
# Fix key permissions (Windows)
icacls "notes-key.pem" /inheritance:r /grant:r "$($env:USERNAME):(R)"

# SSH into EC2 (replace with your EC2 Public IP)
ssh -i "notes-key.pem" ubuntu@<EC2-PUBLIC-IP>
```

### Inside EC2 — Install dependencies:
```bash
# Update packages
sudo apt update -y && sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3 python3-pip

# Install Git (to clone your code)
sudo apt install -y git
```

### Upload your code (two options):

**Option A — SCP (copy from your machine):**
```powershell
# Run from PowerShell on your machine
scp -i "notes-key.pem" -r "d:\CLOUD_LAB\aws-lab\" ubuntu@<EC2-PUBLIC-IP>:/home/ubuntu/aws-lab
```

**Option B — Git clone (if pushed to GitHub):**
```bash
git clone https://github.com/yourusername/aws-lab.git
cd aws-lab
```

### Install Python dependencies:
```bash
cd aws-lab
pip3 install -r requirements.txt
```

### Set environment variables:
```bash
export DB_HOST="notes-db.xxxxxx.us-east-1.rds.amazonaws.com"
export DB_USER="admin"
export DB_PASSWORD="YourPassword123"
export DB_NAME="notesdb"
export S3_BUCKET="your-notes-app-bucket"
export AWS_REGION="us-east-1"
```

### Run the app:
```bash
python3 app.py
```

### Access it in your browser:
```
http://<EC2-PUBLIC-IP>:5000
```

---

## ✅ Step 6 — Verify Everything Works

### Check the app is running:
```bash
# In a new terminal / SSH session
curl http://localhost:5000
```

### Verify data in RDS:
```bash
# Connect to MySQL from EC2
mysql -h $DB_HOST -u admin -p notesdb
# Enter password

# Check notes table
SELECT * FROM notes;
```

### Verify image in S3:
- Go to **AWS Console → S3 → your-notes-app-bucket**
- You should see uploaded image files listed

---

## 🛑 Step 7 — Stop/Cleanup (Save Free Tier Credits)

```
EC2 Console → Select instance → Instance State → Stop
RDS Console → Select DB → Actions → Stop temporarily
S3 → Empty bucket → Delete bucket (if done)
```

> [!WARNING]
> If you **terminate** (not stop) EC2, you lose all data on it. RDS data is safe even if EC2 is stopped.

---

## 📝 Key AWS Concepts Summary

| Service | Role | Docker Equivalent |
|---|---|---|
| **EC2** | Virtual server running your app | Docker container |
| **RDS MySQL** | Managed relational database | MongoDB container |
| **S3** | Object storage for files/images | Volume mount |
| **Security Group** | Firewall rules (allow port 5000) | `ports:` in docker-compose |
| **IAM Role** | Grants EC2 permission to use S3 | No Docker equivalent (not needed) |
| **VPC** | Isolated private network | Docker bridge network |
| **Public IP** | Access app from browser | `localhost:5000` |

---

## 📸 Screenshots to Take for Submission

1. ✅ EC2 instance showing **Running** state in AWS Console
2. ✅ RDS database showing **Available** state
3. ✅ S3 bucket with uploaded image file
4. ✅ App running at `http://<EC2-IP>:5000` in browser
5. ✅ MySQL query output showing notes in the database

---

> [!TIP]
> The app's `init_db()` auto-creates the `notes` table when Flask starts. You only need to manually create the `notesdb` database in MySQL first.
