# Supply Chain Attacks
English: Supply Chain Attacks
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## NPM Package Name Typosquatting
- ID: supply-typosquat
- Difficulty: intermediate
- Subcategory: Package Manager Poisoning
- Tags: supply chain, NPM, Typosquatting, package poisoning, postinstall
- Original Extracted Source: original extracted web-security-wiki source/supply-typosquat.md
Description:
By registering malicious packages with names highly similar to popular NPM package names (e.g. lodash→1odash, colors→co1ors), trick developers into installing them by mistake. The malicious package executes a reverse shell, steals environment variables, or plants a backdoor in the install/postinstall hook.
Prerequisites:
- NPM account
- Knowledge of the target project's dependencies
- Malicious package infrastructure
Execution Outline:
1. 1. Reconnaissance of target dependencies
2. 2. Generate typosquatted package names
3. 3. Construct the malicious package
4. 4. Detection and forensics
## CI/CD Pipeline Poisoning
- ID: supply-ci-poison
- Difficulty: advanced
- Subcategory: CI/CD Attacks
- Tags: supply chain, CI/CD, GitHub Actions, Jenkins, Pipeline
- Original Extracted Source: original extracted web-security-wiki source/supply-ci-poison.md
Description:
Attack the CI/CD pipeline through malicious Pull Requests, Actions injection, or build script tampering. The attacker can steal build secrets, poison build artifacts, or plant backdoor code in the deployment process.
Prerequisites:
- Target uses public CI/CD
- Able to submit a PR or Fork
Execution Outline:
1. 1. Identify CI/CD configuration
2. 2. PR-triggered workflow injection
3. 3. Actions expression injection
4. 4. Build artifact poisoning
## Dependency Confusion Attack
- ID: supply-dependency-confusion
- Difficulty: intermediate
- Subcategory: Dependency Confusion
- Tags: supply chain, dependency confusion, NPM, PyPI, Dependency Confusion
- Original Extracted Source: original extracted web-security-wiki source/supply-dependency-confusion.md
Description:
Exploit the resolution priority flaw of package managers between public and private registries. When an enterprise uses internal package names, the attacker registers a package with the same name but a higher version number on the public NPM/PyPI; the package manager preferentially installs the public higher-version package, thereby executing malicious code.
Prerequisites:
- Known target internal package name
- Public registry account
Execution Outline:
1. 1. Discover internal package names
2. 2. Register a package with the same name on the public registry
3. 3. Monitor DNS callbacks to confirm a hit
4. 4. Impact assessment and reporting
