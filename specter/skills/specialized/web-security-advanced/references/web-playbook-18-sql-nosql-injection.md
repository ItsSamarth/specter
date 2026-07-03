# SQL/NoSQL Injection
English: SQL/NoSQL Injection
- Entry Count: 17
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## MySQL Injection - Basic Detection
- ID: sqli-mysql-basic
- Difficulty: beginner
- Subcategory: MySQL
- Tags: sqli, mysql, injection, database
- Original Extracted Source: original extracted web-security-wiki source/sqli-mysql-basic.md
Description:
Basic detection and data extraction techniques for MySQL database injection
Prerequisites:
- Target has an SQL injection point
- Backend database is MySQL
- Familiar with basic SQL syntax
Execution Outline:
1. 1. Detect injection point
2. 2. Determine column count
3. 3. Determine display positions
4. 4. Retrieve database information
## MySQL Injection - Advanced Techniques
- ID: sqli-mysql-advanced
- Difficulty: advanced
- Subcategory: MySQL
- Tags: sqli, mysql, advanced, file-read, rce
- Original Extracted Source: original extracted web-security-wiki source/sqli-mysql-advanced.md
Description:
Advanced MySQL injection techniques: file read/write, UDF privilege escalation, command execution
Prerequisites:
- MySQL user has FILE privilege
- Know the absolute path of the web root
- secure_file_priv configuration allows it
Execution Outline:
1. 1. Detect FILE privilege
2. 2. Obtain web root path
3. 3. Read sensitive files
4. 4. Write WebShell
## MSSQL Injection - Basic Detection
- ID: sqli-mssql-basic
- Difficulty: intermediate
- Subcategory: MSSQL
- Tags: sqli, mssql, sqlserver, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-mssql-basic.md
Description:
Microsoft SQL Server database injection techniques
Prerequisites:
- Target has an SQL injection point
- Backend uses MSSQL database
Execution Outline:
1. 1. Detect injection point
2. 2. Retrieve version information
3. 3. Retrieve user information
4. 4. Retrieve database information
## MSSQL Injection - Advanced Techniques
- ID: sqli-mssql-advanced
- Difficulty: advanced
- Subcategory: MSSQL
- Tags: sqli, mssql, xp_cmdshell, rce
- Original Extracted Source: original extracted web-security-wiki source/sqli-mssql-advanced.md
Description:
Advanced MSSQL injection: xp_cmdshell, SP_OACREATE command execution
Prerequisites:
- MSSQL has high privileges
- xp_cmdshell is available or can be enabled
Execution Outline:
1. 1. Detect xp_cmdshell status
2. 2. Enable xp_cmdshell
3. 3. Execute system commands
4. 4. Write WebShell
## Oracle Injection - Basic Detection
- ID: sqli-oracle-basic
- Difficulty: intermediate
- Subcategory: Oracle
- Tags: sqli, oracle, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-oracle-basic.md
Description:
Basic Oracle database injection techniques
Prerequisites:
- Target has an SQL injection point
- Backend uses Oracle database
Execution Outline:
1. 1. Detect injection point
2. 2. Retrieve version information
3. 3. Retrieve user information
4. 4. Retrieve table names
## Oracle Injection - Advanced Techniques
- ID: sqli-oracle-advanced
- Difficulty: advanced
- Subcategory: Oracle
- Tags: sqli, oracle, advanced, rce
- Original Extracted Source: original extracted web-security-wiki source/sqli-oracle-advanced.md
Description:
Advanced Oracle injection techniques: Java stored procedures, UTL_FILE file operations
Prerequisites:
- Oracle high privileges
- Java Virtual Machine available
Execution Outline:
1. 1. Detect Java permissions
2. 2. Create Java execution function
3. 3. UTL_FILE file reading
## PostgreSQL Injection - Basic Detection
- ID: sqli-postgres-basic
- Difficulty: intermediate
- Subcategory: PostgreSQL
- Tags: sqli, postgresql, postgres, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-postgres-basic.md
Description:
PostgreSQL database injection techniques
Prerequisites:
- Target has an SQL injection point
- Backend uses PostgreSQL
Execution Outline:
1. 1. Detect injection point
2. 2. Retrieve version information
3. 3. Retrieve table names
4. 4. Retrieve column names
## SQLite Injection
- ID: sqli-sqlite-basic
- Difficulty: intermediate
- Subcategory: SQLite
- Tags: sqli, sqlite
- Original Extracted Source: original extracted web-security-wiki source/sqli-sqlite-basic.md
Description:
SQLite database injection attacks
Prerequisites:
- SQLite database
- Injection point exists
Execution Outline:
1. 1. Detect injection point
2. 2. Retrieve version
3. 3. Retrieve table names
4. 4. Retrieve table structure
## MongoDB Injection
- ID: sqli-mongodb-basic
- Difficulty: intermediate
- Subcategory: MongoDB
- Tags: nosql, mongodb, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-mongodb-basic.md
Description:
NoSQL database injection attack techniques
Prerequisites:
- Target uses MongoDB
- User input is concatenated into queries
Execution Outline:
1. 1. Detect injection point
2. 2. Bypass authentication
3. 3. Logical operator injection
4. 4. Regex injection
## Redis Unauthorized Access
- ID: sqli-redis
- Difficulty: intermediate
- Subcategory: Redis
- Tags: redis, nosql, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-redis.md
Description:
Redis unauthorized access and command injection
Prerequisites:
- Redis service is accessible
- Unauthorized or weak password
Execution Outline:
1. 1. Probe Redis
2. 2. Unauthorized access
3. 3. Write Webshell
4. 4. Write SSH public key
## Boolean Blind Injection
- ID: sqli-blind
- Difficulty: intermediate
- Subcategory: Blind Injection
- Tags: sqli, blind, boolean
- Original Extracted Source: original extracted web-security-wiki source/sqli-blind.md
Description:
SQL blind injection technique based on boolean conditions
Prerequisites:
- SQL injection exists
- Page has two different responses for true/false conditions
Execution Outline:
1. 1. Confirm blind injection
2. 2. Retrieve database name length
3. 3. Enumerate database name character by character
4. 4. Use tools for automation
## Time-Based Blind Injection
- ID: sqli-time-based
- Difficulty: intermediate
- Subcategory: Blind Injection
- Tags: sqli, blind, time
- Original Extracted Source: original extracted web-security-wiki source/sqli-time-based.md
Description:
SQL blind injection technique based on time delays
Prerequisites:
- SQL injection exists
- Page response time is controllable
Execution Outline:
1. 1. Confirm time-based blind injection
2. 2. Retrieve database name length
3. 3. Extract data character by character
4. 4. Time delay functions for different databases
## Error-Based Injection
- ID: sqli-error-based
- Difficulty: intermediate
- Subcategory: Error-Based Injection
- Tags: sqli, error, extractvalue
- Original Extracted Source: original extracted web-security-wiki source/sqli-error-based.md
Description:
SQL injection that extracts data using error messages
Prerequisites:
- SQL injection exists
- Error messages are displayed on the page
Execution Outline:
1. 1. Confirm error-based injection
2. 2. Retrieve database information
3. 3. Retrieve table names
4. 4. Retrieve data
## Second-Order SQL Injection
- ID: sqli-second-order
- Difficulty: advanced
- Subcategory: Second-Order Injection
- Tags: sqli, second-order, stored
- Original Extracted Source: original extracted web-security-wiki source/sqli-second-order.md
Description:
SQL injection attack triggered after data is stored
Prerequisites:
- Data storage functionality exists
- Stored data is reused in a second query
Execution Outline:
1. 1. Probe for second-order injection
2. 2. Username injection
3. 3. Password reset injection
4. 4. Order/comment injection
## UNION-Based Injection
- ID: sqli-union
- Difficulty: beginner
- Subcategory: UNION Query
- Tags: sqli, union, select
- Original Extracted Source: original extracted web-security-wiki source/sqli-union.md
Description:
Extracting data using UNION SELECT
Prerequisites:
- Injection point exists
- Query results are displayed
Execution Outline:
1. 1. Determine column count
2. 2. Determine display columns
3. 3. Extract data
4. 4. Bypass filters
## Stacked Query Injection
- ID: sqli-stacked
- Difficulty: intermediate
- Subcategory: Stacked Queries
- Tags: sqli, stacked, queries
- Original Extracted Source: original extracted web-security-wiki source/sqli-stacked.md
Description:
Injection that executes multiple SQL statements
Prerequisites:
- Multiple statement execution is supported
- MySQL/PostgreSQL/MSSQL
Execution Outline:
1. 1. Probe stacked queries
2. 2. MySQL stacked queries
3. 3. MSSQL stacked queries
4. 4. PostgreSQL stacked queries
## SQL Injection WAF Bypass
- ID: sqli-waf-bypass
- Difficulty: advanced
- Subcategory: WAF Bypass
- Tags: sqli, waf, bypass
- Original Extracted Source: original extracted web-security-wiki source/sqli-waf-bypass.md
Description:
Techniques for bypassing Web Application Firewalls
Prerequisites:
- Target has an SQL injection point
- WAF protection is in place
Execution Outline:
1. Chunked transfer encoding
2. HTTP Parameter Pollution (HPP)
3. Equivalent function substitution
4. Comma-free injection
