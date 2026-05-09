# Plan: Servis Test Bug Fix + OpenWebUI Bağlantı Paneli Redesign

## Context
Dosya: `C:\Users\emre\OneDrive\Desktop\seda\iddaa.html`  
Sorun: Kullanıcı doğru URL giriyor ama `testAI()` fonksiyonu "test hatalı" (❌) gösteriyor.  
İstek: Bug düzeltme + servisleri OpenWebUI bağlantı paneline benzet.

---

## Bug Analizi (Root Cause)

### 1. AggregateError — Worker + Direct her ikisi birden çöküyor
`Promise.any([_direct(), _worker()])` → iki attempt de fail edince `AggregateError` fırlatıyor.  
Catch bloğu (`~line 10160+`) generic "❌ test hatalı" veya boş sonuç gösteriyor.

**Neden _direct() çöküyor:** Browser CORS politikası — cross-origin GET'i engelliyor.  
**Neden _worker() çöküyor:** Worker (`iddaaworkerjs.aksu1993.workers.dev`) ya:
- Custom servis ID'sini tanımıyor
- Timeout'a düşüyor  
- 4xx/5xx döndürüyor

### 2. URL Normalizasyon Sorunu (line 9807-9809)
`_normalizeBaseUrl(c.url) === _normalizeBaseUrl(ai.u)` true olunca **hardcoded endpoint tablosu** kullanılıyor, custom URL yok sayılıyor. Kullanıcı custom bir URL girmişse bile eğer base kısmı default ile eşleşirse test yanlış endpoint'e gidiyor.

### 3. Catch Bloğu — Eksik Tanı
`AggregateError` yakalanınca neden başarısız olduğu gösterilmiyor → Kullanıcı neden hatalı anlamıyor.

---

## Çözüm Planı

### BÖLÜM A: Bug Fix (~10 satır değişiklik)

**A1. Catch bloğu düzeltme** (`~line 10162-10180`):
```javascript
// ÖNCE (tahmini):
}catch(e){
  _writeTestEl(id,"<span style='color:#ef4444'>❌ test hatalı</span>");
  _clearTestAfter(id,5000);
}

// SONRA:
}catch(e){
  var errMsg='Bağlantı başarısız';
  if(e instanceof AggregateError){
    var reasons=e.errors.map(function(er){return er&&er.message?er.message:'';}).filter(Boolean);
    if(reasons.some(function(r){return /cors|blocked|failed to fetch/i.test(r)})) errMsg='CORS engeli — worker proxy üzerinden tekrar dene';
    else if(reasons.some(function(r){return /timeout|abort/i.test(r)})) errMsg='10sn timeout — servis yanıt vermedi';
    else if(reasons.some(function(r){return /network/i.test(r)})) errMsg='Ağ hatası — internet bağlantısını kontrol et';
    else if(reasons.length) errMsg=reasons[0].slice(0,80);
  }
  _writeTestEl(id,"<span style='color:#ef4444;font-weight:700'>❌ "+_esc(errMsg)+"</span>");
  _clearTestAfter(id,30000); // 5s→30s: kullanıcı okusun
  _testingAI[id]=false;
}
```

**A2. URL pre-validation** — testAI başında, modelsUrl boşsa daha net mesaj:
```javascript
// line ~9959'dan sonra, modelsUrl boşsa:
if(!modelsUrl){
  var hasCustomUrl=!!(c.url&&c.url.trim());
  _writeTestEl(id,hasCustomUrl
    ?"<span style='color:#ef4444;font-weight:700'>❌ URL geçersiz — /models endpoint türetilemedi. Örnek: https://api.servis.com/v1</span>"
    :"<span style='color:#3b82f6;font-weight:700'>ℹ Bu servis test edilemez (özel handler)</span>"
  );
  _clearTestAfter(id,15000);
  return;
}
```

**A3. Test result süresini uzat** — tüm `_clearTestAfter(id,5000)` → `_clearTestAfter(id,30000)` (testAI içinde).

---

### BÖLÜM B: OpenWebUI-style Bağlantı Paneli (UI Redesign)

**Hedef UI:** OpenWebUI'nin "Connections" paneli gibi — her servis kartında:
1. **Bağlantı Durumu Badgei** (kalıcı, 5 sn sonra silinmez)
   - ⚪ Test edilmedi
   - 🟡 ⏳ Test ediliyor...
   - 🟢 ✅ Bağlı — N model
   - 🔴 ❌ Bağlantı hatası — [sebep]
2. **TEST butonu içinde spinner** — test süresince buton "⏳ Test ediliyor..." gösterir, tıklanamaz
3. **Kalıcı durum** — test sonucu bir sonraki teste kadar kartın üstünde görünür (sayfa yenilenene kadar)

**Değişecek alanlar:**

**B1. `test_${id}` div** (line 11937) — stilini ve konumunu güncelle:
```html
<!-- ÖNCE -->
<div id='test_${id}' style='margin-top:4px;font-size:10px;...'></div>

<!-- SONRA -->
<div id='test_${id}' style='margin-top:6px;min-height:24px;display:flex;align-items:center;
  gap:6px;padding:4px 10px;border-radius:6px;background:transparent;font-size:11px;
  font-weight:600;line-height:1.4;transition:background .2s;word-break:break-word'></div>
```

**B2. TEST butonu** (line 11925) — spinner state ile:
```javascript
// testAI() başında:
var _btn=document.getElementById('testBtn_'+id);
if(_btn){_btn.disabled=true;_btn.innerHTML='⏳';}

// testAI() sonunda (her exit noktasında):
if(_btn){_btn.disabled=false;_btn.innerHTML='⚡ TEST';}
```

Button markup değişikliği (line 11925):
```html
<!-- id ekle -->
<button id='testBtn_${id}' onclick="testAI('${id}')" ...>⚡ TEST</button>
```

**B3. _writeTestEl() güncelleme** — duruma göre arka plan rengi:
```javascript
function _writeTestEl(id,html){
  var e=document.getElementById("test_"+id);
  if(e){
    e.innerHTML=html;
    // OpenWebUI tarzı: renkli arka plan
    if(/✅/.test(html)) e.style.background='#16a34a18';
    else if(/❌/.test(html)) e.style.background='#dc262618';
    else if(/⏳/.test(html)) e.style.background='#d9770618';
    else if(/ℹ/.test(html)) e.style.background='#3b82f618';
    else e.style.background='transparent';
  }
  _testActiveResults[id]=html;
}
```

---

## Değiştirilecek Dosya

**Tek dosya:** `C:\Users\emre\OneDrive\Desktop\seda\iddaa.html`

Değiştirilecek satır grupları:
| Satır | Değişiklik |
|-------|-----------|
| ~9959-9963 | URL boşsa daha net hata mesajı (A2) |
| ~9977 | ⏳ mesajından önce testBtn disable (B2) |
| ~9629-9665 | `_writeTestEl()` arka plan rengi (B3) |
| ~10069, 10089, 10097, 10151 | `_clearTestAfter` 5000→30000 (A3) |
| ~10162-10180 | AggregateError catch bloğu (A1) |
| ~11925 | TEST butonuna id ekle (B2) |
| ~11937 | test div stilini güncelle (B1) |

Toplam edit: ~7 cerrahi değişiklik, hepsi aynı dosyada.

---

## Doğrulama
- node --check ile JS syntax doğrulama (inline script extract)
- Test flow: URL gir → TEST bas → ⏳ göster → ✅/❌ kalıcı göster
- AggregateError senaryosu: CORS + worker fail → "CORS engeli" mesajı
- Boş URL: "URL geçersiz" spesifik mesajı
