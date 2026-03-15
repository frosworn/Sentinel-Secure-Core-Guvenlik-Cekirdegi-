import os, time, subprocess, requests, random, sys, io, threading
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import pyautogui
import psutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

PHONE_IP = os.getenv("PHONE_IP")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not all([PHONE_IP, BOT_TOKEN, CHAT_ID]):
    print("HATA: Gerekli ortam değişkenleri (PHONE_IP, BOT_TOKEN, CHAT_ID) ayarlanmamış.\nLütfen .env dosyasını oluşturup bu değişkenleri tanımlayın.")
    sys.exit(1)

def bildirim_at(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": CHAT_ID, "text": mesaj}, timeout=5)
    except: pass

def acil_siren_bombardimani():
    def gonder():
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        uyarilar = [
            "🚨 ACİL DURUM: SİSTEME SIZMA VAR!",
            "🔥 DİKKAT: YANLIŞ ŞİFRE GİRİLDİ!",
            "📢 SİREN ÇALIYOR - BİLGİSAYARINI KONTROL ET!",
            "🆘 GÜVENLİK İHLALİ TESPİT EDİLDİ!"
        ]
        print("📢 Telegram Siren Bombardımanı Başlatıldı!")
        for i in range(10):
            try:
                requests.post(url, data={
                    "chat_id": CHAT_ID, 
                    "text": f"{random.choice(uyarilar)} ({i+1}/10)",
                    "disable_notification": False 
                }, timeout=5)
                time.sleep(1.2) 
            except: pass
            
    threading.Thread(target=gonder, daemon=True).start()

def ekran_yakala_ve_at(window):
    dosya = f"ihlal_{int(time.time())}.png"
    try:
        window.withdraw()
        time.sleep(0.5)
        pyautogui.screenshot(dosya)
        window.deiconify()
        window.attributes("-fullscreen", True)
        window.attributes("-topmost", True)
        
        def yukle_ve_sil():
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            try:
                with open(dosya, "rb") as f:
                    requests.post(url, files={"photo": f}, data={"chat_id": CHAT_ID, "caption": "🚨 İHLAL ANI GÖRÜNTÜSÜ!"}, timeout=10)
                os.remove(dosya)
            except: pass
            
        threading.Thread(target=yukle_ve_sil, daemon=True).start()
    except: window.deiconify()

class FortressLock:
    def __init__(self, otp, sebep):
        self.otp = otp
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(background='black')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.fail_count = 0

        tk.Label(self.root, text="🛡️ SENTINEL SECURE CORE", fg="red", bg="black", font=("Arial", 40, "bold")).pack(pady=50)
        tk.Label(self.root, text=f"DURUM: {sebep}", fg="orange", bg="black", font=("Arial", 15)).pack()
        
        self.entry = tk.Entry(self.root, show="*", font=("Arial", 30), justify='center')
        self.entry.pack(pady=20)
        self.entry.focus_set()

        tk.Button(self.root, text="SİSTEMİ AÇ", command=self.kontrol_et, font=("Arial", 20), bg="green", fg="white").pack(pady=40)

    def kontrol_et(self):
        if self.entry.get() == self.otp:
            self.root.destroy()
        else:
            self.fail_count += 1
            ekran_yakala_ve_at(self.root)
            if self.fail_count >= 2:
                acil_siren_bombardimani()
            messagebox.showerror("HATA", f"Geçersiz Kod! (Deneme: {self.fail_count})")
            self.entry.delete(0, tk.END)

def sistemi_kilitle(sebep):
    otp = str(random.randint(1000, 9999))
    bildirim_at(f"🚨 SİSTEM KİLİTLENDİ!\n🔑 OTP Kodun: {otp}")
    if "Bağlantı" in sebep:
        acil_siren_bombardimani()
    os.system("rundll32.exe user32.dll,LockWorkStation")
    app = FortressLock(otp, sebep)
    app.root.mainloop()

print("--- SENTINEL v23.0: ULTIMATE PROTECTION ---")

while True:
    try:
        check = subprocess.run(['ping', '-n', '1', '-w', '1000', PHONE_IP], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rdp_var = any(c.laddr.port == 3389 and c.status == 'ESTABLISHED' for c in psutil.net_connections())

        if rdp_var:
            sistemi_kilitle("Şüpheli Uzak Bağlantı")
            time.sleep(600)
        elif check.returncode != 0:
            sistemi_kilitle("Telefon Menzil Dışı")
            time.sleep(600)
        time.sleep(10)
    except: time.sleep(5)