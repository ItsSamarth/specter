# SSRF Server-Side Request Forgery
English: SSRF Server-Side Request Forgery
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Basic SSRF Attack
- ID: ssrf-basic
- Difficulty: intermediate
- Subcategory: Basic Attack
- Tags: ssrf, server-side, request
- Original Extracted Source: original extracted web-security-wiki source/ssrf-basic.md
Description:
Basic server-side request forgery attack techniques
Prerequisites:
- A URL input point exists
- The server fetches URLs provided by the user
Execution Outline:
1. 1. Probe for SSRF
2. 2. Scan internal network ports
3. 3. Access internal services
4. 4. Read local files
## AWS Metadata Attack
- ID: ssrf-cloud-aws
- Difficulty: intermediate
- Subcategory: Cloud Metadata
- Tags: ssrf, aws, metadata, cloud
- Original Extracted Source: original extracted web-security-wiki source/ssrf-cloud-aws.md
Description:
Using SSRF to access AWS EC2 instance metadata service
Prerequisites:
- SSRF vulnerability exists
- Target runs on AWS EC2
Execution Outline:
1. 1. Access metadata service
2. 2. Retrieve IAM credentials
3. 3. Retrieve user data
4. 4. Bypass using IMDSv2
## GCP Metadata Attack
- ID: ssrf-cloud-gcp
- Difficulty: intermediate
- Subcategory: GCP Metadata
- Tags: ssrf, gcp, cloud, metadata
- Original Extracted Source: original extracted web-security-wiki source/ssrf-cloud-gcp.md
Description:
Using SSRF to attack Google Cloud metadata service
Prerequisites:
- SSRF vulnerability exists
- Target runs on GCP
Execution Outline:
1. 1. Access metadata service
2. 2. Retrieve access token
3. 3. Retrieve service account information
4. 4. Retrieve project information
## Azure Metadata Attack
- ID: ssrf-cloud-azure
- Difficulty: intermediate
- Subcategory: Azure Metadata
- Tags: ssrf, azure, cloud, metadata
- Original Extracted Source: original extracted web-security-wiki source/ssrf-cloud-azure.md
Description:
Using SSRF to attack Azure metadata service
Prerequisites:
- SSRF vulnerability exists
- Target runs on Azure
Execution Outline:
1. 1. Access metadata service
2. 2. Retrieve access token
3. 3. Retrieve compute information
4. 4. Retrieve network information
## SSRF Protocol Exploitation
- ID: ssrf-protocol
- Difficulty: intermediate
- Subcategory: Protocol Exploitation
- Tags: ssrf, protocol, file, gopher
- Original Extracted Source: original extracted web-security-wiki source/ssrf-protocol.md
Description:
Using various protocols for SSRF attacks
Prerequisites:
- SSRF vulnerability exists
- Server supports multiple protocols
Execution Outline:
1. 1. File protocol
2. 2. Dict protocol
3. 3. Gopher protocol
4. 4. LDAP protocol
## Gopher Protocol Attack
- ID: ssrf-gopher
- Difficulty: advanced
- Subcategory: Gopher Attack
- Tags: ssrf, gopher, redis, mysql
- Original Extracted Source: original extracted web-security-wiki source/ssrf-gopher.md
Description:
Using Gopher protocol to attack internal network services
Prerequisites:
- SSRF vulnerability exists
- Server supports Gopher protocol
Execution Outline:
1. 1. Gopher basic format
2. 2. Attack Redis
3. 3. Attack MySQL
4. 4. Attack FastCGI
## Dict Protocol Attack
- ID: ssrf-dict
- Difficulty: intermediate
- Subcategory: Dict Protocol
- Tags: ssrf, dict, redis, memcached
- Original Extracted Source: original extracted web-security-wiki source/ssrf-dict.md
Description:
Using Dict protocol to probe and attack internal network services
Prerequisites:
- SSRF vulnerability exists
- Server supports Dict protocol
Execution Outline:
1. 1. Dict protocol format
2. 2. Probe Redis
3. 3. Probe Memcached
4. 4. Write file via Redis
## File Protocol Attack
- ID: ssrf-file
- Difficulty: beginner
- Subcategory: File Protocol
- Tags: ssrf, file, lfi, read
- Original Extracted Source: original extracted web-security-wiki source/ssrf-file.md
Description:
Using File protocol to read local files
Prerequisites:
- SSRF vulnerability exists
- Server supports File protocol
Execution Outline:
1. 1. Linux sensitive files
2. 2. Windows sensitive files
3. 3. Web configuration files
4. 4. Cloud environment files
## SSRF Bypass Techniques
- ID: ssrf-bypass
- Difficulty: intermediate
- Subcategory: Bypass Techniques
- Tags: ssrf, bypass, waf, filter
- Original Extracted Source: original extracted web-security-wiki source/ssrf-bypass.md
Description:
Various techniques for bypassing SSRF filters
Prerequisites:
- SSRF vulnerability exists
- Filtering mechanism is in place
Execution Outline:
1. 1. IP format bypass
2. 2. URL parsing discrepancies
3. 3. Redirect bypass
4. 4. DNS rebinding
## DNS Rebinding Attack
- ID: ssrf-dns-rebinding
- Difficulty: advanced
- Subcategory: DNS Rebinding
- Tags: ssrf, dns, rebinding, bypass
- Original Extracted Source: original extracted web-security-wiki source/ssrf-dns-rebinding.md
Description:
Using DNS rebinding to bypass SSRF protections
Prerequisites:
- SSRF vulnerability exists
- DNS resolution validation is in place
Execution Outline:
1. 1. DNS rebinding principles
2. 2. Use public services
3. 3. Self-host DNS server
4. 4. Attack flow
## SSRF Attack on Redis
- ID: ssrf-redis
- Difficulty: intermediate
- Subcategory: Redis Attack
- Tags: ssrf, redis, rce, webshell
- Original Extracted Source: original extracted web-security-wiki source/ssrf-redis.md
Description:
Using SSRF to attack internal Redis service
Prerequisites:
- SSRF vulnerability exists
- Unauthorized Redis exists on internal network
Execution Outline:
1. 1. Probe Redis
2. 2. Write WebShell
3. 3. Write SSH public key
4. 4. Write cron job
## SSRF Attack on MySQL
- ID: ssrf-mysql
- Difficulty: advanced
- Subcategory: MySQL Attack
- Tags: ssrf, mysql, gopher, database
- Original Extracted Source: original extracted web-security-wiki source/ssrf-mysql.md
Description:
Using SSRF to attack internal MySQL service
Prerequisites:
- SSRF vulnerability exists
- MySQL service exists on internal network
- MySQL username is known
Execution Outline:
1. 1. MySQL protocol basics
2. 2. Attack MySQL using Gopher
3. 3. Use tools to generate payload
4. 4. Execute SQL commands
