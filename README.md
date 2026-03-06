# Bal Line MMC — Etopaz Platform Analytics Dashboard

İnteraktiv analitika paneli. Hər ay yeni Excel fayllarını yükləyərək dashboardu yeniləyə bilərsiniz.

---

## 📋 Tələblər

- Python 3.9 və ya daha yeni
- İnternet bağlantısı (ilk quraşdırma üçün)

---

## 💻 Lokal İşə Salma (Öz Kompüterinizdə)

### Addım 1 — Python yoxlayın
Terminalı açın (Windows: `Win + R` → `cmd`) və yazın:
```
python --version
```
Əgər Python quraşdırılıbsa versiya nömrəsi görünəcək.

### Addım 2 — Layihə qovluğuna keçin
```
cd "streamlit_dashboard qovluğunun yolu"
```
Məsələn:
```
cd "C:\Users\Nicat\Desktop\OMT data\streamlit_dashboard"
```

### Addım 3 — Paketləri quraşdırın
```
pip install -r requirements.txt
```
Bu əmr bir dəfə işə salınır — sonra tekrar lazım deyil.

### Addım 4 — Dashboardu başladın
```
streamlit run app.py
```

Brauzer avtomatik açılacaq. Əgər açılmasa, ünvanı özünüz daxil edin:
```
http://localhost:8501
```

### Hər ay yeniləmə
Yeni Excel faylları gəldikdə sadəcə sol paneldən yeni faylları yükləyin — dashboard dərhal yenilənəcək. Kompüteri yenidən başlatmağa ehtiyac yoxdur.

---

## ☁️ Streamlit Cloud-da Hosting (İnternetdə)

Bu üsul ilə dashboard **ictimai bir link** vasitəsilə hər yerdən açıla bilər.

### Bir dəfəlik quraşdırma:

**1. GitHub hesabı açın**
→ [github.com](https://github.com) saytında pulsuz hesab açın.

**2. Yeni repository (repo) yaradın**
→ GitHub-da "New repository" düyməsinə basın.
→ Ad verin: `bal-line-analytics`
→ "Public" seçin → "Create repository".

**3. Faylları yükləyin**
→ Repo səhifəsindən "uploading an existing file" linkini seçin.
→ Aşağıdakı faylları yükləyin:
```
app.py
requirements.txt
.streamlit/config.toml
```

**4. Streamlit Cloud-a qoşulun**
→ [share.streamlit.io](https://share.streamlit.io) saytına keçin.
→ GitHub hesabınızla giriş edin.
→ "New app" düyməsinə basın.
→ Repository: `bal-line-analytics`, Branch: `main`, File: `app.py`
→ "Deploy" düyməsinə basın.

**5. Linkinizi alın**
Deployment tamamlandıqdan sonra sizə belə bir link veriləcək:
```
https://bal-line-analytics.streamlit.app
```
Bu linki istədiyiniz şəxslərlə paylaşa bilərsiniz.

### Aylıq yeniləmə (Cloud versiya):
Dashboard Excel fayllarını yükləmə üsulu ilə işləyir — serverdə heç bir dəyişiklik lazım deyil. Sadəcə linki açın və yeni Excel fayllarını yükləyin.

---

## 📁 Fayl Strukturu

```
streamlit_dashboard/
│
├── app.py                    ← Əsas dashboard kodu
├── requirements.txt          ← Python paket siyahısı
├── README.md                 ← Bu fayl
│
└── .streamlit/
    └── config.toml           ← Tema və server konfiqurasiyası
```

---

## 🔧 Texniki Məlumat

| Texnologiya | İstifadə |
|---|---|
| Streamlit | Web interfeysi |
| Pandas | Excel oxuma və hesablamalar |
| Plotly | İnteraktiv qrafiklər |
| OpenPyXL | .xlsx fayl dəstəyi |

---

## ❓ Suallar

Hər hansı problem yaranarsa və ya yeni xüsusiyyət lazım olarsa müraciət edin.
