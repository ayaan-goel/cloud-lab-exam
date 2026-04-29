# 📚 Cloud Computing Viva Preparation Guide
### Virtualization | Migration | AWS Services | General Cloud

---

## SECTION 1 — VIRTUALIZATION

---

### 1.1 What is Virtualization?

**Definition:** Virtualization is the process of creating a software-based (virtual) version of a physical resource — such as a server, storage, network, or OS — so that multiple virtual instances can run on a single physical machine.

**Key Idea:** One physical machine → Many virtual machines (VMs)

**Benefits:**
- Better hardware utilization (resource sharing)
- Cost reduction (fewer physical servers)
- Isolation (each VM is independent)
- Easy backup, snapshot, and recovery
- Fast provisioning of new environments

---

### 1.2 Types of Virtualization

| Type | What is Virtualized | Example |
|---|---|---|
| **Server Virtualization** | Physical server into multiple VMs | VMware, VirtualBox |
| **Desktop Virtualization** | Desktop environments hosted on server | Citrix, VMware Horizon |
| **Network Virtualization** | Physical network into virtual networks | VLAN, SDN, VMware NSX |
| **Storage Virtualization** | Multiple storage devices as one pool | SAN, NAS, AWS EBS |
| **Application Virtualization** | Apps run in isolated containers | Docker, Wine |
| **OS Virtualization** | Multiple OS instances on one kernel | Containers (Linux) |
| **Data Virtualization** | Unified view of data from multiple sources | Denodo |

---

### 1.3 Hypervisor (Virtual Machine Monitor — VMM)

**Definition:** A hypervisor is software/firmware that creates and manages virtual machines. It sits between the hardware and the VMs, allocating resources to each VM.

#### Type 1 Hypervisor — "Bare Metal"

- Runs **directly on physical hardware** (no host OS)
- More efficient, better performance
- Used in **enterprise/production**

| Hypervisor | Vendor |
|---|---|
| VMware ESXi | VMware |
| Microsoft Hyper-V | Microsoft |
| Xen | Open source |
| KVM | Linux kernel |

```
┌──────────────┬──────────────┐
│     VM 1     │     VM 2     │
├──────────────┴──────────────┤
│        Hypervisor           │  ← Type 1 (directly on HW)
├─────────────────────────────┤
│       Physical Hardware     │
└─────────────────────────────┘
```

#### Type 2 Hypervisor — "Hosted"

- Runs **on top of a host OS** (like any other application)
- Easier to set up, used for development/testing
- Slightly slower (extra OS layer)

| Hypervisor | Vendor |
|---|---|
| VirtualBox | Oracle |
| VMware Workstation | VMware |
| Parallels | Parallels |

```
┌──────────────┬──────────────┐
│     VM 1     │     VM 2     │
├──────────────┴──────────────┤
│        Hypervisor           │  ← Type 2 (on top of Host OS)
├─────────────────────────────┤
│          Host OS            │
├─────────────────────────────┤
│       Physical Hardware     │
└─────────────────────────────┘
```

#### Type 1 vs Type 2 — Quick Comparison

| Feature | Type 1 (Bare Metal) | Type 2 (Hosted) |
|---|---|---|
| Runs on | Hardware directly | Host OS |
| Performance | High | Moderate |
| Use case | Servers, Data centers | Dev, Testing |
| Example | ESXi, Hyper-V, KVM | VirtualBox, Workstation |

---

### 1.4 VM vs Container

| Feature | Virtual Machine | Container |
|---|---|---|
| OS | Each VM has its own OS | Shares host OS kernel |
| Size | GBs | MBs |
| Startup | Minutes | Seconds |
| Isolation | Strong (hardware-level) | Process-level |
| Overhead | High | Low |
| Example | VMware, VirtualBox | Docker, Podman |

```
VMs:                        Containers:
┌────┬────┐               ┌────┬────┐
│App │App │               │App │App │
├────┴────┤               ├────┴────┤
│Guest OS │               │Docker  │  ← No separate OS
│Guest OS │               │Engine  │
├─────────┤               ├─────────┤
│Hypervisor│              │Host OS  │
├─────────┤               ├─────────┤
│Hardware │               │Hardware │
└─────────┘               └─────────┘
```

---

### 1.5 Full Virtualization vs Para-Virtualization

| Type | Description | Example |
|---|---|---|
| **Full Virtualization** | Guest OS runs unmodified; hypervisor translates all hardware calls | VMware, VirtualBox |
| **Para-Virtualization** | Guest OS is modified to cooperate with hypervisor; faster | Xen (with modified guest) |
| **Hardware-Assisted** | CPU provides native virtualization support (Intel VT-x, AMD-V) | KVM, modern VMware |

---

## SECTION 2 — CLOUD MIGRATION

---

### 2.1 What is Cloud Migration?

**Definition:** Cloud migration is the process of moving an organization's digital assets — applications, data, infrastructure — from on-premises (local servers) or legacy systems to a cloud environment (AWS, Azure, GCP).

**Why Migrate?**
- Reduce infrastructure costs
- Improve scalability and flexibility
- Better disaster recovery
- Access to managed services (AI, ML, DBs)
- Go global instantly

---

### 2.2 The 7 Rs of Cloud Migration (Migration Strategies)

These are the standard strategies for migrating workloads to the cloud:

| Strategy | Also Called | Description | Use When |
|---|---|---|---|
| **1. Retire** | — | Shut down apps that are no longer needed | Legacy, unused apps |
| **2. Retain** | Revisit | Keep on-premises for now | Apps not ready to migrate |
| **3. Rehost** | Lift & Shift | Move as-is to cloud VMs, no code change | Quick migration needed |
| **4. Relocate** | Hypervisor lift & shift | Move to cloud without changing OS/hypervisor | VMware to VMware Cloud |
| **5. Repurchase** | Drop & Shop | Replace with SaaS alternative | Move CRM to Salesforce |
| **6. Replatform** | Lift, Tinker & Shift | Small optimizations without full redesign | Move DB to RDS |
| **7. Refactor / Re-architect** | — | Fully redesign for cloud-native (microservices) | Long-term, max benefit |

> **Most Common in Exams:** Rehost (Lift & Shift), Replatform, Refactor

---

### 2.3 Types of Migration

#### A. Physical to Virtual (P2V)
- Moving workloads from **physical servers to VMs**
- Example: Moving an app from a Dell server to a VMware VM
- Tool: VMware vCenter Converter

#### B. Virtual to Virtual (V2V)
- Moving VMs **between different hypervisors**
- Example: Moving from VirtualBox to VMware ESXi
- Challenge: Different VM formats (OVF/OVA standard helps)

#### C. Physical to Cloud (P2C)
- Moving on-premises physical servers **directly to cloud**
- Example: Migrating a bare-metal app to EC2
- Tool: AWS Application Migration Service (MGN)

#### D. Cloud to Cloud (C2C)
- Moving from **one cloud provider to another**
- Example: Azure to AWS
- Challenge: Different APIs and services

#### E. On-Premises to Cloud (Lift & Shift)
- Most common type; moving apps **as-is** to cloud VMs
- Minimal code changes
- Tools: AWS SMS, Azure Migrate

#### F. Data Migration
- Moving **databases or data stores** to cloud
- Example: MySQL on-prem → Amazon RDS
- Tools: AWS DMS (Database Migration Service)

#### G. Application Migration
- Moving the **application layer** to cloud
- May involve containerization (Docker) or serverless

---

### 2.4 Migration Phases (General Process)

```
1. ASSESS         2. PLAN           3. MIGRATE        4. OPTIMIZE
─────────────     ─────────────     ─────────────     ─────────────
Discover all      Define scope,     Execute the       Monitor, tune
assets,           timeline,         move using        costs, use
dependencies,     strategy per      tools (AWS        managed
costs             app (7 Rs)        MGN, DMS)         services
```

---

### 2.5 Migration Tools (AWS)

| Tool | Purpose |
|---|---|
| **AWS Migration Hub** | Central place to track all migrations |
| **AWS Application Migration Service (MGN)** | Lift & shift servers to EC2 |
| **AWS Database Migration Service (DMS)** | Migrate databases (homogeneous & heterogeneous) |
| **AWS Schema Conversion Tool (SCT)** | Convert DB schema (e.g., Oracle → MySQL) |
| **AWS DataSync** | Move large amounts of data to S3/EFS |
| **AWS Snowball** | Physical device to transfer petabytes of data |
| **AWS Server Migration Service (SMS)** | Migrate on-prem VMs to AWS |

---

## SECTION 3 — AWS SERVICES (BASICS)

---

### 3.1 Core Compute — EC2 (Elastic Compute Cloud)

**What it is:** Virtual servers in the cloud (like a VM you rent)

**Key Concepts:**

| Term | Meaning |
|---|---|
| **Instance** | A single virtual server |
| **AMI** | Amazon Machine Image — template for OS + software |
| **Instance Type** | CPU/RAM config (t2.micro, t3.medium, etc.) |
| **Key Pair** | SSH login credentials (.pem file) |
| **Security Group** | Virtual firewall — controls inbound/outbound traffic |
| **Elastic IP** | Static public IP address |
| **User Data** | Script that runs on instance launch |

**EC2 Instance Families:**

| Family | Optimized For | Example |
|---|---|---|
| t (General) | Burstable general purpose | t2.micro, t3.small |
| m (General) | Balanced compute/memory | m5.large |
| c (Compute) | CPU-intensive workloads | c5.xlarge |
| r (Memory) | Memory-intensive (DBs) | r5.large |
| p/g (GPU) | ML, graphics | p3.2xlarge |

**Free Tier:** t2.micro — 750 hours/month for 12 months

---

### 3.2 Storage — S3 (Simple Storage Service)

**What it is:** Object storage — store any file (images, videos, backups, static websites) at unlimited scale

**Key Concepts:**

| Term | Meaning |
|---|---|
| **Bucket** | Container for storing files (globally unique name) |
| **Object** | A file stored in S3 (up to 5TB each) |
| **Key** | The filename/path of an object |
| **ACL** | Access Control List — who can read/write |
| **Bucket Policy** | JSON rules for access control |
| **Versioning** | Keep multiple versions of the same file |
| **Static Hosting** | Host a static website directly from S3 |

**S3 Storage Classes:**

| Class | Use Case | Cost |
|---|---|---|
| Standard | Frequently accessed data | Higher |
| Standard-IA | Infrequently accessed | Lower |
| Glacier | Archival (minutes to hours retrieval) | Very low |
| Glacier Deep Archive | Long-term archive (12 hour retrieval) | Lowest |

---

### 3.3 Database — RDS (Relational Database Service)

**What it is:** Managed relational database — AWS handles backups, patching, scaling

**Supported Engines:**
MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Amazon Aurora

**Key Concepts:**

| Term | Meaning |
|---|---|
| **DB Instance** | The database server |
| **Multi-AZ** | Automatic failover to another availability zone |
| **Read Replica** | Read-only copy for scaling reads |
| **Endpoint** | The hostname to connect to your DB |
| **Parameter Group** | DB configuration settings |
| **Subnet Group** | Which VPC subnets RDS can use |

---

### 3.4 Networking — VPC (Virtual Private Cloud)

**What it is:** Your own isolated private network inside AWS

| Term | Meaning |
|---|---|
| **VPC** | Your private network in AWS |
| **Subnet** | Subdivision of VPC (public or private) |
| **Internet Gateway** | Allows VPC to connect to internet |
| **Route Table** | Rules for where network traffic goes |
| **Security Group** | Instance-level firewall (stateful) |
| **NACL** | Subnet-level firewall (stateless) |

---

### 3.5 Other Important AWS Services

| Service | Category | Purpose |
|---|---|---|
| **IAM** | Security | Users, roles, permissions |
| **Lambda** | Compute | Serverless functions (no server to manage) |
| **CloudWatch** | Monitoring | Logs, metrics, alarms |
| **SNS** | Messaging | Push notifications, alerts |
| **SQS** | Messaging | Message queue between services |
| **ELB** | Networking | Load balancer (distributes traffic) |
| **Auto Scaling** | Compute | Automatically add/remove EC2 instances |
| **CloudFront** | CDN | Content delivery network |
| **Route 53** | DNS | Domain name system / DNS routing |
| **DynamoDB** | Database | Managed NoSQL database |
| **ECS/EKS** | Containers | Run Docker/Kubernetes on AWS |
| **Elastic Beanstalk** | PaaS | Deploy apps without managing servers |

---

### 3.6 Cloud Service Models

| Model | Full Name | You Manage | Provider Manages | Example |
|---|---|---|---|---|
| **IaaS** | Infrastructure as a Service | OS, Apps, Data | Hardware, Network | EC2, VirtualBox |
| **PaaS** | Platform as a Service | Apps, Data | OS, Runtime, HW | Elastic Beanstalk, Heroku |
| **SaaS** | Software as a Service | Nothing (just use it) | Everything | Gmail, Salesforce |

---

### 3.7 Cloud Deployment Models

| Model | Description | Example |
|---|---|---|
| **Public Cloud** | Resources owned by provider, shared with public | AWS, Azure, GCP |
| **Private Cloud** | Dedicated to one organization | On-prem VMware cloud |
| **Hybrid Cloud** | Mix of public + private | AWS + on-prem data center |
| **Community Cloud** | Shared by specific group (e.g., government) | GovCloud |
| **Multi-Cloud** | Using multiple public cloud providers | AWS + Azure together |

---

## SECTION 4 — VIVA QUESTIONS & ANSWERS

---

### 🔵 Virtualization Questions

**Q1. What is a hypervisor?**
> A hypervisor (VMM) is software that creates and runs virtual machines by abstracting hardware resources and allocating them to VMs. Type 1 runs on hardware directly; Type 2 runs on a host OS.

**Q2. What is the difference between Type 1 and Type 2 hypervisor?**
> Type 1 (bare metal) runs directly on hardware — faster, used in production (ESXi, KVM). Type 2 (hosted) runs on top of a host OS — slower, used for development (VirtualBox, VMware Workstation).

**Q3. What is full virtualization?**
> Full virtualization allows an unmodified guest OS to run on a hypervisor. The hypervisor translates all hardware instructions. The guest OS doesn't know it's virtualized.

**Q4. What is para-virtualization?**
> Para-virtualization requires modifying the guest OS to be aware it's running on a hypervisor. It communicates directly with the hypervisor using "hypercalls" instead of hardware emulation — making it faster than full virtualization.

**Q5. What is the difference between a VM and a container?**
> VMs virtualize hardware and include a full OS (GBs, minutes to start). Containers share the host OS kernel and are lightweight (MBs, seconds to start). Containers offer less isolation but much better performance.

**Q6. What is a snapshot in virtualization?**
> A snapshot captures the exact state of a VM (memory, disk, settings) at a point in time. You can revert to it later — useful for testing or before major changes.

**Q7. What is live migration?**
> Live migration moves a running VM from one physical host to another without downtime. The VM keeps running while memory pages are copied to the destination. Used in VMware (vMotion) and KVM.

---

### 🟠 Migration Questions

**Q8. What is cloud migration?**
> Cloud migration is the process of moving applications, data, and infrastructure from on-premises or legacy systems to a cloud platform like AWS, Azure, or GCP.

**Q9. What is Lift and Shift migration?**
> Lift and Shift (Rehost) moves applications to the cloud as-is, without modifying the code or architecture. It's the fastest migration strategy but doesn't fully leverage cloud features.

**Q10. What is the difference between Rehost and Refactor?**
> Rehost = move as-is to cloud (no changes). Refactor = completely redesign the app for cloud-native architecture (microservices, serverless). Rehost is faster; Refactor gives maximum long-term benefits.

**Q11. What is P2V migration?**
> Physical to Virtual (P2V) migration moves workloads from physical hardware servers to virtual machines. The tool VMware vCenter Converter is commonly used.

**Q12. What is AWS DMS?**
> AWS Database Migration Service migrates databases to AWS with minimal downtime. It supports homogeneous (MySQL → RDS MySQL) and heterogeneous (Oracle → Aurora) migrations.

**Q13. What is AWS Snowball?**
> AWS Snowball is a physical appliance sent to your data center to transfer large amounts of data (terabytes to petabytes) to AWS S3 when internet transfer would take too long.

---

### 🟢 AWS Questions

**Q14. What is EC2?**
> EC2 (Elastic Compute Cloud) is AWS's virtual server service. You can launch virtual machines (instances) with your choice of OS, CPU, RAM, and storage, and pay per hour/second.

**Q15. What is an AMI?**
> An Amazon Machine Image (AMI) is a template containing the OS, application server, and applications needed to launch an EC2 instance. AWS provides pre-built AMIs (Ubuntu, Amazon Linux) and you can create custom ones.

**Q16. What is S3?**
> S3 (Simple Storage Service) is object storage for storing any type of file. Data is stored in "buckets" and accessed via HTTP. It offers 99.999999999% (11 9s) durability.

**Q17. What is the difference between S3 and EBS?**
> S3 is object storage (accessed via HTTP, not attached to a server, unlimited). EBS (Elastic Block Store) is block storage that attaches directly to an EC2 instance like a hard drive — needed for OS and databases.

**Q18. What is a Security Group in AWS?**
> A Security Group is a virtual firewall for EC2 instances that controls inbound and outbound traffic using rules (port, protocol, source). It is stateful — if you allow inbound traffic, the response is automatically allowed out.

**Q19. What is IAM?**
> IAM (Identity and Access Management) manages who (users, roles, groups) can do what (permissions/policies) on AWS resources. It controls authentication and authorization.

**Q20. What is the difference between IAM User and IAM Role?**
> IAM User = a person with permanent credentials (username/password or access keys). IAM Role = temporary credentials assigned to AWS services (like giving EC2 permission to access S3) without embedding keys in code.

**Q21. What is VPC?**
> A Virtual Private Cloud (VPC) is a logically isolated private network inside AWS where you launch your resources. You control IP ranges, subnets, routing, and security.

**Q22. What is the difference between Public and Private subnet?**
> Public subnet has a route to the Internet Gateway (accessible from internet). Private subnet has no internet route — used for databases and internal services for security.

**Q23. What is RDS?**
> RDS (Relational Database Service) is a managed database service supporting MySQL, PostgreSQL, Oracle, etc. AWS handles backups, patching, and replication — you just use the database.

**Q24. What is the difference between RDS and DynamoDB?**
> RDS = relational (SQL), structured data with fixed schema. DynamoDB = NoSQL, flexible schema, key-value/document store, designed for high-speed, high-scale applications.

**Q25. What is Auto Scaling?**
> Auto Scaling automatically increases or decreases the number of EC2 instances based on traffic/load. It ensures high availability and cost efficiency by scaling out (add instances) and scaling in (remove instances).

**Q26. What is a Load Balancer?**
> An Elastic Load Balancer (ELB) distributes incoming traffic across multiple EC2 instances to prevent any single instance from being overwhelmed, improving availability and fault tolerance.

**Q27. What is CloudWatch?**
> CloudWatch is AWS's monitoring service. It collects logs, metrics (CPU, memory, network), and allows you to set alarms that trigger actions (like scaling or notifications) when thresholds are crossed.

**Q28. What is Lambda?**
> AWS Lambda is a serverless compute service. You upload code (function) and it runs in response to events (HTTP request, file upload, DB change) without managing any server. You pay only for execution time.

**Q29. What is the difference between IaaS, PaaS, and SaaS?**
> IaaS = you manage OS + apps (EC2). PaaS = you manage only apps (Elastic Beanstalk, Heroku). SaaS = you just use the software (Gmail, Salesforce). More "as a service" = less you manage.

**Q30. What are Availability Zones and Regions?**
> A Region is a geographic area (e.g., us-east-1 = N. Virginia). Each region has multiple Availability Zones (AZs) — physically separate data centers. Deploying across AZs ensures fault tolerance.

---

### 🟣 Docker (Bonus from Lab)

**Q31. What is Docker?**
> Docker is a platform for building, packaging, and running applications in containers — lightweight, isolated environments that share the host OS kernel.

**Q32. What is a Dockerfile?**
> A Dockerfile is a text file with instructions to build a Docker image. It specifies the base image, dependencies, files to copy, and the command to run.

**Q33. What is Docker Hub?**
> Docker Hub is a public container registry where you can push (upload) and pull (download) Docker images — similar to GitHub but for containers.

**Q34. What is Docker Compose?**
> Docker Compose is a tool that uses a `docker-compose.yml` file to define and run multi-container applications with a single command (`docker compose up`).

**Q35. How do containers communicate in Docker?**
> Containers on the same Docker network can communicate using their **service/container name** as a hostname. Docker's internal DNS resolves the name to the container's IP automatically.

---

> **Exam Tip 💡:** For any "What is X?" question, answer with: Definition → How it works → Real-world example. Keep answers under 30 seconds when speaking.
