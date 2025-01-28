# ❄️ Snow Crash

**Snow Crash** is a cybersecurity training project for School 42, built on a Kali-based Docker image. It provides a solver system that connects to levels via SSH, extracts flags, and automates challenges.

## ✨ Features
- 🐧 **Kali Linux** base with essential security tools  
- 🐍 **Python virtual environment** including paramiko & scp  
- 🤖 **Automated solver scripts** for each level  
- 📚 **Detailed walkthroughs** for each level  
- ⚙️ **Flexible Makefile commands** for quick setup & troubleshooting

## 🚀 Installation
1. **Clone this repository:**  
   ```bash
   git clone https://github.com/username/snow-crash.git
   cd snow-crash
   ```

## 🛠️ Usage
1. **Configure environment:**  
   ```bash
   make config
   ```
   The configuration script will also build and run the container.

2. **Solve a level or range of levels:**  
   ```bash
   make solve        # Solve all levels
   make solve LEVEL=02  # Specific level
   make solve LEVEL=00-05  # Range of levels
   make solve LEVEL=00,02,04  # Multiple levels
   ```
   The flags will be stored in a JSON file.
   
3. **Enter a shell in the container:**  
   ```bash
   make shell
   ```
4. **Stop the container:**  
   ```bash
   make stop
   ```
5. **For more commands:**  
   ```bash
   make help
   ```

## 🤝 Contributing
Contributions are welcome! Please fork this repository and submit pull requests.

## 📜 License
Distributed under your chosen license. See `LICENSE` for details.
