# DNS Sinkhole and Honeypot Project

This project demonstrates DNS spoofing by redirecting queries for a malicious domain to a honeypot web server. It integrates a DNS sinkhole (using `dnschef`) with a Flask-based honeypot. The honeypot simulates a fake login page and logs all access attempts and submitted credentials for analysis.

---

## Objective

Demonstrate how DNS spoofing can redirect malicious traffic to a controlled honeypot environment for monitoring and logging.

---

## Components

- **Kali Linux:**
  - Hosts the DNS sinkhole using `dnschef`
  - Spoofs a chosen domain (e.g., `malicious.com`) to the honeypot server

- **Windows:**
  - Runs a Flask web server (`honeypot/`)
  - Hosts a fake login page
  - Logs access attempts and submitted credentials in `logs/honeypot.log`

---

## Technologies

- **Kali Linux:** `dnschef`, terminal-based configuration
- **Windows:** Python 3, Flask, HTML/CSS, managed with VS Code

---

## Repository Structure

```
honeypot/
├── app.py              # Flask application for the honeypot
├── templates/
│   └── index.html      # Fake login page HTML
├── static/
│   └── style.css       # CSS for login page styling
├── logs/
│   └── honeypot.log    # Log file for access and credentials
├── requirements.txt    # Python dependencies (Flask)
└── README.md           # Project documentation
```

---

## Prerequisites

### Kali Linux

- Kali Linux system (VM, live USB, or installed; 2 vCPUs, 4GB RAM recommended)
- `dnschef` package
- Network connectivity to the honeypot machine

### Windows

- Python 3
- Visual Studio Code
- Network connectivity to the sinkhole machine

### Network

- Both systems on the same subnet
- Firewalls allow:
  - Port 53 (Kali, DNS)
  - Port 80 (Windows, HTTP)

---

## Setup Instructions

### 1. Kali Linux - DNS Sinkhole Setup

#### Set IP Address

```sh
ip addr show
sudo ip addr add <kali-ip>/24 dev eth0
sudo ip route add default via <gateway-ip>
```

#### Install dnschef

```sh
sudo apt update
sudo apt install dnschef
dnschef --version
```

#### Configure DNS Resolver

```sh
sudo cp /etc/resolv.conf /etc/resolv.conf.bak
echo 'nameserver 127.0.0.1' | sudo tee /etc/resolv.conf
```

#### Disable NetworkManager DNS

Edit `/etc/NetworkManager/NetworkManager.conf` and add:
```
[main]
dns=none
```
Then restart:
```sh
sudo systemctl restart NetworkManager
```

#### Allow DNS Traffic

```sh
sudo ufw allow 53
sudo ufw reload
```

#### Check and Free Port 53

```sh
sudo netstat -tulnp | grep :53
sudo kill -9 $(sudo lsof -t -i:53)
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
```

#### Start dnschef

```sh
sudo dnschef --fakeip=<honeypot-ip> --fakedomains=malicious.com --nameservers=8.8.8.8 --interface=0.0.0.0
```

**Expected Output:**
```
[*] DNSChef started on interface: 0.0.0.0
[*] Using the following nameservers: 8.8.8.8
[*] Cooking A replies to: <honeypot-ip> for: malicious.com
```

---

### 2. Windows - Honeypot Setup

#### Set IP Address

In Command Prompt (as administrator):
```sh
ipconfig
netsh interface ip set address name="Ethernet" static <honeypot-ip> 255.255.255.0 <gateway-ip>
```

#### Clone Repository

```sh
git clone <your-github-repo-url>
cd honeypot
```

#### Install Dependencies

```sh
pip install -r requirements.txt
```

#### Configure Firewall

In PowerShell (as administrator):

```sh
New-NetFirewallRule -DisplayName "Allow HTTP Port 80" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
```

#### Run Honeypot

In Command Prompt (as administrator):

```sh
python app.py
```

- Visit `http://<honeypot-ip>` in your browser to verify.

---

## Testing the Project

### Verify DNS Spoofing (Kali Linux)

```sh
nslookup malicious.com
# Expected: Address: <honeypot-ip>

nslookup google.com
# Expected: Valid Google IPs
```

### Test Honeypot Integration

- On Kali Linux: Open a browser and visit `http://malicious.com`
- Enter test credentials (e.g., username: `demo`, password: `pass123`) and submit
- On Windows: Check `logs/honeypot.log` for entries like:

```
[Timestamp] - Access from IP: <source-ip>, User-Agent: ...
[Timestamp] - Credentials submitted - IP: <source-ip>, Username: demo, Password: pass123
```

---

## Demo Instructions

### Windows

- Open VS Code, show `app.py` (logging code) and `templates/index.html` (login page)
- Run `python app.py` in Command Prompt (as administrator)

### Kali Linux

- Terminal 1: Run `dnschef` as above
- Terminal 2: Run `nslookup malicious.com` to show sinkhole redirection
- Open browser, visit `http://malicious.com`, submit credentials

### Windows

- Open `logs/honeypot.log` in VS Code to display logged data

---

## Troubleshooting

### dnschef Fails

```sh
sudo netstat -tulnp | grep :53
sudo kill -9 $(sudo lsof -t -i:53)
```

### Honeypot Inaccessible

```sh
netstat -ano | findstr :80
```

Check firewall:
```sh
Get-NetFirewallRule -DisplayName "Allow HTTP Port 80"
```

### Network Issues

```sh
ping <honeypot-ip>  # From Kali
ping <sinkhole-ip>  # From Windows
```

---

## Notes

- Run `dnschef` and `app.py` with administrative privileges.
- Use a Kali live USB if boot issues persist.
- Add `logs/` and `__pycache__/` to `.gitignore`.
- Project tested on Kali Linux 2024.x and Windows 10/11.
- Do not disclose real IP addresses in documentation or demos.

---

## License

This project is for educational purposes and is not licensed for commercial use.
