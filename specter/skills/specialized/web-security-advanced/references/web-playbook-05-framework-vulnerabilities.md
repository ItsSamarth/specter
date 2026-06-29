# Framework Vulnerabilities
English: Framework Vulnerabilities
- Entry Count: 18
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Log4j RCE (Log4Shell)
- ID: log4j-rce
- Difficulty: intermediate
- Subcategory: Log4j
- Tags: log4j, rce, cve-2021-44228, log4shell
- Original Extracted Source: original extracted web-security-wiki source/log4j-rce.md
Description:
Apache Log4j remote code execution vulnerability
Prerequisites:
- Uses Log4j 2.x
- User input is written to the log
Execution Outline:
1. 1. Probe for the vulnerability
2. 2. DNS out-of-band test
3. 3. Build a malicious LDAP server
4. 4. Obtain a shell
## Spring Actuator Vulnerability
- ID: spring-actuator
- Difficulty: intermediate
- Subcategory: Spring
- Tags: spring, actuator, rce, java
- Original Extracted Source: original extracted web-security-wiki source/spring-actuator.md
Description:
Spring Boot Actuator endpoint security vulnerability
Prerequisites:
- Spring Boot application
- Actuator endpoints exposed
Execution Outline:
1. 1. Probe Actuator endpoints
2. 2. Obtain sensitive information
3. 3. Download the heap dump
4. 4. env endpoint RCE
## Fastjson RCE
- ID: fastjson-rce
- Difficulty: advanced
- Subcategory: Fastjson
- Tags: fastjson, rce, deserialization, java
- Original Extracted Source: original extracted web-security-wiki source/fastjson-rce.md
Description:
Alibaba Fastjson deserialization remote code execution
Prerequisites:
- Uses the Fastjson library
- A deserialization point exists
Execution Outline:
1. 1. Probe for Fastjson
2. 2. JNDI injection
3. 3. Stand up a malicious service
4. 4. Bypass the AutoType check
## Spring SpEL Injection
- ID: spring-spel
- Difficulty: intermediate
- Subcategory: Spring SpEL
- Tags: spring, spel, expression, rce
- Original Extracted Source: original extracted web-security-wiki source/spring-spel.md
Description:
Spring Expression Language injection attack
Prerequisites:
- Uses the Spring framework
- A SpEL injection point exists
Execution Outline:
1. 1. Probe for SpEL injection
2. 2. Command execution
3. 3. File read
4. 4. DNS out-of-band
## Spring Cloud Vulnerabilities
- ID: spring-cloud
- Difficulty: advanced
- Subcategory: Spring Cloud
- Tags: spring, cloud, rce, deserialization
- Original Extracted Source: original extracted web-security-wiki source/spring-cloud.md
Description:
Exploitation of Spring Cloud-related vulnerabilities
Prerequisites:
- Uses Spring Cloud
- A vulnerable version is present
Execution Outline:
1. 1. Spring Cloud Gateway RCE
2. 2. Spring Cloud Function SpEL
3. 3. Spring Cloud Netflix
## Struts2 Remote Code Execution
- ID: struts2-rce
- Difficulty: intermediate
- Subcategory: Struts2
- Tags: struts2, rce, java, apache
- Original Extracted Source: original extracted web-security-wiki source/struts2-rce.md
Description:
Apache Struts2 framework RCE vulnerability
Prerequisites:
- Uses the Struts2 framework
- A vulnerable version is present
Execution Outline:
1. 1. S2-045 vulnerability
2. 2. S2-046 vulnerability
3. 3. S2-057 vulnerability
4. 4. S2-061/S2-062 vulnerabilities
## Struts2 OGNL Expression Injection
- ID: struts2-ognl
- Difficulty: advanced
- Subcategory: Struts2 OGNL
- Tags: struts2, ognl, expression, injection
- Original Extracted Source: original extracted web-security-wiki source/struts2-ognl.md
Description:
Detailed walkthrough of Struts2 OGNL expression injection techniques
Prerequisites:
- Uses the Struts2 framework
- An OGNL injection point exists
Execution Outline:
1. 1. OGNL basic syntax
2. 2. Bypassing security restrictions
3. 3. Command execution techniques
4. 4. File operations
## WebLogic Remote Code Execution
- ID: weblogic-rce
- Difficulty: advanced
- Subcategory: WebLogic
- Tags: weblogic, rce, java, oracle
- Original Extracted Source: original extracted web-security-wiki source/weblogic-rce.md
Description:
Oracle WebLogic Server RCE vulnerability
Prerequisites:
- Uses WebLogic Server
- A vulnerable version is present
Execution Outline:
1. 1. CVE-2017-10271
2. 2. CVE-2019-2725
3. 3. CVE-2020-14882
## WebLogic T3 Protocol Attack
- ID: weblogic-t3
- Difficulty: advanced
- Subcategory: WebLogic T3
- Tags: weblogic, t3, deserialization, java
- Original Extracted Source: original extracted web-security-wiki source/weblogic-t3.md
Description:
WebLogic T3 protocol deserialization vulnerability
Prerequisites:
- WebLogic has the T3 port open
- A vulnerable version is present
Execution Outline:
1. 1. Probe the T3 service
2. 2. Attack using tooling
3. 3. Build a malicious T3 request
## WebLogic IIOP Protocol Attack
- ID: weblogic-iiop
- Difficulty: advanced
- Subcategory: WebLogic IIOP
- Tags: weblogic, iiop, deserialization, corba
- Original Extracted Source: original extracted web-security-wiki source/weblogic-iiop.md
Description:
WebLogic IIOP protocol deserialization vulnerability
Prerequisites:
- WebLogic has the IIOP port open
- A vulnerable version is present
Execution Outline:
1. 1. Probe the IIOP service
2. 2. CVE-2020-2551
3. 3. Build an IIOP request
## ThinkPHP Remote Code Execution
- ID: thinkphp-rce
- Difficulty: intermediate
- Subcategory: ThinkPHP
- Tags: thinkphp, rce, php, framework
- Original Extracted Source: original extracted web-security-wiki source/thinkphp-rce.md
Description:
ThinkPHP framework RCE vulnerability
Prerequisites:
- Uses the ThinkPHP framework
- A vulnerable version is present
Execution Outline:
1. 1. ThinkPHP 5.x RCE
2. 2. ThinkPHP 5.1.x RCE
3. 3. ThinkPHP 5.0.23 RCE
4. 4. Information gathering
## Laravel远程代码执行
- ID: laravel-rce
- Difficulty: intermediate
- Subcategory: Laravel
- Tags: laravel, rce, php, framework
- Original Extracted Source: original extracted web-security-wiki source/laravel-rce.md
Description:
Laravel framework RCE vulnerability
Prerequisites:
- Uses the Laravel framework
- A vulnerable version or configuration is present
Execution Outline:
1. 1. CVE-2021-3129
2. 2. Debug mode information disclosure
3. 3. .env file disclosure
4. 4. APP_KEY exploitation
## Apache Shiro反序列化
- ID: shiro-deserialize
- Difficulty: intermediate
- Subcategory: Apache Shiro
- Tags: shiro, deserialization, java, rememberme
- Original Extracted Source: original extracted web-security-wiki source/shiro-deserialize.md
Description:
Apache Shiro RememberMe deserialization vulnerability
Prerequisites:
- Uses Apache Shiro
- A vulnerable version is present
Execution Outline:
1. 1. Detect Shiro
2. 2. Generate a payload with ysoserial
3. 3. Send the malicious request
4. 4. Common key list
## JBoss漏洞利用
- ID: jboss-vuln
- Difficulty: intermediate
- Subcategory: JBoss
- Tags: jboss, rce, java, deserialization
- Original Extracted Source: original extracted web-security-wiki source/jboss-vuln.md
Description:
JBoss application server vulnerabilities
Prerequisites:
- Uses a JBoss server
- A vulnerable version is present
Execution Outline:
1. 1. JMXInvokerServlet deserialization
2. 2. Deploy a War package via JMX Console
3. 3. BSHDeployer deployment
4. 4. Use tooling
## Apache Tomcat漏洞
- ID: tomcat-vuln
- Difficulty: intermediate
- Subcategory: Tomcat
- Tags: tomcat, rce, java, manager
- Original Extracted Source: original extracted web-security-wiki source/tomcat-vuln.md
Description:
Apache Tomcat server exploitation
Prerequisites:
- Uses a Tomcat server
- A vulnerable version or configuration is present
Execution Outline:
1. 1. Manager App weak password
2. 2. Deploy a War package
3. 3. CVE-2020-1938 Ghostcat
4. 4. Arbitrary file write via the PUT method
## Django框架漏洞
- ID: django-vuln
- Difficulty: intermediate
- Subcategory: Django
- Tags: django, python, framework, sql
- Original Extracted Source: original extracted web-security-wiki source/django-vuln.md
Description:
Django framework security vulnerabilities
Prerequisites:
- Uses the Django framework
- A vulnerable version is present
Execution Outline:
1. 1. SQL injection
2. 2. Debug mode information disclosure
3. 3. SECRET_KEY exploitation
4. 4. Path traversal
## Flask框架漏洞
- ID: flask-vuln
- Difficulty: intermediate
- Subcategory: Flask
- Tags: flask, python, framework, ssti
- Original Extracted Source: original extracted web-security-wiki source/flask-vuln.md
Description:
Flask framework security vulnerabilities
Prerequisites:
- Uses the Flask framework
- A vulnerable configuration is present
Execution Outline:
1. 1. SSTI template injection
2. 2. SECRET_KEY exploitation
3. 3. Debug mode RCE
4. 4. PIN code bypass
## WebLogic XMLDecoder
- ID: weblogic-xmldecoder
- Difficulty: intermediate
- Subcategory: WebLogic
- Tags: weblogic, xmldecoder, rce
- Original Extracted Source: original extracted web-security-wiki source/weblogic-xmldecoder.md
Description:
Exploit the XMLDecoder deserialization vulnerability in WebLogic Server (CVE-2017-10271/CVE-2017-3506) to achieve remote code execution
Prerequisites:
- Target runs WebLogic Server
- The /wls-wsat/ or /_async/ path exists
- The XMLDecoder component is not disabled
- The WebLogic version is vulnerable (10.3.6.0/12.1.3.0, etc.)
Execution Outline:
1. Probe the WebLogic version and paths
2. CVE-2017-10271 XMLDecoder RCE
3. CVE-2019-2725 deserialization RCE
4. Write a Webshell to gain persistent access

