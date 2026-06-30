# AI Baseline Security - Container and Sandbox Escape Practical Methodology

> Source: AISS Green Alliance Large Model Security Smart Chain Community | Extracted from ai-baseline-security.md
> Topic: Container escape/persistence/lateral movement practical methodology

## Twenty. Container and Sandbox Escape Practical Testing Methodology

> Systematic escape and isolation testing for AI application deployment environments (Docker/Sysbox/Daytona/Kubernetes)
> **General container deployment security**: Web application container deployment security check → [web-deployment-security.md §Two](web-deployment-security.md)

### I. Testing Process Overview

```
Information Collection → Environment Identification → Isolation Assessment → Escape Attempts → Persistence Verification → Lateral Movement → Report
```

### II. Information Collection Phase

#### 2.1 Container Runtime Identification

| Detection Item | Command | Basis for Judgment |
|----------------|---------|-------------------|
| Whether inside a container | `cat /proc/1/cgroup` | Contains `docker`/`kubepods`/`containerd` |
| Docker flag file | `ls /.dockerenv` | File exists = Docker container |
| Container runtime type | `cat /proc/1/cgroup \| head` | `sysbox-fs`→Sysbox, `docker`→Docker |
| Kernel version | `uname -r` | Match CVE impact range |
| User Namespace | `cat /proc/self/uid_map` | `0 0 4294967295`→No isolation (dangerous) |
| Capabilities | `cat /proc/self/status \| grep Cap` | Check dangerous capabilities after decoding |
| Seccomp | `cat /proc/self/status \| grep Seccomp` | 0=disabled, 2=filter |
| AppArmor | `cat /proc/self/attr/current` | `unconfined`→No protection |
| Mount points | `mount \| grep -v overlay` | Detect sensitive host path mounts |

#### 2.2 Sysbox-Specific Detection

| Detection Item | Method | Security Impact |
|----------------|--------|----------------|
| CE vs EE version | `sysbox-runc --version` or check UID mapping range | CE shared mapping has cross-tenant risk |
| UID mapping exclusivity | `cat /proc/self/uid_map`, CE typically `0 165536 65536` (shared) | Shared mapping→possible cross-container privilege escalation |
| Virtualized /proc | `ls /proc/sys/net/` | Sysbox virtualization degree |
| Docker-in-Docker | `docker ps 2>/dev/null` | Inner Docker may have no security restrictions |
| /dev/kvm | `ls /dev/kvm` | KVM available→nested virtualization escape |

### III. Isolation Assessment Phase

#### 3.1 Process Isolation

```bash
# PID Namespace check
ps aux   # Can other containers/host processes be seen?
ls /proc/*/cmdline   # Enumerate visible processes

# If PID 1 is not the container init but systemd/dockerd → isolation failed
cat /proc/1/cmdline | tr '\0' ' '
```

#### 3.2 Network Isolation

```bash
# Network interfaces
ip addr   # Check network interfaces and IP ranges
ip route  # Routing table, can other subnets be reached?

# Same-subnet scan (discover neighboring containers)
for i in $(seq 1 254); do
  (ping -c 1 -W 1 $SUBNET.$i &>/dev/null && echo "$SUBNET.$i alive") &
done; wait

# Internal DNS probe
cat /etc/resolv.conf
nslookup kubernetes.default.svc.cluster.local 2>/dev/null
```

#### 3.3 Filesystem Isolation

```bash
# Check host filesystem mounts
mount | grep -E "ext4|xfs|btrfs" | grep -v overlay
findmnt

# Path traversal test
ls -la /var/lib/sysbox/ 2>/dev/null
ls -la /var/lib/docker/ 2>/dev/null
ls -la /run/containerd/ 2>/dev/null

# Symlink escape
ln -s /proc/1/root/etc/shadow /tmp/test_escape
cat /tmp/test_escape 2>&1  # If successful → isolation failed
```

### IV. Escape Test Matrix

| Escape Path | Prerequisite | Risk Level | Test Method |
|-------------|-------------|------------|-------------|
| cgroup release_agent | CAP_SYS_ADMIN + cgroup v1 | Critical | Write release_agent to execute host commands |
| Docker Socket | /var/run/docker.sock exposed | Critical | Create privileged container via API |
| /proc/1/root | PID Namespace not isolated | Critical | Directly read/write host files |
| Privileged container | --privileged mode | Critical | Mount host disk |
| runc fd leak | CVE-2024-21626 | High | Use /proc/self/fd to access host |
| Dirty Pipe | CVE-2022-0847, 5.8≤kernel≤5.16.11 | High | Overwrite read-only files for privilege escalation |
| OverlayFS | CVE-2023-0386, 5.11≤kernel≤6.2 | High | SUID file privilege escalation |
| Sensitive mounts | Host path mounted into container | High | Write host files |
| CAP_DAC_READ_SEARCH | Capability unrestricted | Medium | Read files with open_by_handle_at |
| CAP_SYS_PTRACE | Capability unrestricted | Medium | Inject into host processes |
| Docker-in-Docker | Inner Docker unrestricted | Medium | Create privileged container in inner layer |

### V. Persistence Testing

> Verify feasibility of cross-session persistence attacks in sandboxes (especially applicable to persistent sandboxes like Daytona)

| Test Item | Session 1 Operation | Session 2 Verification | Expected Security Result |
|-----------|--------------------|-----------------------|-------------------------|
| .bashrc backdoor | `echo 'malicious_cmd' >> ~/.bashrc` | Open new shell to check if executed | New session does not inherit/resets |
| Crontab | `echo "* * * * * cmd" \| crontab -` | `crontab -l` | Crontab is cleaned up or unavailable |
| SSH keys | Write to ~/.ssh/authorized_keys | SSH connection test | SSH service unavailable or keys cleaned |
| Background process | `nohup cmd &` | `ps aux \| grep cmd` | Process terminates after session closes |
| File poisoning | Write malicious file to workspace | Whether AI reads and executes it | AI does not auto-execute instructions in files |
| History residue | Enter sensitive command in shell | `cat ~/.bash_history` | History commands cleared across sessions |
| Environment variables | `export SECRET=leaked` | `echo $SECRET` | Environment variables not preserved across sessions |

### VI. Lateral Movement Testing

```
Inside container → Internal network service discovery → Direct access to DB/cache/API → Other tenant sandboxes
                ↓
                Cloud metadata service (169.254.169.254) → IAM credential theft → Cloud resource access
                ↓
                K8s API (kubernetes.default.svc) → Pod list/Secret retrieval
```

| Target | Detection Command | Exploitation Method |
|--------|------------------|---------------------|
| Cloud metadata | `curl 169.254.169.254` | Obtain IAM temporary credentials |
| K8s API | `curl -k https://kubernetes.default.svc` | Enumerate Pods/obtain Secrets |
| K8s ServiceAccount | `cat /var/run/secrets/kubernetes.io/serviceaccount/token` | Authenticate K8s API |
| Internal database | `echo \| nc DB_HOST 5432` | Direct database connection |
| Redis | `redis-cli -h REDIS_HOST ping` | Unauthorized access |
| Docker Registry | `curl http://REGISTRY:5000/v2/_catalog` | Pull sensitive images |

### VII. Defense Verification Checklist

```
[ ] Container runs as non-root user (or User Namespace isolation is effective)
[ ] No unnecessary Capabilities (minimum principle: only required ones such as NET_BIND_SERVICE)
[ ] Seccomp profile is enabled (not disabled)
[ ] AppArmor/SELinux not unconfined
[ ] /var/run/docker.sock not exposed
[ ] Not running with --privileged mode
[ ] No sensitive host path mounts (/, /etc, /var/run)
[ ] Kernel version not affected by known escape CVEs
[ ] cgroup v2 or release_agent is not writable
[ ] PID Namespace isolation is effective (only own processes visible)
[ ] Network Policy/firewall restricts inter-container communication
[ ] 169.254.169.254 metadata service is blocked
[ ] Sensitive data (history/credentials) cleared between sessions
[ ] All user data fully cleared when sandbox is destroyed
[ ] Sysbox uses EE version or exclusive UID mapping
```

---
