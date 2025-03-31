# Domain Sorgulama Aracı

Domain Sorgulama Aracı, alan adlarının (domainlerin) durumunu hızlı ve toplu şekilde kontrol edebilmenizi sağlayan ücretsiz ve açık kaynaklı bir Python uygulamasıdır. Modern arayüzü ve gelişmiş özellikleriyle domain kontrolü işlemlerinizi kolaylaştırır.

![Domain Sorgulama Aracı Ekran Görüntüsü](./screenshots/main_screen.png)

## 🚀 Özellikler

- **Toplu Domain Sorgulama**: Yüzlerce domaini tek seferde kontrol edin
- **Akıllı Liste Tanıma**: Virgülle ayrılmış veya alt alta yazılmış domain listelerini otomatik olarak tanır
- **Kategorize Sonuçlar**: Boş, dolu ve belirsiz domainleri ayrı sekmelerde görüntüler 
- **Detaylı Kontrol**: Belirsiz domainler için IP adresi, DNS kayıtları ve WHOIS detaylarını kontrol eder
- **Dışa Aktarma**: Sonuçları TXT dosyasına aktarabilme özelliği
- **Modern Arayüz**: Blitz temalı, göz yormayan karanlık tema ve glow efektleri

## 🔧 Kurulum

### Gereksinimler

- Python 3.6 veya üzeri
- pip (Python paket yöneticisi)

### Adım Adım Kurulum

1. **Repoyu klonlayın**

```bash
git clone https://github.com/kullaniciadi/domain-sorgulama-araci.git
cd domain-sorgulama-araci
```

2. **Sanal ortam oluşturun (isteğe bağlı ama önerilir)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Bağımlılıkları yükleyin**

```bash
pip install -r requirements.txt
```

4. **Uygulamayı çalıştırın**

```bash
python domain_sorgulama.py
```

## 📋 Kullanım

1. **Domain Ekleme**:
   - Tek domain girmek için metin kutusuna yazın ve Enter'a basın
   - Virgülle ayırarak birden fazla domain ekleyin: `domain1.com, domain2.com, domain3.net`
   - Kopyala-yapıştır ile alt alta yazılmış listeler ekleyin

2. **Sorgulama**:
   - "Sorgula" butonuna tıklayarak listedeki tüm domainleri kontrol edin
   - İlerleme çubuğu sorgu durumunu gösterir

3. **Sonuçları Görüntüleme**:
   - "Boş Domainler": Kayıt edilmemiş, satın alınabilir domainler
   - "Dolu Domainler": Kayıt edilmiş, kullanımda olan domainler
   - "Belirsiz Domainler": Durumu kesin olarak belirlenemeyen domainler

4. **Belirsiz Domainleri İleri Düzey Kontrol**:
   - "Belirsiz Domainler" sekmesine gidin
   - "Detaylı Kontrol" butonuna tıklayın
   - Program detaylı analiz yapar ve sonuçları gösterir

5. **Sonuçları Dışa Aktarma**:
   - "Dışa Aktar" butonuna tıklayın ve dosya adını belirtin
   - Sonuçlar kategorilere ayrılmış şekilde kaydedilir

## 🏗️ Kendi EXE Dosyanızı Oluşturma

Bu projeyi çalıştırılabilir tek bir EXE dosyasına dönüştürmek için:

```bash
# PyInstaller'ı yükleyin
pip install pyinstaller

# EXE dosyasını oluşturun
pyinstaller --onefile --windowed --icon=domain.ico --name=DomainSorgulama domain_sorgulama.py
```

Oluşturulan EXE dosyası `dist` klasöründe bulunacaktır.

## 📦 Bağımlılıklar

Proje aşağıdaki Python kütüphanelerini kullanmaktadır:

- python-whois: Domain WHOIS sorgulamaları için
- dnspython: İleri düzeyde DNS sorgulamaları için
- tkinter: Grafiksel kullanıcı arayüzü için (Python ile birlikte gelir)

## 🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz!

1. Bu repo'yu fork edin
2. Kendi branch'inizi oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inize push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request açın

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## ⚠️ Not

Bu program sadece eğitim amaçlıdır ve domain durumlarını kontrol etmek için ücretsiz API'lar kullanır. Aşırı kullanım durumunda hız sınırlamaları oluşabilir.
