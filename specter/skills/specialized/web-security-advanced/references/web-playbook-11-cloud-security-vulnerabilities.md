# Cloud Security Vulnerabilities
English: Cloud Security Vulnerabilities
- Entry Count: 4
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Cloud SSRF to Steal Metadata Credentials
- ID: cloud-ssrf-metadata
- Difficulty: intermediate
- Subcategory: IMDS Attacks
- Tags: Cloud Security, SSRF, AWS, GCP, Azure, IMDS, Metadata
- Original Extracted Source: original extracted web-security-wiki source/cloud-ssrf-metadata.md
Description:
Exploit an SSRF vulnerability to access the Instance Metadata Service (IMDS) of cloud providers (AWS/GCP/Azure) and obtain temporary IAM credentials. With the obtained Access Key, an attacker can take over cloud resources, achieving lateral escalation from a web vulnerability into the cloud environment.
Prerequisites:
- Target runs in a cloud environment
- An SSRF vulnerability exists
- The instance has an IAM role attached
Execution Outline:
1. 1. AWS metadata service probing
2. 2. GCP/Azure metadata exploitation
3. 3. Lateral movement using obtained credentials
4. 4. Deep exploitation — S3 data exfiltration / privilege escalation
## S3 Bucket Misconfiguration Exploitation
- ID: cloud-s3-misconfig
- Difficulty: beginner
- Subcategory: S3 Security
- Tags: Cloud Security, S3, AWS, Misconfiguration, Data Leak
- Original Extracted Source: original extracted web-security-wiki source/cloud-s3-misconfig.md
Description:
Exploit access-control misconfigurations of AWS S3 buckets (public read/write/list) to obtain sensitive data or plant malicious files. Common in static website hosting, log storage, and backup buckets, this can lead to data leakage, website defacement, or supply chain attacks.
Prerequisites:
- Target S3 bucket name is known
- AWS CLI or HTTP access
Execution Outline:
1. 1. S3 bucket name enumeration
2. 2. Permission enumeration
3. 3. Sensitive data search
4. 4. Exploitation validation (static website defacement/XSS)
## AWS IAM Privilege Escalation
- ID: cloud-iam-escalation
- Difficulty: advanced
- Subcategory: IAM Privilege Escalation
- Tags: Cloud Security, AWS, IAM, Privilege Escalation, Privilege Escalation
- Original Extracted Source: original extracted web-security-wiki source/cloud-iam-escalation.md
Description:
After obtaining low-privilege AWS credentials, exploit over-permissive IAM policies (such as iam:PassRole, lambda:CreateFunction, etc.) to escalate privileges to administrator. Covers 20+ known AWS IAM privilege-escalation paths.
Prerequisites:
- AWS credentials already obtained
- Over-permissive entries exist in IAM policies
Execution Outline:
1. 1. Enumerate current permissions
2. 2. iam:PassRole + Lambda privilege escalation
3. 3. Other privilege-escalation paths
4. 4. Automated privilege-escalation tooling
## Kubernetes Container Escape
- ID: cloud-k8s-escape
- Difficulty: expert
- Subcategory: Container Security
- Tags: Cloud Security, Kubernetes, Container Escape, Docker, Privileged Container
- Original Extracted Source: original extracted web-security-wiki source/cloud-k8s-escape.md
Description:
Given an already-obtained Kubernetes Pod shell, exploit misconfigurations (privileged container, host path mounts, high-privilege ServiceAccount) to achieve container escape, then take control of the host or the entire Kubernetes cluster.
Prerequisites:
- A shell inside the Pod is already obtained
- The Pod has misconfigurations
Execution Outline:
1. 1. Container environment reconnaissance
2. 2. Privileged container escape
3. 3. Cluster takeover via ServiceAccount
4. 4. Create a privileged Pod for a reverse shell
