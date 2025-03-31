import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import whois
import threading
from datetime import datetime
import re
import json
import os
import socket
import dns.resolver
from tkinter import font

class BlitzTheme:
    # Ana renkler
    BG_COLOR = "#0f1519"  # Blitz koyu arka plan
    DARKER_BG = "#0a0e11"  # Daha koyu panel arka planı
    PANEL_BG = "#1a1f25"   # Panel arka planı
    
    # Glow ve Neon renkler
    PRIMARY_GLOW = "#1890ff"  # Ana glow rengi
    SUCCESS_GLOW = "#52c41a"  # Başarılı glow
    ERROR_GLOW = "#ff4d4f"    # Hata glow
    WARNING_GLOW = "#faad14"  # Uyarı glow
    
    # Metin renkleri
    TEXT_PRIMARY = "#ffffff"   # Ana metin
    TEXT_SECONDARY = "#8b8b8b" # İkincil metin
    TEXT_HIGHLIGHT = "#40a9ff" # Vurgulu metin
    
    # UI elementleri
    BUTTON_BG = "#177ddc"     # Buton arka planı
    BUTTON_HOVER = "#1890ff"  # Buton hover
    INPUT_BG = "#141414"      # Input arka planı
    BORDER_COLOR = "#434343"  # Kenarlık rengi

class GlowButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = BlitzTheme.BUTTON_BG
        self.hover_bg = BlitzTheme.BUTTON_HOVER
        self.configure(
            background=self.default_bg,
            foreground=BlitzTheme.TEXT_PRIMARY,
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground=self.hover_bg,
            activeforeground=BlitzTheme.TEXT_PRIMARY
        )
        
        # Glow efekti için canvas
        self.glow_canvas = tk.Canvas(master, 
                                   highlightthickness=0, 
                                   bg=BlitzTheme.BG_COLOR,
                                   width=self.winfo_reqwidth()+20,
                                   height=self.winfo_reqheight()+20)
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self.configure(background=self.hover_bg)
        # Glow efekti
        self.glow_canvas.create_oval(0, 0, 20, 20, 
                                   fill=self.hover_bg,
                                   stipple='gray50')

    def on_leave(self, e):
        self.configure(background=self.default_bg)
        self.glow_canvas.delete("all")

class DomainSorgulamaUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Domain Sorgulama Aracı")
        self.root.geometry("1200x800")
        self.root.configure(bg=BlitzTheme.BG_COLOR)
        
        # Font ayarları
        self.title_font = ('Segoe UI', 24, 'bold')
        self.header_font = ('Segoe UI', 16, 'bold')
        self.normal_font = ('Segoe UI', 11)
        self.small_font = ('Segoe UI', 10)
        
        # Ana container
        self.main_container = tk.Frame(root, bg=BlitzTheme.BG_COLOR, padx=30, pady=30)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        self.title_frame = tk.Frame(self.main_container, bg=BlitzTheme.BG_COLOR)
        self.title_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = tk.Label(self.title_frame, 
                             text=".....DOMAIN CHECKER", 
                             font=self.title_font,
                             bg=BlitzTheme.BG_COLOR,
                             fg=BlitzTheme.PRIMARY_GLOW)
        title_label.pack(side=tk.LEFT)
        
        # Dışa aktar butonu
        self.export_button = GlowButton(self.title_frame,
                                      text="Dışa Aktar",
                                      command=self.disa_aktar)
        self.export_button.pack(side=tk.RIGHT)
        
        # Glow efekti için
        def create_glow(widget, color, radius):
            x = widget.winfo_x() + widget.winfo_width()/2
            y = widget.winfo_y() + widget.winfo_height()/2
            canvas = tk.Canvas(widget.master, width=radius*2, height=radius*2,
                             bg=BlitzTheme.BG_COLOR, highlightthickness=0)
            canvas.create_oval(0, 0, radius*2, radius*2, fill=color, stipple='gray50')
            canvas.place(x=x-radius, y=y-radius)
            return canvas
        
        self.title_glow = create_glow(title_label, BlitzTheme.PRIMARY_GLOW, 50)
        
        # Input alanı
        self.input_frame = tk.Frame(self.main_container, bg=BlitzTheme.PANEL_BG, padx=20, pady=20)
        self.input_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(self.input_frame,
                text="Domain Adları",
                font=self.header_font,
                bg=BlitzTheme.PANEL_BG,
                fg=BlitzTheme.TEXT_PRIMARY).pack(anchor=tk.W, pady=(0, 10))
        
        self.domain_entry = tk.Entry(self.input_frame,
                                   font=self.normal_font,
                                   bg=BlitzTheme.INPUT_BG,
                                   fg=BlitzTheme.TEXT_PRIMARY,
                                   insertbackground=BlitzTheme.TEXT_HIGHLIGHT,
                                   relief=tk.FLAT,
                                   width=70)
        self.domain_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Butonlar
        self.sorgula_button = GlowButton(self.input_frame,
                                       text="Sorgula",
                                       command=self.sorgula_thread)
        self.sorgula_button.pack(side=tk.LEFT, padx=5)
        
        self.temizle_button = GlowButton(self.input_frame,
                                       text="Temizle",
                                       command=self.temizle)
        self.temizle_button.pack(side=tk.LEFT)
        
        # Ana içerik
        self.content_frame = tk.Frame(self.main_container, bg=BlitzTheme.BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sol panel
        self.left_frame = tk.Frame(self.content_frame, bg=BlitzTheme.PANEL_BG)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        tk.Label(self.left_frame,
                text="Domain Listesi",
                font=self.header_font,
                bg=BlitzTheme.PANEL_BG,
                fg=BlitzTheme.TEXT_PRIMARY).pack(anchor=tk.W, padx=20, pady=15)
        
        self.domain_list = tk.Listbox(self.left_frame,
                                    font=self.normal_font,
                                    bg=BlitzTheme.INPUT_BG,
                                    fg=BlitzTheme.TEXT_PRIMARY,
                                    selectmode=tk.EXTENDED,
                                    relief=tk.FLAT,
                                    borderwidth=0,
                                    highlightthickness=1,
                                    highlightcolor=BlitzTheme.PRIMARY_GLOW,
                                    selectbackground=BlitzTheme.PRIMARY_GLOW,
                                    selectforeground=BlitzTheme.TEXT_PRIMARY)
        self.domain_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Sağ panel
        self.right_frame = tk.Frame(self.content_frame, bg=BlitzTheme.PANEL_BG)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Sekme stili
        self.style = ttk.Style()
        self.style.theme_create("BlitzTheme", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "background": BlitzTheme.PANEL_BG,
                    "tabmargins": [2, 5, 2, 0]
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [15, 10],
                    "background": BlitzTheme.BG_COLOR,
                    "foreground": BlitzTheme.TEXT_SECONDARY
                },
                "map": {
                    "background": [("selected", BlitzTheme.PANEL_BG)],
                    "foreground": [("selected", BlitzTheme.PRIMARY_GLOW)],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            }
        })
        self.style.theme_use("BlitzTheme")
        
        # Sonuç sekmeleri
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sekme içerikleri
        self.bos_frame = tk.Frame(self.notebook, bg=BlitzTheme.PANEL_BG)
        self.dolu_frame = tk.Frame(self.notebook, bg=BlitzTheme.PANEL_BG)
        self.belirsiz_frame = tk.Frame(self.notebook, bg=BlitzTheme.PANEL_BG)
        
        self.notebook.add(self.bos_frame, text="Boş Domainler")
        self.notebook.add(self.dolu_frame, text="Dolu Domainler")
        self.notebook.add(self.belirsiz_frame, text="Belirsiz Domainler")
        
        # Metin alanları
        self.bos_text = scrolledtext.ScrolledText(self.bos_frame,
                                                font=self.normal_font,
                                                bg=BlitzTheme.INPUT_BG,
                                                fg=BlitzTheme.SUCCESS_GLOW,
                                                relief=tk.FLAT)
        self.bos_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.dolu_text = scrolledtext.ScrolledText(self.dolu_frame,
                                                 font=self.normal_font,
                                                 bg=BlitzTheme.INPUT_BG,
                                                 fg=BlitzTheme.ERROR_GLOW,
                                                 relief=tk.FLAT)
        self.dolu_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Belirsiz domainler için özel panel
        belirsiz_container = tk.Frame(self.belirsiz_frame, bg=BlitzTheme.PANEL_BG)
        belirsiz_container.pack(fill=tk.BOTH, expand=True)
        
        self.belirsiz_text = scrolledtext.ScrolledText(belirsiz_container,
                                                    font=self.normal_font,
                                                    bg=BlitzTheme.INPUT_BG,
                                                    fg=BlitzTheme.WARNING_GLOW,
                                                    relief=tk.FLAT,
                                                    height=15)
        self.belirsiz_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Belirsiz domainler için buton çubuğu
        belirsiz_buttons = tk.Frame(belirsiz_container, bg=BlitzTheme.PANEL_BG, padx=5, pady=5)
        belirsiz_buttons.pack(fill=tk.X)
        
        self.tekrar_kontrol_button = GlowButton(belirsiz_buttons, 
                                              text="Detaylı Kontrol", 
                                              command=self.detayli_kontrol)
        self.tekrar_kontrol_button.pack(side=tk.LEFT, padx=5)
        
        # Detaylı kontrol için seçeneklerin bulunduğu panel
        self.detay_frame = tk.Frame(belirsiz_container, bg=BlitzTheme.PANEL_BG, padx=5, pady=5)
        
        # Kontrol sonuçları için alan
        self.detay_sonuc = scrolledtext.ScrolledText(self.detay_frame,
                                                   font=self.normal_font,
                                                   bg=BlitzTheme.INPUT_BG,
                                                   fg=BlitzTheme.TEXT_PRIMARY,
                                                   relief=tk.FLAT,
                                                   height=8)
        self.detay_sonuc.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Alt panel
        self.bottom_frame = tk.Frame(self.main_container, bg=BlitzTheme.PANEL_BG, padx=20, pady=15)
        self.bottom_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.durum_label = tk.Label(self.bottom_frame,
                                  text="Hazır",
                                  font=self.small_font,
                                  bg=BlitzTheme.PANEL_BG,
                                  fg=BlitzTheme.TEXT_SECONDARY)
        self.durum_label.pack(side=tk.LEFT)
        
        # Progress bar stili
        self.style.configure("Blitz.Horizontal.TProgressbar",
                           troughcolor=BlitzTheme.BG_COLOR,
                           background=BlitzTheme.PRIMARY_GLOW,
                           borderwidth=0,
                           thickness=6)
        
        self.progress = ttk.Progressbar(self.bottom_frame,
                                      style="Blitz.Horizontal.TProgressbar",
                                      mode='determinate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)
        
        # Event bindings
        self.domain_entry.bind('<KeyRelease>', self.otomatik_ayir)
        self.domain_list.bind('<Delete>', self.secili_domainleri_sil)
        
        # Pencere ayarları
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def otomatik_ayir(self, event):
        text = self.domain_entry.get()
        if ',' in text or '\n' in text:
            # Yükleme göstergesini etkinleştir
            self.durum_label.config(text="Domain listesi işleniyor...")
            self.progress['value'] = 0
            
            # İşlemi ayrı bir thread'de başlat
            threading.Thread(target=self.parse_domainler, args=(text,)).start()

    def parse_domainler(self, text):
        try:
            # Hem virgül hem de yeni satır ile ayırma
            # Önce yeni satırlara göre ayır
            lines = text.split('\n')
            domains = []
            
            # İlerleme çubuğunu ayarla
            self.progress['maximum'] = len(lines)
            
            # Sonra her satırdaki virgüllerle ayrılmış domainleri işle
            for i, line in enumerate(lines):
                if ',' in line:
                    domains.extend([d.strip() for d in line.split(',')])
                else:
                    domains.append(line.strip())
                
                # Her 5 satırda bir ilerleme çubuğunu güncelle
                if i % 5 == 0:
                    self.progress['value'] = i
                    self.root.update_idletasks()
            
            # Boş domainleri ve tekrarları temizle
            domains = [d for d in domains if d]
            
            # İşlenen domain sayısını göster
            self.durum_label.config(text=f"{len(domains)} domain işlendi")
            
            # Listeye ekleme işlemini ana thread'de yap
            self.root.after(0, lambda: self.add_domains_to_list(domains))
            
        except Exception as e:
            self.durum_label.config(text=f"Hata: {str(e)}")
            self.progress['value'] = 0

    def add_domains_to_list(self, domains):
        try:
            # Listeye ekle
            self.domain_list.delete(0, tk.END)
            for domain in domains:
                if domain:
                    self.domain_list.insert(tk.END, domain)
            self.domain_entry.delete(0, tk.END)
            
            # İşlem tamamlandı
            self.progress['value'] = 0
            self.durum_label.config(text=f"{len(domains)} domain başarıyla listeye eklendi")
        except Exception as e:
            messagebox.showerror("Hata", f"Domainler eklenirken hata oluştu: {str(e)}")

    def secili_domainleri_sil(self, event):
        selected = self.domain_list.curselection()
        for index in reversed(selected):
            self.domain_list.delete(index)
    
    def temizle(self):
        self.domain_entry.delete(0, tk.END)
        self.domain_list.delete(0, tk.END)
        self.bos_text.delete(1.0, tk.END)
        self.dolu_text.delete(1.0, tk.END)
        self.belirsiz_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.durum_label.config(text="Hazır")
    
    def domain_kontrol(self, domain):
        try:
            w = whois.whois(domain)
            if w.domain_name is None:
                return "bos"
            elif w.creation_date is None or w.expiration_date is None:
                return "belirsiz"
            else:
                return "dolu"
        except:
            return "belirsiz"
    
    def domain_sorgula(self):
        try:
            domains = list(self.domain_list.get(0, tk.END))
            if not domains:
                messagebox.showerror("Hata", "Lütfen en az bir domain adı girin!")
                return
            
            # Sonuç alanlarını temizle
            self.bos_text.delete(1.0, tk.END)
            self.dolu_text.delete(1.0, tk.END)
            self.belirsiz_text.delete(1.0, tk.END)
            
            # İlerleme çubuğunu ayarla
            self.progress['maximum'] = len(domains)
            self.progress['value'] = 0
            
            # Domain sayısına göre durum metnini güncelle
            domain_count = len(domains)
            self.durum_label.config(text=f"{domain_count} domain sorgulanıyor (0/{domain_count})")
            
            # Arayüzün güncellenmesini sağla
            self.root.update_idletasks()
            
            for i, domain in enumerate(domains):
                if not domain:
                    continue
                    
                # Domain formatını kontrol et
                if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$', domain):
                    self.belirsiz_text.insert(tk.END, f"{domain} - Geçersiz domain formatı\n")
                    continue
                
                # İlk sorgu
                durum = self.domain_kontrol(domain)
                
                # Eğer belirsizse ikinci sorgu yap
                if durum == "belirsiz":
                    durum = self.domain_kontrol(domain)
                
                # Sonuçları ilgili sekmeye ekle
                if durum == "bos":
                    self.bos_text.insert(tk.END, f"✓ {domain}\n")
                elif durum == "dolu":
                    self.dolu_text.insert(tk.END, f"✗ {domain}\n")
                else:
                    self.belirsiz_text.insert(tk.END, f"? {domain}\n")
                
                # İlerleme çubuğunu güncelle
                self.progress['value'] = i + 1
                
                # Durum metnini güncelle
                self.durum_label.config(text=f"{domain_count} domain sorgulanıyor ({i+1}/{domain_count})")
                
                # Her 5 domain'de bir arayüzü güncelleştir
                if i % 5 == 0:
                    self.root.update_idletasks()
            
            messagebox.showinfo("Tamamlandı", "Domain sorgulama işlemi tamamlandı!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
        
        finally:
            self.sorgula_button.config(state='normal')
            self.durum_label.config(text="Hazır")
            self.progress['value'] = 0
    
    def sorgula_thread(self):
        self.sorgula_button.config(state='disabled')
        self.durum_label.config(text="Sorgulanıyor...")
        
        thread = threading.Thread(target=self.domain_sorgula)
        thread.start()

    def disa_aktar(self):
        try:
            # Tüm sekmelerdeki verileri topla
            bos_domains = self.bos_text.get('1.0', tk.END).strip().split('\n')
            dolu_domains = self.dolu_text.get('1.0', tk.END).strip().split('\n') 
            belirsiz_domains = self.belirsiz_text.get('1.0', tk.END).strip().split('\n')
            
            # Boş satırları temizle
            bos_domains = [d for d in bos_domains if d]
            dolu_domains = [d for d in dolu_domains if d]
            belirsiz_domains = [d for d in belirsiz_domains if d]
            
            if not (bos_domains or dolu_domains or belirsiz_domains):
                messagebox.showwarning("Uyarı", "Dışa aktarılacak sonuç bulunamadı!")
                return
            
            # Dosya kaydetme penceresi
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Sonuçları Kaydet"
            )
            
            if not file_path:
                return  # Kullanıcı iptal ettiyse
            
            # Dosyaya yaz
            with open(file_path, 'w', encoding='utf-8') as f:
                # Başlık
                f.write("==== DOMAIN SORGULAMA SONUÇLARI ====\n")
                f.write(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
                
                # Boş domainler
                if bos_domains:
                    f.write("=== BOŞ DOMAINLER ===\n")
                    for domain in bos_domains:
                        # Simgeleri temizleyerek yaz
                        clean_domain = domain.replace("✓ ", "")
                        f.write(f"{clean_domain}\n")
                    f.write("\n")
                
                # Dolu domainler
                if dolu_domains:
                    f.write("=== DOLU DOMAINLER ===\n")
                    for domain in dolu_domains:
                        clean_domain = domain.replace("✗ ", "")
                        f.write(f"{clean_domain}\n")
                    f.write("\n")
                
                # Belirsiz domainler
                if belirsiz_domains:
                    f.write("=== BELİRSİZ DOMAINLER ===\n")
                    for domain in belirsiz_domains:
                        clean_domain = domain.replace("? ", "")
                        f.write(f"{clean_domain}\n")
            
            messagebox.showinfo("Başarılı", f"Sonuçlar başarıyla kaydedildi:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken bir hata oluştu: {str(e)}")

    def detayli_kontrol(self):
        """Belirsiz domainler için detaylı DNS kontrolleri yapar"""
        # Seçili sekmeyi kontrol et ve eğer belirsiz sekmesi değilse uyar
        if self.notebook.select() != str(self.belirsiz_frame):
            messagebox.showinfo("Bilgi", "Lütfen önce 'Belirsiz Domainler' sekmesini seçin")
            return
            
        # Belirsiz domainleri al
        belirsiz_domains = self.belirsiz_text.get('1.0', tk.END).strip().split('\n')
        belirsiz_domains = [d.replace("? ", "").strip() for d in belirsiz_domains if d.strip()]
        
        if not belirsiz_domains:
            messagebox.showinfo("Bilgi", "Kontrol edilecek belirsiz domain bulunamadı")
            return
        
        # Detay frame'i göster
        if not self.detay_frame.winfo_ismapped():
            self.detay_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Kontrol işlemini başlat
        self.detay_sonuc.delete(1.0, tk.END)
        self.detay_sonuc.insert(tk.END, "Detaylı kontrol başlatılıyor...\n")
        
        thread = threading.Thread(target=self.run_detayli_kontrol, args=(belirsiz_domains,))
        thread.start()
    
    def run_detayli_kontrol(self, domains):
        """Detaylı domain kontrolü gerçekleştirir"""
        self.tekrar_kontrol_button.config(state='disabled')
        self.durum_label.config(text="Detaylı kontrol yapılıyor...")
        
        try:
            for domain in domains:
                self.detay_sonuc.insert(tk.END, f"\n--- {domain} için detaylı kontrol ---\n")
                
                # 1. Socket bağlantı kontrolü
                try:
                    socket.gethostbyname(domain)
                    self.detay_sonuc.insert(tk.END, "✓ IP Adresi Bulundu\n")
                    is_active = True
                except:
                    self.detay_sonuc.insert(tk.END, "✗ IP Adresi Bulunamadı\n")
                    is_active = False
                
                # 2. DNS kayıtları kontrolü
                dns_records = []
                
                try:
                    for qtype in ['A', 'MX', 'NS', 'TXT']:
                        try:
                            answers = dns.resolver.resolve(domain, qtype)
                            for rdata in answers:
                                dns_records.append(f"{qtype}: {rdata}")
                        except dns.resolver.NoAnswer:
                            pass
                        except:
                            pass
                except:
                    pass
                
                if dns_records:
                    self.detay_sonuc.insert(tk.END, f"✓ DNS Kayıtları Bulundu ({len(dns_records)} kayıt)\n")
                    for i, record in enumerate(dns_records[:3]):  # İlk 3 kaydı göster
                        self.detay_sonuc.insert(tk.END, f"  - {record}\n")
                    if len(dns_records) > 3:
                        self.detay_sonuc.insert(tk.END, f"  ... {len(dns_records) - 3} kayıt daha var\n")
                else:
                    self.detay_sonuc.insert(tk.END, "✗ DNS Kaydı Bulunamadı\n")
                
                # 3. WHOIS detay kontrolü
                try:
                    whois_info = whois.whois(domain)
                    if whois_info.registrar:
                        self.detay_sonuc.insert(tk.END, f"✓ Kayıt Şirketi: {whois_info.registrar}\n")
                    
                    if whois_info.creation_date:
                        creation_date = whois_info.creation_date
                        if isinstance(creation_date, list):
                            creation_date = creation_date[0]
                        self.detay_sonuc.insert(tk.END, f"✓ Kayıt Tarihi: {creation_date}\n")
                    
                    # Sonuca karar ver
                    if ((is_active and dns_records) or 
                        (whois_info.registrar and whois_info.creation_date)):
                        self.detay_sonuc.insert(tk.END, "➤ SONUÇ: Domain aktif görünüyor\n")
                        # Dolu domainler listesine ekle
                        self.dolu_text.insert(tk.END, f"✗ {domain}\n")
                        # Belirsiz listesinden domain'i çıkar
                        self.remove_from_uncertain(domain)
                    else:
                        self.detay_sonuc.insert(tk.END, "➤ SONUÇ: Domain muhtemelen boş\n")
                        # Boş domainler listesine ekle
                        self.bos_text.insert(tk.END, f"✓ {domain}\n")
                        # Belirsiz listesinden domain'i çıkar
                        self.remove_from_uncertain(domain)
                
                except Exception as e:
                    self.detay_sonuc.insert(tk.END, f"✗ WHOIS Hatası: {str(e)}\n")
                    self.detay_sonuc.insert(tk.END, "➤ SONUÇ: Halen belirsiz\n")
        
        except Exception as e:
            self.detay_sonuc.insert(tk.END, f"\nHata oluştu: {str(e)}\n")
        
        finally:
            self.tekrar_kontrol_button.config(state='normal')
            self.durum_label.config(text="Hazır")
    
    def remove_from_uncertain(self, domain):
        """Belirsiz domainler listesinden belirli bir domain'i kaldırır"""
        uncertain_text = self.belirsiz_text.get('1.0', tk.END)
        lines = uncertain_text.split('\n')
        new_lines = []
        
        for line in lines:
            if line.strip() and domain not in line:
                new_lines.append(line)
        
        self.belirsiz_text.delete(1.0, tk.END)
        self.belirsiz_text.insert(tk.END, '\n'.join(new_lines))

if __name__ == "__main__":
    root = tk.Tk()
    app = DomainSorgulamaUygulamasi(root)
    root.mainloop() 