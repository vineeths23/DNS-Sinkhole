DNS Sinkhole and Honeypot Project
This project demonstrates a DNS sinkhole integrated with a honeypot to detect and log malicious activity. The DNS sinkhole, running on Kali Linux (192.168.153.136), uses dnschef to redirect queries for malicious.com to a Windows-based honeypot (192.168.153.15). The honeypot, built with Flask, serves a fake login page and logs access attempts and submitted credentials.
Project Structure
honeypot/
├── app.py              # Flask application for the honeypot
├── templates/
│   └── index.html      # HTML for the fake login page
├── static/
│   └── style.css       # CSS for styling the login page
├── logs/
│   └── honeypot.log    # Log file for access and credentials
├── requirements.txt     # Python dependencies
└── README.md           # This file


Kali Linux (DNS Sinkhole): Configured via terminal using dnschef to spoof malicious.com to 192.168.153.15.
Windows (Honeypot): Flask app hosted in VS Code, running on 192.168.153.15, logging to logs/honeypot.log.

Prerequisites

Kali Linux (192.168.153.136):
Kali Linux (VM or live USB, 2 vCPUs, 4GB RAM recommended).
dnschef installed (sudo apt install dnschef).
Network connectivity to 192.168.153.15.


Windows (192.168.153.15):
Python 3 (python.org).
VS Code (code.visualstudio.com).
Network connectivity to 192.168.153.136.


Network: Both systems on the 192.168.153.0/24 subnet, with firewalls allowing port 53 (Kali, DNS) and port 80 (Windows, HTTP).

Setup Instructions
Kali Linux (DNS Sinkhole)

Set IP address:
sudo ip addr add 192.168.153.136/24 dev eth0
sudo ip route add default via 192.168.153.1


Install dnschef:
sudo apt update
sudo apt install dnschef


Configure DNS resolver:
sudo cp /etc/resolv.conf /etc/resolv.conf.bak
echo 'nameserver 127.0.0.1' | sudo tee /etc/resolv.conf


Disable NetworkManager DNS:
sudo nano /etc/NetworkManager/NetworkManager.conf

Add:
[main]
dns=none

Save and restart:
sudo systemctl restart NetworkManager


Allow DNS traffic:
sudo ufw allow 53
sudo ufw reload


Check and free port 53:
sudo netstat -tulnp | grep :53
sudo kill -9 $(sudo lsof -t -i:53)
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved


Start dnschef:
sudo dnschef --fakeip=192.168.153.15 --fakedomains=malicious.com --nameservers=8.8.8.8 --interface=0.0.0.0


Test DNS:
nslookup malicious.com  # Should return 192.168.153.15
nslookup google.com    # Should resolve normally



Windows (Honeypot)

Set IP address:
netsh interface ip set address name="Ethernet" static 192.168.153.15 255.255.255.0 192.168.153.1


Clone or download the repository:
git clone <your-github-repo-url>
cd honeypot


Install dependencies:
pip install -r requirements.txt


Allow HTTP traffic:Run in PowerShell (as administrator):
New-NetFirewallRule -DisplayName "Allow HTTP Port 80" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow


Run the honeypot:Run in Command Prompt (as administrator):
python app.py


Test locally:Open a browser and navigate to http://192.168.153.15 to verify the login page.


Testing the Project

On Kali Linux, open Firefox and navigate to http://malicious.com.
The browser should load the fake login page served by the Windows honeypot.
Enter test credentials (e.g., username: demo, password: pass123) and submit.
On Windows, check logs/honeypot.log for entries like:2025-05-10 10:00:00 - Access from IP: 192.168.153.136, User-Agent: Mozilla/5.0...
2025-05-10 10:01:00 - Credentials submitted - IP: 192.168.153.136, Username: demo, Password: pass123



Demo Instructions

Windows: Open VS Code, show app.py and index.html, run python app.py to start the honeypot.
Kali Linux:
In Terminal 1, run dnschef (see above).
In Terminal 2, show nslookup malicious.com (returns 192.168.153.15).
Open Firefox, navigate to http://malicious.com, submit credentials.


Windows: Open logs/honeypot.log to show logged access and credentials.

Notes

Ensure both systems are on the same network (192.168.153.0/24).
If Kali Linux fails to boot, use a Kali live USB and repeat the setup.
The honeypot requires administrative privileges to bind to port 80.
For GitHub, ensure .gitignore includes logs/ and __pycache__/.
