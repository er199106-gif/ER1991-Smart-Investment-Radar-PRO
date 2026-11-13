# 📡 ER1991 Smart Investment Radar PRO — نسخة GitHub

نفس أداة Colab (v7.0) **بنفس المنطق والحسابات والنتائج وتصميم HTML** — الفرق الوحيد أن لوحة أزرار Colab (ipywidgets) استُبدلت بملف إعدادات `config.json` ومشغّل `run_radar.py`، وأن التشغيل يتم من تبويب **Actions** في GitHub (يدوياً أو مجدولاً) والنتائج تُحفظ كملفات قابلة للتنزيل أو تُنشر كصفحة ويب.

## محتويات المجلد
| الملف | وظيفته |
|---|---|
| `er1991_radar.py` | الكود الكامل v7.0 كما هو دون أي تعديل في المنطق |
| `run_radar.py` | مشغّل سطر الأوامر: يقرأ الإعدادات → `run_scan` → يصدّر HTML/Excel/CSV/PDF/PNG |
| `config.json` | الرموز والأسلوب واللغة ورأس المال وكل إعدادات لوحة الإعدادات |
| `symbols.txt` | قائمة رموز بديلة (تُستخدم فقط إن كان `"symbols"` فارغاً في config.json) |
| `requirements.txt` | حزم بايثون |
| `.github/workflows/run-radar.yml` | سير عمل GitHub Actions (يدوي + مجدول + نشر Pages اختياري) |

## الخطوات (من المتصفح فقط — بلا تثبيت أي شيء)

### 1) إنشاء المستودع
1. ادخل github.com ← **New repository**.
2. الاسم مثلاً `er1991-radar`. اختر **Private** (موصى به لأن قائمة رموزك لن تظهر للعموم) ← **Create repository**.

### 2) رفع الملفات
1. في صفحة المستودع: **Add file ← Upload files**.
2. اسحب هذه الملفات: `er1991_radar.py` · `run_radar.py` · `config.json` · `symbols.txt` · `requirements.txt` · `.gitignore` · `README.md` ← **Commit changes**.
3. ملف سير العمل (المجلد المخفي `.github`): الأسهل إنشاؤه يدوياً:
   **Add file ← Create new file** ثم اكتب في خانة الاسم بالضبط: `.github/workflows/run-radar.yml`
   (عند كتابة `/` يتحول إلى مجلد تلقائياً) ← الصق محتوى الملف المرفق ← **Commit changes**.
   (أو اسحب مجلد `.github` كاملاً إلى صفحة الرفع إن دعم متصفحك ذلك.)

### 3) تفعيل Actions وأول تشغيل
1. تبويب **Actions** ← إن ظهرت رسالة تفعيل اضغط **I understand my workflows, enable them**.
2. اختر **ER1991 Radar** من اليسار ← **Run workflow** ← عدّل الرموز/الأسلوب/اللغة إن أردت ← **Run workflow**.
3. انتظر 3–10 دقائق. افتح التشغيل: ستجد **ملخص جدول القرارات** أعلى الصفحة، وفي الأسفل **Artifacts ← er1991-reports** (ملف ZIP فيه HTML التفاعلي وExcel وCSV). حمّله وافتح `index.html` في المتصفح.

### 4) تعديل الإعدادات (بديل لوحة الإعدادات في Colab)
افتح `config.json` ← أيقونة القلم ✏️ ← عدّل ← Commit. أهم المفاتيح:
- `"symbols"`: الرموز (مثل `EGX:COMI, TADAWUL:2222, AAPL`) — أو اتركه فارغاً واستخدم `symbols.txt`.
- `"style"`: `Auto` أو `Value` أو `Growth` أو `Swing` أو `Medium Term` أو `Long Term`.
- `"settings"`: **نفس مفاتيح لوحة الإعدادات**. في Colab اضغط «⬆ تصدير الإعدادات» وانسخ الناتج هنا كما هو، مثل:
```json
"settings": {
  "fvExt": {"SWDY": 115.6},
  "fvW.pe": 0.45,
  "mktCrashDay": 7.0,
  "fvCoe": {"EGX": {"rf": 20.0, "g": 12.0, "gr": 4.0, "erp": 5.0}}
}
```
(`fvExt` = أهداف خارجية مثل متوسط بنوك الاستثمار، و`fvCoe` = فائدة/تضخم/نمو حقيقي/علاوة لكل سوق.)
- `"exports"`: من `html, excel, csv, pdf, png`.

### 5) نشر التقرير كصفحة ويب (اختياري)
1. **Settings ← Pages ← Source: GitHub Actions**.
2. شغّل الـWorkflow واختر `publish_pages = true` (أو أنشئ متغيراً **Settings ← Secrets and variables ← Actions ← Variables** باسم `PUBLISH_PAGES` وقيمته `true` ليُنشر كل تشغيل مجدول).
3. الرابط يظهر في المهمة `deploy-pages` (شكله `https://اسمك.github.io/er1991-radar/`).
⚠️ الصفحة **علنية** لأي شخص عنده الرابط في المستودعات العامة، وتتطلب خطة مدفوعة للمستودعات الخاصة. إن كان ما تحلله خاصاً فاكتفِ بالـArtifacts.

### 6) التشغيل المجدول
الجدول الحالي (UTC): أحد–خميس 13:30 بعد إغلاق مصر/السعودية، واثنين–جمعة 21:45 بعد إغلاق أمريكا. عدّل أو احذف سطور `cron` في ملف الـworkflow. ملاحظات: GitHub قد يتأخر دقائق، ويوقف الجدولة بعد 60 يوماً بلا نشاط في المستودعات العامة (يكفي تشغيل يدوي لإعادتها).

## تشغيل على جهازك أو Codespaces
```bash
pip install -r requirements.txt
pip install git+https://github.com/rongardF/tvdatafeed.git   # اختياري: تاريخ مصر/السعودية عند نقص ياهو
python run_radar.py --selftest                 # اختبار ذاتي بلا إنترنت
python run_radar.py                            # حسب config.json
python run_radar.py --symbols "EGX:COMI,EGX:SWDY" --style Growth --exports html,excel
```
النتائج في مجلد `ER1991_Reports/`. ولو أردت واجهة الأزرار القديمة: افتح `er1991_radar.py` في Colab كما كان — لم يتغير.

## ما يختلف عن Colab (بصراحة)
- **لا لوحة أزرار تفاعلية** على GitHub؛ الإعدادات من `config.json` أو من مدخلات تشغيل الـWorkflow.
- **تصدير Google Sheet** يحتاج تسجيل دخول Colab فلا يعمل هنا (الباقي يعمل).
- **مصادر البيانات:** ياهو وTradingView قد يقيّدان الطلبات من عناوين خوادم GitHub المشتركة (أخطاء 429 أو بيانات ناقصة). الكود يكمل ويكتب تحذيراً في السجل؛ إن تكرر فأعد التشغيل لاحقاً أو شغّل من جهازك/Codespaces. لم أستطع اختبار الاتصال الحي من بيئتي، فاختبرت كل شيء بدون إنترنت ببيانات تجريبية (المشغّل والتصدير والإعدادات).
- مسار الحفظ صار `ER1991_Reports/` داخل المشروع بدل `/content/...`.

أداة مساعدة في قراءة وفحص الأسهم والمساعدة في القرار الاستثماري، وليست توصية بالشراء أو البيع.
