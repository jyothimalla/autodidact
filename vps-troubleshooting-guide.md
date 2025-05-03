
# 🚀 VPS Setup & Troubleshooting Documentation for `autodidact` Project

## 🐧 System Specs
- **OS:** Ubuntu 24.10 (Linux Kernel 6.11)
- **VPS Specs:** 1 vCPU, 2 GB RAM, 20 GB SSD
- **Disk Usage:** `/dev/sda1` - 40% used (~7.2GB of 19GB)
- **Memory:** 1.9GB RAM, 0 Swap
- **Docker Compose:** used for deploying backend and frontend services

---

## 📌 Common Issues & Fixes

### 1. **SSH Connection Timeout / Broken Pipe**
**Issue:** SSH session exits unexpectedly (`Broken pipe` / `Operation timed out`)

**Fix:** Add the following to the bottom of `/etc/ssh/sshd_config`:
```bash
ClientAliveInterval 60
ClientAliveCountMax 120
```

**Steps to apply:**
```bash
sudo nano /etc/ssh/sshd_config
# Add lines at bottom
sudo systemctl restart ssh
```

---

### 2. **Out of Disk Space During Docker Build**
**Symptoms:**
- `write /usr/lib/...: no space left on device`
- `failed to register layer`
- Docker build fails due to cached images and layers.

**Fix:** Clean up unused Docker data.

```bash
# Remove all stopped containers
docker container prune -f

# Remove all unused volumes
docker volume prune -f

# Remove all unused images
docker image prune -a -f

# Remove all build cache and metadata
docker builder prune -a -f
```

---

### 3. **Docker Compose Warning: `version` is obsolete**
**Message:**
```
the attribute `version` is obsolete, it will be ignored
```

**Fix:** Remove `version:` line from `docker-compose.yml` to avoid confusion.

---

### 4. **Frontend Docker Build Error: No Space in Angular Cache**
**Error:**
```
write /app/.angular/cache/... no space left on device
```

**Fix:**
- Ensure Angular `.cache` and `node_modules` aren't copied unnecessarily.
- Add `.dockerignore` file with:
```dockerignore
node_modules
.angular
dist
```

---

## ✅ Best Practices

- **Use Swap:** Add a swap file if needed.
```bash
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

- **Minimize Docker Layers:** Use `.dockerignore`, and clean builds.

- **Monitor Storage:**
```bash
df -h        # disk usage
free -h      # RAM usage
docker system df
```

- **Optimize Docker Images:** Regularly remove `<none>` images:
```bash
docker image prune -a
```

---

## 🔁 Useful Commands Recap

| Task                         | Command |
|------------------------------|---------|
| Check disk space             | `df -h` |
| Check memory usage           | `free -h` |
| Restart SSH service          | `sudo systemctl restart ssh` |
| Prune Docker images          | `docker image prune -a -f` |
| Prune Docker containers      | `docker container prune -f` |
| Prune Docker volumes         | `docker volume prune -f` |
| Remove Docker builder cache  | `docker builder prune -a -f` |
| Build Docker Compose         | `docker compose up --build` |
