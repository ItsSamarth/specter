# SSTI Template Injection
English: SSTI Template Injection
- Entry Count: 10
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Jinja2 Template Injection
- ID: ssti-jinja2
- Difficulty: advanced
- Subcategory: Jinja2
- Tags: ssti, jinja2, twig, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-jinja2.md
Description:
Jinja2/Twig template injection attack techniques
Prerequisites:
- Uses the Jinja2/Twig template engine
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution
4. 4. Reverse shell
## FreeMarker Template Injection
- ID: ssti-freemarker
- Difficulty: intermediate
- Subcategory: FreeMarker
- Tags: ssti, freemarker, java, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-freemarker.md
Description:
FreeMarker template engine injection attack techniques
Prerequisites:
- Uses the FreeMarker template engine
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution - new
4. 4. Command execution - api
## Velocity Template Injection
- ID: ssti-velocity
- Difficulty: advanced
- Subcategory: Velocity
- Tags: ssti, velocity, java, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-velocity.md
Description:
Velocity template engine injection attack techniques
Prerequisites:
- Uses the Velocity template engine
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution - ClassTool
4. 4. Command execution - reflection
## Thymeleaf Template Injection
- ID: ssti-thymeleaf
- Difficulty: intermediate
- Subcategory: Thymeleaf
- Tags: ssti, thymeleaf, java, spring, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-thymeleaf.md
Description:
Thymeleaf template engine injection attack techniques
Prerequisites:
- Uses the Thymeleaf template engine
- Spring framework
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution - Spring expression
4. 4. Command execution - ProcessBuilder
## Smarty Template Injection
- ID: ssti-smarty
- Difficulty: intermediate
- Subcategory: Smarty
- Tags: ssti, smarty, php, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-smarty.md
Description:
Smarty template engine injection attack techniques
Prerequisites:
- Uses the Smarty template engine
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution - system
4. 4. Command execution - passthru
## Mako Template Injection
- ID: ssti-mako
- Difficulty: intermediate
- Subcategory: Mako
- Tags: ssti, mako, python, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-mako.md
Description:
Mako template engine injection attack techniques
Prerequisites:
- Uses the Mako template engine
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution - os module
4. 4. Command execution - subprocess
## Tornado Template Injection
- ID: ssti-tornado
- Difficulty: intermediate
- Subcategory: Tornado
- Tags: ssti, tornado, python, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-tornado.md
Description:
Tornado template engine injection attack techniques
Prerequisites:
- Uses the Tornado template engine
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution - os
4. 4. Command execution - subprocess
## Django Template Injection
- ID: ssti-django
- Difficulty: intermediate
- Subcategory: Django
- Tags: ssti, django, python, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-django.md
Description:
Django template engine injection attack techniques
Prerequisites:
- Uses the Django template engine
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution - via settings
4. 4. Command execution - object chain
## ERB Template Injection
- ID: ssti-erb
- Difficulty: intermediate
- Subcategory: ERB
- Tags: ssti, erb, ruby, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-erb.md
Description:
ERB (Ruby) template engine injection attack techniques
Prerequisites:
- Uses the ERB template engine
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution - backticks
4. 4. Command execution - system
## Pug/Jade Template Injection
- ID: ssti-pug
- Difficulty: intermediate
- Subcategory: Pug
- Tags: ssti, pug, jade, nodejs, template
- Original Extracted Source: original extracted web-security-wiki source/ssti-pug.md
Description:
Pug/Jade template engine injection attack techniques
Prerequisites:
- Uses the Pug/Jade template engine
- User input is rendered directly into the template
Execution Outline:
1. 1. Probe for SSTI
2. 2. Information gathering
3. 3. Command execution - child_process
4. 4. Command execution - execSync
