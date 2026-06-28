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
## Spring Actuator漏洞
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
## Spring SpEL注入
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
## Spring Cloud漏洞
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
## Struts2远程代码执行
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
## Struts2 OGNL表达式注入
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
## WebLogic远程代码执行
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
## WebLogic T3协议攻击
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
## WebLogic IIOP协议攻击
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
## ThinkPHP远程代码执行
- ID: thinkphp-rce
- Difficulty: intermediate
- Subcategory: ThinkPHP
- Tags: thinkphp, rce, php, framework
- Original Extracted Source: original extracted web-security-wiki source/thinkphp-rce.md
Description:
ThinkPHP框架RCE漏洞
Prerequisites:
- 使用ThinkPHP框架
- 存在漏洞版本
Execution Outline:
1. 1. ThinkPHP 5.x RCE
2. 2. ThinkPHP 5.1.x RCE
3. 3. ThinkPHP 5.0.23 RCE
4. 4. 信息收集
## Laravel远程代码执行
- ID: laravel-rce
- Difficulty: intermediate
- Subcategory: Laravel
- Tags: laravel, rce, php, framework
- Original Extracted Source: original extracted web-security-wiki source/laravel-rce.md
Description:
Laravel框架RCE漏洞
Prerequisites:
- 使用Laravel框架
- 存在漏洞版本或配置
Execution Outline:
1. 1. CVE-2021-3129
2. 2. 调试模式信息泄露
3. 3. .env文件泄露
4. 4. APP_KEY利用
## Apache Shiro反序列化
- ID: shiro-deserialize
- Difficulty: intermediate
- Subcategory: Apache Shiro
- Tags: shiro, deserialization, java, rememberme
- Original Extracted Source: original extracted web-security-wiki source/shiro-deserialize.md
Description:
Apache Shiro RememberMe反序列化漏洞
Prerequisites:
- 使用Apache Shiro
- 存在漏洞版本
Execution Outline:
1. 1. 检测Shiro
2. 2. 使用ysoserial生成payload
3. 3. 发送恶意请求
4. 4. 常见密钥列表
## JBoss漏洞利用
- ID: jboss-vuln
- Difficulty: intermediate
- Subcategory: JBoss
- Tags: jboss, rce, java, deserialization
- Original Extracted Source: original extracted web-security-wiki source/jboss-vuln.md
Description:
JBoss应用服务器漏洞
Prerequisites:
- 使用JBoss服务器
- 存在漏洞版本
Execution Outline:
1. 1. JMXInvokerServlet反序列化
2. 2. JMX Console部署War包
3. 3. BSHDeployer部署
4. 4. 使用工具
## Apache Tomcat漏洞
- ID: tomcat-vuln
- Difficulty: intermediate
- Subcategory: Tomcat
- Tags: tomcat, rce, java, manager
- Original Extracted Source: original extracted web-security-wiki source/tomcat-vuln.md
Description:
Apache Tomcat服务器漏洞利用
Prerequisites:
- 使用Tomcat服务器
- 存在漏洞版本或配置
Execution Outline:
1. 1. Manager App弱口令
2. 2. 部署War包
3. 3. CVE-2020-1938 Ghostcat
4. 4. PUT方法任意文件写入
## Django框架漏洞
- ID: django-vuln
- Difficulty: intermediate
- Subcategory: Django
- Tags: django, python, framework, sql
- Original Extracted Source: original extracted web-security-wiki source/django-vuln.md
Description:
Django框架安全漏洞
Prerequisites:
- 使用Django框架
- 存在漏洞版本
Execution Outline:
1. 1. SQL注入
2. 2. 调试模式信息泄露
3. 3. SECRET_KEY利用
4. 4. 路径遍历
## Flask框架漏洞
- ID: flask-vuln
- Difficulty: intermediate
- Subcategory: Flask
- Tags: flask, python, framework, ssti
- Original Extracted Source: original extracted web-security-wiki source/flask-vuln.md
Description:
Flask框架安全漏洞
Prerequisites:
- 使用Flask框架
- 存在漏洞配置
Execution Outline:
1. 1. SSTI模板注入
2. 2. SECRET_KEY利用
3. 3. 调试模式RCE
4. 4. PIN码绕过
## WebLogic XMLDecoder
- ID: weblogic-xmldecoder
- Difficulty: intermediate
- Subcategory: WebLogic
- Tags: weblogic, xmldecoder, rce
- Original Extracted Source: original extracted web-security-wiki source/weblogic-xmldecoder.md
Description:
利用WebLogic Server中XMLDecoder反序列化漏洞(CVE-2017-10271/CVE-2017-3506)实现远程代码执行
Prerequisites:
- 目标运行WebLogic Server
- 存在/wls-wsat/或/_async/路径
- XMLDecoder组件未被禁用
- WebLogic版本存在漏洞(10.3.6.0/12.1.3.0等)
Execution Outline:
1. 探测WebLogic版本和路径
2. CVE-2017-10271 XMLDecoder RCE
3. CVE-2019-2725 反序列化RCE
4. 写入Webshell获取持久权限

