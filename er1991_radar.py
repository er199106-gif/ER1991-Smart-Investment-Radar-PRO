# -*- coding: utf-8 -*-
# =====================================================================================
# ER1991 Smart Investment Radar PRO — v7.0 (قيمة عادلة v2 + مراحل السوق المؤسسية + لوحة إعدادات + واجهة Cairo)
# (الكود الأساسي v2.0 بنفس تصميم الواجهة وملف الـHTML التفاعلي + كل حسابات ومعادلات v5.2
#  + معالجة كاملة لملاحظات التقرير التحليلي — لا شيء من المنطق الأصلي حُذف، وكل الإضافات موسومة بـ🆕 v6)
# ----------------------------------------------------------------------------------------------
# (أ) إصلاحات المشاكل المؤثرة:
#  1) R:R مزدوج في خطة الدخول: يُحسب R:R من سعر دخول الخطة (zb_rr) + حقل جديد «R:R عند سعر السوق»
#     (zb_rr_mkt / rd_rr_mkt) يظهر بجواره دون حذف الحقل الأصلي — فلا تتضخم النسبة على الشاشة.
#  2) تحول رموز الأسهم إلى عملات رقمية بصمت: الرموز المتقاطعة مع أسماء أسهم (DASH=DoorDash، STX=Seagate،
#     SOL، ATOM، LINK، FET، NEAR…) لا تعتبر عملات رقمية إلا مع لاحقة صريحة (-USD / USDT / USD)؛
#     الأسماء الرقمية غير المتقاطعة فقط (BTC، ETH، DOGE…) تُحوَّل تلقائياً بدون لاحقة.
#  3) انخفاض تقييم الفوركس والمؤشرات لغياب الحجم: عندما يكون حجم التداول صفراً تُستبعد فئة «الحجم/السيولة»
#     من الحد الأقصى للمجموع ومن متوسط الدرجة المركبة (إعادة توزيع الأوزان) بدل خسارة 8–16 نقطة.
#  4) _INFO_CACHE: لا يُخزَّن الفشل (خطأ 429 مثلاً) — يُخزَّن النجاح فقط، ومفتاح الكاش يتضمن قيمة deep،
#     مع إعادة محاولة عند التقييد.
# (ب) إصلاحات الملاحظات المتوسطة:
#  5) القيمة العادلة: حارس النطاق 0.5×–2.5×، نمو جراهام-نمو مقيد بـ15%، وزن المحلل الواحد 10%،
#     ولا يُربط التقدير بالأسلوب الفني التلقائي فقط (بديل فني موصوف عند غياب المالية).
#  6) كسور الأصول (Fractional): حجم الصفقة يسمح بكسور للعملات الرقمية/المعادن/العملات/المؤشرات
#     وعندما لا يكفي رأس المال لسهم واحد (بيتكوين/ذهب/رأس مال صغير مثل 10,000).
#  7) لغة الأسباب: التعريب عبر trtext على مستوى الصف (بلا سياق عام _LOC_CTX) — الأسباب تظهر بالعربية
#     دائماً في التقرير العربي وبالإنجليزية في الإنجليزي.
#  8) القوة النسبية للمرجع نفسه (ذهب/بيتكوين كمرجع لنفسه): يُستبعد مكون القوة النسبية من الدرجة
#     بإعادة توزيع الأوزان بدل قيمة صفرية تخفض التقييم.
#  9) البيانات الأقل من 200 شمعة: EMA200 الفارغ لا يُكتم سقف الاتجاه بصمت — الاتجاه يُحسب على المتوسطات
#     المتاحة فقط مع إعادة معايرة النسبة، وعلامة «تاريخ قصير» تظهر في الأسباب.
# 10) طغيان قرار «بيع» على الدرجة الموحدة: إشارة البيع الفنية لا تحول قراراً بدرجة ≥60 إلى بيع —
#     تُخفَّض إلى «متابعة» مع ذكر السبب، وتتوافق دائماً مع الدرجة الكلية.
# (ج) إصلاحات الملاحظات البسيطة:
# 11) التوقيت الصيفي لأمريكا: إغلاق جلسة US/FX يتحول تلقائياً بين 21:00 شتاءً و20:00 صيفاً (UTC).
# 12) تصنيف القطاعات: sector_profile بمطابقة حدود الكلمات (word boundaries) — «Electrical Equipment»
#     و«Waters» لم تعدا يُلتقطان خطأً بكلمات electric/water.
# 13) حد ROE: لا يُلغى ROE الحقيقي — يُستبعد فقط غير المنطقي (>500%)، والدرجة مقيدة داخلياً.
# 14) dividendYield: من العائد الفعلي ÷ السعر أولاً، مع كشف تضاعف النسب في المحاولات الاحتياطية.
# 15) ترميز البحث: تنظيف الرموز من علامات خاصة (‘ ’ ' ` &) قبل اللاحقة/القواميس.
# 16) مؤشرات إقليمية: ^CASE30 و^TASI.SR مع بديل ETF (KSA) ومؤشر تركيبي عند غياب البيانات. (🆕 v6.1: أُوقف EGPT — مطفأ على ياهو)
# (د) دعم المؤشرات والرموز الذكية:
# 17) البورصة المصرية: EGX30 ^CASE30 · EGX70 ^EGX70EWI.CA (وبديل ^CCSI) · EGX100 ^EGX100EWI.CA ·
#     EGX Shariah ^EGXSHARIAH.CA — مع محاولة المرشحين بالترتيب ثم بديل ETF/تركيبي.
# 18) أمريكا: Dow Jones ^DJI / S&P 500 ^GSPC / Nasdaq ^IXIC / Nasdaq100 ^NDX كلها مراجع متاحة.
# 19) تعيين ذكي للرموز (Smart Symbol Mapping): INTC→إنتل مباشرة · JUFO→جهينة تلقائياً عبر .CA ·
#     XAUUSD→الذهب GC=F · GOLD/SILVER/WTI… · أسماء شائعة (INTEL/APPLE/جوهينة…) بقاموس الأسماء.
# (هـ) سلامة مؤكدة (لا تُعدَّل): مؤشرات RSI/ATR/ADX/EMA/WMA/CMF/Chop/SuperTrend مطابقة، الصفقة الافتراضية
#     بلا بيانات مستقبلية، نماذج Piotroski/Altman/Beneish/Graham سليمة، جلسات مصر والسعودية صحيحة.
# ----------------------------------------------------------------------------------------------
# 🆕🆕 v6.1 — إصلاحات من لقطات شاشة المستخدم (2026-11-01) — دون أي تأثير على بقية الكود:
# 20) خطأ «HTTP Error 404: Quote not found for symbol: EGPT» (المرفق 3): صندوق EGPT أوقفته ياهو نهائياً،
#     وكان v6 يجربه كبديل لمؤشر مصر في كل فحص — أُوقف الطلب (بقي بديل TASI: KSA)؛ تغطية EGX تتم عبر
#     الرموز البديلة (^CCSI…) ثم المؤشر التركيبي المتساوي الأوزان كما في السابق، فلا مزيد من أخطاء 404.
# 21) التصدير لا يبدأ التنزيل مثل الكود الأساسي (المرفق 2): كروم/كولاب يحجب التنزيلات التلقائية المتتالية
#     بعد الأولى — أصبح التنزيل موثوقاً: مهلة 1.2 ثانية بين ملفات التصدير المتعددة (PNG مثلاً)، وإظهار
#     حالة واضحة «⬇️ الملف + حجمه» بعد كل تصدير، مع إرشاد فوري لطريقة التحميل اليدوي من مجلد
#     ER1991_Reports أو السماح بتنزيل «ملفات متعددة» من أيقونة القفل — دوال التصدير نفسها كما هي تماماً.
# 🆕🆕🆕 v6.2 — إصلاح تأخر أسعار البورصة المصرية (طلب المستخدم 2026-11-02) — بقية الكود والحسابات والتصميم كما هي دون حذف:
# 22) المشكلة: ياهو فاينانس لا يحدّث أسعار أسهم .CA أولاً بأول — في تقرير 2026-11-02 كانت آخر شمعة لكل أسهم مصر 2026-10-29
#     (تأخر 3 أيام تقويمية = جلسة كاملة) فتُحسب كل المؤشرات والقرارات على سعر قديم (مثال: COMI 120.47 بدل 118 الحالي).
#     الحل: قبل التحليل تُقرأ أسعار كل أسهم البورصة المصرية (كل EGX وليس أسهماً بعينها) دفعة واحدة من ماسح TradingView
#     (نفس مصدر قائمة المتابعة المصوّرة) وتُضاف كشمعة سعر اليوم/آخر جلسة فوق تاريخ ياهو (أو تُستبدل شمعة نفس اليوم) —
#     فتُحسب كل النتائج (RSI/ATR/الأهداف/القيمة العادلة/الصفقة الافتراضية…) على السعر الحالي. الدوال الجديدة: apply_egx_live /
#     egx_live_snapshot / egx_universe (القسم 3b). تحقق أمان: رفض أي سعر ينحرف >50% عن آخر إغلاق (رمز غير مطابق/تجزئة)،
#     وعدم تكرار شمعة عطلة رسمية، وعند فشل الاتصال تظهر رسالة تحذير واضحة بدل الصمت.
# 23) إغلاق جلسة EGX يحسب بتوقيت القاهرة (14:30 محلياً) مع التوقيت الصيفي المصري بدل ثابت 12:30 UTC.
# 24) رموز بديلة لمصر: COMI.EGX / COMI.CAI / COMI.EG → COMI.CA. وتصحيح مفتاح قاموس الأسماء 'COCAcola' (لم يكن يطابق أبداً).
# 25) مؤشر EGX30 المرجعي يُحدَّث بشمعة اليوم من TradingView عند توفره (وإلا يبقى كما كان، والمؤشر التركيبي يستفيد من الأسعار الحية).
# 🆕🆕🆕🆕 v6.3 — تدقيق القيمة العادلة والحسابات (طلب المستخدم 2026-11-02) — لا حذف لأي منطق أو تصميم:
# 26) القيمة العادلة كانت تتغير بين فحصين لنفس السهم رغم ثبات EPS وBVPS: مضاعف P/E كان مرتبطاً بـ«الأسلوب» (12 للقيمة · 25 للنمو ·
#     18 لغيرهما) والأسلوب يُقترح تلقائياً من RSI/CMF/حجم اليوم فيتبدل مع حركة السعر — فتتحول القيمة العادلة لنفس السهم من 12.85 إلى 17.06
#     (JUFO) ومن 18.35 إلى 21.59 (FWRY) دون أي تغيير في الأساسيات. القيمة العادلة قيمة جوهرية يجب ألا تتبع أسلوب المتاجرة.
#     الإصلاح: مضاعف محايد موحّد = 15× (سقف غراهام للمستثمر الدفاعي ومتوسط P/E العالمي طويل الأجل) في fair_value وdeep_analysis معاً
#     (الدرجة العميقة/هامش الأمان الراداري). مفتاحان: fvNeutralPE=15.0 · fvStyleLinkedPE=False (True يعيد السلوك القديم).
# 27) حارس القيمة العادلة (استبعاد نموذج أقل من 0.5× أو أكثر من 2.5× السعر) صار يستند إلى الأوسع من «السعر الحالي» و«وسيط إغلاق سنة»
#     بدل سعر اليوم وحده — فلا يدخل نموذج أو يخرج بسبب حركة يوم واحد. معادلات النماذج (P/E · Graham Number · Graham-Growth · المحللون) كما هي.
# 28) أخطاء yfinance الطويلة (مثل TAQA.CA: «possibly delisted») لم تعد تُطبع مكررة؛ يظهر بدلها سطر واحد واضح في السجل مع السعر الحالي من
#     TradingView للسهم الذي لا يوفر ياهو تاريخه (التحليل الفني يحتاج ≥60 شمعة تاريخية).
# 🆕🆕🆕🆕🆕 v6.4 — مضاعف عادل لكل سوق + بدائل تاريخ مصر (طلب المستخدم 2026-11-02) — لا حذف لأي منطق أو تصميم:
# 29) مضاعف P/E العادل صار مشتقاً من الفائدة الخالية من المخاطر لكل سوق بصيغة جوردون: P/E = (1+g) ÷ (r − g) حيث r = الفائدة الخالية + علاوة مخاطر
#     السوق وg = النمو الاسمي طويل الأجل (= التضخم، أي بلا نمو حقيقي) ويُقيَّد بين 5 و15. المدخلات في جدول FV_COE وكلها تقديرية قابلة للتعديل.
#     أمريكا = 15 (مطابق للسابق) · السعودية ≈ 11.3 · مصر ≈ 8.6 (بمدخلات 20% فائدة · 12% تضخم · 5% علاوة). نتائج مصر حساسة جداً لهذه المدخلات.
#     مفاتيح: fvMarketPE=True (False = مضاعف محايد 15 لكل الأسواق كما في v6.3).
# 30) حارس القيمة العادلة: الحد الأدنى (0.5× السعر) يتناسب الآن مع مضاعف السوق (×مضاعف السوق ÷ 15). السبب: مع مضاعف مصر 8.6 تقع نماذج P/E وGraham
#     لأي سهم غالٍ (P/E>17) تحت 0.5× السعر فتُستبعد ولا يبقى إلا جراهام-نمو المتفائل (FWRY كانت ستظهر +100% بدل −14%). أمريكا لا تتأثر (15÷15=1).
# 31) عمود جديد «مضاعف P/E العادل» (fv_pe_x) في مجموعة القيمة العادلة يوضح المضاعف المستخدم لكل سهم.
# 32) بديل تاريخ البورصة المصرية: إن لم يوفر ياهو تاريخ سهم مصري (مثل TAQA) أو مؤشر EGX30/EGX70 يُجلب من TradingView عبر مكتبة tvDatafeed
#     (اختيارية: pip install git+https://github.com/rongardF/tvdatafeed.git — تُثبَّت تلقائياً في كولاب). لا يغطي البيانات المالية (تبقى من ياهو).
# 🆕🆕🆕🆕🆕🆕 v6.5 — تعميم سعر اليوم على السعودية + مدخلات القيمة العادلة قابلة للتعديل من الواجهة (2026-11-03) — لا حذف لأي منطق أو تصميم:
# 33) ملف نتائج 2026-11-03 أظهر أن أسهم السعودية الـ19 كلها بآخر شمعة 2026-11-01 رغم تداول الاثنين 2-11 (نفس تأخر ياهو الذي ظهر في مصر).
#     عُمِّمت آلية TradingView: سعر جلسة اليوم لأسهم .SR من ماسح /ksa/scan (TADAWUL:xxxx) + تاريخ السهم/مؤشر TASI عبر tvDatafeed إن غاب على ياهو
#     (فيُستبدل بديل ETF بمؤشر تاسي الحقيقي). دوال عامة: live_snapshot(mk) · apply_live(prices, mk) · apply_index_live · fill_tv_history · fill_tv_index
#     (أسماء مصر القديمة باقية كما هي). جلسة تداول: الأحد–الخميس 10:00 بتوقيت الرياض.
# 34) مدخلات مضاعف القيمة العادلة (الفائدة/التضخم/العلاوة لكل سوق) صارت حقولاً في الواجهة (⚙️ مدخلات القيمة العادلة) أو p_over={'fvCoe': {...}}
#     فلا حاجة لتعديل الكود عند تغيّر الفائدة؛ وكل تشغيل يسجّل المضاعف المستخدم، ويحذّر إن تجاوز عمر جدول FV_COE 120 يوماً (FV_COE_ASOF).
# 🆕🆕🆕🆕🆕🆕🆕 v6.6 — مطابقة مؤشري Pine (مراجعة 2026-11-11) — لا حذف لأي منطق أو تصميم أو نتيجة:
# 35) عدّادات الوصول TP1/TP2/TP3 لا تُحتسب في شمعة AMBIGUOUS (مطابقة tp1Event/tp2Event/tp3Event في Pine).
# 36) أسلوب Long Term: اكتمال الشمعة يُقاس أسبوعياً (week_closed) كما في time_close للإطار W بدل اكتمال جلسة اليوم.
# 37) VPOC بلا حجم يعيد NaN (كما في Pine) بدل مركز أول شريحة.   38) الدعم/المقاومة التلقائي: محاكاة تسلسلية مطابقة (قائمة 5 + حذف المكسور).
# 39) انحياز الاتجاه bias يعرف حالة التعادل (0).   40) الماسح يعرف STANDBY.   41) عمود rd_rr_mkt يُملأ.
# 42) ADX/DMI بذر RMA بلا أصفار، EMA/RMA ببذر SMA مثل Pine (مفتاح pineSeed)، الفحص السريع يستخدم نفس EMA.
# 43) خيار تعويض الفجوة gapAware (موجود في Pine، مطفأ افتراضياً).
# 44) مفتاح pineParity=True: عتبات ATR% ثابتة · الاتجاه 3 مقارنات · RS بوزن 1 عند غياب المرجع · فئة الحجم باقية في الحد الأقصى ·
#     الأقران على scChg وحالة 0 · مضاعف Deep حسب الأسلوب (12/18/25) · الارتباط على الأسعار الخام. False = سلوك v6.5 كما كان.
#     والافتراضيات صارت مطابقة لـPine: beNextBar=False وuseCorr=True. + دالة selftest() للفحص الذاتي.
# 🆕🆕🆕🆕🆕🆕🆕🆕 v7.0 — مراجعة 2026-11-12 (ملاحظات المستخدم على سهم السويدي SWDY.CA) — لا حذف لأي منطق أو نتيجة أخرى:
# 45) القيمة السوقية: ياهو يعيد أحياناً marketCap قديماً (SWDY: 102B ≈ 47.7×2.14B سهم بينما الحقيقي ≈ 260B). الآن تُقارَن بـ(السعر الحالي × عدد الأسهم)
#     وبقيمة TradingView (لمصر والسعودية): عند الانحراف >15% تُستبدل بالمحسوبة، ويُعرض مصدرها في عمود mcap_src. وهي تدخل في Altman Z فتصحّح معه.
# 46) EPS: الأولوية لـ TTM من TradingView (مصر/السعودية) ← trailingEps ← مجموع 4 أرباع ← السنوي. مع حماية العملة (ADR) بمقارنة السعر/PE.
#     مصدر EPS يظهر في العمود fv_eps_src، ويُخفَّض مستوى ثقة القيمة العادلة عند الاعتماد على EPS سنوي قديم.
# 47) مضاعف P/E العادل: النمو الاسمي طويل الأجل = (1+التضخم)×(1+النمو الحقيقي)−1 (كان = التضخم فقط أي نمو حقيقي صفر فيظلم أسواق التضخم المرتفع:
#     مصر 8.6× → 11.3×). جدول FV_COE فيه حقل gr (النمو الحقيقي %). علاوة/خصم نمو وجودة (Piotroski/ROE/FCF/Altman/Beneish) مقيّدة.
# 48) نماذج القيمة العادلة صارت 7: P/E العادل · P/B عادل بـ ROE (الأساس للبنوك) · رقم جراهام مُعايَر للسوق (k = 22.5 × مضاعف السوق ÷ 15) ·
#     جراهام-نمو بالنمو الحقيقي (بعد خصم التضخم) · مضاعف نسبي من وسيط القطاع/السوق (من ماسح TradingView) · هدف المحللين · «هدف خارجي» تُدخله أنت
#     (مثل متوسط بنوك الاستثمار) بوزن قابل للتعديل. أوزان مختلفة للقطاع المالي. ثقة القيمة العادلة (0–100) وتقل وزنها/أثرها في القرار عندما تقل الثقة.
# 49) فلتر «نوع الاستثمار» في HTML + إصلاح التصنيف: عند اختيار أسلوب محدد تُفحص كل الأسهم وتُرتَّب وتُعرض حصرياً بهذا الأسلوب (عمود «نوع الاستثمار» = الأسلوب
#     المستخدم)، وعند Auto يُختار النوع لكل سهم بقواعد فنية + أساسية ثم يُرتَّب حسب قرار الشراء ثم الدرجة.
# 50) حالة السوق المؤسسية (مطابقة Pine v4.2): انهيار / سوق هابط / تصحيح / تراجع / ضعف / صحي / تعافٍ + قمة جديدة + ارتداد غير مؤكد، بعتبات قابلة للتعديل.
# 51) لوحة إعدادات خارجية في الواجهة (تبويبات: القيمة العادلة · السوق · الرادار · الحارس · الخطة · الأسلوب) + تصدير/استيراد الإعدادات كنص JSON — فلا حاجة لتعديل الكود.
# 52) واجهة HTML: خط Cairo (مضمَّن في الملف عند توفر التحميل ليعمل دون إنترنت) + تصميم مالي احترافي + لوحة مؤشرات + فلتر نوع الاستثمار — بنفس التفاعلية.
# أداة مساعدة في قراءة وفحص الأسهم والقرار الاستثماري، وليست توصية بالشراء أو البيع.
# =====================================================================================
# %% [الخلية 1] ———— التثبيت (شغّلها مرة واحدة في كولاب)
import subprocess, sys, os
def _pip(*pk):
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', *pk], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if 'google.colab' in sys.modules or os.path.exists('/content'):
    _pip('yfinance>=0.2.40', 'xlsxwriter', 'weasyprint', 'pdf2image', 'plotly', 'gspread', 'openpyxl')
    _pip('git+https://github.com/rongardF/tvdatafeed.git')      # 🆕 v6.4: اختياري — تاريخ مصر من TradingView عند نقص ياهو
    subprocess.run('apt-get -qq install -y fonts-noto-core fonts-noto-color-emoji poppler-utils > /dev/null 2>&1', shell=True)

# %% [الخلية 2] ———— الكود الرئيسي
import subprocess, sys, os   # 🆕 v6: استيراد مستقل للخلية حتى تعمل حتى لو لم تُشغَّل خلية التثبيت
import warnings, math, json, io, re, time, zipfile, datetime as dt, html as _html
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')
try:
    import yfinance as yf
except Exception:      # يسمح باختبار المنطق بدون إنترنت
    yf = None
logging.getLogger('yfinance').setLevel(logging.CRITICAL)   # 🆕 v6.3: لا نُغرق الشاشة برسائل ياهو المكررة — يُعرض بدلها سطر واحد واضح في السجل

MAX_SYMBOLS = 100
OUT_DIR = '/content/ER1991_Reports' if os.path.exists('/content') else os.path.abspath('./ER1991_Reports')
os.makedirs(OUT_DIR, exist_ok=True)
NaN = float('nan')
def nn(x):  # not-NaN
    return x is not None and x == x

# -----------------------------------------------------------------------------
# 1) الإعدادات (نفس القيم الافتراضية للمؤشرين)
# -----------------------------------------------------------------------------
P = dict(
    # ── تحليل الشارت (الفئات السبع والأزرار والإشارات) ──
    emaFast=5, smaSlow=16, wmaLen=52, chopLen=14, chopTrend=38.2, chopChoppy=61.8,
    stPeriod=10, stMult=3.0, atrPeriod=14, rsiFast=8, rsiSlow=14,
    stochK=11, stochD=4, stochSmooth=4, macdFast=11, macdSlow=23, macdSignal=10,
    cmfLen=20, volPressLen=20, marketStateLen=20, msHigh=1.5, msLow=0.7,
    minScore=9, minCats=3, cooldown=5, useCatConf=True, allowOpposite=True,
    wRSI=1, wMACD=1, wEMA=1, wVWAP=2, wCMF=1, wVolPress=1, wDiv=3, wSweep=3, wMS=4, wSqueeze=1, wSMC=2, wPat=1,
    pctAplus=85.0, pctA=70.0, pctBplus=55.0, pctB=40.0,
    fastBreakMaxAge=20, smcBiasMaxAge=30, fractalArm=2, sweepLookback=20, bbPeriod=20,
    crashPct=3.0, gapATR=2.0, useGapFilter=True, useFastBreak=True,
    smcOBLookback=15, smcMaxOB=3, vwapLen=20,
    srPivot=10, srMax=5,
    slATR=1.0, tp1ATR=0.5, tp2ATR=1.5, tp3ATR=3.0, beAfterTP1=True, beNextBar=False, ambAsLoss=True,   # 🆕 v6.6: beNextBar=False (الافتراضي مطابق لـPine: الوقف يُفحص في نفس شمعة TP1) — True = سلوك v5.2 (من الشمعة التالية)
    requireHTF=True, useCorr=True, corrLen=20, corrThresh=0.3,   # 🆕 v6.6: useCorr=True مطابق لـPine
    # ── Radar ──
    riskLow=2.0, riskHigh=4.0, crashCandle=3.0, lookbackManual=50, cmfManual=20,
    stopAtr=2.0, targetAtr=3.0, capAtRes=True, capAtEma=True, gapThresh=3.0,
    mktCorrPct=5.0, minTradedValue=0.0, closedAsConfirmed=True, stabilize=True,
    # الحارس (نفس نظام الحماية في إصدار TradingView): يخفض «شراء قوي» إلى «شراء عند التراجع» عند تحقق أي شرط
    guardOn=True, guardRiskMax=80.0, guardChase=6.0, guardNeedTech=True, guardOnCorr=True,
    # ── عام ──
    capital=10000.0, riskPct=1.0, zbTargetR=1.5, zbStopATR=0.5,
    vtOn=True,   # 🆕 v5.0 إظهار الصفقة الافتراضية في النتائج (مفتاح قبل الفحص)
    fibMktDDCrash=-15.0,   # 🆕 v5.0 حد اعتبار هبوط المؤشر العام «انهياراً» (%)
    # أوزان الدرجة الموحدة
    wUniRadar=0.35, wUniPrime=0.30, wUniFair=0.20, wUniDeep=0.15,
    # 🆕 v5.2 مفاتيح السلوك الجديدة (كلها يمكن إيقافها بوضعها False)
    entryFirst=True,       # إظهار «إشارة الشراء/البيع الآن» قبل «صفقة جارية» في قرار تحليل الشارت
    epsFallback=True,      # EPS بديل من القوائم السنوية عند غيابه في info (يُفعّل P/E وجراهام للأسهم المصرية)
    fvGuardLo=0.5, fvGuardHi=2.5,   # حارس القيمة العادلة: استبعاد النماذج أقل من نصف السعر أو أكثر من 2.5 ضعفه
    fvSingleAnalystW=0.10, # وزن هدف المحللين عندما يكون هناك محلل واحد فقط (بدل 25%)
    fvTechCut=True,        # وزن القيمة العادلة الفنية = نصف وزنها في الدرجة الموحدة (لأنها ليست تقييمًا ماليًا)
    noShortAsAvoid=True,   # أسواق مصر/السعودية: قرار «بيع» يُعرض «تجنّب/خروج» لأن البيع على المكشوف غير متاح للأفراد
    sectorAware=True,      # استبعاد Altman Z وهامش FCF عن البنوك/التأمين/المرافق/العقار (غير معبّرين عنها)
    monthlyData=True,      # تحميل بيانات شهرية 10 سنوات ليعمل إطار M1 في مصفوفة الأطر دائمًا
    # أوزان نماذج القيمة العادلة
    fvNeutralPE=15.0,        # 🆕 v6.3: مضاعف P/E المحايد (سقف غراهام ومتوسط السوق العالمي طويل الأجل) — مستقل عن الأسلوب والسعر
    fvStyleLinkedPE=False,   # 🆕 v6.3: True = السلوك القديم (12/18/25 حسب الأسلوب)
    fvMarketPE=True,         # 🆕 v6.4: مضاعف P/E العادل حسب الفائدة الخالية من المخاطر لكل سوق (جدول FV_COE) بدل 15 للجميع
    fvGuardScaleLo=True,     # 🆕 v6.4: الحد الأدنى للحارس يتناسب مع مضاعف السوق (أمريكا بلا تغيير)
    tvHistoryFallback=True,  # 🆕 v6.4: تاريخ مصر من TradingView (tvDatafeed) عند نقص ياهو
    fvRefLookback=252,       # 🆕 v6.3: نافذة وسيط الإغلاق لمرساة حارس القيمة العادلة (سنة تداول)
    pineParity=True, pineSeed=True, gapAware=False,   # 🆕 v6.6: pineParity = مطابقة Pine حرفياً (False = سلوك v6.5) · pineSeed = بذر EMA/RMA بـSMA مثل Pine · gapAware = تعويض الفجوة في كشف الانهيار
    # ── 🆕 v7.0: القيمة العادلة v2 ──
    fvTvFund=True,           # بيانات TradingView الأساسية (EPS TTM + القيمة السوقية + مضاعفات القطاع/السوق) لمصر/السعودية/أمريكا
    fvRelOn=True,            # نموذج المضاعف النسبي (وسيط القطاع/السوق)
    fvRelMinPeers=5,         # أقل عدد شركات في القطاع ليُستخدم وسيط القطاع (وإلا وسيط السوق)
    fvMinConf=60.0,          # أدنى ثقة لتؤثر القيمة العادلة بكامل وزنها في القرار
    fvGrowthW=0.5,           # وزن نمو الشركة الفعلي في النمو المتوقع (0–1)
    fvPeHardCap=25.0,        # سقف مضاعف P/E العادل بعد علاوة النمو
    fvPbMin=0.5, fvPbMax=4.0, fvGrahamScale=True,   # fvGrahamScale: رقم جراهام = 22.5 × مضاعف السوق ÷ 15
    fvBand=15.0, fvDeepBand=30.0,   # نطاق «عادل» ± وحد الخصم/العلاوة الكبيرة
    fvW=dict(pe=0.40, pb=0.10, graham=0.05, grahamG=0.05, rel=0.15, analyst=0.25, ext=0.35),
    fvWFin=dict(pe=0.20, pb=0.45, graham=0.05, grahamG=0.00, rel=0.15, analyst=0.25, ext=0.35),
    fvExt={},                # {'SWDY': 115.6} هدف خارجي (مثل متوسط بنوك الاستثمار) يدخل كنموذج مستقل
    # ── 🆕 v7.0: حالة السوق المؤسسية ──
    mktCrashDay=7.0, mktCrashWin=10.0, mktCorrDD=10.0, mktBearDD=20.0, mktBounceMin=5.0,
    # ── 🆕 v7.0: نوع الاستثمار والترتيب ──
    autoStyleFund=True,      # تصنيف Auto يستعين بالأساسيات (P/E · P/B · نمو EPS) إلى جانب الفني
    sortByDecision=True,     # الترتيب النهائي: قرار الشراء ثم الدرجة
)

# -----------------------------------------------------------------------------
# 2) الرموز والأسواق
# -----------------------------------------------------------------------------
_EX_EG = {'EGX', 'EGS', 'CASE', 'EGYPT', 'NASDAQ_EG'}
_EX_SA = {'TADAWUL', 'TASI', 'SAU', 'SAUDI', 'SR'}
# 🆕 v6: مؤشرات البورصة المصرية على ياهو — تُجرَّب المرشحات بالترتيب وعند الفشل يُستخدم بديل ETF/تركيبي
_EGX_INDICES = {'EGX30': ['^CASE30'], 'EGX_30': ['^CASE30'],
                'EGX70': ['^EGX70EWI.CA', '^CCSI'], 'EGX_70': ['^EGX70EWI.CA', '^CCSI'],
                'EGX100': ['^EGX100EWI.CA'], 'EGX_100': ['^EGX100EWI.CA'],
                'EGXSHARIAH': ['^EGXSHARIAH.CA'], 'EGX_SHARIAH': ['^EGXSHARIAH.CA'], 'SHARIAH': ['^EGXSHARIAH.CA']}
# 🆕 v5.2: تعريب رموز المعادن/السلع والعملات الرقمية والفوركس (كل فئات الأصول)
_COMMODITY_ALIASES = {'XAUUSD': 'GC=F', 'GOLD': 'GC=F', 'XAU': 'GC=F', 'XAGUSD': 'SI=F', 'SILVER': 'SI=F', 'XAG': 'SI=F',
                      'WTI': 'CL=F', 'OIL': 'CL=F', 'CRUDE': 'CL=F', 'BRENT': 'BZ=F', 'NATGAS': 'NG=F', 'GAS': 'NG=F',
                      'COPPER': 'HG=F', 'PLATINUM': 'PL=F', 'PALLADIUM': 'PA=F', 'WHEAT': 'ZW=F', 'CORN': 'ZC=F', 'SOYBEAN': 'ZS=F'}
_CRYPTO_NAMES = {'BTC', 'XBT', 'ETH', 'XRP', 'SOL', 'ADA', 'DOGE', 'BNB', 'LTC', 'TRX', 'DOT', 'LINK', 'MATIC', 'POL', 'AVAX', 'TON',
                 'SHIB', 'XLM', 'BCH', 'NEAR', 'ATOM', 'ETC', 'FIL', 'ARB', 'OP', 'INJ', 'SUI', 'PEPE', 'APT', 'ICP', 'HBAR', 'VET',
                 'ALGO', 'AAVE', 'UNI', 'ETC2', 'RENDER', 'RNDR', 'SEI', 'TIA', 'STX', 'FET', 'AGLD', 'EOS', 'XMR', 'ZEC', 'DASH'}
# 🆕 v6 (إصلاح 2): رموز رقمية متقاطعة مع أسهم حقيقية على ياهو (DASH=DoorDash، STX=Seagate، SOL=Emeren،
# ATOM/LINK/FET/NEAR/…) — لا تعتبر عملات رقمية إلا إذا أُلحق بها -USD أو USDT/USD صراحةً.
_CRYPTO_AMBIGUOUS = {'DASH', 'STX', 'SOL', 'ATOM', 'LINK', 'FET', 'NEAR', 'OP', 'ARB', 'EOS', 'ETC', 'SUI', 'APT', 'TIA',
                     'INJ', 'FIL', 'ICP', 'HBAR', 'VET', 'ALGO', 'AAVE', 'UNI', 'AGLD', 'RENDER', 'RNDR', 'POL', 'MATIC',
                     'TON', 'ADA', 'LTC', 'TRX', 'DOT', 'AVAX', 'XLM', 'BCH', 'XMR', 'ZEC', 'PEPE'}
_FX_CODES = {'USD', 'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'CAD', 'NZD', 'SAR', 'AED', 'EGP', 'KWD', 'QAR', 'BHD', 'OMR', 'JOD', 'TRY',
             'SEK', 'NOK', 'DKK', 'PLN', 'CZK', 'HUF', 'ZAR', 'MXN', 'CNY', 'HKD', 'SGD', 'THB', 'KRW', 'INR', 'BRL', 'ILS', 'PKR'}
# 🆕 v6 (طلب 5): تعيين ذكي للأسماء الشائعة — كتابة الاسم تُحوَّل تلقائياً لرمز ياهو (INTEL→INTC، جوهينة→JUFO.CA…)
_NAME_ALIASES = {
    # شركات أمريكية/عالمية شائعة
    'INTEL': 'INTC', 'APPLE': 'AAPL', 'MICROSOFT': 'MSFT', 'GOOGLE': 'GOOGL', 'ALPHABET': 'GOOGL', 'AMAZON': 'AMZN',
    'TESLA': 'TSLA', 'NVIDIA': 'NVDA', 'FACEBOOK': 'META', 'META': 'META', 'NETFLIX': 'NFLX', 'PAYPAL': 'PYPL',
    'COCACOLA': 'KO', 'COCA': 'KO', 'PEPSI': 'PEP', 'DISNEY': 'DIS', 'BOEING': 'BA', 'MCDONALDS': 'MCD', 'MCDONALD': 'MCD',
    'STARBUCKS': 'SBUX', 'NIKE': 'NKE', 'IBM': 'IBM', 'SALESFORCE': 'CRM', 'ADOBE': 'ADBE', 'QUALCOMM': 'QCOM',
    'CISCO': 'CSCO', 'ORACLE': 'ORCL', 'AMD': 'AMD', 'BROADCOM': 'AVGO', 'TOYOTA': 'TM', 'SAMSUNG': '005930.KS',
    # البورصة المصرية (الأكثر تداولاً — تُكتب بالإنجليزية أو بحرف أول مختصر)
    'COMI': 'COMI.CA', 'HRHO': 'HRHO.CA', 'JUFO': 'JUFO.CA', 'TMGH': 'TMGH.CA', 'ABUK': 'ABUK.CA', 'SWDY': 'SWDY.CA',
    'ETEL': 'ETEL.CA', 'AMOC': 'AMOC.CA', 'EGAL': 'EGAL.CA', 'EKHO': 'EKHO.CA', 'HELI': 'HELI.CA', 'ORHD': 'ORHD.CA',
    'ORAS': 'ORAS.CA', 'SUGR': 'SUGR.CA', 'EAST': 'EAST.CA', 'CANPH': 'CANPH.CA', 'CIRA': 'CIRA.CA', 'GWLD': 'GWLD.CA',
    'ALCN': 'ALCN.CA', 'DSCW': 'DSCW.CA', 'ISPH': 'ISPH.CA', 'RMDA': 'RMDA.CA', 'CLHO': 'CLHO.CA', 'PRMH': 'PRMH.CA',
    'FWRY': 'FWRY.CA', 'ADIB': 'ADIB.CA', 'EFID': 'EFID.CA', 'ZMID': 'ZMID.CA', 'MTIE': 'MTIE.CA',
    # أسماء عربية شائعة (كلمة واحدة)
    'جوهينة': 'JUFO.CA', 'التجاري': 'COMI.CA', 'قناة': 'CANPH.CA', 'ابوقير': 'ABUK.CA', 'هرمي': 'HRHO.CA',
    'سمارت': 'SWDY.CA', 'فوري': 'FWRY.CA', 'الاهلية': 'ABUK.CA', 'طيبة': 'TMGH.CA',
}

def _san(sym):
    """🆕 v6 (إصلاح 15): تنظيف الرموز من علامات خاصة (اقتباسات ووصلات) قبل أي بحث/مطابقة."""
    s = str(sym)
    for ch in ("'", '’', '‘', '`', '&', '"'):
        s = s.replace(ch, '')
    return s.strip()

def _crypto_pair(sym):
    """يحوّل BTCUSDT/BTCUSD إلى صيغة ياهو BTC-USD (ويهمل لاحقات USDT/USD/BUSD/USDC)."""
    s = str(sym).upper()
    m = re.fullmatch(r'([A-Z0-9]{2,10})(USDT|USD|BUSD|USDC)', s)
    if m and m.group(1) in _CRYPTO_NAMES:
        return m.group(1) + '-USD'
    return None

def asset_class(sym):
    """🆕 v5.2: نوع الأصل من الرمز — stock/crypto/forex/commodity/index (يُوجّه المعايرة والأساسيات والجلسة)."""
    s = str(sym).upper()
    if s.startswith('^'):
        return 'index'
    if s.endswith('=F'):
        return 'commodity'
    if s.endswith('=X'):
        return 'forex'
    if re.fullmatch(r'[A-Z0-9]{2,12}-[A-Z]{3,4}', s):
        return 'crypto'
    return 'stock'

ASSET_TXT = {'stock': ('Stock', 'سهم'), 'crypto': ('Crypto', 'عملة رقمية'), 'forex': ('Forex', 'عملات (فوركس)'),
             'commodity': ('Commodity/Metal', 'معادن وسلع'), 'index': ('Index', 'مؤشر')}
# عتبات المخاطرة (ATR%) لكل فئة أصول على الإطار اليومي — تُضرب في √5 على الإطار الأسبوعي
ASSET_RISK = {'crypto': (5.0, 10.0), 'forex': (1.0, 2.0), 'commodity': (2.5, 5.0), 'index': (1.5, 3.0)}
# أسواق بلا بيع مكشوف للأفراد (يُعرض «تجنّب/خروج» بدل «بيع»)
NO_SHORT_MARKETS = {'EGX', 'TASI'}

def normalize_symbol(raw, market='AUTO'):
    """يحوّل صيغة TradingView/المستخدم إلى صيغة yfinance (أسهم + رقمية + فوركس + معادن + مؤشرات مصر).
    🆕 v6: الرموز المتقاطعة مع أسهم (DASH/STX/SOL/…) لا تصبح عملات رقمية إلا بلاحقة -USD/USDT صراحةً،
    مع تعيين ذكي للأسماء الشائعة (INTEL→INTC، JUFO→JUFO.CA، XAUUSD→GC=F، جوهينة→JUFO.CA)."""
    if raw is None:
        return None
    s = str(raw).strip().upper().replace(' ', '')
    s = _san(s)
    if not s:
        return None
    if s in _COMMODITY_ALIASES:
        return _COMMODITY_ALIASES[s]
    if s in _NAME_ALIASES:
        return _NAME_ALIASES[s]
    m_eg = re.fullmatch(r'([A-Z0-9]{2,10})\.(EGX|CAI|EG)', s)      # 🆕 v6.2: COMI.EGX / COMI.CAI / COMI.EG → COMI.CA
    if m_eg:
        return m_eg.group(1) + '.CA'
    if ':' in s:
        ex, sym = s.split(':', 1)
        if ex in _EX_EG:
            if sym in _EGX_INDICES:
                return _EGX_INDICES[sym][0]
            return '^CASE30' if sym in ('EGX30', 'EGX_30') else sym + '.CA'
        if ex in _EX_SA:
            return '^TASI.SR' if sym == 'TASI' else sym + '.SR'
        cp = _crypto_pair(sym)          # 🆕 BINANCE:BTCUSDT وغيرها
        if cp:
            return cp
        if sym in _NAME_ALIASES:
            return _NAME_ALIASES[sym]
        s = sym
    if s in _EGX_INDICES:               # 🆕 v6: EGX30/EGX70/EGX100/EGX Shariah بأي صيغة
        return _EGX_INDICES[s][0]
    if s in ('TASI',):  return '^TASI.SR'
    cp = _crypto_pair(s)                # 🆕 BTCUSDT → BTC-USD (لاحقة صريحة دائماً)
    if cp:
        return cp
    # 🆕 v6 (إصلاح 2): الاسم المجرّد يتحول لعملة رقمية فقط إذا كان غير متقاطع مع أسهم ياهو
    if s in _CRYPTO_NAMES and s not in _CRYPTO_AMBIGUOUS:
        return s + '-USD'
    if re.fullmatch(r'[A-Z]{6}', s) and s[:3] in _FX_CODES and s[3:] in _FX_CODES:
        return s + '=X'                 # 🆕 EURUSD → EURUSD=X
    if s.startswith('^') or '.' in s or '=' in s or '-' in s:
        return s
    if market == 'EGX': return s + '.CA'
    if market == 'TASI': return s + '.SR'
    if market == 'AUTO' and s.isdigit() and len(s) == 4: return s + '.SR'
    return s

def parse_symbols(text, market='AUTO'):
    toks = re.split(r'[,\n;\t\s]+', text or '')
    seen, out = set(), []
    for t in toks:
        s = normalize_symbol(t, market)
        if s and s not in seen:
            seen.add(s); out.append(s)
    return out[:MAX_SYMBOLS], max(0, len(set(filter(None, (normalize_symbol(t, market) for t in toks)))) - MAX_SYMBOLS)

def market_of(sym):
    if sym.endswith('.CA') or sym == '^CASE30': return 'EGX'
    if sym.endswith('.SR') or sym == '^TASI.SR': return 'TASI'
    ac = asset_class(sym)
    if ac == 'crypto': return 'CRYPTO'
    if sym.endswith('=X'): return 'FX'
    if sym.endswith('=F'): return 'CMDTY'
    return 'US'

BENCH_BY_MARKET = {'US': '^NDX', 'EGX': '^CASE30', 'TASI': '^TASI.SR',
                   'CRYPTO': 'BTC-USD', 'FX': 'DX-Y.NYB', 'CMDTY': 'GC=F'}
# 🆕 v5.1: بديل ETF متوفر على ياهو عندما يفشل مؤشر السوق نفسه (يحدث حالياً مع ^CASE30 و ^TASI.SR: ياهو لا يعيد سوى صف واحد)
# 🆕 v6.1: حُذف بديل مصر ETF (EGPT) لأن ياهو أوقفته — كل فحص كان يُظهر «HTTP Error 404: Quote not found for symbol: EGPT» دون فائدة.
#    تغطية EGX تتم كما هي عبر: رموز بديلة (^CCSI وغيرها) ثم المؤشر التركيبي المتساوي الأوزان عند غياب البيانات.
_BENCH_PROXY = {'TASI': 'KSA'}
BENCH_OPTIONS = [
    ('تلقائي حسب سوق كل سهم (Auto)', 'AUTO'),
    ('🇺🇸 Nasdaq 100', '^NDX'), ('🇺🇸 S&P 500', '^GSPC'), ('🇺🇸 Dow Jones', '^DJI'), ('🇺🇸 Nasdaq Composite', '^IXIC'),
    ('🇪🇬 EGX 30', '^CASE30'), ('🇪🇬 EGX 70', '^EGX70EWI.CA'), ('🇪🇬 EGX 100', '^EGX100EWI.CA'), ('🇪🇬 EGX Shariah', '^EGXSHARIAH.CA'),
    ('🇸🇦 TASI', '^TASI.SR'),
    ('🪙 Bitcoin', 'BTC-USD'), ('🥇 Gold', 'GC=F'), ('💵 DXY', 'DX-Y.NYB'),
]
# إغلاق الجلسة بتوقيت UTC لاكتشاف "الشمعة المؤكدة بعد الإغلاق" — 🆕 v6: US/FX تتغير مع التوقيت الصيفي
SESSION_CLOSE_UTC = {'US': (21, 0), 'EGX': (12, 30), 'TASI': (12, 10), 'FX': (21, 0), 'CMDTY': (20, 0)}
# 🆕 v5.2: أيام التداول لكل سوق (weekday: الاثنين=0 … الأحد=6) — مصر والسعودية تتداولان الأحد–الخميس
MARKET_WEEKDAYS = {'US': {0, 1, 2, 3, 4}, 'EGX': {6, 0, 1, 2, 3}, 'TASI': {6, 0, 1, 2, 3},
                   'FX': {0, 1, 2, 3, 4}, 'CMDTY': {0, 1, 2, 3, 4}, 'CRYPTO': None}   # None = 24/7

def _us_dst(now):
    """🆕 v6 (إصلاح 11): التوقيت الصيفي الأمريكي — من ثاني أحد في مارس إلى أول أحد في نوفمبر."""
    y = now.year
    # ثاني أحد في مارس
    d = dt.datetime(y, 3, 1)
    start = d + dt.timedelta(days=(6 - d.weekday()) % 7 + 7)
    # أول أحد في نوفمبر
    d = dt.datetime(y, 11, 1)
    end = d + dt.timedelta(days=(6 - d.weekday()) % 7)
    return start <= now < end

def session_closed(sym, last_date):
    """True إذا كانت شمعة آخر يوم قد اكتملت (بحسب أيام وساعات تداول سوق هذا الرمز)."""
    now = dt.datetime.utcnow()
    d = pd.Timestamp(last_date).date()
    if market_of(sym) == 'EGX':          # 🆕 v6.2: جلسة مصر 10:00–14:30 بتوقيت القاهرة (يشمل التوقيت الصيفي المصري)
        cn = _cairo_now()
        if d < cn.date() or cn.weekday() not in MARKET_WEEKDAYS['EGX']:
            return True
        return (cn.hour, cn.minute) >= (14, 30)
    if d < now.date():
        return True
    if asset_class(sym) == 'crypto':   # سوق يعمل 24/7: الشمعة الحية دائماً
        return False
    mk = market_of(sym)
    wd = MARKET_WEEKDAYS.get(mk, {0, 1, 2, 3, 4})
    if wd is not None and now.weekday() not in wd:
        return True
    h, m = SESSION_CLOSE_UTC.get(mk, (21, 0))
    if mk in ('US', 'FX') and _us_dst(now):   # 🆕 v6: 20:00 UTC صيفاً بدل 21:00
        h, m = 20, 0
    return (now.hour, now.minute) >= (h, m)

def week_closed(sym, last_date):
    """🆕 v6.6: اكتمال شمعة W-FRI الحالية (يطابق time_close للإطار الأسبوعي W في Pine)."""
    d = pd.Timestamp(last_date).normalize()
    wk_end = d + pd.Timedelta(days=(4 - d.weekday()) % 7)        # جمعة أسبوع الشمعة
    now_d = pd.Timestamp(dt.datetime.utcnow().date())
    if now_d > wk_end: return True
    if asset_class(sym) == 'crypto': return False
    last_wd = 3 if market_of(sym) in ('EGX', 'TASI') else 4        # آخر يوم تداول (الخميس / الجمعة)
    return d.weekday() == last_wd and session_closed(sym, last_date)

# -----------------------------------------------------------------------------
# 3) جلب البيانات
# -----------------------------------------------------------------------------
OHLCV = ['Open', 'High', 'Low', 'Close', 'Volume']
def _extract(df, t):
    if df is None or len(df) == 0:
        return None
    try:
        if isinstance(df.columns, pd.MultiIndex):
            l0 = df.columns.get_level_values(0); l1 = df.columns.get_level_values(1)
            if t in set(l0): sub = df[t]
            elif t in set(l1): sub = df.xs(t, axis=1, level=1)
            else: return None
        else:
            sub = df
        sub = sub[[c for c in OHLCV if c in sub.columns]].copy()
        if 'Close' not in sub.columns: return None
        sub = sub.dropna(subset=['Close'])
        for c in ('Open', 'High', 'Low'):
            if c not in sub: sub[c] = sub['Close']
            sub[c] = sub[c].fillna(sub['Close'])
        if 'Volume' not in sub: sub['Volume'] = 0.0
        sub['Volume'] = sub['Volume'].fillna(0.0)
        if getattr(sub.index, 'tz', None) is not None:
            sub.index = sub.index.tz_localize(None)
        sub = sub[~sub.index.duplicated(keep='last')].sort_index()
        return sub if len(sub) else None
    except Exception:
        return None

def fetch_prices(tickers, period='2y', interval='1d', chunk=20, progress=None):
    """تحميل دفعي (سريع) + محاولة فردية للفاشل."""
    out = {}
    if yf is None:
        return out
    tickers = list(dict.fromkeys(tickers))
    for k in range(0, len(tickers), chunk):
        part = tickers[k:k + chunk]
        try:
            raw = yf.download(part, period=period, interval=interval, group_by='ticker',
                              auto_adjust=True, progress=False, threads=True)
        except Exception:
            raw = None
        for t in part:
            d = _extract(raw, t)
            if d is not None and len(d) > 0:
                out[t] = d
        if progress: progress(min(k + chunk, len(tickers)), len(tickers), 'تحميل الأسعار')
    for t in [t for t in tickers if t not in out]:
        try:
            raw = yf.download(t, period=period, interval=interval, auto_adjust=True, progress=False)
            d = _extract(raw, t)
            if d is not None: out[t] = d
        except Exception:
            pass
    return out

def fetch_prices_with_fallback(tickers, market='AUTO', progress=None):
    """للرموز بدون لاحقة: إن فشلت نجرّب .CA ثم .SR"""
    data = fetch_prices(tickers, progress=progress)
    alias = {}
    miss = [t for t in tickers if t not in data and market_of(t) == 'US' and '.' not in t and not t.startswith('^')]
    if miss:
        for suf in ('.CA', '.SR'):
            if not miss: break
            cand = {t: t + suf for t in miss}
            got = fetch_prices(list(cand.values()))
            for t, c in cand.items():
                if c in got:
                    data[c] = got[c]; alias[t] = c
            miss = [t for t in miss if t not in alias]
    return data, alias

# -----------------------------------------------------------------------------
# 3b) 🆕 v6.2: سعر اليوم / السعر اللحظي للبورصة المصرية (حل تأخر ياهو 3 أيام) — يشمل كل أسهم EGX
# -----------------------------------------------------------------------------
import urllib.request, urllib.error
_TV_SCAN = 'https://scanner.tradingview.com/{market}/scan'
_TV_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
               'Origin': 'https://www.tradingview.com', 'Referer': 'https://www.tradingview.com/'}
_TV_COLS_FULL = ['name', 'close', 'open', 'high', 'low', 'volume', 'change', 'change_abs', 'type', 'update_mode']
_TV_COLS_MIN = ['name', 'close', 'open', 'high', 'low', 'volume', 'change']      # يُستخدم إن رفض TradingView عموداً (400)
# 🆕 v6.5: الأسواق التي يتأخر ياهو في سعر يومها — scan: اسم السوق في الماسح · exch: بورصة TradingView · suf: لاحقة ياهو · tz/utc_off: توقيت السوق
LIVE_MKT = {
    'EGX':  dict(scan='egypt', exch='EGX', suf='.CA', tz='Africa/Cairo', utc_off=2, open=(10, 0), ar='البورصة المصرية'),
    'TASI': dict(scan='ksa', exch='TADAWUL', suf='.SR', tz='Asia/Riyadh', utc_off=3, open=(10, 0), ar='السوق السعودي (تداول)'),
}
_EGX_LIVE = {'t': 0.0, 'rows': {}}
_TASI_LIVE = {'t': 0.0, 'rows': {}}
_LIVE_CACHE = {'EGX': _EGX_LIVE, 'TASI': _TASI_LIVE}
_SCAN_EXCH = {'egypt': 'EGX', 'ksa': 'TADAWUL'}
EGX_LIVE_MAX_DEV = 0.5       # أقصى انحراف مسموح بين سعر TradingView وآخر إغلاق ياهو (حماية من رمز غير مطابق/تجزئة غير معدّلة)
_MODE_AR = {'streaming': 'لحظي', 'delayed_streaming_900': 'متأخر 15 دقيقة', 'endofday': 'إغلاق نهاية اليوم', 'delayed': 'متأخر'}

def _local_now(mk='EGX'):
    """توقيت السوق الحالي (naive) — يراعي التوقيت الصيفي عند توفر zoneinfo وإلا يستخدم الإزاحة الثابتة."""
    cfg = LIVE_MKT[mk]
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo(cfg['tz'])).replace(tzinfo=None)
    except Exception:
        return dt.datetime.utcnow() + dt.timedelta(hours=cfg['utc_off'])

def _cairo_now():
    return _local_now('EGX')

def _session_date(mk='EGX', now=None):
    """تاريخ آخر جلسة تداول بدأت في السوق (أحد–خميس، الافتتاح 10:00 بتوقيت السوق). قبل الافتتاح أو في الجمعة/السبت = آخر يوم تداول سابق."""
    now = now or (_cairo_now() if mk == 'EGX' else _local_now(mk))
    wd = MARKET_WEEKDAYS[mk]
    oh, om = LIVE_MKT[mk]['open']
    d = now.date()
    if d.weekday() in wd and (now.hour, now.minute) >= (oh, om):
        return d
    d -= dt.timedelta(days=1)
    while d.weekday() not in wd:
        d -= dt.timedelta(days=1)
    return d

def _egx_session_date(now=None):
    return _session_date('EGX', now)

def _tv_post(market, body, timeout=15):
    req = urllib.request.Request(_TV_SCAN.format(market=market), data=json.dumps(body).encode('utf-8'), headers=_TV_HEADERS, method='POST')
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))

def _fnum(x):
    try:
        v = float(x)
        return v if v == v and not math.isinf(v) else NaN
    except Exception:
        return NaN

def _tv_rows(js, cols, exch='EGX'):
    """يحوّل رد TradingView إلى {TICKER: {close, open, high, low, volume, prev, chg, mode, type}} لرموز البورصة exch فقط."""
    out = {}
    for it in ((js or {}).get('data') or []):
        s_ = str(it.get('s', ''))
        if not s_.startswith(exch + ':'):
            continue
        rec = dict(zip(cols, it.get('d') or []))
        c = _fnum(rec.get('close'))
        if not nn(c) or c <= 0:
            continue
        ca, cp = _fnum(rec.get('change_abs')), _fnum(rec.get('change'))
        prev = c - ca if nn(ca) else (c / (1 + cp / 100.0) if nn(cp) and cp > -100 else NaN)
        o, h, l = _fnum(rec.get('open')), _fnum(rec.get('high')), _fnum(rec.get('low'))
        o = o if nn(o) and o > 0 else c
        h = max([x for x in (h, o, c) if nn(x)]); l = min([x for x in (l, o, c) if nn(x) and x > 0] or [c])
        v = _fnum(rec.get('volume'))
        out[s_.split(':', 1)[1].upper()] = dict(close=c, open=o, high=h, low=l, volume=v if nn(v) else 0.0,
                                                prev=prev if nn(prev) and prev > 0 else NaN,
                                                chg=((c - prev) / prev * 100.0) if nn(prev) and prev > 0 else (cp if nn(cp) else NaN),
                                                mode=str(rec.get('update_mode') or ''), type=str(rec.get('type') or ''))
    return out

def _tv_scan(tickers=None, market='egypt', tries=2, exch=None):
    """tickers=None → كل السوق دفعة واحدة. وإلا قائمة مثل ['EGX:COMI']. يعيد {} عند الفشل (بلا استثناءات)."""
    exch = exch or _SCAN_EXCH.get(market, 'EGX')
    for cols in (_TV_COLS_FULL, _TV_COLS_MIN):
        if tickers:
            body = {'symbols': {'tickers': list(tickers), 'query': {'types': []}}, 'columns': cols}
        else:
            body = {'filter': [], 'options': {'lang': 'en'}, 'markets': [market], 'symbols': {'query': {'types': []}, 'tickers': []},
                    'columns': cols, 'sort': {'sortBy': 'name', 'sortOrder': 'asc'}, 'range': [0, 1500]}
        for attempt in range(tries):
            try:
                return _tv_rows(_tv_post(market, body), cols, exch)
            except urllib.error.HTTPError as e:
                if e.code == 400:      # عمود غير مدعوم → جرّب الأعمدة الأدنى
                    break
                time.sleep(0.7 * (attempt + 1))
            except Exception:
                if attempt == tries - 1:
                    return {}          # مشكلة شبكة — لا فائدة من إعادة المحاولة بأعمدة أخرى
                time.sleep(0.7 * (attempt + 1))
    return {}

def live_snapshot(mk='EGX', force=False, ttl=45):
    """لقطة أسعار كل سوق (EGX/TASI) الآن (كاش 45 ثانية). عند فشل الاتصال تُستخدم لقطة عمرها <10 دقائق إن وُجدت."""
    cache, cfg = _LIVE_CACHE[mk], LIVE_MKT[mk]
    age = time.time() - cache['t']
    if not force and cache['rows'] and age < ttl:
        return cache['rows']
    rows = _tv_scan(None, cfg['scan'], exch=cfg['exch'])
    if rows:
        cache.update(t=time.time(), rows=rows)
        return rows
    return cache['rows'] if (cache['rows'] and age < 600) else {}

def egx_live_snapshot(force=False, ttl=45):
    return live_snapshot('EGX', force, ttl)

def egx_universe(stocks_only=True):
    """كل رموز البورصة المصرية الحالية من TradingView (للاستخدام البرمجي): egx_universe() → ['ABUK', 'COMI', …]
    ثم scan(','.join('EGX:' + t for t in egx_universe()[:100]))."""
    snap = egx_live_snapshot()
    has_type = any(q.get('type') for q in snap.values())
    return sorted(t for t, q in snap.items() if not (stocks_only and has_type and q.get('type') not in ('stock', 'dr')))

def _merge_live_bar(df, q, sd):
    """يدمج شمعة سعر اليوم q في df: إضافة (جلسة أحدث)، استبدال (نفس اليوم)، أو تجاهل. يعيد (df, الحالة)."""
    cols = list(df.columns)
    last_d = pd.Timestamp(df.index[-1]).normalize()
    last_c = float(df['Close'].iloc[-1])
    if last_c > 0 and abs(q['close'] / last_c - 1) > EGX_LIVE_MAX_DEV:
        return df, 'rejected'
    vals = dict(Open=q['open'], High=q['high'], Low=q['low'], Close=q['close'], Volume=q['volume'])
    if sd > last_d:
        lr = df.iloc[-1]
        if all(abs(float(lr[k]) - vals[k]) < 1e-9 for k in cols if k in vals):
            return df, 'same'              # شمعة مطابقة تماماً (عطلة رسمية في يوم عمل) — لا نكرّرها
        new = pd.DataFrame([[vals[k] for k in cols]], columns=cols, index=pd.DatetimeIndex([sd]))
        return pd.concat([df, new]), 'appended'
    if sd == last_d:
        df = df.copy()
        for k in cols:
            if k in vals: df.iloc[-1, df.columns.get_loc(k)] = vals[k]
        return df, 'replaced'
    return df, 'ahead'                     # ياهو أحدث من ساعة الجلسة المحسوبة — لا تعديل

def apply_live(prices, mk='EGX', log=None):
    """🆕 v6.5 (تعميم v6.2): يحدّث أسهم السوق mk (EGX=.CA · TASI=.SR) في قاموس prices بسعر اليوم/آخر جلسة من TradingView.
    تعديل في المكان. يعيد ملخصاً dict(n, ok, appended, replaced, same, missing, rejected, failed, session, mode)."""
    cfg = LIVE_MKT[mk]; suf = cfg['suf']; nm = cfg['ar']
    info = dict(n=0, ok=0, appended=0, replaced=0, same=0, missing=[], rejected=[], failed=False, session=None, mode='')
    syms_ = [t for t, d in prices.items() if t.endswith(suf) and asset_class(t) == 'stock' and d is not None and len(d)]
    info['n'] = len(syms_)
    if not syms_:
        return info
    L = log if log is not None else []
    key = lambda t: t[:-len(suf)].upper()
    snap = live_snapshot(mk)
    if not snap:
        info['failed'] = True; info['missing'] = list(syms_)
        L.append(f'⚠️ {nm}: تعذّر جلب السعر اللحظي من TradingView (تحقق من الإنترنت) — الأسعار من ياهو وقد تتأخر عن سعر اليوم: ' + ', '.join(syms_))
        return info
    miss = [t for t in syms_ if key(t) not in snap]
    if miss:                                # أسهم غابت عن المسح العام → طلب مباشر بالرموز
        snap = {**snap, **_tv_scan([cfg['exch'] + ':' + key(t) for t in miss], cfg['scan'], exch=cfg['exch'])}
    sd = pd.Timestamp(_session_date(mk))
    info['session'] = str(sd.date())
    modes = {}
    for t in syms_:
        q = snap.get(key(t))
        if q is None:
            info['missing'].append(t); continue
        try:
            prices[t], st = _merge_live_bar(prices[t], q, sd)
        except Exception:
            info['missing'].append(t); continue
        if st == 'rejected': info['rejected'].append(t)
        elif st in ('appended', 'replaced', 'same', 'ahead'):
            info['ok'] += 1
            if st in ('appended', 'replaced', 'same'): info[st] += 1
            if q.get('mode'): modes[q['mode']] = modes.get(q['mode'], 0) + 1
    if modes:
        info['mode'] = max(modes, key=modes.get)
    md = info['mode']; md_txt = _MODE_AR.get(md, md) if md else ''
    L.append(f"✅ {nm}: سعر جلسة {info['session']} من TradingView لـ{info['ok']} من {info['n']} سهم "
             f"(شموع مضافة {info['appended']} · مستبدلة {info['replaced']} · مطابقة لياهو {info['same']})" + (f' — نوع البيانات: {md_txt}' if md_txt else ''))
    if info['missing']:
        L.append('⚠️ لا يوجد سعر لحظي على TradingView لـ: ' + ', '.join(info['missing']) + ' — بقي سعر ياهو (قد يكون متأخراً).')
    if info['rejected']:
        L.append('⚠️ رُفض سعر TradingView (انحراف >50% عن آخر إغلاق ياهو — رمز غير مطابق أو تجزئة غير معدّلة) لـ: ' + ', '.join(info['rejected']))
    return info

def apply_egx_live(prices, log=None):
    return apply_live(prices, 'EGX', log)

# مؤشر ياهو → (سوق، رمز المؤشر على TradingView) لتحديث شمعة اليوم
_LIVE_INDEX = {'^CASE30': ('EGX', 'EGX30'), '^TASI.SR': ('TASI', 'TASI')}

def apply_index_live(bench_data, log=None):
    """🆕 v6.5: يحدّث مؤشر EGX30/تاسي المرجعي بشمعة اليوم إن توفر في TradingView (يُتجاهل بصمت إن لم يتوفر)."""
    for sym, (mk, nm) in _LIVE_INDEX.items():
        try:
            df = bench_data.get(sym)
            if df is None or len(df) < 25:
                continue
            cfg = LIVE_MKT[mk]; q = None
            for scan in dict.fromkeys([cfg['scan'], 'global']):
                q = _tv_scan([cfg['exch'] + ':' + nm], market=scan, exch=cfg['exch']).get(nm)
                if q: break
            if not q: continue
            sd = pd.Timestamp(_session_date(mk))
            bench_data[sym], st = _merge_live_bar(df, q, sd)
            if log is not None and st in ('appended', 'replaced'):
                log.append(f'✅ مؤشر {nm} المرجعي: حُدّث بسعر جلسة {sd.date()} من TradingView.')
        except Exception:
            pass

def apply_egx_index_live(bench_data, log=None):
    apply_index_live(bench_data, log)

# -----------------------------------------------------------------------------
# 3c) 🆕 v6.4/6.5: بديل تاريخ مصر والسعودية من TradingView عبر tvDatafeed (اختياري) — للأسهم/المؤشرات التي لا يوفرها ياهو
# -----------------------------------------------------------------------------
logging.getLogger('tvDatafeed').setLevel(logging.CRITICAL)
_TVD = {'obj': None, 'failed': False}
# مؤشر ياهو → (بورصة TradingView، رموز مرشحة تُجرَّب بالترتيب) — ما لا يوجد منها يُتجاهل بصمت ويعمل البديل القديم (مؤشر تركيبي/ETF)
_TV_INDEX = {'^CASE30': ('EGX', ['EGX30']), '^EGX70EWI.CA': ('EGX', ['EGX70EWI', 'EGX70']), '^CCSI': ('EGX', ['EGX70EWI', 'EGX70']),
             '^EGX100EWI.CA': ('EGX', ['EGX100EWI', 'EGX100']), '^EGXSHARIAH.CA': ('EGX', ['EGX33', 'EGX33SHARIAH']),
             '^TASI.SR': ('TADAWUL', ['TASI'])}
_TV_INSTALL_HINT = 'pip install git+https://github.com/rongardF/tvdatafeed.git'

def _tvd_client():
    if _TVD['obj'] is None and not _TVD['failed']:
        try:
            from tvDatafeed import TvDatafeed
            _TVD['obj'] = TvDatafeed()          # بلا تسجيل دخول (بيانات يومية تكفي)
        except Exception:
            _TVD['failed'] = True
    return _TVD['obj']

def _tv_fix_index(idx):
    """شموع TradingView اليومية قد تأتي بتوقيت UTC/الجلسة (مثلاً 22:00 من اليوم السابق) — نختار الإزاحة التي تضع أغلب الشموع في أيام التداول (أحد–خميس)."""
    idx = pd.DatetimeIndex(idx)
    if idx.tz is not None: idx = idx.tz_localize(None)
    best, bs = None, -1.0
    for h in (12, 0, 6, 18):
        cand = (idx + pd.Timedelta(hours=h)).normalize()
        sc = float(np.mean([d.weekday() in MARKET_WEEKDAYS['EGX'] for d in cand]))
        if sc > bs + 1e-9: best, bs = cand, sc
    return best

def fetch_tv_history(tv_symbol, exchange='EGX', n_bars=520, tries=2):
    """تاريخ يومي OHLCV من TradingView عبر tvDatafeed → DataFrame بنفس أعمدة ياهو، أو None عند أي فشل (بلا استثناءات)."""
    tv = _tvd_client()
    if tv is None: return None
    try:
        from tvDatafeed import Interval
        iv = Interval.in_daily
    except Exception:
        return None
    d = None
    for a in range(tries):
        try:
            d = tv.get_hist(symbol=tv_symbol, exchange=exchange, interval=iv, n_bars=n_bars)
        except Exception:
            d = None
        if d is not None and len(d) >= 2: break
        d = None
        time.sleep(0.8 * (a + 1))
    if d is None: return None
    try:
        d = d.rename(columns={c: str(c).title() for c in d.columns})
        d = d[[c for c in OHLCV if c in d.columns]].astype(float)
        d.index = _tv_fix_index(d.index)
        d = d[~d.index.duplicated(keep='last')].sort_index()
        d = d.dropna(subset=['Close']); d = d[d['Close'] > 0]
        for c in ('Open', 'High', 'Low'):
            if c not in d: d[c] = d['Close']
        if 'Volume' not in d: d['Volume'] = 0.0
        d['Volume'] = d['Volume'].fillna(0.0)
        return d[OHLCV] if len(d) else None
    except Exception:
        return None

def fill_tv_history(prices, syms_actual, log, p):
    """أسهم .CA/.SR بلا تاريخ على ياهو (أو <60 شمعة) → تاريخها من TradingView. تعديل في المكان؛ يعيد قائمة المُكمَّل."""
    if not p.get('tvHistoryFallback', True): return []
    done, need_all = [], []
    for suf, exch in (('.CA', 'EGX'), ('.SR', 'TADAWUL')):
        need = [t for t in dict.fromkeys(syms_actual) if t.endswith(suf) and asset_class(t) == 'stock' and (t not in prices or len(prices[t]) < 60)]
        need_all += need
        for t in need:
            d = fetch_tv_history(t[:-len(suf)].upper(), exch)
            if d is not None and len(d) >= 60 and (t not in prices or len(d) > len(prices[t])):
                prices[t] = d; done.append(t)
    if need_all and not done and _TVD['failed']:
        log.append(f'ℹ️ مكتبة tvDatafeed غير مثبتة — لا يمكن جلب تاريخ {", ".join(need_all)} من TradingView. للتفعيل: {_TV_INSTALL_HINT}')
    if done:
        log.append('✅ تاريخ الأسعار من TradingView (tvDatafeed) لأن ياهو لا يوفره كاملاً لـ: ' + ', '.join(done) +
                   ' — البيانات المالية/القيمة العادلة تبقى من ياهو وقد لا تتوفر لها.')
    return done

def fill_egx_history_tv(prices, syms_actual, log, p):
    return fill_tv_history(prices, syms_actual, log, p)

def fill_tv_index(bench_data, bench_syms, log, p):
    """مؤشرات مصر/السعودية التي يعيد لها ياهو أقل من 25 شمعة → التاريخ من TradingView إن توفرت المكتبة."""
    if not p.get('tvHistoryFallback', True): return
    for bs in dict.fromkeys(bench_syms):
        if bs not in _TV_INDEX: continue
        b0 = bench_data.get(bs)
        if b0 is not None and len(b0) >= 25: continue
        exch, cands = _TV_INDEX[bs]
        got = False
        for cand in cands:
            d = fetch_tv_history(cand, exch)
            if d is not None and len(d) >= 25:
                bench_data[bs] = d; got = True
                log.append(f'✅ مؤشر {bs}: التاريخ من TradingView ({exch}:{cand}، {len(d)} شمعة) لأن ياهو لا يوفره — حالة السوق العام الآن من المؤشر الحقيقي.')
                break
        if not got and _TVD['failed']:
            log.append(f'ℹ️ مؤشر {bs}: مكتبة tvDatafeed غير مثبتة فاستُخدم البديل القديم. للتفعيل: {_TV_INSTALL_HINT}')

def fill_egx_index_tv(bench_data, bench_syms, log, p):
    fill_tv_index(bench_data, bench_syms, log, p)

# -----------------------------------------------------------------------------
# 🆕 v7.0: بيانات TradingView الأساسية — EPS TTM + القيمة السوقية الحية + مضاعفات القطاع/السوق (للمضاعف النسبي)
#   عمود غير مدعوم → يُحذف تلقائياً (فحص كل عمود على حدة) · أي فشل → {} بلا استثناءات والتحليل يكمل بياهو.
# -----------------------------------------------------------------------------
TV_FUND_MKT = {'EGX': dict(scan='egypt', exch='EGX', suf='.CA'), 'TASI': dict(scan='ksa', exch='TADAWUL', suf='.SR'), 'US': dict(scan='america', exch=None, suf='')}
_TV_FUND_COLS = ['name', 'sector', 'market_cap_basic', 'earnings_per_share_diluted_ttm', 'earnings_per_share_basic_ttm', 'price_earnings_ttm',
                 'price_book_fq', 'return_on_equity', 'price_target_average', 'price_target_high', 'price_target_low', 'type']
_TV_FUND_OK = {}
_TV_FUND_CACHE = {}

def tv_key(sym, mk):
    """رمز ياهو → رمز TradingView المجرد (COMI.CA → COMI · 2222.SR → 2222 · BRK-B → BRK.B)."""
    s = str(sym).upper()
    if mk in ('EGX', 'TASI') and '.' in s: return s.rsplit('.', 1)[0]
    return s.replace('-', '.')

def _tv_probe_cols(market, cols):
    ok = ['name']
    for c in cols:
        if c == 'name': continue
        try:
            _tv_post(market, {'filter': [], 'options': {'lang': 'en'}, 'markets': [market], 'symbols': {'query': {'types': []}, 'tickers': []}, 'columns': ['name', c], 'range': [0, 1]}, timeout=10)
            ok.append(c)
        except Exception:
            pass
    return ok

def _tv_fund_rows(js, cols, cfg):
    out = {}
    for it in ((js or {}).get('data') or []):
        s_ = str(it.get('s', ''))
        if ':' not in s_: continue
        ex_, tk_ = s_.split(':', 1)
        if cfg['exch'] and ex_ != cfg['exch']: continue
        if not cfg['exch'] and ex_ in ('OTC', 'PINK'): continue
        rec = dict(zip(cols, it.get('d') or []))
        eps = _fnum(rec.get('earnings_per_share_diluted_ttm'))
        if not nn(eps): eps = _fnum(rec.get('earnings_per_share_basic_ttm'))
        mc = _fnum(rec.get('market_cap_basic'))
        out[tk_.upper()] = dict(eps_ttm=eps, mcap=mc if nn(mc) and mc > 0 else NaN, pe=_fnum(rec.get('price_earnings_ttm')), pb=_fnum(rec.get('price_book_fq')),
                                roe=_fnum(rec.get('return_on_equity')), tgt=_fnum(rec.get('price_target_average')), tgt_hi=_fnum(rec.get('price_target_high')),
                                tgt_lo=_fnum(rec.get('price_target_low')), sector=str(rec.get('sector') or ''), type=str(rec.get('type') or ''))
    return out

def _tv_fund_stats(rows):
    """وسيط P/E للسوق وللقطاعات (أسهم عادية بربح موجب فقط) — وسيط لا متوسط لمقاومة القيم الشاذة."""
    pes, sec = [], {}
    for r in rows.values():
        if r['type'] and r['type'] not in ('stock', 'dr'): continue
        pe = r['pe']
        if nn(pe) and 0 < pe <= 100 and nn(r['mcap']):
            pes.append(pe)
            if r['sector']: sec.setdefault(r['sector'], []).append(pe)
    return dict(market_pe=float(np.median(pes)) if len(pes) >= 8 else NaN, n_market=len(pes),
                sector={k: (float(np.median(v)), len(v)) for k, v in sec.items()})

def tv_fund_universe(mk, force=False, ttl=6 * 3600):
    """يعيد dict(rows={TICKER: {...}}, stats={...}) للسوق mk (EGX/TASI/US) أو {} عند الفشل. كاش 6 ساعات."""
    cfg = TV_FUND_MKT.get(mk)
    if not cfg: return {}
    c = _TV_FUND_CACHE.get(mk)
    if c and not force and time.time() - c['t'] < ttl: return c['data']
    cols = _TV_FUND_OK.get(mk) or list(_TV_FUND_COLS)
    def body(cs):
        return {'filter': [], 'options': {'lang': 'en'}, 'markets': [cfg['scan']], 'symbols': {'query': {'types': []}, 'tickers': []}, 'columns': cs,
                'sort': {'sortBy': 'market_cap_basic' if 'market_cap_basic' in cs else 'name', 'sortOrder': 'desc' if 'market_cap_basic' in cs else 'asc'},
                'range': [0, 1200 if mk == 'US' else 1500]}
    js = None
    for attempt in range(2):
        try:
            js = _tv_post(cfg['scan'], body(cols), timeout=25); break
        except urllib.error.HTTPError as e:
            if e.code == 400 and mk not in _TV_FUND_OK:
                cols = _tv_probe_cols(cfg['scan'], cols); _TV_FUND_OK[mk] = cols
                if len(cols) <= 1: return {}
                continue
            time.sleep(0.8)
        except Exception:
            return (c or {}).get('data', {})
    rows = _tv_fund_rows(js, cols, cfg) if js else {}
    if not rows: return (c or {}).get('data', {})
    data = dict(rows=rows, stats=_tv_fund_stats(rows))
    _TV_FUND_CACHE[mk] = dict(t=time.time(), data=data)
    return data

_INFO_CACHE = {}
def fetch_fundamentals_one(t, deep=True):
    """info دائمًا (لازم للقيمة العادلة) + القوائم المالية عند deep.
    🆕 v6 (إصلاح 4): الكاش يُخزَّن عند النجاح فقط (فشل 429 لا يُخزَّن فيبقى السهم بلا بيانات)،
    ومفتاح الكاش يتضمن قيمة deep (فلا يفقد السهم القوائم المالية إذا بدأ بـdeep=False)،
    مع إعادة محاولة عند تقييد الطلبات."""
    key = (t, bool(deep))                       # 🆕 v6: قيمة deep جزء من مفتاح التخزين المؤقت
    if key in _INFO_CACHE:
        return _INFO_CACHE[key]
    res = dict(info={}, fin=None, bs=None, cf=None, qfin=None)
    if yf is None:
        return res
    try:
        tk = yf.Ticker(t)
        for attempt in range(3):                # 🆕 v6: إعادة المحاولة عند 429/تقييد — والفشل لا يُخزَّن
            try:
                info_ = tk.info or {}
                if info_:
                    res['info'] = info_
                    break
                res['info'] = {}
            except Exception:
                res['info'] = {}
            time.sleep(0.6 * (attempt + 1))
        if deep:
            for key2, attr in (('fin', 'financials'), ('bs', 'balance_sheet'), ('cf', 'cashflow'), ('qfin', 'quarterly_financials')):   # 🆕 v7.0: القوائم الربعية لحساب EPS TTM
                try: res[key2] = getattr(tk, attr)
                except Exception: res[key2] = None
    except Exception:
        pass
    if res['info']:                             # 🆕 v6: تخزين النجاح فقط — الفشل يُترك للمحاولة التالية
        if len(_INFO_CACHE) > 4000: _INFO_CACHE.clear()
        _INFO_CACHE[key] = res
    return res

def _clean_name(sym, info):
    """🆕 v5.1: تنظيف الأسماء المشوهة من ياهو لبعض الأسواق (مثال مصر: "AMOC.CA,0P0000BRQQ,1787402").
    النمط المرفوض: الرمز نفسه + فاصلة + معرفات داخلية (0P… أو أرقام). في هذه الحالة نُفرغ الاسم ليُعرض الرمز فقط."""
    nm = str(info.get('shortName') or info.get('longName') or '').strip()
    if not nm or ',' not in nm:
        return nm
    base = re.split(r'[.\-\^]', sym)[0].upper()
    segs = [x.strip() for x in nm.split(',')]
    if len(segs) > 1 and base and segs[0].upper().startswith(base) and any(s.isdigit() or s.upper().startswith('0P') for s in segs[1:]):
        return ''
    return nm

def fetch_fundamentals(tickers, deep=True, workers=8, progress=None):
    out = {}
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fetch_fundamentals_one, t, deep): t for t in tickers}
        for f in as_completed(futs):
            t = futs[f]
            try: out[t] = f.result()
            except Exception: out[t] = dict(info={}, fin=None, bs=None, cf=None, qfin=None)
            done += 1
            if progress: progress(done, len(tickers), 'تحميل البيانات المالية')
    return out

def fetch_intraday_all(tickers, progress=None):
    """15m / 30m / 60m لمصفوفة الأطر (اختياري)."""
    res = {'15m': {}, '30m': {}, '60m': {}}
    if yf is None: return res
    for iv, per in (('15m', '30d'), ('30m', '60d'), ('60m', '120d')):
        res[iv] = fetch_prices(tickers, period=per, interval=iv, chunk=20)
        if progress: progress(0, 1, f'أطر {iv}')
    return res

# -----------------------------------------------------------------------------
# 4) المؤشرات الفنية (مطابقة لمنطق Pine قدر الإمكان)
# -----------------------------------------------------------------------------
def _pine_ma(s, n, alpha):
    """🆕 v6.6: متوسط متحرك أسّي ببذر Pine: أول قيمة = SMA لأول n قيمة صالحة، ثم alpha*x + (1-alpha)*prev."""
    s = pd.Series(s)
    v = s.to_numpy(dtype=float)
    sma = pd.Series(v).rolling(n, min_periods=n).mean().to_numpy()
    out = np.full(len(v), np.nan); prev = np.nan
    for i in range(len(v)):
        cur = sma[i] if prev != prev else alpha * v[i] + (1 - alpha) * prev
        out[i] = cur; prev = cur
    return pd.Series(out, index=s.index)
def s_ema(s, n):
    return _pine_ma(s, n, 2.0 / (n + 1)) if P.get('pineSeed', True) else s.ewm(span=n, adjust=False, min_periods=n).mean()
def s_rma(s, n):
    return _pine_ma(s, n, 1.0 / n) if P.get('pineSeed', True) else s.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
def s_sma(s, n):  return s.rolling(n, min_periods=n).mean()
def s_wma(s, n):
    w = np.arange(1, n + 1, dtype=float)
    return s.rolling(n, min_periods=n).apply(lambda x: np.dot(x, w) / w.sum(), raw=True)
def true_range(df):
    pc = df['Close'].shift(1)
    return pd.concat([df['High'] - df['Low'], (df['High'] - pc).abs(), (df['Low'] - pc).abs()], axis=1).max(axis=1)
def s_atr(df, n=14):  return s_rma(true_range(df), n)
def s_rsi(s, n):
    d = s.diff()
    up = s_rma(d.clip(lower=0), n); dn = s_rma((-d).clip(lower=0), n)
    rs = up / dn.replace(0, np.nan)
    r = 100 - 100 / (1 + rs)
    r[(dn == 0) & up.notna()] = 100.0
    return r
def s_stoch(df, n):
    ll = df['Low'].rolling(n, min_periods=n).min(); hh = df['High'].rolling(n, min_periods=n).max()
    return 100 * (df['Close'] - ll) / (hh - ll).replace(0, np.nan)
def s_macd(s, f, sl, sg):
    m = s_ema(s, f) - s_ema(s, sl); sig = s_ema(m, sg)
    return m, sig, m - sig
def s_cmf(df, n):
    rng = (df['High'] - df['Low'])
    mfm = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / rng.replace(0, np.nan)
    mfm = mfm.fillna(0.0)
    return (mfm * df['Volume']).rolling(n, min_periods=n).sum() / df['Volume'].rolling(n, min_periods=n).sum().replace(0, np.nan)
def s_chop(df, n):
    tr = true_range(df)
    rng = df['High'].rolling(n, min_periods=n).max() - df['Low'].rolling(n, min_periods=n).min()
    v = 100 * np.log10(tr.rolling(n, min_periods=n).sum() / rng.replace(0, np.nan)) / math.log10(n)
    return v.replace([np.inf, -np.inf], np.nan)
def s_supertrend(df, period, mult):
    """يعيد (قيمة الخط, الاتجاه) — الاتجاه -1 = صاعد، +1 = هابط (كما في Pine)."""
    atr = s_rma(true_range(df), period).values
    h, l, c = df['High'].values, df['Low'].values, df['Close'].values
    n = len(c); hl2 = (h + l) / 2
    st = np.full(n, np.nan); d = np.ones(n)
    up = np.full(n, np.nan); lo = np.full(n, np.nan)
    for i in range(n):
        if math.isnan(atr[i]):
            continue
        u = hl2[i] + mult * atr[i]; lw = hl2[i] - mult * atr[i]
        if i > 0 and not math.isnan(up[i - 1]):
            lw = lw if (lw > lo[i - 1] or c[i - 1] < lo[i - 1]) else lo[i - 1]
            u = u if (u < up[i - 1] or c[i - 1] > up[i - 1]) else up[i - 1]
            if st[i - 1] == up[i - 1]:
                d[i] = -1 if c[i] > u else 1
            else:
                d[i] = 1 if c[i] < lw else -1
        else:
            d[i] = 1
        up[i], lo[i] = u, lw
        st[i] = lw if d[i] == -1 else u
    return pd.Series(st, index=df.index), pd.Series(d, index=df.index)
def s_dmi(df, n=14):
    """🆕 v6.6: ADX/DMI ببذر Wilder مطابق لـPine (بلا ملء NaN الأولية بصفر داخل RMA)."""
    h, l = df['High'], df['Low']
    up = h.diff(); dn = -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=df.index).where(up.notna())
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=df.index).where(dn.notna())
    atr = s_rma(true_range(df), n)
    pdi = 100 * s_rma(pdm, n) / atr
    mdi = 100 * s_rma(mdm, n) / atr
    ssum = pdi + mdi
    adx = 100 * s_rma((pdi - mdi).abs() / ssum.where(ssum != 0, 1.0), n)
    return pdi, mdi, adx
def calc_vpoc(df, bars=100, bins=24):
    d = df.tail(bars)
    if len(d) < 5: return NaN
    hi, lo = d['High'].max(), d['Low'].min()
    if hi <= lo: return float(hi)
    edges = np.linspace(hi, lo, bins + 1)       # من الأعلى للأسفل
    H, L, C, V = d['High'].values, d['Low'].values, d['Close'].values, d['Volume'].values
    best, poc = 0.0, NaN      # 🆕 v6.6: بلا حجم يبقى POC فارغاً (NaN) كما في Pine (max_vol يبدأ 0.0)
    for i in range(bins):
        top, bot = edges[i], edges[i + 1]
        ov = np.maximum(0.0, np.minimum(H, top) - np.maximum(L, bot))
        rg = H - L
        frac = np.where(rg > 0, ov / np.where(rg > 0, rg, 1), ((C >= bot) & (C <= top)).astype(float))
        vol = float((V * frac).sum())
        if vol > best: best, poc = vol, (top + bot) / 2
    return poc
def pivots(h, l, arm):
    n = len(h); ph = np.full(n, np.nan); pl = np.full(n, np.nan)
    for i in range(2 * arm, n):
        c = i - arm
        if h[c] > h[c - arm:c].max() and h[c] >= h[c + 1:i + 1].max(): ph[i] = h[c]
        if l[c] < l[c - arm:c].min() and l[c] <= l[c + 1:i + 1].min(): pl[i] = l[c]
    return ph, pl

def resample_ohlc(df, rule):
    agg = dict(Open='first', High='max', Low='min', Close='last', Volume='sum')
    try:
        return df.resample(rule).agg(agg).dropna(subset=['Close'])
    except Exception:
        return df.resample(rule.upper() if rule.endswith('h') else rule).agg(agg).dropna(subset=['Close'])

def frame_net(df, p):
    """اتجاه إطار واحد: +1 صاعد / -1 هابط / 0 محايد  (EMA>SMA & RSI>50 & MACD>Signal)."""
    if df is None or len(df) < p['smaSlow'] + 5: return None
    c = df['Close']
    e, s_ = s_ema(c, p['emaFast']).iloc[-1], s_sma(c, p['smaSlow']).iloc[-1]
    r = s_rsi(c, p['rsiFast']).iloc[-1]
    m, sg, _ = s_macd(c, p['macdFast'], p['macdSlow'], p['macdSignal'])
    m, sg = m.iloc[-1], sg.iloc[-1]
    if any(math.isnan(x) for x in (e, s_, r, m, sg)): return None
    if e > s_ and r > 50 and m > sg: return 1
    if e < s_ and r < 50 and m < sg: return -1
    return 0

# %% [الخلية 3]
# 5) محرك تحليل الشارت الفني متعدد الفئات (شمعة بشمعة): النقاط + الهيكل + الدايفرجنس + الصفقة الافتراضية
# -----------------------------------------------------------------------------
def get_grade(pct, p=P):
    return 'A+' if pct >= p['pctAplus'] else 'A' if pct >= p['pctA'] else 'B+' if pct >= p['pctBplus'] else 'B' if pct >= p['pctB'] else 'C'

def prime_x_engine(df, p, htf_buy=None, htf_sell=None, last_override=None):
    n = len(df)
    o, h, l, c, v = (df[k].values.astype(float) for k in ('Open', 'High', 'Low', 'Close', 'Volume'))
    cs = df['Close']
    emaF = s_ema(cs, p['emaFast']).values; smaS = s_sma(cs, p['smaSlow']).values; wmaV = s_wma(cs, p['wmaLen']).values
    atr = s_atr(df, p['atrPeriod']).values
    stV, stD = s_supertrend(df, p['stPeriod'], p['stMult']); stV, stD = stV.values, stD.values
    chop = s_chop(df, p['chopLen']).fillna(50).values
    rsiF = s_rsi(cs, p['rsiFast']).values; rsiS = s_rsi(cs, p['rsiSlow']).values
    stK = s_sma(s_stoch(df, p['stochK']), p['stochSmooth']); stDv = s_sma(stK, p['stochD']); stK, stDv = stK.values, stDv.values
    mm, ms_, mh = s_macd(cs, p['macdFast'], p['macdSlow'], p['macdSignal']); mm, ms_, mh = mm.values, ms_.values, mh.values
    hl2 = (df['High'] + df['Low']) / 2
    ao = (s_sma(hl2, 5) - s_sma(hl2, 34)).values
    hlc3 = (df['High'] + df['Low'] + df['Close']) / 3
    vw = ((hlc3 * df['Volume']).rolling(p['vwapLen']).sum() / df['Volume'].rolling(p['vwapLen']).sum().replace(0, np.nan)).values
    cmf = s_cmf(df, p['cmfLen']).values
    volMA = s_sma(df['Volume'], p['volPressLen']).values
    volSt = s_sma(df['Volume'], p['marketStateLen']).values
    bbm = s_sma(cs, p['bbPeriod']); bbs = cs.rolling(p['bbPeriod']).std(ddof=0)
    bbw = ((bbm + 2 * bbs) - (bbm - 2 * bbs)) / bbm
    bbp = bbw.rolling(100, min_periods=100).quantile(0.20)
    sq = (bbw <= bbp).fillna(False).values
    sqRel = np.zeros(n, bool); sqRel[1:] = sq[:-1] & ~sq[1:]
    bbMid = bbm.values
    hh50 = df['High'].rolling(50, min_periods=1).max().values; ll50 = df['Low'].rolling(50, min_periods=1).min().values
    swL = p['sweepLookback']
    llN = df['Low'].rolling(swL).min().shift(1).values; hhN = df['High'].rolling(swL).max().shift(1).values
    PH, PL = pivots(h, l, p['fractalArm'])
    # أنماط الشموع (متجهة)
    sh = lambda a, k: np.concatenate([np.full(k, np.nan), a[:-k]]) if k else a
    o1, c1, o2, c2, h1, l1 = sh(o, 1), sh(c, 1), sh(o, 2), sh(c, 2), sh(h, 1), sh(l, 1)
    body = np.abs(c - o); rng = h - l
    with np.errstate(invalid='ignore'):
        isHammer = (c > o) & ((o - l) > 2 * (c - o)) & ((h - c) < (c - o))
        isInvH = (c > o) & ((h - c) > 2 * (c - o)) & ((o - l) < (c - o))
        isHang = (c < o) & ((c - l) > 2 * (o - c)) & ((h - o) < (o - c))
        isShoot = (c < o) & ((h - o) > 2 * (o - c)) & ((c - l) < (o - c))
        isBullEng = (c1 < o1) & (c > o) & (c > o1) & (o < c1)
        isBearEng = (c1 > o1) & (c < o) & (c < o1) & (o > c1)
        isDoji = body < rng * 0.1
        isMaru = ((h - c) < rng * 0.05) & ((o - l) < rng * 0.05)
        isMorn = (c2 < o2) & (np.abs(c1 - o1) < (h1 - l1) * 0.3) & (c > o) & (c > (o2 + c2) / 2)
        isEven = (c2 > o2) & (np.abs(c1 - o1) < (h1 - l1) * 0.3) & (c < o) & (c < (o2 + c2) / 2)
    barChg = np.concatenate([[np.nan], (c[1:] - c[:-1]) / c[:-1] * 100])
    gapDist = np.concatenate([[np.nan], o[1:] - c[:-1]])

    W = dict(RSI=p['wRSI'], MACD=p['wMACD'], EMA=p['wEMA'], VWAP=p['wVWAP'], CMF=p['wCMF'], VP=p['wVolPress'],
             Div=p['wDiv'], Sweep=p['wSweep'], MS=p['wMS'], Sq=p['wSqueeze'], SMC=p['wSMC'], Pat=p['wPat'])
    has_vol = bool(np.nansum(v) > 0)   # 🆕 v6 (إصلاح 3): فوركس/مؤشرات يعيدها ياهو بحجم 0
    catMax = dict(T=W['EMA'] + 2, M=2 * W['RSI'] + W['MACD'] + 2, V=W['VWAP'] + W['CMF'] + W['VP'], S=W['MS'],
                  L=W['Div'] + W['Sweep'] + 1 + W['Sq'], SMC=W['SMC'] * 4, P=W['Pat'] * 4)
    if not has_vol and not p.get('pineParity', True):
        catMax['V'] = 0   # 🆕 v6: بلا بيانات حجم — فئة السيولة تُستبعد من الحد الأقصى فلا تُخفَّض النِسَب زوراً (🆕 v6.6: مع pineParity تبقى كما في Pine)
    arm = p['fractalArm']
    # ── الحالة ──
    ph_last = ph_prev = rsi_ph = pl_last = pl_prev = rsi_pl = NaN
    ph_idx = pl_idx = -1
    cH = cL = NaN; cHb = cLb = -1; lastType = 0
    msTrend = 0; fLB = fLBr = -1; fPers = 0; fBar = -10**9
    smcBias = 0; smcBiasBar = -10**9; sLB = sLBr = -1
    smcCnt = dict(bb=0, bc=0, sb=0, sc=0); smcLast = ''; smcLastBar = -10**9
    bullOB, bearOB, fvgs = [], [], []
    lastBuy = lastSell = lastSig = None
    divLast = (-10**9, ''); eqLast = (-10**9, '')
    gradesOK = p['pctAplus'] > p['pctA'] > p['pctBplus'] > p['pctB']
    # الصفقة
    st = 'WAITING'; tdir = ''; tE = tSL = tT1 = tT2 = tT3 = NaN; hit1 = hit2 = hit3 = tBE = False
    mfe = mae = 0.0; slDist0 = tp3Dist0 = NaN; outcome = ''; rmult = NaN
    W_ = L_ = BE_ = AMB = 0; sumR = sumWin = sumLoss = 0.0; closedN = 0
    opened = r1 = r2 = r3 = 0
    lastOutcome = ''; lastR = NaN; lastDir = ''; entryBar = -1
    trades = []; signals = []
    last = {}
    start = max(60, p['wmaLen'] + 2)
    for i in range(n):
        # ---- الفراكتل/الدايفرجنس/EQH-EQL ----
        divBull = divBear = False
        trapTol = atr[i] * 0.05 if nn(atr[i]) else NaN
        pH, pL = PH[i], PL[i]
        if nn(pH):
            pidx = i - arm; ra = rsiS[pidx]
            if nn(ph_last):
                divBear = (pH > ph_last) and nn(rsi_ph) and (ra < rsi_ph)
                if nn(trapTol) and abs(pH - ph_last) < trapTol: eqLast = (i, 'EQH')
            ph_prev, ph_last, rsi_ph, ph_idx = ph_last, pH, ra, pidx
            if lastType == 1:
                if not nn(cH) or pH > cH: cH, cHb = pH, pidx
            else:
                cH, cHb, lastType = pH, pidx, 1
        if nn(pL):
            pidx = i - arm; ra = rsiS[pidx]
            if nn(pl_last):
                divBull = (pL < pl_last) and nn(rsi_pl) and (ra > rsi_pl)
                if nn(trapTol) and abs(pL - pl_last) < trapTol: eqLast = (i, 'EQL')
            pl_prev, pl_last, rsi_pl, pl_idx = pl_last, pL, ra, pidx
            if lastType == -1:
                if not nn(cL) or pL < cL: cL, cLb = pL, pidx
            else:
                cL, cLb, lastType = pL, pidx, -1
        if divBull: divLast = (i, 'Bull Div')
        if divBear: divLast = (i, 'Bear Div')
        if nn(ph_prev) and nn(pl_prev):
            if ph_last > ph_prev and pl_last > pl_prev: msTrend = 1
            elif ph_last < ph_prev and pl_last < pl_prev: msTrend = -1
        # كسر الهيكل اللحظي
        if nn(ph_last) and h[i] > ph_last and ph_idx != fLB: fLB = ph_idx; fPers = 1; fBar = i
        elif nn(pl_last) and l[i] < pl_last and pl_idx != fLBr: fLBr = pl_idx; fPers = -1; fBar = i
        fastActive = fPers != 0 and (i - fBar) <= p['fastBreakMaxAge']
        msEff = fPers if (p['useFastBreak'] and fastActive) else msTrend
        # فيبوناتشي
        useConf = nn(cH) and nn(cL) and cH > cL
        fibH = cH if useConf else hh50[i]; fibL = cL if useConf else ll50[i]
        fib618 = fibH - (fibH - fibL) * 0.618
        inFib = nn(atr[i]) and abs(c[i] - fib618) < atr[i] * 0.25
        # ---- SMC ----
        biasAct = smcBias != 0 and (i - smcBiasBar) <= p['smcBiasMaxAge']
        biasEv = smcBias if biasAct else 0
        newBull = nn(ph_last) and h[i] > ph_last and ph_idx != sLB
        newBear = nn(pl_last) and l[i] < pl_last and pl_idx != sLBr
        if newBull:
            sLB = ph_idx; ch = biasEv <= 0
            smcLast = 'CHoCH ↑' if ch else 'BOS ↑'; smcCnt['bc' if ch else 'bb'] += 1; smcBias = 1; smcBiasBar = i; smcLastBar = i
        elif newBear:
            sLBr = pl_idx; ch = biasEv >= 0
            smcLast = 'CHoCH ↓' if ch else 'BOS ↓'; smcCnt['sc' if ch else 'sb'] += 1; smcBias = -1; smcBiasBar = i; smcLastBar = i
        biasNow = smcBias != 0 and (i - smcBiasBar) <= p['smcBiasMaxAge']
        if newBull:
            for k in range(1, p['smcOBLookback'] + 1):
                if i - k >= 0 and c[i - k] < o[i - k]:
                    bullOB.append((h[i - k], l[i - k])); break
            if len(bullOB) > p['smcMaxOB']: bullOB.pop(0)
        if newBear:
            for k in range(1, p['smcOBLookback'] + 1):
                if i - k >= 0 and c[i - k] > o[i - k]:
                    bearOB.append((h[i - k], l[i - k])); break
            if len(bearOB) > p['smcMaxOB']: bearOB.pop(0)
        bullOB = [b for b in bullOB if not c[i] < b[1]]
        bearOB = [b for b in bearOB if not c[i] > b[0]]
        if i >= 2:
            if l[i] > h[i - 2]: fvgs.append((True, l[i], h[i - 2], h[i - 2]))
            if h[i] < l[i - 2]: fvgs.append((False, l[i - 2], h[i], l[i - 2]))
            fvgs = [f for f in fvgs if not ((c[i] < f[3]) if f[0] else (c[i] > f[3]))]
            if len(fvgs) > 20: fvgs.pop(0)
        hasBullFVG = any(f[0] for f in fvgs); hasBearFVG = any(not f[0] for f in fvgs)
        zr = fibH - fibL
        inPrem = nn(zr) and c[i] >= fibH - zr * 0.25
        inDisc = nn(zr) and c[i] <= fibL + zr * 0.25
        # ---- النقاط ----
        cT = [0, 0]; cM = [0, 0]; cV = [0, 0]; cS = [0, 0]; cL_ = [0, 0]; cSMC = [0, 0]; cP = [0, 0]   # [buy, sell]
        if emaF[i] > smaS[i]: cT[0] += W['EMA']
        elif emaF[i] < smaS[i]: cT[1] += W['EMA']
        if stD[i] < 0: cT[0] += 1
        elif stD[i] > 0: cT[1] += 1
        if c[i] > wmaV[i]: cT[0] += 1
        elif c[i] < wmaV[i]: cT[1] += 1
        for rr_ in (rsiF[i], rsiS[i]):
            if rr_ > 50: cM[0] += W['RSI']
            elif rr_ < 50: cM[1] += W['RSI']
        if stK[i] > stDv[i] and stK[i] < 80: cM[0] += 1
        elif stK[i] < stDv[i] and stK[i] > 20: cM[1] += 1
        if mm[i] > ms_[i] and mm[i] > 0: cM[0] += W['MACD']
        elif mm[i] < ms_[i] and mm[i] < 0: cM[1] += W['MACD']
        if ao[i] > 0: cM[0] += 1
        elif ao[i] < 0: cM[1] += 1
        isDist = nn(barChg[i]) and barChg[i] <= -p['crashPct']
        isPump = nn(barChg[i]) and barChg[i] >= p['crashPct']
        if c[i] > vw[i]: cV[0] += W['VWAP']
        elif c[i] < vw[i]: cV[1] += W['VWAP']
        if cmf[i] > 0 and not isDist: cV[0] += W['CMF']
        elif cmf[i] < 0 or isDist: cV[1] += W['CMF']
        if nn(volMA[i]) and v[i] > volMA[i]:
            if c[i] > o[i]: cV[0] += W['VP']
            elif c[i] < o[i]: cV[1] += W['VP']
        if msEff == 1: cS[0] += W['MS']
        elif msEff == -1: cS[1] += W['MS']
        if divBull: cL_[0] += W['Div']
        elif divBear: cL_[1] += W['Div']
        bSw = nn(llN[i]) and l[i] < llN[i] and c[i] > llN[i] and (c[i] - l[i]) > (h[i] - c[i])
        sSw = nn(hhN[i]) and h[i] > hhN[i] and c[i] < hhN[i] and (h[i] - c[i]) < (c[i] - l[i])
        if bSw: cL_[0] += W['Sweep']
        elif sSw: cL_[1] += W['Sweep']
        if inFib and stD[i] < 0: cL_[0] += 1
        elif inFib and stD[i] > 0: cL_[1] += 1
        if sqRel[i] and c[i] > bbMid[i]: cL_[0] += W['Sq']
        elif sqRel[i] and c[i] < bbMid[i]: cL_[1] += W['Sq']
        if biasNow and smcBias == 1: cSMC[0] += W['SMC']
        elif biasNow and smcBias == -1: cSMC[1] += W['SMC']
        if bullOB: cSMC[0] += W['SMC']
        elif bearOB: cSMC[1] += W['SMC']
        if hasBullFVG: cSMC[0] += W['SMC']
        elif hasBearFVG: cSMC[1] += W['SMC']
        if inDisc: cSMC[0] += W['SMC']
        elif inPrem: cSMC[1] += W['SMC']
        for f_ in (isHammer[i], isInvH[i], isBullEng[i], isMorn[i]):
            if f_: cP[0] += W['Pat']
        for f_ in (isHang[i], isShoot[i], isBearEng[i], isEven[i]):
            if f_: cP[1] += W['Pat']
        rg = dict(T=1.0, M=1.0, V=1.0, S=1.0, L=1.0, SMC=1.0)
        if chop[i] < p['chopTrend']: rg = dict(T=1.5, M=1.2, V=1.0, S=1.3, L=0.7, SMC=1.2)
        elif chop[i] > p['chopChoppy']: rg = dict(T=0.5, M=0.8, V=1.2, S=0.6, L=1.3, SMC=0.9)
        def tot(k):
            return cT[k] * rg['T'] + cM[k] * rg['M'] + cV[k] * rg['V'] + cS[k] * rg['S'] + cL_[k] * rg['L'] + cSMC[k] * rg['SMC'] + cP[k] * rg['L']
        buyS, sellS = tot(0), tot(1)
        maxS = (catMax['T'] * rg['T'] + catMax['M'] * rg['M'] + catMax['V'] * rg['V'] + catMax['S'] * rg['S'] +
                catMax['L'] * rg['L'] + catMax['SMC'] * rg['SMC'] + catMax['P'] * rg['L'])
        buyP = min(buyS / maxS * 100, 100) if maxS > 0 else 0; sellP = min(sellS / maxS * 100, 100) if maxS > 0 else 0
        cats = [cT, cM, cV, cS, cL_, cSMC, cP]
        buyAg = sum(1 for x in cats if x[0] > x[1]); sellAg = sum(1 for x in cats if x[1] > x[0])
        # ---- فلاتر الإشارة ----
        coolS = lastSig is None or (i - lastSig) >= p['cooldown']
        coolB = lastBuy is None or (i - lastBuy) >= p['cooldown']
        coolSe = lastSell is None or (i - lastSell) >= p['cooldown']
        canB = gradesOK and (coolB if p['allowOpposite'] else coolS)
        canS = gradesOK and (coolSe if p['allowOpposite'] else coolS)
        hb = True if htf_buy is None else bool(htf_buy[i]); hs = True if htf_sell is None else bool(htf_sell[i])
        cb = cs_ = True
        if i == n - 1 and last_override:
            hb, hs = last_override.get('htf_buy', hb), last_override.get('htf_sell', hs)
            cb, cs_ = last_override.get('corr_buy', True), last_override.get('corr_sell', True)
        gDn = nn(gapDist[i]) and nn(atr[i]) and gapDist[i] < -(atr[i] * p['gapATR'])
        gUp = nn(gapDist[i]) and nn(atr[i]) and gapDist[i] > (atr[i] * p['gapATR'])
        rawB = (i >= start and nn(atr[i]) and buyS >= p['minScore'] and (not p['useCatConf'] or buyAg >= p['minCats']) and hb and cb and canB
                and not isDist and (not p['useGapFilter'] or not gDn))
        rawS = (i >= start and nn(atr[i]) and sellS >= p['minScore'] and (not p['useCatConf'] or sellAg >= p['minCats']) and hs and cs_ and canS
                and not isPump and (not p['useGapFilter'] or not gUp))
        isBuy = rawB and (not rawS or buyP > sellP or (buyP == sellP and buyS > sellS))
        isSell = rawS and (not rawB or sellP > buyP or (sellP == buyP and sellS > buyS))
        if isBuy: lastBuy = lastSig = i
        if isSell: lastSell = lastSig = i
        if isBuy or isSell:
            signals.append((i, 'BUY' if isBuy else 'SELL', get_grade(buyP if isBuy else sellP, p)))
        # ---- الصفقة الافتراضية ----
        if st != 'RUNNING' and (isBuy or isSell):
            st = 'RUNNING'; tdir = 'BUY' if isBuy else 'SELL'; outcome = ''; tE = c[i]; tBE = False; entryBar = i
            sg = 1 if isBuy else -1
            slD, t1D, t2D, t3D = (atr[i] * p[k] for k in ('slATR', 'tp1ATR', 'tp2ATR', 'tp3ATR'))
            tSL = tE - sg * slD; tT1 = tE + sg * t1D; tT2 = tE + sg * t2D; tT3 = tE + sg * t3D
            hit1 = hit2 = hit3 = False; mfe = mae = 0.0; rmult = NaN; slDist0, tp3Dist0 = slD, t3D
            opened += 1; lastDir = tdir
        elif st == 'RUNNING':
            sg = 1 if tdir == 'BUY' else -1
            fav = h[i] if sg == 1 else l[i]; adv = l[i] if sg == 1 else h[i]
            mfe = max(mfe, sg * (fav - tE)); mae = max(mae, sg * (tE - adv))
            reach = lambda lvl: (fav >= lvl) if sg == 1 else (fav <= lvl)
            slhit = lambda lvl: (adv <= lvl) if sg == 1 else (adv >= lvl)
            tp1Now = (not hit1) and reach(tT1)
            closed = False; ambBar = False; new1 = new2 = new3 = False
            if tp1Now and slhit(tSL) and not tBE:
                hit1 = True; closed = True; ambBar = True; AMB += 1
                if p['ambAsLoss']: outcome, rmult = 'LOSS', -1.0; L_ += 1; sumR += -1.0; sumLoss += 1.0; closedN += 1
                else: outcome, rmult = 'AMBIGUOUS', NaN
            else:
                if tp1Now:
                    hit1 = True; new1 = True
                    if p['beAfterTP1'] and not tBE: tSL = tE; tBE = True
                if not hit2 and reach(tT2): hit2 = True; new2 = True
                if not hit3 and reach(tT3): hit3 = True; new3 = True
                slNow = slhit(tSL) and not (p['beNextBar'] and tp1Now)
                tp3Now = reach(tT3)
                if slNow and tp3Now:
                    closed = True; ambBar = True; AMB += 1
                    if p['ambAsLoss']: outcome, rmult = 'LOSS', -1.0; L_ += 1; sumR += -1.0; sumLoss += 1.0; closedN += 1
                    else: outcome, rmult = 'AMBIGUOUS', NaN
                elif slNow:
                    closed = True
                    if tBE: outcome, rmult = 'BE', 0.0; BE_ += 1
                    else: outcome, rmult = 'LOSS', -1.0; L_ += 1; sumR += -1.0; sumLoss += 1.0
                    closedN += 1
                elif hit3:
                    closed = True; outcome = 'WIN'; rmult = tp3Dist0 / slDist0 if slDist0 > 0 else NaN
                    W_ += 1; sumR += rmult; sumWin += rmult; closedN += 1
            if not ambBar:                       # 🆕 v6.6 مطابقة Pine: tp1Event/tp2Event/tp3Event تستثني شمعة AMBIGUOUS
                r1 += int(new1); r2 += int(new2); r3 += int(new3)
            if closed:
                st = 'CLOSED'; lastOutcome = outcome; lastR = rmult
                trades.append(dict(entry_bar=entryBar, exit_bar=i, dir=tdir, outcome=outcome, r=rmult))
        if i == n - 1:
            last = dict(
                i=i, atr=atr[i], emaF=emaF[i], smaS=smaS[i], wma=wmaV[i], stV=stV[i], stD=stD[i], rsiF=rsiF[i], rsiS=rsiS[i],
                stK=stK[i], stD_=stDv[i], macd=mm[i], macdSig=ms_[i], macdHist=mh[i], ao=ao[i], vwap=vw[i], cmf=cmf[i],
                chop=chop[i], volRatio=(v[i] / volSt[i]) if nn(volSt[i]) and volSt[i] > 0 else NaN,
                buyS=buyS, sellS=sellS, buyP=buyP, sellP=sellP, maxS=maxS, buyAg=buyAg, sellAg=sellAg,
                rg=rg, catB=dict(T=cT[0], M=cM[0], V=cV[0], S=cS[0], L=cL_[0], SMC=cSMC[0], P=cP[0]),
                catS=dict(T=cT[1], M=cM[1], V=cV[1], S=cS[1], L=cL_[1], SMC=cSMC[1], P=cP[1]),
                isBuy=isBuy, isSell=isSell, rawB=rawB, rawS=rawS, sweep=('Bull Sweep' if bSw else 'Bear Sweep' if sSw else 'None'),
                squeeze=bool(sq[i]), sqRelease=bool(sqRel[i]), msEff=msEff, msConf=msTrend, smcBias=smcBias, biasNow=biasNow,
                smcLast=smcLast, smcLastAge=i - smcLastBar, smcCnt=dict(smcCnt), fibH=fibH, fibL=fibL, fibConfirmed=useConf,
                inPrem=inPrem, inDisc=inDisc, bullOB=list(bullOB), bearOB=list(bearOB), fvgs=list(fvgs), divLast=divLast, eqLast=eqLast,
                pat=[nm for nm, a in (('Hammer', isHammer), ('InvHammer', isInvH), ('BullEngulf', isBullEng), ('MorningStar', isMorn),
                                      ('HangingMan', isHang), ('ShootingStar', isShoot), ('BearEngulf', isBearEng), ('EveningStar', isEven),
                                      ('Doji', isDoji), ('Marubozu', isMaru)) if a[i]],
                lastBuyAge=(i - lastBuy) if lastBuy is not None else None, lastSellAge=(i - lastSell) if lastSell is not None else None,
                isDist=isDist, isPump=isPump, gDn=gDn, gUp=gUp, barChg=barChg[i])
    # ---- القرار النهائي (نفس منطق القرار في محرك تحليل الشارت) ----
    if not last:
        return None
    mc = p['minCats']
    # 🆕 v5.2: الإشارة الفورية تُعرض قبل «صفقة جارية» (كانت 65/75 حالة تظهر IN TRADE رغم وجود إشارة الآن)
    ef = p.get('entryFirst', True)
    if ef and last['isBuy']: fd = 'ENTRY BUY'
    elif ef and last['isSell']: fd = 'ENTRY SELL'
    elif st == 'RUNNING': fd = 'IN TRADE'
    elif last['buyAg'] >= mc or last['sellAg'] >= mc: fd = 'WATCH'
    elif last['buyAg'] >= max(mc - 2, 1) or last['sellAg'] >= max(mc - 2, 1): fd = 'WAIT'
    else: fd = 'NO TRADE'
    tot_closed = closedN
    last.update(dict(
        final=fd, trade_state=st, trade_dir=tdir, entry=tE, sl=tSL, tp1=tT1, tp2=tT2, tp3=tT3, hit1=hit1, hit2=hit2, hit3=hit3, be=tBE,
        mfe=mfe if st == 'RUNNING' else NaN, mae=mae if st == 'RUNNING' else NaN,
        W=W_, L=L_, BE=BE_, AMB=AMB, closed=tot_closed, opened=opened,
        win_rate=(W_ * 100.0 / tot_closed) if tot_closed else NaN, pf=(sumWin / sumLoss) if sumLoss > 0 else (math.inf if sumWin > 0 else NaN),
        avg_r=(sumR / tot_closed) if tot_closed else NaN,
        reach1=(r1 * 100.0 / opened) if opened else NaN, reach2=(r2 * 100.0 / opened) if opened else NaN, reach3=(r3 * 100.0 / opened) if opened else NaN,
        last_outcome=lastOutcome, last_r=lastR, last_dir=lastDir, signals=signals, trades=trades,
        buyGrade=get_grade(last['buyP'], p), sellGrade=get_grade(last['sellP'], p), gradesOK=gradesOK))
    return last

# -----------------------------------------------------------------------------
# 6) محرك Radar PRO (الأساليب الخمسة + الدرجة المركبة + خطة التداول)
# -----------------------------------------------------------------------------
STYLES = ['Value', 'Growth', 'Swing', 'Medium Term', 'Long Term']
def style_params(style, p):
    sp = dict(tf='D', lb=p['lookbackManual'], emaF=20, emaM=50, emaS=200, rsi=14, mF=12, mS=26, mG=9, cmf=p['cmfManual'])
    if style == 'Swing':   sp.update(lb=15, emaF=8, emaM=21, emaS=50, rsi=7, mF=5, mS=13, mG=6, cmf=10)
    elif style == 'Growth': sp.update(lb=30, emaF=10, emaM=30, emaS=60, rsi=10, mF=8, mS=21, mG=9, cmf=14)
    elif style == 'Value':  sp.update(lb=90, cmf=30)
    elif style == 'Long Term': sp.update(tf='W', lb=52, emaF=10, emaM=30, emaS=50, cmf=13)
    return sp

def to_tf(df, tf):
    return resample_ohlc(df, 'W-FRI') if tf == 'W' else df

def mkt_phase_calc(c, p, tf='D'):
    """🆕 v7.0: مراحل السوق المؤسسية (مطابقة Pine v4.2) على سلسلة إغلاق المرجع بإطار tf.
    المراحل: 6 انهيار · 5 سوق هابط · 7 تعافٍ · 4 تصحيح · 3 تراجع/اتجاه هابط · 2 ضعف · 1 صحي — 0 غير متاح. يعيد None عند نقص البيانات."""
    c = c.dropna()
    if len(c) < 25: return None
    close = float(c.iloc[-1])
    e20, e50 = float(s_ema(c, 20).iloc[-1]), float(s_ema(c, 50).iloc[-1])
    hi20, lo20 = float(c.tail(20).max()), float(c.tail(20).min())
    long_len = 52 if tf == 'W' else 252
    hi_l = float(c.tail(long_len).max()) if len(c) >= long_len else NaN
    chg1 = (close / float(c.iloc[-2]) - 1) * 100
    chg5 = (close / float(c.iloc[-6]) - 1) * 100 if len(c) > 6 else NaN
    dd20 = (close - hi20) / hi20 * 100 if hi20 > 0 else NaN
    state = 0
    if nn(e20) and nn(e50) and nn(dd20):
        corr = dd20 <= -p['mktCorrPct'] or (close < e50 and e20 < e50)
        state = 3 if corr else (2 if close < e20 else 1)
    hi_ref = hi_l if nn(hi_l) else hi20
    dd_ref = (close - hi_ref) / hi_ref * 100 if hi_ref > 0 else NaN
    trough = (lo20 - hi_ref) / hi_ref * 100 if hi_ref > 0 else NaN
    bounce = (close - lo20) / lo20 * 100 if lo20 > 0 else NaN
    phase, crash_day, crash_win, bounce_tag, at_high = 0, False, False, False, False
    if state > 0 and nn(dd_ref):
        crash_day = nn(chg1) and chg1 <= -p.get('mktCrashDay', 7.0)
        crash_win = nn(chg5) and chg5 <= -p.get('mktCrashWin', 10.0)
        bounced = nn(bounce) and bounce >= p.get('mktBounceMin', 5.0)
        was_corr = nn(trough) and trough <= -p.get('mktCorrDD', 10.0)
        if crash_day or crash_win: phase = 6
        elif dd_ref <= -p.get('mktBearDD', 20.0): phase = 5
        elif bounced and was_corr and close >= e50: phase = 7
        elif dd_ref <= -p.get('mktCorrDD', 10.0): phase = 4
        elif state == 3: phase = 3
        else: phase = state
        bounce_tag = bool(bounced and close < e50 and phase >= 3 and phase != 7)
        at_high = bool(phase == 1 and nn(hi_l) and close >= hi_l)
    return dict(phase=phase, state=state, stress=bool(state == 3 or phase in (4, 5, 6)), close=close, ema20=e20, ema50=e50, hi20=hi20, lo20=lo20, hi_long=hi_l, long_len=long_len,
                chg1=chg1, chg5=chg5, dd20=dd20, dd_ref=dd_ref, trough=trough, bounce=bounce, crash_day=bool(crash_day), crash_win=bool(crash_win),
                bounce_tag=bounce_tag, at_high=at_high, below20_up=bool(close < e20 and chg1 > 0),
                vs20=(close - e20) / e20 * 100 if nn(e20) and e20 else NaN, vs50=(close - e50) / e50 * 100 if nn(e50) and e50 else NaN)

def bench_metrics(bdf, sp, p=None):
    if bdf is None or len(bdf) < 25: return None
    p = p if isinstance(p, dict) else P   # 🆕 v5.2: يقرأ الإعدادات من p الممررة (كان يقرأ العام P مباشرة)
    d = to_tf(bdf, sp['tf']); c = d['Close']; lb = sp['lb']
    if len(c) < lb + 3: return None
    r = dict(chgNow=(c.iloc[-1] - c.iloc[-1 - lb]) / c.iloc[-1 - lb] * 100,
             chgPrev=(c.iloc[-2] - c.iloc[-2 - lb]) / c.iloc[-2 - lb] * 100,
             close=c.iloc[-1], ema20=s_ema(c, 20).iloc[-1], ema50=s_ema(c, 50).iloc[-1],
             hi20=c.tail(20).max(), chg1=(c.iloc[-1] - c.iloc[-2]) / c.iloc[-2] * 100)
    dd = (r['close'] - r['hi20']) / r['hi20'] * 100 if r['hi20'] > 0 else NaN
    r['dd'] = dd
    state = 0
    if nn(r['ema20']) and nn(r['ema50']) and nn(dd):
        corr = dd <= -p['mktCorrPct'] or (r['close'] < r['ema50'] and r['ema20'] < r['ema50'])
        state = 3 if corr else (2 if r['close'] < r['ema20'] else 1)
    r['state'] = state
    r['vs20'] = (r['close'] - r['ema20']) / r['ema20'] * 100 if nn(r['ema20']) else NaN
    r['vs50'] = (r['close'] - r['ema50']) / r['ema50'] * 100 if nn(r['ema50']) else NaN
    r['rebound'] = bool(nn(r['ema20']) and r['close'] < r['ema20'] and r['chg1'] > 0)
    ph = mkt_phase_calc(c, p, sp['tf'])      # 🆕 v7.0: المراحل المؤسسية (stress يشمل التراجع/التصحيح/الهابط/الانهيار — لا يشمل التعافي)
    r['phase'] = ph['phase'] if ph else 0
    r['stress'] = bool(ph['stress']) if ph else bool(state == 3)
    r['phase_info'] = ph
    return r

def _synthetic_index(dfs, min_n=2, min_bars=90):
    """🆕 v5.1: مؤشر تركيبي متساوي الأوزان من الأسهم المتاحة (بديل عندما يفشل مؤشر السوق على ياهو).
    يطبّع كل سهم إلى 100 عند بدايته ثم يأخذ متوسط الإغلاقات — بحيث تُحسب حالة السوق العام بنفس
    معادلات bench_metrics تماماً (EMA20/EMA50/هبوط 20 شمعة)."""
    try:
        closes = []
        for d in dfs:
            if d is None or not isinstance(d, pd.DataFrame) or 'Close' not in d.columns:
                continue
            c = pd.to_numeric(d['Close'], errors='coerce').dropna()
            if len(c) < min_bars or not c.iloc[0]:
                continue
            closes.append(c / float(c.iloc[0]) * 100.0)
        if len(closes) < min_n:
            return None
        m = pd.concat(closes, axis=1).ffill().dropna(how='all')
        idx = m.mean(axis=1, skipna=True).dropna()
        if len(idx) < min_bars:
            return None
        out = pd.DataFrame({'Open': idx, 'High': idx, 'Low': idx, 'Close': idx, 'Volume': 0.0}, index=idx.index)
        return out if len(out) >= 25 else None
    except Exception:
        return None

def radar_row(sym, df, style, p, bm, sector='', sess_closed=False, style_ctx=None):
    sp = style_params(style, p); d = to_tf(df, sp['tf']); lb = sp['lb']
    ac = asset_class(sym)
    PAR = p.get('pineParity', True)   # 🆕 v6.6: مطابقة Pine حرفياً (False = سلوك v6.5)
    if sp['tf'] == 'W':               # 🆕 v6.6: اكتمال الشمعة الأسبوعية (يطابق time_close للإطار W في Pine)
        sess_closed = week_closed(sym, df.index[-1])
    row = dict(style=style, tf=sp['tf'], lb=lb, state=0, sector=sector, sessClosed=sess_closed, asset=ASSET_TXT.get(ac, ('Stock', 'سهم'))[0])
    dc = df['Close']
    row['price'] = float(dc.iloc[-1]); row['chg'] = float((dc.iloc[-1] - dc.iloc[-2]) / dc.iloc[-2] * 100) if len(dc) > 1 else NaN
    if len(d) < lb + 3 or len(dc) < 20:
        row.update(state=2, score=-1.0, rating='⚪ N/A', reasons=f'⏳ Insufficient history (needs {lb + 1}+ bars)', sig='—', tech='—')
        return row
    c = d['Close']; h = d['High']; l = d['Low']; v = d['Volume']
    has_vol = bool(np.nansum(v) > 0)   # 🆕 v6 (إصلاح 3): الأصول بلا حجم (فوركس/مؤشرات) تعالَج بأوزان معاد توزيعها
    ema_f, ema_m, ema_s = s_ema(c, sp['emaF']), s_ema(c, sp['emaM']), s_ema(c, sp['emaS'])
    rsi = s_rsi(c, sp['rsi']); mL = s_ema(c, sp['mF']) - s_ema(c, sp['mS']); mS_ = s_ema(mL, sp['mG'])
    mfm = ((c - l) - (h - c)) / (h - l).replace(0, np.nan)
    cmfR = (mfm.fillna(0) * v).rolling(sp['cmf']).sum() / v.rolling(sp['cmf']).sum().replace(0, np.nan)
    volAvg = s_sma(v, 20); atrS = s_atr(d, 14); smC = s_sma(c, 5)
    chgPct = (c - c.shift(lb)) / c.shift(lb) * 100
    swHi = h.rolling(lb).max().iloc[-1]; swLo = l.rolling(lb).min().iloc[-1]
    pdi, mdi, adx = s_dmi(d, 14)
    bbB = s_sma(c, 20); bbD = 2 * c.rolling(20).std(ddof=0)
    bbPB = ((c - (bbB - bbD)) / ((bbB + bbD) - (bbB - bbD)).replace(0, np.nan) * 100).iloc[-1]
    tradedVal = s_sma(v * c, 20).iloc[-1]
    gapPct = (d['Open'].iloc[-1] - c.iloc[-2]) / c.iloc[-2] * 100 if len(c) > 1 else 0.0
    # 🆕 v5.2: كشف بيانات فتح معطّلة من المزود (الفتح = إغلاق الأمس في معظم الصفوف) — كانت الفجوة تُعرض 0% زائفة لكل الأسهم المصرية و9 من 19 سعودية
    o_arr = df['Open'].values.astype(float); c_arr = df['Close'].values.astype(float)
    k0 = max(1, len(c_arr) - 40)
    same_open = float(np.mean(np.abs(o_arr[k0:] - c_arr[k0 - 1:-1]) <= 1e-9)) if len(c_arr) > k0 else 0.0
    open_ok = same_open < 0.9
    if not open_ok:
        gapPct = NaN
    intra = (c.iloc[-1] - d['Open'].iloc[-1]) / d['Open'].iloc[-1] * 100 if d['Open'].iloc[-1] > 0 else 0.0
    liveChg = (c.iloc[-1] - c.iloc[-2]) / c.iloc[-2] * 100
    g = lambda s_, k=-1: float(s_.iloc[k])
    isDaySens = style in ('Swing', 'Growth')
    confirmedNow = p['stabilize'] and not isDaySens and p['closedAsConfirmed'] and sess_closed
    useStab = p['stabilize'] and not isDaySens and not confirmedNow
    k = -2 if useStab else -1
    scEma20, scEma50, scEma200 = g(ema_f, k), g(ema_m, k), g(ema_s, k)
    scRsi, scML, scMS = g(rsi, k), g(mL, k), g(mS_, k)
    scCmf, scChg, scVol, scVolAvg = g(cmfR, k), g(chgPct, k), g(v, k), g(volAvg, k)
    prevC = g(c, -2); scTrendRef = prevC if useStab else (g(c) if (isDaySens or confirmedNow) else g(smC))
    if any(math.isnan(x) for x in (scChg,)):
        row.update(state=2, score=-1.0, rating='⚪ N/A', reasons=f'⏳ Insufficient history (needs {lb + 1}+ bars)', sig='—', tech='—'); return row
    # 🆕 v6 (إصلاح 9): بيانات أقل من 200 شمعة — الاتجاه يُحسب على المتوسطات المتاحة فقط فلا ينخفض السقف بصمت
    # 🆕 v6.6: مع pineParity الاتجاه 3 مقارنات ثابتة (المقارنة الناقصة = 0 كما في Pine)
    if PAR:
        trendPairs = [scTrendRef > scEma20, scEma20 > scEma50, scEma50 > scEma200]
    else:
        trendPairs = [scTrendRef > scEma20]
        if nn(scEma50): trendPairs.append(scEma20 > scEma50)
        if nn(scEma200): trendPairs.append(scEma50 > scEma200)
    trendScore = sum(1 for x in trendPairs if x)
    trendDen = len(trendPairs)
    trendPct = trendScore / trendDen * 100
    short_hist = (not nn(scEma200)) and len(c) < sp['emaS']
    momScore = (50 < scRsi < 70) + (scML > scMS) + (scChg > 0)
    momPct = momScore / 3 * 100
    benchOK = bm is not None
    benchSel = (bm['chgPrev'] if useStab else bm['chgNow']) if benchOK else 0.0
    relStr = (scChg - benchSel) if benchOK else 0.0
    # 🆕 v6 (إصلاح 8): المرجع هو نفسه (ذهب/بيتكوين/مؤشر بلا بيانات) — مكوّن القوة النسبية يُستبعد بإعادة توزيع الأوزان
    # 🆕 v6.6: مع pineParity يبقى المكوّن بقيمة 50 ووزن 1 كما في Pine (benchInvalid → 50)
    use_rs = benchOK or PAR
    relPct = max(0, min(100, 50 + relStr * 2)) if benchOK else 50.0
    wRS_term = 1.0 if use_rs else 0.0
    gapBig = abs(gapPct) >= p['gapThresh'] and open_ok
    distChg = liveChg
    if p.get('gapAware', False) and gapBig and nn(gapPct):   # 🆕 v6.6: تعويض الفجوة (خيار Pine inp_gapAware) — الهبوط يُقاس من الافتتاح
        distChg = float(intra)
    isDist = distChg <= -p['crashCandle']
    cmfPos = scCmf > 0 and not isDist and has_vol      # 🆕 v6: CMF بلا حجم غير معرَّف — لا يُحسب موجباً ولا سالباً
    liqPct = (((1 if cmfPos else 0) + (1 if (has_vol and scVol > scVolAvg) else 0)) / 2 * 100) if has_vol else 50.0
    rngS = swHi - swLo
    distSup = (scTrendRef - swLo) / rngS * 100 if rngS > 0 else 50
    valPct = max(0, 100 - distSup)
    notOB = 0 if scRsi >= 70 else 100 if scRsi <= 30 else (70 - scRsi) / 40 * 100
    atrV = g(atrS); atrPct = atrV / g(c) * 100
    # 🆕 v5.2: عتبات المخاطرة تُعاير حسب فئة الأصل (رقمية/عملات/معادن…) والإطار (الأسبوعي ×√5) — كانت 2%/4% يومية تُطبَّق على ATR أسبوعي فتظهر 14/17 «مخاطرة عالية» في أسلوب Long Term
    # 🆕 v6.6: مع pineParity العتبات ثابتة 2/4 كما في Pine
    wk_scale = math.sqrt(5.0) if sp['tf'] == 'W' else 1.0
    base_lo, base_hi = (p['riskLow'], p['riskHigh']) if ac == 'stock' else ASSET_RISK.get(ac, (p['riskLow'], p['riskHigh']))
    th_lo, th_hi = (p['riskLow'], p['riskHigh']) if PAR else (base_lo * wk_scale, base_hi * wk_scale)
    riskLevel = '🟢 Low' if atrPct < th_lo else '🔴 High' if atrPct > th_hi else '🟡 Medium'
    riskDot = riskLevel[0]
    riskPen = min(20, (atrPct - th_hi) * 5) if atrPct > th_hi else 0
    adxV = g(adx); adxOk = adxV >= 25; adxWeak = adxV < 15; diBull = g(pdi) > g(mdi)
    adxBonus = 5.0 if (adxOk and diBull) else -5.0 if (adxOk and not diBull) else -3.0 if adxWeak else 0.0
    bbOS = bbPB <= 20; bbOB = bbPB >= 95
    bbBonus = 5.0 if bbOS else -5.0 if bbOB else 0.0
    wT = {'Growth': 1.3, 'Long Term': 1.4, 'Swing': 0.8}.get(style, 1.0)
    wM = {'Growth': 1.3, 'Swing': 1.4, 'Value': 0.7}.get(style, 1.0)
    wV = {'Value': 1.4, 'Swing': 0.7}.get(style, 1.0)
    # 🆕 v6: إعادة توزيع الأوزان عند غياب المرجع (قوة نسبية) أو غياب الحجم (سيولة) — بدل خصم صامت من الدرجة
    den_inv = wT + wM + wRS_term + 1.0 + wV + 1.0
    inv = (trendPct * wT + momPct * wM + (relPct if use_rs else 0.0) + (liqPct if has_vol else 0.0) + valPct * wV + notOB) / den_inv
    inv = max(0, min(100, inv - riskPen + adxBonus))
    accum = cmfPos and has_vol and distSup < 25 and scRsi < 60 and scVol > scVolAvg
    structOK = (scEma50 > scEma200) if nn(scEma200) else ((scEma20 > scEma50) if nn(scEma50) else True)   # 🆕 v6 (إصلاح 9)
    isInvStyle = style in ('Value', 'Medium Term', 'Long Term')
    dropTag = ''; distPen = 0.0
    if isDist:
        if not isInvStyle: distPen = min(35, abs(liveChg) * 3); dropTag = '⚠️Crash '
        elif not structOK: distPen = min(25, abs(liveChg) * 2); dropTag = '⚠️Break '
        else: dropTag = '🔻Dip? '
    entryLoc = max(0, 100 - distSup)
    entry = (trendPct * wT + momPct * wM + (relPct if use_rs else 0.0) + (liqPct if has_vol else 0.0) + entryLoc + notOB) / (wT + wM + wRS_term + 1.0 + 1.0 + 1.0)
    entry = max(0, min(100, entry - riskPen - distPen + bbBonus))
    tech = '🟢 Conf' if (trendScore == trendDen and momScore >= 2 and (relStr > 0 or (not benchOK and not PAR))) else '🟡 Dev' if (trendScore >= 1 and momScore >= 1) else '🔴 No'   # 🆕 v6: الاتجاه الكامل = عدد المقارنات المتاحة وليس 3 صامتة
    comp = (inv + entry) / 2
    rating = '🟢 Strong Inv.' if comp >= 80 else '🔵 High Pot.' if comp >= 65 else '🟡 Watchlist' if comp >= 50 else '🟠 Weak Str.' if comp >= 35 else '🔴 Avoid'
    gapTag = ('GapUp ' if gapPct > 0 else 'GapDn ') if gapBig else ('⚠Open? ' if not open_ok else '')
    reasons = ('Trend↑ ' if trendPct >= 66 else '') + ('RS+ ' if (benchOK and relStr > 0) else '') + ('CMF+ ' if cmfPos else '') + dropTag + \
              ('Vol+ ' if (has_vol and scVol > scVolAvg) else '') + ('NearSup ' if distSup < 25 else '') + ('🌱Accum ' if accum else '') + \
              ('ADX+ ' if (adxOk and diBull) else '') + ('Choppy ' if adxWeak else '') + ('BB-Low ' if bbOS else '') + ('BB-High ' if bbOB else '') + \
              ('NoVol ' if not has_vol else '') + ('ShortHist ' if short_hist else '') + gapTag + riskLevel
    # 🆕 v5.0 وسوم أسباب قياسية (للتعريب الكامل في العرض/التصدير)
    tags = []
    if trendPct >= 66: tags.append('trend')
    if benchOK and relStr > 0: tags.append('rs')
    if cmfPos: tags.append('cmf')
    if dropTag == '⚠️Crash ': tags.append('crash')
    elif dropTag == '⚠️Break ': tags.append('break')
    elif dropTag == '🔻Dip? ': tags.append('dip')
    if has_vol and scVol > scVolAvg: tags.append('vol')
    if not has_vol: tags.append('novol')
    if short_hist: tags.append('limdata')
    if distSup < 25: tags.append('nearsup')
    if accum: tags.append('accum')
    if adxOk and diBull: tags.append('adx')
    if adxWeak: tags.append('choppy')
    if bbOS: tags.append('bblow')
    if bbOB: tags.append('bbhigh')
    if gapBig: tags.append('gapup' if gapPct > 0 else 'gapdn')
    if not open_ok: tags.append('nodataopen')
    riskKey = 'low' if atrPct < th_lo else 'high' if atrPct > th_hi else 'medium'
    dropSig = ('🔻 ' if dropTag == '🔻Dip? ' else '⚠ ') if isDist else ''
    gapSig = ('G↑ ' if gapPct > 0 else 'G↓ ') if gapBig else ''
    sig = riskDot + ' ' + ('T ' if trendPct >= 66 else '') + ('RS ' if (benchOK and relStr > 0) else '') + ('C ' if cmfPos else '') + ('V ' if (has_vol and scVol > scVolAvg) else '') + \
          ('S ' if distSup < 25 else '') + ('A ' if accum else '') + ('D ' if (adxOk and diBull) else '') + ('~ ' if adxWeak else '') + \
          ('B↓ ' if bbOS else '') + ('B↑ ' if bbOB else '') + dropSig + gapSig
    tvDaily = tradedVal / 5 if sp['tf'] == 'W' else tradedVal
    st = 3 if (has_vol and p['minTradedValue'] > 0 and nn(tvDaily) and tvDaily < p['minTradedValue']) else 0   # 🆕 v6: بلا حجم لا يُعلَّم سيولة منخفضة
    if st == 3:
        reasons = '💧LowLiq ' + reasons
        tags.append('lowliq')
    # خطة التداول
    dp = row['price']; stopP = max(0.0, dp - p['stopAtr'] * atrV); tgt = dp + p['targetAtr'] * atrV; src = ''
    if p['capAtRes'] and swHi > dp and swHi < tgt: tgt = swHi; src = 'H'
    if p['capAtEma']:
        if g(ema_f) > dp and g(ema_f) < tgt: tgt = g(ema_f); src = 'E' + str(sp['emaF'])
        if g(ema_m) > dp and g(ema_m) < tgt: tgt = g(ema_m); src = 'E' + str(sp['emaM'])
    riskPS = dp - stopP; rr = (tgt - dp) / riskPS if riskPS > 0 else NaN
    raw_qty = min(p['capital'] * p['riskPct'] / 100 / riskPS, p['capital'] / dp) if (riskPS > 0 and p['capital'] > 0 and dp > 0) else NaN
    # 🆕 v6 (إصلاح 6): كسور الأصول — للعملات الرقمية/المعادن/العملات/المؤشرات وعندما لا يكفي رأس المال لسهم واحد
    frac_ok = ac in ('crypto', 'forex', 'commodity', 'index') or (nn(raw_qty) and p['capital'] > 0 and dp > 0 and (p['capital'] / dp) < 1.0)
    qty = (round(raw_qty, 4) if frac_ok else math.floor(raw_qty)) if nn(raw_qty) else NaN
    row.update(dict(
        state=st, score=comp, inv=inv, entryScore=entry, rating=rating, tech=tech, reasons=reasons.strip(), sig=sig.strip(),
        reason_tags=tags, risk_key=riskKey, liveChg=float(liveChg), intraChg=float(intra),
        riskLevel=riskLevel, atrPct=atrPct, atr=atrV, stop=stopP, target=tgt, tgtSrc=src, rr=rr, qty=qty, scChg=scChg,
        adx=adxV, bbPB=float(bbPB), gapPct=float(gapPct), tradedVal=float(tvDaily) if nn(tvDaily) else NaN, swHi=float(swHi), swLo=float(swLo),
        prevC=prevC, ema20=g(ema_f), ema50=g(ema_m), rsiV=g(rsi), macdL=float(g(mL)), macdS=float(g(mS_)), trendPct=trendPct, momPct=momPct, relPct=relPct, liqPct=liqPct, valPct=valPct,
        notOB=notOB, confirmedNow=confirmedNow, benchOK=benchOK, distSup=distSup, open_ok=open_ok, hasVol=has_vol, shortHist=short_hist, trendDen=trendDen))
    return row


# -----------------------------------------------------------------------------
# 7) البيانات المالية: Piotroski / Altman / Beneish + مقاييس أساسية
# -----------------------------------------------------------------------------
def _row_v(df, names, k=0):
    if df is None or not hasattr(df, 'index') or len(df) == 0: return NaN
    for nm in names:
        if nm in df.index:
            try:
                x = df.loc[nm]
                x = x.iloc[k] if hasattr(x, 'iloc') else x
                if x == x: return float(x)
            except Exception:
                pass
    return NaN
def _div(a, b):
    return a / b if (nn(a) and nn(b) and b != 0) else NaN

def piotroski(fin, bs, cf):
    try:
        NI0, NI1 = _row_v(fin, ['Net Income'], 0), _row_v(fin, ['Net Income'], 1)
        TA0, TA1 = _row_v(bs, ['Total Assets'], 0), _row_v(bs, ['Total Assets'], 1)
        CFO0 = _row_v(cf, ['Operating Cash Flow', 'Cash Flow From Continuing Operating Activities'], 0)
        LTD0, LTD1 = _row_v(bs, ['Long Term Debt'], 0), _row_v(bs, ['Long Term Debt'], 1)
        CA0, CA1 = _row_v(bs, ['Current Assets'], 0), _row_v(bs, ['Current Assets'], 1)
        CL0, CL1 = _row_v(bs, ['Current Liabilities'], 0), _row_v(bs, ['Current Liabilities'], 1)
        SH0, SH1 = _row_v(bs, ['Ordinary Shares Number', 'Share Issued'], 0), _row_v(bs, ['Ordinary Shares Number', 'Share Issued'], 1)
        GP0, GP1 = _row_v(fin, ['Gross Profit'], 0), _row_v(fin, ['Gross Profit'], 1)
        RV0, RV1 = _row_v(fin, ['Total Revenue', 'Operating Revenue'], 0), _row_v(fin, ['Total Revenue', 'Operating Revenue'], 1)
        tests = []
        roa0, roa1 = _div(NI0, TA0), _div(NI1, TA1)
        if nn(NI0): tests.append(NI0 > 0)
        if nn(CFO0): tests.append(CFO0 > 0)
        if nn(roa0) and nn(roa1): tests.append(roa0 > roa1)
        if nn(CFO0) and nn(NI0): tests.append(CFO0 > NI0)
        if nn(_div(LTD0, TA0)) and nn(_div(LTD1, TA1)): tests.append(_div(LTD0, TA0) <= _div(LTD1, TA1))
        if nn(_div(CA0, CL0)) and nn(_div(CA1, CL1)): tests.append(_div(CA0, CL0) > _div(CA1, CL1))
        if nn(SH0) and nn(SH1): tests.append(SH0 <= SH1)
        if nn(_div(GP0, RV0)) and nn(_div(GP1, RV1)): tests.append(_div(GP0, RV0) > _div(GP1, RV1))
        if nn(_div(RV0, TA0)) and nn(_div(RV1, TA1)): tests.append(_div(RV0, TA0) > _div(RV1, TA1))
        # 🆕 v5.2: عند توفر 6–8 اختبارات فقط تُطبَّع الدرجة إلى مقياس 9 اختبارات (بدل مجموع خام غير قابل للمقارنة)
        return round(sum(tests) * 9.0 / len(tests), 1) if len(tests) >= 6 else NaN
    except Exception:
        return NaN

def altman_z(fin, bs, mcap):
    try:
        TA = _row_v(bs, ['Total Assets']); TL = _row_v(bs, ['Total Liabilities Net Minority Interest', 'Total Liabilities'])
        CA, CL = _row_v(bs, ['Current Assets']), _row_v(bs, ['Current Liabilities'])
        RE = _row_v(bs, ['Retained Earnings']); EBIT = _row_v(fin, ['EBIT', 'Operating Income']); S = _row_v(fin, ['Total Revenue', 'Operating Revenue'])
        if not all(nn(x) for x in (TA, TL, CA, CL, RE, EBIT, S, mcap)) or TA == 0 or TL == 0: return NaN
        return 1.2 * (CA - CL) / TA + 1.4 * RE / TA + 3.3 * EBIT / TA + 0.6 * mcap / TL + 1.0 * S / TA
    except Exception:
        return NaN

def beneish_m(fin, bs, cf):
    try:
        g_ = lambda df, nm, k: _row_v(df, nm, k)
        AR = [g_(bs, ['Accounts Receivable', 'Net Receivables', 'Receivables'], k) for k in (0, 1)]
        S = [g_(fin, ['Total Revenue', 'Operating Revenue'], k) for k in (0, 1)]
        GP = [g_(fin, ['Gross Profit'], k) for k in (0, 1)]
        CA = [g_(bs, ['Current Assets'], k) for k in (0, 1)]
        PPE = [g_(bs, ['Net PPE', 'Property Plant Equipment'], k) for k in (0, 1)]
        TA = [g_(bs, ['Total Assets'], k) for k in (0, 1)]
        DEP = [g_(cf, ['Depreciation And Amortization', 'Depreciation Amortization Depletion', 'Depreciation'], k) for k in (0, 1)]
        SGA = [g_(fin, ['Selling General And Administration'], k) for k in (0, 1)]
        CL = [g_(bs, ['Current Liabilities'], k) for k in (0, 1)]
        LTD = [g_(bs, ['Long Term Debt'], k) for k in (0, 1)]
        NI, CFO = g_(fin, ['Net Income'], 0), g_(cf, ['Operating Cash Flow'], 0)
        DSRI = _div(_div(AR[0], S[0]), _div(AR[1], S[1])); GMI = _div(_div(GP[1], S[1]), _div(GP[0], S[0]))
        AQI = _div(1 - _div(CA[0] + PPE[0], TA[0]), 1 - _div(CA[1] + PPE[1], TA[1])); SGI = _div(S[0], S[1])
        DEPI = _div(_div(DEP[1], DEP[1] + PPE[1]), _div(DEP[0], DEP[0] + PPE[0]))
        SGAI = _div(_div(SGA[0], S[0]), _div(SGA[1], S[1]))
        LVGI = _div(_div(CL[0] + LTD[0], TA[0]), _div(CL[1] + LTD[1], TA[1])); TATA = _div(NI - CFO, TA[0])
        comps = [DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA]
        if not all(nn(x) for x in comps): return NaN
        return -4.84 + 0.92 * DSRI + 0.528 * GMI + 0.404 * AQI + 0.892 * SGI + 0.115 * DEPI - 0.172 * SGAI + 4.679 * TATA - 0.327 * LVGI
    except Exception:
        return NaN

def sector_profile(sector, industry, name=''):
    """🆕 v5.2: ملف القطاع — Altman Z وهامش FCF غير معبّرين عن البنوك/التأمين/المرافق/العقار فيُستبعدان بدل إطلاق أعلام حمراء زائفة.
    يدعم أيضًا كشف البنوك من اسم الشركة (ياهو لا يوفر قطاعًا لبعض الأسواق مثل مصر)."""
    s = f'{sector} {industry} {name}'.lower()
    def _w(*kws):   # 🆕 v6 (إصلاح 12): مطابقة حدود الكلمات — «Electrical Equipment» لا تُلتقط بـelectric و«Waters» لا تُلتقط بـwater
        return any(re.search(r'(?<![a-z])' + re.escape(k) + r'(?![' + 'a-z' + '])', s) for k in kws)
    if _w('bank', 'banks', 'بنك', 'insurance', 'تأمين', 'financial', 'مالي', 'capital markets', 'credit services',
          'investment banking', 'asset management', 'diversified financial', 'exchange traded fund'):
        return dict(altman_ok=False, fcf_ok=False)
    if _w('utilities', 'utility', 'مرافق', 'electric utility', 'utilities regulated', 'كهرباء', 'water utility', 'gas utility'):
        return dict(altman_ok=False, fcf_ok=True)
    if _w('real estate', 'عقار', 'reit', 'realty', 'property development'):
        return dict(altman_ok=False, fcf_ok=True)
    return dict(altman_ok=True, fcf_ok=True)

def _q_eps_sum(qfin):
    """🆕 v7.0: EPS TTM = مجموع آخر 4 أرباع من القوائم الربعية (NaN عند نقص الأرباع)."""
    try:
        if qfin is None or getattr(qfin, 'empty', True): return NaN
        for nm in ('Diluted EPS', 'Basic EPS'):
            if nm in qfin.index:
                v = pd.to_numeric(qfin.loc[nm], errors='coerce').dropna()
                if len(v) >= 4: return float(v.iloc[:4].sum())
    except Exception:
        pass
    return NaN

_FIN_RX = re.compile(r'(?<![a-z])(bank|banks|insurance|financial|capital markets|credit services|asset management|diversified financial|بنك|تأمين|مالي)(?![a-z])')

def fund_metrics(fund, price, sym='', p=None, tvf=None):
    """🆕 v7.0: tvf = صف TradingView للسهم (اختياري). يصحّح القيمة السوقية القديمة، ويختار EPS TTM الأحدث، ويحمي من اختلاف العملة (ADR)."""
    pp = p if isinstance(p, dict) else P
    info = (fund or {}).get('info', {}) or {}; fin, bs, cf = (fund or {}).get('fin'), (fund or {}).get('bs'), (fund or {}).get('cf')
    qfin = (fund or {}).get('qfin')
    p_eps_fb = pp.get('epsFallback', True)
    tv = tvf or {}
    flags = []
    f = lambda k: (lambda x: float(x) if isinstance(x, (int, float, np.number)) and x == x else NaN)(info.get(k))
    roe = f('returnOnEquity'); roe = roe * 100 if nn(roe) else NaN
    if nn(roe) and roe > 500: roe = NaN   # 🆕 v6 (إصلاح 13): لا يُلغى ROE الحقيقي — يُستبعد غير المنطقي فقط (>500%)
    eps_y = f('trailingEps'); bvps = f('bookValue'); mcap_y = f('marketCap')
    pe_info, pb_info = f('trailingPE'), f('priceToBook')
    cur, fcur = str(info.get('currency') or ''), str(info.get('financialCurrency') or '')
    cur_mis = bool(cur and fcur and cur.upper() != fcur.upper() and not (cur.upper() in ('GBX', 'GBP') and fcur.upper() in ('GBX', 'GBP')))
    e0, e1 = _row_v(fin, ['Diluted EPS', 'Basic EPS'], 0), _row_v(fin, ['Diluted EPS', 'Basic EPS'], 1)
    q_eps = _q_eps_sum(qfin)
    # ── EPS: TradingView TTM ← ياهو TTM ← مجموع 4 أرباع ← السنوي ──
    eps, eps_src = NaN, ''
    tv_eps = tv.get('eps_ttm', NaN)
    if pp.get('fvTvFund', True) and nn(tv_eps) and tv_eps != 0:
        eps, eps_src = float(tv_eps), 'TV-TTM'
    elif nn(eps_y):
        eps, eps_src = eps_y, 'Yahoo-TTM'
    elif nn(q_eps):
        eps, eps_src = q_eps, 'Quarterly-sum'
    elif p_eps_fb and nn(e0):
        eps, eps_src = float(e0), 'FY'
    # حماية العملة: ADR/إدراج مزدوج — EPS وBVPS بعملة القوائم والسعر بعملة التداول ⇒ نشتقهما من السعر ÷ مضاعف ياهو (متسق العملة)
    if cur_mis and nn(price) and price > 0 and eps_src.startswith('Yahoo'):
        if nn(pe_info) and pe_info > 0: eps = price / pe_info; eps_src = 'Price/PE'; flags.append('currency')
        else: eps = NaN; eps_src = ''; flags.append('currency')
    if cur_mis and nn(price) and price > 0 and nn(pb_info) and pb_info > 0:
        bvps = price / pb_info; flags.append('currency')
    tv_pb = tv.get('pb', NaN)
    if (not nn(bvps) or bvps <= 0) and nn(tv_pb) and tv_pb > 0 and nn(price) and price > 0:
        bvps = price / tv_pb
    eps_g = NaN
    if nn(e0) and nn(e1) and e1 > 0:
        rel = (e0 - e1) / abs(e1)
        eps_g = rel * 100 if abs(rel) < 10 else NaN   # 🆕 v5.2: نمو من قاعدة EPS شبه صفرية (±1000%+) غير ذي معنى → «غير متاح»
    elif nn(f('earningsGrowth')):
        eps_g = f('earningsGrowth') * 100
    # نمو TTM مقابل آخر سنة مالية (أحدث من نمو السنة وحدها عند تأخر القوائم السنوية)
    eps_ttm_g = NaN
    if eps_src in ('TV-TTM', 'Yahoo-TTM', 'Quarterly-sum', 'Price/PE') and nn(e0) and e0 > 0 and nn(eps):
        g_ = (eps - e0) / e0 * 100
        eps_ttm_g = g_ if abs(g_) < 300 else NaN
    fcfm = NaN
    fcf, rev = _row_v(cf, ['Free Cash Flow']), _row_v(fin, ['Total Revenue', 'Operating Revenue'])
    if nn(fcf) and nn(rev) and rev > 0: fcfm = fcf / rev * 100
    elif nn(f('freeCashflow')) and nn(f('totalRevenue')) and f('totalRevenue') > 0: fcfm = f('freeCashflow') / f('totalRevenue') * 100
    if not nn(roe):
        ni, eq = _row_v(fin, ['Net Income']), _row_v(bs, ['Stockholders Equity', 'Total Equity Gross Minority Interest'])
        if nn(ni) and nn(eq) and eq > 0: roe = ni / eq * 100
    if not nn(roe) and nn(tv.get('roe', NaN)) and abs(tv['roe']) < 500: roe = float(tv['roe'])
    # ── القيمة السوقية: TradingView ← (السعر الحالي × الأسهم) عند انحراف ياهو >15% ← ياهو ──
    sh_impl, sh_out = f('impliedSharesOutstanding'), f('sharesOutstanding')
    sh = sh_impl if nn(sh_impl) and sh_impl > 0 else sh_out
    calc = price * sh if (nn(price) and price > 0 and nn(sh) and sh > 0) else NaN
    mcap, mcap_src = mcap_y, ('Yahoo' if nn(mcap_y) else '')
    tv_mc = tv.get('mcap', NaN)
    if pp.get('fvTvFund', True) and nn(tv_mc) and tv_mc > 0:
        mcap, mcap_src = float(tv_mc), 'TradingView'
        if nn(mcap_y) and abs(mcap_y / tv_mc - 1) > 0.15: flags.append('mcap_stale')
    elif nn(calc):
        if not nn(mcap_y): mcap, mcap_src = calc, 'Price×Shares'
        elif abs(mcap_y / calc - 1) <= 0.15: pass
        elif mcap_y < calc or nn(sh_impl): mcap, mcap_src = calc, 'Price×Shares'; flags.append('mcap_stale')
    # ── عائد التوزيعات من المعدل السنوي الفعلي ÷ السعر (كان يفترض صيغة كسر عشري ثابتة فتُضرب العوائد دون 1% في 100 خطأً) ──
    div_rate = f('trailingAnnualDividendRate'); dy_info = f('dividendYield'); dy_frac = f('trailingAnnualDividendYield'); div_r = f('dividendRate')
    if nn(div_rate) and nn(price) and price > 0:
        div_yield = div_rate / price * 100
    elif nn(div_r) and nn(price) and price > 0:
        div_yield = div_r / price * 100
    elif nn(dy_frac) and dy_frac > 0:
        div_yield = dy_frac * 100                                  # الكسر السنوي — دائماً كسر عشري
    elif nn(dy_info) and dy_info > 0:
        v_ = dy_info * 100 if dy_info <= 1 else dy_info            # 🆕 v6 (إصلاح 14): كشف تضاعف النسب —
        div_yield = v_ if v_ <= 35 else dy_info                    # نتائج أعلى من 35% تعني مضاعفة خاطئة فتُقرأ كما هي
    else:
        div_yield = NaN
    # 🆕 v5.2: كشف القطاع من الاسم الخام قبل التنظيف (ياهو يمسح أسماء بعض الأسواق لكن longName يبقى كاملًا: Commercial International Bank…)
    raw_name = str(info.get('shortName') or '') + ' ' + str(info.get('longName') or '')
    prof = sector_profile(info.get('sector') or '', info.get('industry') or '', raw_name)
    is_fin = bool(_FIN_RX.search(f"{info.get('sector') or ''} {info.get('industry') or ''} {raw_name}".lower()))
    an, an_hi, an_lo = f('targetMeanPrice'), f('targetHighPrice'), f('targetLowPrice')
    if not nn(an) and nn(tv.get('tgt', NaN)) and tv['tgt'] > 0: an, an_hi, an_lo = tv['tgt'], tv.get('tgt_hi', NaN), tv.get('tgt_lo', NaN)
    return dict(roe=roe, pio=piotroski(fin, bs, cf) if fin is not None else NaN,
                altman=altman_z(fin, bs, mcap) if fin is not None else NaN, beneish=beneish_m(fin, bs, cf) if fin is not None else NaN,
                eps_g=eps_g, eps=eps, bvps=bvps, fcfm=fcfm, mcap=mcap,
                analyst=an, analyst_hi=an_hi, analyst_lo=an_lo, analyst_n=f('numberOfAnalystOpinions'),
                div_yield=div_yield, beta=f('beta'),
                name=_clean_name(sym, info), sector=info.get('sector') or '', industry=info.get('industry') or '',
                currency=info.get('currency') or '', pe_info=pe_info, fwd_pe=f('forwardPE'), pb_info=pb_info,
                w52h=f('fiftyTwoWeekHigh'), w52l=f('fiftyTwoWeekLow'), altman_ok=prof['altman_ok'], fcf_ok=prof['fcf_ok'],
                eps_src=eps_src, eps_fwd=f('forwardEps'), eps_fy=float(e0) if nn(e0) else NaN, eps_ttm_g=eps_ttm_g, mcap_src=mcap_src,
                is_fin=is_fin, fm_flags=flags, tv_sector=str(tv.get('sector') or ''))

# 🆕 v6.4: مدخلات مضاعف جوردون لكل سوق — rf الفائدة الخالية من المخاطر % · g النمو الاسمي طويل الأجل % (= التضخم) · erp علاوة مخاطر السوق %.
# كلها تقديرات قابلة للتعديل وليست حقائق مطلقة. آخر مراجعة 2026-11-02: مصر — الفائدة 19% إيداع/20% إقراض (لجنة السياسة النقدية 24-9-2026)،
# التضخم 12.8% وطنياً و13.9% حضرياً (سبتمبر 2026)؛ السعودية — الريبو ≈ 4.5% والتضخم ≈ 1.8%. القيم أدناه هي المدخلات المقترحة (أكثر تحفظاً قليلاً).
# بالمدخلات الرسمية الحالية يصبح مضاعف مصر ≈ 10.1 والسعودية ≈ 13.2 — عدّل الجدول إن أردت.
FV_COE = {
    'US':   dict(rf=4.3,  g=2.5,  erp=5.0, gr=1.8),     # g = التضخم · gr = النمو الحقيقي طويل الأجل (≈ نمو الناتج الحقيقي) → النمو الاسمي = (1+g)(1+gr)−1 ≈ 4.4% → P/E ≈ 21 ⇒ يُقيَّد 20
    'TASI': dict(rf=5.5,  g=1.5,  erp=5.0, gr=3.0),     # → النمو الاسمي ≈ 4.5% → P/E ≈ 17.4
    'EGX':  dict(rf=20.0, g=12.0, erp=5.0, gr=4.0),     # → النمو الاسمي ≈ 16.5% → P/E ≈ 13.7  (v6.6 كان 8.6 بنمو حقيقي صفر) — شديد الحساسية للمدخلات الثلاثة
}
FV_PE_MIN, FV_PE_MAX = 5.0, 20.0
FV_GR_DEFAULT = 2.0              # 🆕 v7.0: النمو الحقيقي الافتراضي لسوق غير موجود في الجدول أو جدول قديم بلا gr
FV_COE_ASOF = '2026-11-12'      # 🆕 v6.5: تاريخ آخر مراجعة لمدخلات الجدول أعلاه
FV_COE_STALE_DAYS = 120          # 🆕 v6.5: بعدها يظهر تحذير مراجعة في سجل كل تشغيل
_FV_ACTIVE = {}                  # 🆕 v6.5: تجاوزات التشغيل الحالي (من الواجهة أو p_over) — يستخدمها نص المنهجية

def fv_params(mk, p=None):
    """🆕 v7.0: معاملات القيمة العادلة للسوق: r = rf+erp · النمو الاسمي g = (1+التضخم)(1+النمو الحقيقي)−1 (مقيّد ≤ r−4%) · المضاعف = (1+g)÷(r−g) بين 5 و20.
    يعيد None لسوق غير موجود في الجدول."""
    ov = ((p or {}).get('fvCoe') or {}).get(mk) or {}      # تجاوز من الواجهة/p_over (يمكن تحديد جزء من المفاتيح فقط)
    c = {**(FV_COE.get(mk) or {}), **ov}
    if not all(k in c for k in ('rf', 'g', 'erp')): return None
    r = (c['rf'] + c['erp']) / 100.0
    infl, gr = c['g'] / 100.0, float(c.get('gr', FV_GR_DEFAULT)) / 100.0
    g_nom = min((1 + infl) * (1 + gr) - 1, r - 0.04)
    pe = FV_PE_MAX if (r - g_nom) <= 0.005 else (1.0 + g_nom) / (r - g_nom)
    return dict(r=r, infl=infl, gr=gr, g_nom=g_nom, pe=float(min(FV_PE_MAX, max(FV_PE_MIN, pe))))

def market_fair_pe(mk, p=None):
    """مضاعف P/E العادل للسوق = (1+g)÷(r−g)، مقيّداً بين 5 و20. سوق غير موجود في الجدول → المضاعف المحايد."""
    prm = fv_params(mk, p)
    return float((p or {}).get('fvNeutralPE', 15.0)) if prm is None else prm['pe']

def _pe_table_txt(lang='ar'):
    names = {'US': ('US', 'أمريكا'), 'TASI': ('Saudi', 'السعودية'), 'EGX': ('Egypt', 'مصر')}
    i = 1 if lang == 'ar' else 0
    return ' · '.join(f"{names[k][i]} {market_fair_pe(k, {'fvCoe': _FV_ACTIVE}):.1f}×" for k in ('US', 'TASI', 'EGX'))

def fv_inputs_log(p, markets):
    """🆕 v6.5: سطور السجل: المضاعف المستخدم لكل سوق في هذا التشغيل + تحذير إن كان جدول FV_COE قديماً."""
    out = []
    if not p.get('fvMarketPE', True) or p.get('fvStyleLinkedPE', False): return out
    names = {'US': 'أمريكا', 'TASI': 'السعودية', 'EGX': 'مصر'}
    ms = [m for m in ('EGX', 'TASI', 'US') if m in markets]
    if not ms: return out
    ov = bool(p.get('fvCoe'))
    out.append('ℹ️ مضاعف P/E العادل المستخدم: ' + ' · '.join(f"{names[m]} {market_fair_pe(m, p):.1f}×" for m in ms) + ' — ' +
               ('مدخلات الفائدة/التضخم/النمو الحقيقي/العلاوة من الواجهة.' if ov else f'مدخلات جدول FV_COE بتاريخ {FV_COE_ASOF}.'))
    if not ov:
        try:
            age = (dt.date.today() - dt.date.fromisoformat(FV_COE_ASOF)).days
            if age > FV_COE_STALE_DAYS:
                out.append(f'⚠️ مدخلات الفائدة والتضخم عمرها {age} يوماً — راجعها في لوحة الإعدادات (القيمة العادلة) لأن مضاعف مصر شديد الحساسية لها.')
        except Exception:
            pass
    return out

def _fair_pe(style, p, mk=None):
    """🆕 v6.4: مضاعف P/E العادل. الأولوية: السلوك القديم المرتبط بالأسلوب إن طُلب (fvStyleLinkedPE) ← مضاعف السوق من FV_COE (fvMarketPE)
    ← المضاعف المحايد 15 (v6.3). في كل الحالات لا يتغير بتغير الأسلوب المقترح تلقائياً من حركة السعر (إلا بالسلوك القديم)."""
    if p.get('fvStyleLinkedPE', False):
        return 25.0 if style == 'Growth' else 12.0 if style == 'Value' else 18.0
    if p.get('fvMarketPE', True) and mk:
        return market_fair_pe(mk, p)
    return float(p.get('fvNeutralPE', 15.0))

def deep_analysis(fm, c, prevC, ema20, rsiV, atrV, style, p, mk=None):
    roe, pio, alt, ben, eg, eps, bv, fcf = (fm[k] for k in ('roe', 'pio', 'altman', 'beneish', 'eps_g', 'eps', 'bvps', 'fcfm'))
    # 🆕 v5.2: Altman وهامش FCF غير منطبقَين على قطاعات معيّنة (بنوك/تأمين/مرافق/عقار) — يُستبعدان من التقييم والأعلام لا أن يطلقا أحمراً زائفاً
    if p.get('sectorAware', True) and not fm.get('altman_ok', True): alt = NaN
    if p.get('sectorAware', True) and not fm.get('fcf_ok', True): fcf = NaN
    chg = 0 if (not nn(prevC) or prevC == 0) else (c - prevC) / prevC * 100
    pe = c / eps if (nn(eps) and eps > 0) else NaN; pb = c / bv if (nn(bv) and bv > 0) else NaN
    pts = sum(1 for x in (roe, pio, alt, ben, eg, eps, bv, fcf) if nn(x)); conf = pts / 8 * 100
    q = 50.0
    if nn(pio): q += 20 if pio >= 8 else 15 if pio >= 7 else 5 if pio >= 5 else -10 if pio >= 3 else -20
    if nn(roe): q += 15 if roe > 15 else 5 if roe > 8 else -10
    if nn(fcf): q += 15 if fcf > 10 else 10 if fcf > 5 else -15 if fcf < 0 else 0
    q = max(0, min(100, q))
    gr = 50.0
    if nn(eg): gr += 30 if eg > 20 else 20 if eg > 10 else 10 if eg > 0 else -20
    gr = max(0, min(100, gr))
    # 🆕 v6.6: مع pineParity مضاعف Deep حسب الأسلوب (12/18/25) كما في Pine وإلا مضاعف السوق (v6.4)
    fpe = (25.0 if style == 'Growth' else 12.0 if style == 'Value' else 18.0) if p.get('pineParity', True) else _fair_pe(style, p, mk)
    fv = eps * fpe if nn(eps) else NaN
    mos = (fv - c) / fv * 100 if (nn(fv) and fv > 0) else NaN
    vs = 50.0
    if nn(mos): vs += 30 if mos > 30 else 20 if mos > 10 else 10 if mos > 0 else -20
    if nn(pe): vs += 10 if pe < 15 else -20 if pe > 40 else 0
    if nn(pb): vs += 10 if pb < 1.5 else -10 if pb > 5 else 0
    vs = max(0, min(100, vs))
    risk = 0.0
    wk_scale = math.sqrt(5.0) if (style == 'Long Term' and not p.get('pineParity', True)) else 1.0   # 🆕 v5.2: ATR أسبوعي في أسلوب Long Term (🆕 v6.6: مع pineParity بلا معايرة كما في Pine)
    if nn(atrV): risk += (atrV / c * 100 / (p['riskHigh'] * wk_scale)) * 50
    risk += abs(chg) * 5; risk = max(0, min(100, risk))
    ent = 50.0
    if nn(ema20): ent += 15 if c > ema20 else -10
    if nn(rsiV): ent += -20 if rsiV > 70 else 15 if rsiV < 30 else 10
    ent += 10 if chg > 0 else -5; ent = max(0, min(100, ent))
    flags = (1 if (nn(alt) and alt < 1.8) else 0) + (1 if (nn(ben) and ben > -1.8) else 0)
    inv = (q + gr + vs) / 3
    if conf < 50: status = 'INSUFFICIENT_DATA'
    elif flags >= 2: status = 'AVOID'
    elif ent < 40: status = 'WAIT_ENTRY'
    elif inv >= 75 and ent >= 60: status = 'STRONG_BUY'
    elif inv >= 60: status = 'BUY_DIP'
    else: status = 'WATCHLIST'
    return dict(pe=pe, pb=pb, status=status, inv=inv, ent=ent, conf=conf, risk=risk, flags=flags, qual=q, growth=gr, valscore=vs, mos_radar=mos, fair_pe=fpe, fair_val_pe=fv)

DEC_TXT = {'STRONG_BUY': ('🟢 STRONG BUY', '🟢 شراء قوي'), 'BUY_DIP': ('🔵 BUY DIP', '🔵 شراء عند التراجع'),
           'WATCHLIST': ('🟡 WATCH', '🟡 مراقبة'), 'INSUFFICIENT_DATA': ('⚪ NO DATA', '⚪ بيانات ناقصة'),
           'WAIT_ENTRY': ('🟠 WAIT ENT', '🟠 انتظر الدخول'), 'AVOID': ('🔴 AVOID', '🔴 تجنّب')}
def align_code(tech, st):
    if st in (None, '—'): return 9
    good, bad = tech == '🟢 Conf', tech in ('🔴 No', '—')
    fg, fb = st in ('STRONG_BUY', 'BUY_DIP'), st == 'AVOID'
    if st == 'INSUFFICIENT_DATA': return 5
    if fg and good: return 2
    if fb and bad: return -2
    if (fg and bad) or (fb and good): return -1
    return 1
ALIGN_TXT = {2: ('✅ Full', '✅ توافق كامل'), 1: ('🟡 Partial', '🟡 جزئي'), -1: ('⚠️ Conflict', '⚠️ تعارض'),
             -2: ('⛔ Both Neg', '⛔ سلبي معاً'), 5: ('⚪ Tech only', '⚪ فني فقط'), 9: ('—', '—')}

# -----------------------------------------------------------------------------
# 8) القيمة العادلة + الدرجة الأساسية + اقتراح الأسلوب
# -----------------------------------------------------------------------------
def _fv_growth(fm):
    """🆕 v7.0: نمو الأرباح المتوقع (كسر عشري) = متوسط المتاح من: نمو EPS السنوي · نمو TTM مقابل آخر سنة · نمو EPS المتوقع — كلٌّ مقيّد −20%…+35%. None عند غياب كل المصادر."""
    gs = []
    for v in (fm.get('eps_g'), fm.get('eps_ttm_g')):
        if nn(v): gs.append(max(-0.20, min(0.35, v / 100.0)))
    e, ef = fm.get('eps'), fm.get('eps_fwd')
    if nn(e) and nn(ef) and e > 0 and ef > 0: gs.append(max(-0.20, min(0.35, ef / e - 1)))
    return float(np.mean(gs)) if gs else None

def _fv_quality(fm, p):
    """🆕 v7.0: عامل الجودة 0.80–1.10 (Piotroski · FCF · Altman · Beneish · ROE) — نفس منطق مؤشر Pine مع إضافة ROE."""
    q = 1.0
    pio, fcf, alt, ben, roe = fm.get('pio'), fm.get('fcfm'), fm.get('altman'), fm.get('beneish'), fm.get('roe')
    if p.get('sectorAware', True):
        if not fm.get('altman_ok', True): alt = NaN
        if not fm.get('fcf_ok', True): fcf = NaN
    if nn(pio): q += 0.05 if pio >= 8 else 0.03 if pio >= 7 else 0.0 if pio >= 5 else -0.05 if pio >= 3 else -0.10
    if nn(fcf): q += 0.03 if fcf > 10 else -0.05 if fcf < 0 else 0.0
    if nn(alt) and alt < 1.8: q -= 0.05
    if nn(ben) and ben > -1.8: q -= 0.05
    if nn(roe): q += 0.03 if roe >= 20 else -0.05 if roe < 5 else 0.0
    return max(0.80, min(1.10, q))

def fair_value(fm, price, style, tech_ref, p, ref_price=None, mk=None, rel=None, ext=None):
    """🆕 v7.0 — قيمة عادلة v2: مزيج مرجّح من نماذج مستقلة (P/E عادل بنمو وجودة · P/B بـROE · جراهام مُعايَر للسوق · جراهام-نمو حقيقي · مضاعف نسبي ·
    المحللون · هدف خارجي) + ثقة 0–100. وإن غابت البيانات المالية يُستخدم بديل فني محسوب (VPOC/WMA/SMA120).
    rel = dict(pe, n, scope) وسيط P/E للقطاع/السوق · ext = هدف خارجي يُدخله المستخدم."""
    eps, bv, an = fm['eps'], fm['bvps'], fm['analyst']
    an_n = fm.get('analyst_n', NaN)
    prm = fv_params(mk, p) if (p.get('fvMarketPE', True) and mk and not p.get('fvStyleLinkedPE', False)) else None
    fpe = _fair_pe(style, p, mk)                      # مضاعف السوق الأساسي (v6.3 محايد 15 · قديماً مرتبط بالأسلوب)
    infl = prm['infl'] if prm else 0.025
    g_nom = prm['g_nom'] if prm else 0.04
    r = prm['r'] if prm else 0.093
    g_co = _fv_growth(fm)
    g_eff = g_nom if g_co is None else g_nom + p.get('fvGrowthW', 0.5) * (g_co - g_nom)
    prem = max(-0.15, min(0.30, (g_eff - g_nom) * 1.5))            # علاوة/خصم النمو على المضاعف الأساسي
    peLo = min(FV_PE_MIN, fpe)
    pe_fair = max(peLo, min(float(p.get('fvPeHardCap', 25.0)), fpe * (1 + prem)))
    q = _fv_quality(fm, p)
    models = {}
    if nn(eps) and eps > 0: models['pe'] = eps * pe_fair * q
    if nn(eps) and eps > 0 and nn(bv) and bv > 0:
        k = 22.5 * (fpe / 15.0) if p.get('fvGrahamScale', True) else 22.5       # رقم جراهام الأصلي = 15 × 1.5 (مضاعف أمريكا) → يُعايَر لمضاعف السوق
        models['graham'] = math.sqrt(k * eps * bv)
    if nn(eps) and eps > 0:
        g_real = 0.0 if g_co is None else max(0.0, min(15.0, ((1 + g_co) / (1 + infl) - 1) * 100))   # النمو الحقيقي بعد خصم التضخم (صيغة جراهام مصمّمة لنمو حقيقي)
        models['grahamG'] = eps * (8.5 * fpe / 15.0 + 2 * g_real)
    roe_use = fm['roe'] / 100.0 if nn(fm.get('roe')) else ((eps / bv) if (nn(eps) and nn(bv) and bv > 0) else NaN)
    if nn(bv) and bv > 0 and nn(roe_use):
        pbf = max(min(p.get('fvPbMin', 0.5), p.get('fvPbMax', 4.0)), min(p.get('fvPbMax', 4.0), (roe_use - g_nom) / (r - g_nom)))
        models['pb'] = bv * pbf * q
    rel_pe = NaN
    if p.get('fvRelOn', True) and rel and nn(rel.get('pe')) and rel['pe'] > 0 and nn(eps) and eps > 0:
        rel_pe = float(rel['pe']) * q
        models['rel'] = eps * rel_pe
    if nn(an) and an > 0: models['analyst'] = an
    # حارس: استبعاد النماذج أقل من نصف السعر أو أكثر من 2.5 ضعفه — يُستثنى الهدف الخارجي (قرار المستخدم)
    glo, ghi = p.get('fvGuardLo', 0.5), p.get('fvGuardHi', 2.5)
    if p.get('fvGuardScaleLo', True) and not p.get('fvStyleLinkedPE', False):
        glo = glo * min(1.0, fpe / float(p.get('fvNeutralPE', 15.0)))
    lo_a = min(price, ref_price) if (ref_price is not None and nn(ref_price) and ref_price > 0) else price
    hi_a = max(price, ref_price) if (ref_price is not None and nn(ref_price) and ref_price > 0) else price
    models = {k: v for k, v in models.items() if price > 0 and glo * lo_a <= v <= ghi * hi_a}
    if nn(ext) and ext > 0: models['ext'] = float(ext)
    names = {'pe': 'P/E', 'pb': 'P/B', 'graham': 'Graham', 'grahamG': 'Graham-G', 'rel': 'Relative', 'analyst': 'Analysts', 'ext': 'External'}
    order = ['pe', 'pb', 'graham', 'grahamG', 'rel', 'analyst', 'ext']
    conf, low, high = 0.0, NaN, NaN
    if models:
        wtab = {**P['fvW'], **(p.get('fvW') or {})} if not fm.get('is_fin') else {**P['fvWFin'], **(p.get('fvWFin') or {})}
        w = {}
        for k in models:
            # هدف محلل واحد لا يستحق وزن 25% — يُخفّض إلى 10% (كان 4280 و4090 يُقيَّمان بهدف واحد)
            w[k] = p.get('fvSingleAnalystW', 0.10) if (k == 'analyst' and nn(an_n) and an_n <= 1) else float(wtab.get(k, 0.1))
        sw = sum(w.values())
        if sw <= 0: w = {k: 1.0 for k in models}; sw = float(len(models))
        fair = sum(models[k] * w[k] for k in models) / sw; src = 'Fundamental'   # 🆕 v6: توكن موحّد يُترجم للعرض (مالي/Fundamental)
        used = ' + '.join(names[k] for k in order if k in models)
        if 'ext' in models: src = 'External+Fundamental' if len(models) > 1 else 'External'
        # الثقة: عدد النماذج المستقلة + اكتمال البيانات − تباعد النماذج − الخسائر (مطابقة منطق Pine)
        indep = [k for k in ('pe', 'pb', 'graham', 'grahamG', 'rel') if k in models]
        base_c = 60.0 if len(indep) >= 3 else 50.0 if len(indep) == 2 else 35.0 if len(indep) == 1 else 20.0
        if 'analyst' in models or 'ext' in models: base_c += 10.0
        pts = sum(1 for k_ in ('roe', 'pio', 'altman', 'beneish', 'eps_g', 'eps', 'bvps', 'fcfm') if nn(fm.get(k_)))
        vals = [models[k] for k in models if k != 'ext']
        disp_ = (max(vals) - min(vals)) / (sum(vals) / len(vals)) if len(vals) >= 2 else 0.0
        conf = base_c + (pts / 8 * 100) * 0.3 - min(25.0, disp_ * 20.0) - (15.0 if (nn(eps) and eps <= 0) else 0.0) - (5.0 if fm.get('eps_src') == 'FY' else 0.0)
        if 'ext' in models: conf = max(conf, 70.0)
        conf = max(0.0, min(100.0, conf))
        prim = [models[k] for k in ('pe', 'rel', 'analyst', 'ext') if k in models] or list(models.values())
        low, high = float(min(prim)), float(max(prim))
    else:
        refs = [x for x in tech_ref if nn(x) and x > 0]
        fair = float(np.mean(refs)) if refs else NaN; src = 'Technical estimate'; used = 'VPOC/WMA/SMA120' if refs else '—'
        conf = 25.0 if refs else 0.0
    up = (fair - price) / price * 100 if nn(fair) and price > 0 else NaN        # فرق النسبة عن السعر
    mos = (fair - price) / fair * 100 if nn(fair) and fair > 0 else NaN         # أسلوب Radar
    bd, db = p.get('fvBand', 15.0), p.get('fvDeepBand', 30.0)
    verdict = ('N/A' if not nn(up) else 'Deep Value' if up >= db else 'Undervalued' if up >= bd else 'Fair' if up > -bd else 'Overvalued' if up > -db else 'Rich')   # 🆕 v7.0: مطابق لرموز Pine (±15 / ±30)
    return dict(fair=fair, upside=up, mos=mos, verdict=verdict, source=src, used=used,
                pe_model=models.get('pe', NaN), graham=models.get('graham', NaN), grahamG=models.get('grahamG', NaN), analyst=models.get('analyst', NaN), pe_x=pe_fair,
                pb_model=models.get('pb', NaN), rel_model=models.get('rel', NaN), ext_model=models.get('ext', NaN), rel_pe=rel_pe, conf=conf, low=low, high=high,
                base_pe=fpe, growth=(NaN if g_co is None else g_co * 100.0), quality=q)

def base_engine(df, bench_df, p):
    """درجة الكود الأصلي (BUY Score) + اقتراح نوع الاستثمار."""
    c = df['Close']; close = float(c.iloc[-1])
    e20, e50 = s_ema(c, 20).iloc[-1], s_ema(c, 50).iloc[-1]      # 🆕 v6.6: نفس EMA في Pine (بذر SMA) بدل ewm(adjust=True)
    e200 = s_ema(c, 200).iloc[-1] if len(c) >= 200 else e50
    trend = (close > e20) * 33.3 + (e20 > e50) * 33.3 + (e50 > e200) * 33.3
    # 🆕 v5.2: RSI(14) بطريقة Wilder — كان هنا متوسط بسيط فيختلف الرقم عن عمود rd_rsi لنفس السهم
    rsi = float(s_rsi(c, 14).iloc[-1]) if len(c) >= 15 else 50.0
    mom = 100 if 50 <= rsi <= 70 else (60 if rsi > 70 else 30)
    cmf = float(s_cmf(df, 20).iloc[-1]) if (len(df) > 25 and float(np.nansum(df['Volume'])) > 0) else NaN
    vol_avg = df['Volume'].rolling(20).mean().iloc[-1]; vol_ratio = df['Volume'].iloc[-1] / (vol_avg + 1e-9) if (nn(vol_avg) and float(np.nansum(df['Volume'])) > 0) else NaN
    ret = (c.iloc[-1] - c.iloc[-20]) / c.iloc[-20] * 100 if len(c) > 20 else 0.0
    bm_ret = 0.0
    if bench_df is not None and len(bench_df) > 20:
        bc = bench_df['Close']; bm_ret = (bc.iloc[-1] - bc.iloc[-20]) / bc.iloc[-20] * 100
    rs = float(np.clip((ret - bm_ret) * 2 + 50, 0, 100))
    if nn(cmf):   # 🆕 v6 (إصلاح 3): بلا حجم يُعاد توزيع وزن CMF على بقية المكونات بدل خسارة 25 نقطة
        buy = trend * 0.25 + mom * 0.25 + rs * 0.25 + (1 if cmf > 0 else 0) * 100 * 0.25
    else:
        buy = trend * (1 / 3) + mom * (1 / 3) + rs * (1 / 3)
    if buy >= 75: rating, dec = 'A+ (Strong Buy)', 'STRONG BUY'
    elif buy >= 60: rating, dec = 'B+ (Buy Dip)', 'BUY DIP'
    elif buy >= 45: rating, dec = 'C (Neutral)', 'WATCH / WAIT'
    else: rating, dec = 'D (Avoid)', 'AVOID'
    w = df.tail(126)
    vol = float(w['Close'].pct_change().std() * np.sqrt(252) * 100)
    if vol > 35 and vol_ratio > 1.5: style = ('⚡ مضاربة سريعة (Swing)', 'Swing')
    elif trend >= 66 and nn(cmf) and cmf > 0.05: style = ('📈 نمو (Growth)', 'Growth')
    elif rsi < 45 and nn(cmf) and cmf > 0: style = ('💰 قيمة (Value)', 'Value')
    elif trend >= 66: style = ('📊 مدى متوسط (Medium Term)', 'Medium Term')
    else: style = ('🏛️ مدى طويل (Long Term)', 'Long Term')
    wv = ((w['Close'] * w['Volume']).cumsum() / w['Volume'].cumsum().replace(0, np.nan)).iloc[-1]
    return dict(score=float(buy), rating=rating, decision=dec, style_label=style[0], style=style[1], trend=float(trend), cmf=cmf, rsi=rsi,
                rs=rs, vwap_pos='Above' if close > wv else 'Below', support=float(df['Low'].tail(20).min()), resistance=float(df['High'].tail(20).max()),
                vol_ann=vol, vol_ratio=float(vol_ratio) if nn(vol_ratio) else NaN)


# -----------------------------------------------------------------------------
# 9) الأطر الزمنية (MTF) + الدعم/المقاومة + RS + الارتباط
# -----------------------------------------------------------------------------
def _month_rule():
    try:
        pd.Series([1], index=pd.to_datetime(['2024-01-31'])).resample('ME').last(); return 'ME'
    except Exception:
        return 'M'

def ema_sma_state(df, p):
    if df is None or len(df) < p['smaSlow'] + 2: return None
    e, s_ = s_ema(df['Close'], p['emaFast']).iloc[-1], s_sma(df['Close'], p['smaSlow']).iloc[-1]
    if not (nn(e) and nn(s_)): return None
    return 1 if e > s_ else -1 if e < s_ else 0

def dots(vals):
    return ''.join('⚪' if x is None else '🟢' if x == 1 else '🔴' if x == -1 else '⚪' for x in vals)

def mtf_info(sym, df, intraday, p, bias, mo_df=None):
    out = dict(mode='PROXY', frames=[], nets=[], h1=None, h2=None)
    d15 = intraday.get('15m', {}).get(sym) if intraday else None
    d30 = intraday.get('30m', {}).get(sym) if intraday else None
    d60 = intraday.get('60m', {}).get(sym) if intraday else None
    have_intra = d60 is not None and len(d60) > 40
    if have_intra:
        d240 = resample_ohlc(d60, '4h') if len(d60) > 80 else None
        out['mode'] = 'INTRADAY'; out['frames'] = ['M15', 'M30', 'H1', 'H4', 'D1']
        out['nets'] = [frame_net(d15, p), frame_net(d30, p), frame_net(d60, p), frame_net(d240, p), frame_net(df, p)]
        out['h1'], out['h2'] = ema_sma_state(d60, p), ema_sma_state(d240, p)
        n4, n5 = out['nets'][3], out['nets'][4]
    else:
        wk = resample_ohlc(df, 'W-FRI')
        # 🆕 v5.2: بيانات شهرية حقيقية (10 سنوات) عند توفرها — كان إطار M1 يتطلب 34 شهرًا من سنتين فقط فيبقى ⚪ دائمًا
        mo = mo_df if (mo_df is not None and len(mo_df) >= 34) else resample_ohlc(df, _month_rule())
        out['frames'] = ['D1', 'W1', 'M1']
        out['nets'] = [frame_net(df, p), frame_net(wk, p), frame_net(mo, p)]
        out['h1'], out['h2'] = ema_sma_state(df, p), ema_sma_state(wk, p)       # بدائل H1/H4 : D1/W1
        n4, n5 = out['nets'][1], out['nets'][2]
    out['matrix'] = dots(out['nets'])
    if bias == 0: lab = '⚪ Neutral'
    elif n4 == bias and n5 == bias:
        # 🆕 v5.2: وسم التأكيد يوضح اتجاهه (كان يظهر 🚀 حتى لو كان التأكيد هابطًا)
        lab = '🚀 STRONG CONFIRMED' if bias == 1 else '🚀 STRONG CONFIRMED ↓'
    elif n5 not in (None, 0) and n5 != bias: lab = '⚠️ AGAINST TREND'
    else: lab = '🔸 MIXED'
    out['label'] = lab
    out['avail'] = out['h1'] is not None and out['h2'] is not None
    out['buy_ok'] = (not p['requireHTF']) or (out['avail'] and out['h1'] == 1 and out['h2'] == 1)
    out['sell_ok'] = (not p['requireHTF']) or (out['avail'] and out['h1'] == -1 and out['h2'] == -1)
    return out

def hist_htf_arrays(df, p):
    """بديل تاريخي لفلتر H1/H4 في المحاكاة: اتجاه آخر أسبوع *مكتمل* قبل شمعة كل يوم.
    🆕 v5.2: كان الالتقاط عبر shift(1) + ffill يجعل شموع الاثنين–الخميس تأخذ حالة أسبوعين ماضيين؛
    الآن كل يوم يُحمَّل على جمعة الأسبوع السابق مباشرة (آخر أسبوع مكتمل فعلاً)."""
    if not p['requireHTF']: return None, None
    wk = resample_ohlc(df, 'W-FRI')
    e, s_ = s_ema(wk['Close'], p['emaFast']), s_sma(wk['Close'], p['smaSlow'])
    stt = pd.Series(np.where(e > s_, 1, np.where(e < s_, -1, 0)), index=wk.index).where(e.notna() & s_.notna())
    idx = pd.DatetimeIndex(df.index)
    prev_fri = (idx + pd.offsets.Week(weekday=4)) - pd.Timedelta(days=7)   # جمعة الأسبوع السابق (المكتمل)
    al = stt.reindex(prev_fri).ffill()
    al.index = idx
    return (al == 1).values, (al == -1).values

def auto_sr(df, p, price):
    """🆕 v6.6: محاكاة تسلسلية مطابقة لـPine — قائمة من 5 (الأحدث أولاً) + حذف المستوى عند كسره بالإغلاق."""
    h, l, c = df['High'].values, df['Low'].values, df['Close'].values
    n = len(c); k = p['srPivot']
    PH, PL = pivots(h, l, k)
    res, sup = [], []
    for i in range(n):
        if nn(PH[i]): res.insert(0, float(PH[i])); del res[p['srMax']:]
        if nn(PL[i]): sup.insert(0, float(PL[i])); del sup[p['srMax']:]
        res = [x for x in res if not c[i] > x]
        sup = [x for x in sup if not c[i] < x]
    above = [x for x in res if x > price]; below = [x for x in sup if x < price]
    return (min(above) if above else NaN), (max(below) if below else NaN), res[::-1], sup[::-1]

def rs_multi(df, bdf):
    out = {}
    if bdf is None or len(bdf) < 30: return dict(label='⚪ N/A', detail='—', vals={})
    c, b = df['Close'], bdf['Close']; vals = {}
    for nm, k in (('1M', 21), ('3M', 63), ('6M', 126), ('12M', 252)):
        if len(c) > k and len(b) > k:
            vals[nm] = (c.iloc[-1] / c.iloc[-1 - k] - 1) * 100 - (b.iloc[-1] / b.iloc[-1 - k] - 1) * 100
    if not vals: return dict(label='⚪ N/A', detail='—', vals={})
    outp = sum(1 for x in vals.values() if x > 0)
    lab = ('🟢 Stronger' if outp >= math.ceil(len(vals) / 2) else '🔴 Weaker')
    det = '  '.join(f"{k}:{'+' if v >= 0 else ''}{v:.1f}%" for k, v in vals.items())
    return dict(label=lab, detail=det, vals=vals)


# -----------------------------------------------------------------------------
# 10) القرار الموحّد + خطة الدخول + الحالة العامة للسوق + أهداف فيبوناتشي + الشرح (جديد v5.0)
# -----------------------------------------------------------------------------
# 🆕 تصنيف حالة المؤشر العام (Benchmark) الذي يتبعه السهم:
#    تصاعد / هبوط / تصحيح / ارتداد غير مؤكد / انهيار / عرضي — يُحسب من نفس بيانات المرجع بلا طلبات إضافية
MKT_TXT = {
    'uptrend':    ('🟢 Uptrend', '🟢 تصاعد'),
    'downtrend':  ('🔴 Downtrend', '🔴 هبوط'),
    'correction': ('🔻 Correction', '🔻 تصحيح'),
    'rebound':    ('↗ Rebound (unconfirmed)', '↗ ارتداد غير مؤكد'),
    'crash':      ('🩸 Collapse', '🩸 انهيار'),
    'bear':       ('🐻 Bear market', '🐻 سوق هابط'),
    'recovery':   ('🔵 Recovery', '🔵 تعافٍ'),
    'range':      ('⚪ Range / sideways', '⚪ عرضي (تذبذب)'),
    'na':         ('⚪ N/A', '⚪ غير متاح'),
}

def market_class(bm, p):
    """تصنيف حالة السوق العام من مقاييس المرجع المحسوبة في bench_metrics (🆕 v7.0: يعتمد المراحل المؤسسية)."""
    if not bm:
        return 'na'
    if nn(bm.get('dd')) and bm['dd'] <= p.get('fibMktDDCrash', -15.0):
        return 'crash'
    ph = bm.get('phase', 0)
    if ph == 6: return 'crash'
    if ph == 5: return 'bear'
    if ph == 4: return 'correction'
    if ph == 7: return 'recovery'
    if bm.get('state') == 3:
        return 'correction' if ph != 3 else 'downtrend'
    if bm.get('rebound'):
        return 'rebound'
    if bm.get('state') == 2:
        return 'downtrend'
    if bm.get('state') == 1:
        return 'uptrend' if (nn(bm.get('vs50')) and bm['vs50'] > 0) else 'range'
    return 'na'

# 🆕 أهداف فيبوناتشي: امتدادات آخر موجة مؤكدة (قاع→قمة أو قمة→قاع) على إطار الأسلوب.
#    إذا كان السعر قد تجاوز امتدادات الموجة الأخيرة يُعاد الحساب على مدى 52 أسبوع (أهداف طويلة 30-100%+).
FIB_MULT = {'Swing': (1.272, 1.618, 2.000), 'Growth': (1.272, 1.618, 2.000),
            'Medium Term': (1.272, 1.618, 2.000), 'Value': (1.272, 1.618, 2.618),
            'Long Term': (1.272, 1.618, 2.618)}

def fib_targets(df, style, p, price, w52h, w52l):
    """🆕 v5.1: أهداف فيبوناتشي للمستثمر.
    المنهج: تُقاس آخر موجة كبرى صاعدة (أدنى قاع → أعلى قمة داخل نافذة الأسلوب الموسّعة)،
    وتُطلق الامتدادات (1.272 / 1.618 / 2.0-2.618 حسب الأسلوب) من قاع التصحيح بعد القمة
    (أو من السعر الحالي إن كانت القمة حديثة بلا تصحيح). وإن كان السعر قد تجاوز أكبر امتداد
    يُعاد الحساب على مدى 52 أسبوعاً كي تظهر أهداف 30-100%+ المناسبة للاستثمار متوسط/طويل الأجل.
    """
    sp = style_params(style, p)
    d = to_tf(df, sp['tf'])
    if d is None or len(d) < 60 or not (nn(price) and price > 0):
        return None
    h, l = d['High'].values, d['Low'].values
    n = len(h)
    invest_style = style in ('Value', 'Medium Term', 'Long Term')
    look = min(max(sp['lb'], 120 if invest_style else 60), n - 1)
    H_i = int(np.argmax(h[n - look:])) + (n - look)
    H = float(h[H_i])
    L = float(np.min(l[max(0, H_i - look):H_i + 1]))
    rng = H - L
    if not (rng > 0) or rng < price * 0.03:
        return None
    # قاع التصحيح بعد القمة (أو السعر نفسه إن كانت القمة حديثة)
    if H_i < n - 1:
        base = float(np.min(l[H_i:]))
    else:
        PH, PL = pivots(h, l, 3)
        pls = [float(x) for x in PL if nn(x)]
        base = pls[-1] if (pls and price > pls[-1] > L) else price
    if base > price:
        base = price          # لا نُطلق الأهداف من فوق السعر الحالي
    m1, m2, m3 = FIB_MULT.get(style, (1.272, 1.618, 2.0))
    use52 = False
    # موجة ضيقة (سهم عرضي) → مدى 52 أسبوع حتى تظهر أهداف ذات معنى للمستثمر
    if rng < price * 0.10 and nn(w52h) and nn(w52l) and (w52h - w52l) > rng * 1.2:
        use52 = True
        rng = float(w52h - w52l)
        base = float(price)
    tgts = [base + m1 * rng, base + m2 * rng, base + m3 * rng]
    if not use52 and price >= tgts[1] * 0.999:   # السعر تجاوز امتداد 1.618 → مدى 52 أسبوع (أهداف أطول)
        use52 = True
        if nn(w52h) and nn(w52l) and (w52h - w52l) > 0:
            rng = float(w52h - w52l)
            base = float(price)
            tgts = [base + m1 * rng, base + m2 * rng, base + m3 * rng]
    out = [t for t in tgts if t > price * 1.005]
    if not out:
        return None
    mults = {1: m1, 2: m2, 3: m3}
    res = dict(fib_src=('52W' if use52 else 'SW'), fib_lo=L, fib_hi=H, fib_n=min(len(out), 3))
    for i, t in enumerate(out[:3], 1):
        res[f'fib_t{i}'] = float(t)
        res[f'fib_p{i}'] = (t - price) / price * 100
        res[f'fib_m{i}'] = mults[i]   # 🆕 v5.2: معامل كل هدف يُخزَّن معه فلا تنزاح التسمية عند حذف هدف أدنى من السعر
    return res

# 🆕 تعريب الأسباب (Reasons) والعوائد
REASON_TXT = {
    'trend':   ('Trend↑', 'اتجاه صاعد'), 'rs': ('RS+', 'قوة نسبية موجبة'), 'cmf': ('CMF+', 'تدفق أموال موجب'),
    'crash':   ('⚠️ Crash', '⚠️ انهيار حاد'), 'break': ('⚠️ Break', '⚠️ كسر بنية'), 'dip': ('🔻 Dip?', '🔻 تراجع محتمل'),
    'vol':     ('Vol+', 'حجم مرتفع'), 'nearsup': ('NearSup', 'قرب الدعم'), 'accum': ('Accum', 'تجميع'),
    'adx':     ('ADX+', 'اتجاه قوي'), 'choppy': ('Choppy', 'تذبذب بلا اتجاه'), 'bblow': ('BB-Low', 'تشبع بيعي'),
    'bbhigh':  ('BB-High', 'تشبع شرائي'), 'gapup': ('GapUp', 'فجوة صاعدة'), 'gapdn': ('GapDn', 'فجوة هابطة'),
    'lowliq':  ('LowLiq', 'سيولة منخفضة'), 'nodataopen': ('⚠ Open data?', '⚠ بيانات الفتح ناقصة من المزود'),
    'novol':   ('NoVol', 'بلا حجم تداول (فوركس/مؤشر)'), 'limdata': ('ShortHist', 'تاريخ أقل من 200 شمعة'),
}
RISK_TXT = {'low': ('🟢 Low risk', '🟢 مخاطرة منخفضة'), 'medium': ('🟡 Medium risk', '🟡 مخاطرة متوسطة'), 'high': ('🔴 High risk', '🔴 مخاطرة عالية')}

def fmt_reasons(tags, risk_key, lang):
    ar = lang == 'عربي'
    parts = [REASON_TXT[t][1 if ar else 0] for t in (tags or []) if t in REASON_TXT]
    if risk_key in RISK_TXT:
        parts.append(RISK_TXT[risk_key][1 if ar else 0])
    return ' · '.join(parts) if parts else '—'

# 🆕 v6 (إصلاح 10): رموز ملاحظات القرار (تُترجم للعرض مثل تصميم v2.0) — الحارس بأربعة أسباب
NOTE_CODE = {'N_FLAGS': ('red financial flags', 'أعلام مالية حمراء'),
             'N_OVERVALUED': ('price above fair value', 'السعر أعلى من القيمة العادلة'),
             'N_GUARD_MKT': ('guard: market correction', 'الحارس: السوق في تصحيح'),
             'N_GUARD_RISK': ('guard: high deep risk', 'الحارس: مخاطرة عميقة مرتفعة'),
             'N_GUARD_CHASE': ('guard: candle chasing', 'الحارس: مطاردة شمعة'),
             'N_GUARD_TECH': ('guard: tech not confirmed', 'الحارس: التأكيد الفني غير مكتمل'),
             'N_TECH_SELL': ('technical sell signal', 'إشارة بيع فنية'),
             'N_SELL_VS_SCORE': ('sell signal tempered by high unified score', 'إشارة بيع خُفِّضت لارتفاع الدرجة الموحدة')}

# 🆕 قواميس الترجمة الكاملة لكل قيم النتائج (إنجليزي | عربي)
TR = {
 'rd_tech': {'🟢 Conf': ('🟢 Confirmed', '🟢 مؤكد'), '🟡 Dev': ('🟡 Developing', '🟡 يتطور'), '🔴 No': ('🔴 Weak', '🔴 ضعيف'), '—': ('—', '—')},
 'rd_rating': {'🟢 Strong Inv.': ('🟢 Strong investment', '🟢 استثمار قوي'), '🔵 High Pot.': ('🔵 High potential', '🔵 إمكانات عالية'),
               '🟡 Watchlist': ('🟡 Watchlist', '🟡 مراقبة'), '🟠 Weak Str.': ('🟠 Weak structure', '🟠 بنية ضعيفة'),
               '🔴 Avoid': ('🔴 Avoid', '🔴 تجنّب'), '⚪ N/A': ('⚪ N/A', '⚪ غير متاح')},
 'rd_risk': {'🟢 Low': ('🟢 Low', '🟢 منخفضة'), '🟡 Medium': ('🟡 Medium', '🟡 متوسطة'), '🔴 High': ('🔴 High', '🔴 عالية')},
 'dp_status': {'STRONG_BUY': ('🟢 STRONG BUY', '🟢 شراء قوي'), 'BUY_DIP': ('🔵 BUY DIP', '🔵 شراء عند التراجع'),
               'WATCHLIST': ('🟡 WATCH', '🟡 مراقبة'), 'INSUFFICIENT_DATA': ('⚪ NO DATA', '⚪ بيانات ناقصة'),
               'WAIT_ENTRY': ('🟠 WAIT ENTRY', '🟠 انتظر الدخول'), 'AVOID': ('🔴 AVOID', '🔴 تجنّب'), '—': ('—', '—')},
 'dp_align': {2: ('✅ Full', '✅ توافق كامل'), 1: ('🟡 Partial', '🟡 جزئي'), -1: ('⚠️ Conflict', '⚠️ تعارض'),
              -2: ('⛔ Both negative', '⛔ سلبي معاً'), 5: ('⚪ Tech only', '⚪ فني فقط'), 9: ('—', '—')},
 'uni_decision': {'STRONG BUY': ('🟢 STRONG BUY', '🟢 شراء قوي'), 'BUY DIP': ('🔵 BUY DIP', '🔵 شراء عند التراجع'),
                  'WATCH': ('🟡 WATCH', '🟡 مراقبة'), 'AVOID': ('🔴 AVOID', '🔴 تجنّب'), 'SELL': ('🔴 SELL / AVOID', '🔴 بيع / تجنّب')},
 'uni_signal': {'STRONG BUY': ('Strong buy signal', 'إشارة شراء قوية'), 'BUY DIP': ('Technical buy signal', 'إشارة شراء فنية'),
                'WATCH': ('Watch', 'مراقبة'), 'AVOID': ('Avoid', 'تجنّب'), 'SELL': ('Sell signal', 'إشارة بيع')},
 'px_final': {'IN TRADE': ('Running virtual trade', 'صفقة افتراضية جارية'), 'ENTRY BUY': ('Buy signal now', 'إشارة شراء الآن'),
              'ENTRY SELL': ('Sell signal now', 'إشارة بيع الآن'), 'WATCH': ('Watch', 'مراقبة'), 'WAIT': ('Wait', 'انتظار'),
              'NO TRADE': ('No trade', 'لا تداول')},
 'px_signal': {'BUY': ('BUY', 'شراء'), 'SELL': ('SELL', 'بيع'), 'None': ('—', '—')},
 'px_regime': {'🚀 Strong Trend': ('🚀 Strong trend', '🚀 اتجاه قوي'), '🌊 Choppy': ('🌊 Choppy', '🌊 متذبذب'), '😴 Calm': ('😴 Calm', '😴 هادئ')},
 'px_state': {'🔥 High Activity': ('High activity', 'نشاط عالٍ'), '💤 Low Liquidity': ('Low liquidity', 'سيولة ضعيفة'),
              '⚖️ Normal Activity': ('Normal activity', 'نشاط طبيعي'), '⚪ N/A': ('N/A', 'غير متاح')},
 'px_struct_conf': {'Bullish': ('Bullish', 'صاعد'), 'Bearish': ('Bearish', 'هابط'), 'Neutral': ('Neutral', 'محايد')},
 'px_struct_live': {'Bullish': ('Bullish', 'صاعد'), 'Bearish': ('Bearish', 'هابط'), 'Neutral': ('Neutral', 'محايد')},
 'px_zone_txt': {'🔴 Premium': ('🔴 Premium', '🔴 مرتفع'), '🟢 Discount': ('🟢 Discount', '🟢 منخفض'), '🟡 Equilibrium': ('🟡 Equilibrium', '🟡 توازن')},
 'px_near': {'No Nearby Zones': ('No nearby zones', 'لا مناطق قريبة'), '🟦OB↑': ('🟦 OB↑ demand', '🟦 تجميع صاعد'),
             '🟪OB↓': ('🟪 OB↓ supply', '🟪 تجميع هابط'), '🟢FVG↑': ('🟢 FVG↑', '🟢 فجوة صاعدة'), '🟠FVG↓': ('🟠 FVG↓', '🟠 فجوة هابطة')},
 'px_sweep': {'Bull Sweep': ('Bull sweep', 'اصطياد سيولة صاعد'), 'Bear Sweep': ('Bear sweep', 'اصطياد سيولة هابط'), 'None': ('None', 'لا يوجد')},
 'px_div': {'Bull Div': ('Bullish divergence', 'دايفرجنس صاعد'), 'Bear Div': ('Bearish divergence', 'دايفرجنس هابط'), 'None': ('None', 'لا يوجد')},
 'px_squeeze': {'⚠️ Active Squeeze': ('⚠️ Active squeeze', '⚠️ انكماش نشط'), 'Release': ('Release', 'انفلات'), 'Normal': ('Normal', 'طبيعي')},
 'px_mtf_label': {'🚀 STRONG CONFIRMED': ('🚀 Strong confirmed (bullish)', '🚀 تأكيد قوي صاعد'), '🚀 STRONG CONFIRMED ↓': ('🚀 Strong confirmed (bearish)', '🚀 تأكيد قوي هابط'), '⚠️ AGAINST TREND': ('⚠️ Against trend', '⚠️ ضد الاتجاه'),
                  '🔸 MIXED': ('🔸 Mixed', '🔸 متباين'), '⚪ Neutral': ('⚪ Neutral', '⚪ محايد')},
 'px_st_dir': {'🟢 Up': ('🟢 Up', '🟢 صاعد'), '🔴 Down': ('🔴 Down', '🔴 هابط')},
 'px_rs_label': {'🟢 Stronger': ('🟢 Stronger', '🟢 أقوى'), '🔴 Weaker': ('🔴 Weaker', '🔴 أضعف'), '⚪ N/A': ('⚪ N/A', '⚪ غير متاح')},
 'px_vwap': {'🟢 Above': ('🟢 Above', '🟢 فوق'), '🔴 Below': ('🔴 Below', '🔴 تحت'), '⚪': ('⚪', '⚪')},
 'base_decision': {'STRONG BUY': ('Strong buy', 'شراء قوي'), 'BUY DIP': ('Buy dip', 'شراء عند التراجع'),
                   'WATCH / WAIT': ('Watch / Wait', 'مراقبة / انتظار'), 'AVOID': ('Avoid', 'تجنّب')},
 'base_rating': {'A+ (Strong Buy)': ('A+ (Strong buy)', 'A+ (شراء قوي)'), 'B+ (Buy Dip)': ('B+ (Buy dip)', 'B+ (شراء عند التراجع)'),
                 'C (Neutral)': ('C (Neutral)', 'C (محايد)'), 'D (Avoid)': ('D (Avoid)', 'D (تجنّب)')},
 'fv_verdict': {'رخيص (Undervalued)': ('Undervalued', 'رخيص'), 'عادل (Fair)': ('Fair', 'عادل'),
                'مرتفع (Overvalued)': ('Overvalued', 'مرتفع'), 'N/A': ('N/A', 'غير متاح')},
 'fv_source': {'مالي': ('Financial models', 'مالي (نماذج التقييم)'), 'فني': ('Technical composite (VPOC/WMA/SMA120)', 'فني محسوب (VPOC/WMA/SMA120)')},
 'zb_dir': {'LONG': ('Long (buy)', 'شراء'), 'SHORT': ('Short (sell)', 'بيع')},
 'vt_state': {'WAITING': ('Waiting for signal', 'بانتظار إشارة'), 'RUNNING': ('Running', 'جارية'), 'CLOSED': ('Closed', 'مغلقة')},
 'vt_dir': {'BUY': ('Buy', 'شراء'), 'SELL': ('Sell', 'بيع'), '': ('—', '—')},
 'vt_last_outcome': {'WIN': ('Win', 'ربح'), 'LOSS': ('Loss', 'خسارة'), 'BE': ('Break-even', 'تعادل'),
                     'AMBIGUOUS': ('Ambiguous', 'غامض'), '—': ('—', '—')},
 'sc_signal': {'🟢 BUY': ('🟢 BUY', '🟢 شراء'), '🔴 SELL': ('🔴 SELL', '🔴 بيع')},
 'sc_regime': {'Trending': ('Trending', 'اتجاهي'), 'Choppy': ('Choppy', 'متذبذب'), 'Neutral': ('Neutral', 'محايد')},
 'rd_peer_src': {'Sec': ('Sector', 'قطاع'), 'All': ('All', 'الكل'), '': ('', '')},
 'rd_style': {'Value': ('Value', 'قيمة'), 'Growth': ('Growth', 'نمو'), 'Swing': ('Swing', 'مضاربة سريعة'),
              'Medium Term': ('Medium term', 'مدى متوسط'), 'Long Term': ('Long term', 'مدى طويل'), 'Auto': ('Auto', 'تلقائي')},
}
GUARD_TXT = {'correction': ('market correction', 'تصحيح السوق'), 'risk': ('high deep risk', 'مخاطرة عميقة مرتفعة'),
             'chase': ('candle chasing', 'مطاردة شمعة'), 'tech': ('tech not confirmed', 'التأكيد الفني غير مكتمل')}
UNI_REASON_TXT = {'redflags': ('red financial flags (Altman/Beneish)', 'أعلام مالية حمراء (Altman/Beneish)'),
                  'abovefair': ('price above fair value', 'السعر أعلى من القيمة العادلة'),
                  'sell_signal': ('sell signal from chart analysis', 'إشارة بيع من تحليل الشارت')}
PX_FD = TR['px_final']

def fmt_uni_reasons(keys, note, lang):
    ar = lang == 'عربي'
    parts = []
    for k in (keys or []):
        if k == 'guard':
            g = ' + '.join(GUARD_TXT[x][1 if ar else 0] for x in (note or []) if x in GUARD_TXT)
            parts.append(('الحارس: ' + g) if g else ('الحارس' if ar else 'Guard'))
        else:
            parts.append(UNI_REASON_TXT.get(k, (k, k))[1 if ar else 0])
    return '، '.join(parts) if parts else '—'

# ---- القرار الموحّد (نفس الأوزان الأصلية) + الحارس الكامل بنفس شروط TradingView ----
def unified_decision(rec, mkt_state, p, no_short=False):
    comps = []
    rd = rec.get('rd_score')
    if nn(rd) and rd >= 0:
        comps.append((p['wUniRadar'], rd))
    comps.append((p['wUniPrime'], float(np.clip(50 + (rec['px_buy_pct'] - rec['px_sell_pct']) / 2, 0, 100))))
    up = rec.get('fv_upside')
    if nn(up):
        # 🆕 v5.2: القيمة العادلة الفنية (بديل عند غياب المالية) ليست تقييمًا ماليًا — وزنها نصف الوزن
        wf = p['wUniFair'] * 0.5 if (p.get('fvTechCut', True) and rec.get('fv_source') == 'Technical estimate') else p['wUniFair']
        fc_ = rec.get('fv_conf')
        if nn(fc_): wf *= float(np.clip(fc_ / max(p.get('fvMinConf', 60.0), 1.0), 0.25, 1.0))      # 🆕 v7.0: ثقة أقل ⇒ وزن أقل للقيمة العادلة
        comps.append((wf, float(np.clip(50 + up * 1.25, 0, 100))))
    if rec.get('dp_status') not in (None, '—', 'INSUFFICIENT_DATA') and nn(rec.get('dp_inv')):
        comps.append((p['wUniDeep'], rec['dp_inv']))
    sw = sum(w for w, _ in comps)
    score = sum(w * s for w, s in comps) / sw if sw else NaN
    if score >= 75: dec = 'STRONG BUY'
    elif score >= 60: dec = 'BUY DIP'
    elif score >= 45: dec = 'WATCH'
    else: dec = 'AVOID'
    keys_ar, keys_en, notes = [], [], []
    if rec.get('dp_status') == 'AVOID' and dec in ('STRONG BUY', 'BUY DIP'):
        dec = 'WATCH'; keys_ar.append('أعلام مالية حمراء'); keys_en.append('red financial flags'); notes.append('N_FLAGS')
    fv_ok = (not nn(rec.get('fv_conf'))) or rec['fv_conf'] >= p.get('fvMinConf', 60.0)      # 🆕 v7.0: لا يؤثر الرفض/الخفض إلا بثقة كافية
    if dec == 'STRONG BUY' and nn(up) and up < -10 and fv_ok:
        dec = 'BUY DIP'; keys_ar.append('السعر أعلى من القيمة العادلة بأكثر من 10%'); keys_en.append('price >10% above fair value'); notes.append('N_OVERVALUED')
    # 🛡 الحارس (نفس نظام الحماية في مؤشر الرادار على TradingView): يخفض «شراء قوي» إلى «شراء عند التراجع»
    if p['guardOn'] and dec == 'STRONG BUY':
        gr = []
        if p['guardOnCorr'] and mkt_state == 3: gr.append('correction')
        if p['guardRiskMax'] > 0 and nn(rec.get('dp_risk')) and rec['dp_risk'] >= p['guardRiskMax']: gr.append('risk')
        if p['guardChase'] > 0 and nn(rec.get('chg')) and rec['chg'] >= p['guardChase']: gr.append('chase')
        if p['guardNeedTech'] and rec.get('rd_tech') != '🟢 Conf': gr.append('tech')
        if gr:
            dec = 'BUY DIP'
            keys_ar.append('الحارس: ' + ' + '.join(GUARD_TXT[g][1] for g in gr))
            keys_en.append('Guard: ' + ' + '.join(GUARD_TXT[g][0] for g in gr))
            rec['guard_keys'] = gr
            notes.append('N_GUARD_' + {'correction': 'MKT', 'risk': 'RISK', 'chase': 'CHASE', 'tech': 'TECH'}[gr[0]])
    # 🆕 v6 (إصلاح 10): قرار «بيع» يبقى متوافقاً مع الدرجة الموحدة — إشارة بيع مع درجة ≥60 تُخفَّض إلى «متابعة»
    sell_sig = rec['px_final'] in ('T_SELL', 'ENTRY SELL') or (rec['px_sell_pct'] - rec['px_buy_pct'] > 15 and rec['px_sell_cats'] >= p['minCats'])
    if sell_sig:
        if score >= 60:
            dec = 'WATCH'
            keys_ar.append('إشارة بيع من تحليل الشارت خُفِّضت لأن الدرجة الموحدة مرتفعة')
            keys_en.append('chart sell signal tempered by high unified score')
            notes.append('N_SELL_VS_SCORE')
        else:
            dec = 'SELL'
            keys_ar.append('إشارة بيع من تحليل الشارت الفني'); keys_en.append('sell signal from chart analysis')
            notes.append('N_TECH_SELL')
            # 🆕 v5.2: أسواق بلا بيع مكشوف للأفراد (مصر/السعودية) — «بيع» تعني فعليًا: ابتعد/اخرج
            if no_short and p.get('noShortAsAvoid', True):
                dec = 'AVOID'
                keys_ar.append('البيع على المكشوف غير متاح في سوق هذا السهم — القرار العملي: تجنّب/خروج للحيازة القائمة')
                keys_en.append('short selling unavailable in this market — practical verdict: avoid/exit')
    grade = 'A+' if score >= 75 else 'B+' if score >= 60 else 'C' if score >= 45 else 'D'
    rec['uni_note_codes'] = '|'.join(dict.fromkeys(notes))
    return score, grade, dec, ('، '.join(keys_ar) if keys_ar else '—'), ('; '.join(keys_en) if keys_en else '—')

def zb_plan(price, atr, support, resistance, decision, p):
    """بطاقة الدخول: نطاق شراء، دخول، وقف، هدف، وR:R محسوب من سعر الدخول الفعلي (v5.2 — كان ثابتًا 1.5 من السعر).
    🆕 v6 (إصلاح 1): حقل إضافي zb_rr_mkt = عائد/مخاطرة عند الشراء بسعر السوق الحالي بجوار R:R من سعر دخول الخطة —
    فالخطة تفترض دخولاً أعمق في النطاق بينما الشراء الفوري عند السوق يعطي نسبة أدق واقعية."""
    if not (nn(price) and nn(atr) and atr > 0):
        return {}
    short = decision == 'SELL'
    if not short:
        hi = price; lo = max(support, price - 1.0 * atr) if (nn(support) and support < price * 0.999) else price - 0.5 * atr
        entry = lo + 0.33 * (hi - lo); stop = lo - p['zbStopATR'] * atr
        risk = price - stop; target = price + p['zbTargetR'] * risk
        risk_e = entry - stop
        rr = (target - entry) / risk_e if risk_e > 0 else NaN            # R:R من الدخول (متغير حقيقي وليس ثابتًا)
        rr_mkt = (target - price) / risk if risk > 0 else NaN            # 🆕 v6: R:R عند سعر السوق
    else:
        lo = price; hi = min(resistance, price + 1.0 * atr) if (nn(resistance) and resistance > price * 1.001) else price + 0.5 * atr
        entry = hi - 0.33 * (hi - lo); stop = hi + p['zbStopATR'] * atr
        risk = stop - price; target = price - p['zbTargetR'] * risk
        risk_e = stop - entry
        rr = (entry - target) / risk_e if risk_e > 0 else NaN
        rr_mkt = (price - target) / risk if risk > 0 else NaN            # 🆕 v6: R:R عند سعر السوق (بيع)
    return dict(zb_dir='SHORT' if short else 'LONG', zb_low=lo, zb_high=hi, zb_entry=entry, zb_stop=stop,
                zb_stop_pct=(stop - price) / price * 100, zb_target=target, zb_target_pct=(target - price) / price * 100,
                zb_rr=rr, zb_rr_mkt=rr_mkt)

# 🆕 الشرح النصي المبسط: يشرح أسباب القرار بالأرقام بالعربية والإنجليزية
def build_explain(rec, p):
    ar, en = [], []
    dec_ar = {'STRONG BUY': 'شراء قوي', 'BUY DIP': 'شراء عند التراجع', 'WATCH': 'مراقبة', 'AVOID': 'تجنّب', 'SELL': 'بيع / تجنّب'}
    dec_en = {'STRONG BUY': 'STRONG BUY', 'BUY DIP': 'BUY DIP', 'WATCH': 'WATCH', 'AVOID': 'AVOID', 'SELL': 'SELL / AVOID'}
    dec = rec.get('uni_decision')
    sc = rec.get('uni_score')
    ar.append(f"القرار النهائي: «{dec_ar.get(dec, dec)}» بدرجة {(sc if nn(sc) else 0):.0f} من 100.")
    en.append(f"Final verdict: “{dec_en.get(dec, dec)}” with a score of {(sc if nn(sc) else 0):.0f}/100.")
    # الاتجاه
    tp = rec.get('rd_trend')
    if nn(tp):
        if tp >= 66:
            ar.append('الاتجاه صاعد: السعر فوق المتوسطات القصيرة والمتوسطة.')
            en.append('The trend is up: price trades above the short and medium moving averages.')
        elif tp >= 33:   # 🆕 v5.2: كانت العتبة 34% فتُخطئ قيمة 33.3% وتُعرَض «هابطًا» — «مختلط» الآن تظهر فعلاً
            ar.append('الاتجاه مختلط: المتوسطات متقاربة ولا يعطي تأكيداً واضحاً بعد.')
            en.append('The trend is mixed: moving averages are close, no clear confirmation yet.')
        else:
            ar.append('الاتجاه هابط: السعر تحت المتوسطات ما يعني ضغطاً بيعياً عاماً.')
            en.append('The trend is down: price is below its moving averages (overall selling pressure).')
    # RSI
    rs_ = rec.get('rd_rsi')
    if nn(rs_):
        if rs_ >= 70:
            ar.append(f'مؤشر القوة النسبية RSI = {rs_:.0f} في منطقة تشبع شرائي، أي احتمال تصحيح قريب.')
            en.append(f'RSI = {rs_:.0f} is in overbought territory, so a pullback is likely.')
        elif rs_ >= 50:
            ar.append(f'مؤشر القوة النسبية RSI = {rs_:.0f} أعلى من 50 أي زخم إيجابي بلا تشبع.')
            en.append(f'RSI = {rs_:.0f} is above 50 (positive momentum, not overbought).')
        elif rs_ >= 30:
            ar.append(f'مؤشر القوة النسبية RSI = {rs_:.0f} أقل من 50 أي الزخم ضعيف.')
            en.append(f'RSI = {rs_:.0f} is below 50 (weak momentum).')
        else:
            ar.append(f'مؤشر القوة النسبية RSI = {rs_:.0f} في منطقة تشبع بيعي وقد يرتد السعر منه.')
            en.append(f'RSI = {rs_:.0f} is oversold and may bounce from here.')
    # MACD
    ml, ms = rec.get('rd_macdL'), rec.get('rd_macdS')
    if nn(ml) and nn(ms):
        if ml > ms:
            ar.append('خط MACD أعلى من خط الإشارة (زخم صاعد).')
            en.append('MACD line is above its signal line (rising momentum).')
        else:
            ar.append('خط MACD تحت خط الإشارة (زخم هابط).')
            en.append('MACD line is below its signal line (falling momentum).')
    # تدفق الأموال
    cmf = rec.get('px_cmf')
    if nn(cmf):
        if cmf > 0.03:
            ar.append(f'تدفق الأموال CMF = {cmf:+.2f} موجب — دخول أموال وضغط شرائي.')
            en.append(f'Money flow CMF = {cmf:+.2f} is positive — inflows and buying pressure.')
        elif cmf < -0.03:
            ar.append(f'تدفق الأموال CMF = {cmf:+.2f} سالب — ضغط بيعي/توزيع، وقد يدل على مصيدة سيولة إذا كان السعر عند قمم.')
            en.append(f'Money flow CMF = {cmf:+.2f} is negative — selling pressure/distribution; a liquidity trap is possible near highs.')
        else:
            ar.append(f'تدفق الأموال CMF = {cmf:+.2f} محايد.')
            en.append(f'Money flow CMF = {cmf:+.2f} is neutral.')
    # الحجم
    tags = rec.get('rd_tags') or []
    if 'vol' in tags:
        ar.append('الحجم أعلى من متوسط 20 شمعة (تأكيد سيولة).')
        en.append('Volume is above its 20-bar average (liquidity confirmation).')
    else:
        ar.append('الحجم أقل من المتوسط (لا تأكيد قوي من السيولة بعد).')
        en.append('Volume is below average (no strong liquidity confirmation yet).')
    # الدعم
    ds = rec.get('rd_dist_sup')
    if nn(ds):
        if ds < 25:
            ar.append(f'السعر قريب من قاع النطاق (يبعد {ds:.0f}% عن الدعم) — موقع دخول أفضل.')
            en.append(f'Price is near the bottom of its range ({ds:.0f}% above support) — a better entry location.')
        elif ds > 75:
            ar.append(f'السعر قريب من قمة النطاق ({ds:.0f}%) — شراؤه الآن مطاردة للسعر.')
            en.append(f'Price is near the top of its range ({ds:.0f}%) — buying now is chasing.')
        else:
            ar.append(f'السعر في وسط نطاقه ({ds:.0f}% فوق الدعم).')
            en.append(f'Price sits mid-range ({ds:.0f}% above support).')
    # الشمعة والفجوة
    chg = rec.get('chg')
    if nn(chg) and chg <= -p['crashCandle']:
        ar.append(f'الشمعة الأخيرة هابطة {chg:.1f}% (بيع جبري) — يُفضّل انتظار استقرار السعر.')
        en.append(f'The last candle dropped {chg:.1f}% (forced selling) — better to wait for stabilization.')
    elif nn(chg) and chg >= p['crashCandle']:
        ar.append(f'الشمعة الأخيرة صاعدة {chg:.1f}% (مطاردة محتملة) — تجنّب الشراء المتأخر.')
        en.append(f'The last candle rose {chg:.1f}% (possible chase) — avoid late buying.')
    gp = rec.get('rd_gap')
    if nn(gp) and abs(gp) >= p['gapThresh']:
        ar.append(f'يوجد فجوة سعرية {"صاعدة" if gp > 0 else "هابطة"} {gp:.1f}% — تحقق من سببها (خبر؟).')
        en.append(f'There is a {"gap up" if gp > 0 else "gap down"} of {gp:.1f}% — check the reason (news?).')
    # اصطياد السيولة
    swp = rec.get('px_sweep')
    if swp == 'Bear Sweep':
        ar.append('رُصد اصطياد سيولة هابط (كسر قيعان سابقة) — فخ شراء محتمل على المدى القصير.')
        en.append('A bearish liquidity sweep was detected (prior lows taken) — a short-term bull trap is possible.')
    elif swp == 'Bull Sweep':
        ar.append('رُصد اصطياد سيولة صاعد (كسر قمم سابقة ثم عودة) — غالباً خروج بائعين.')
        en.append('A bullish liquidity sweep was detected (prior highs taken then reclaimed) — often shorts being flushed.')
    # المخاطرة
    ap = rec.get('rd_atr_pct')
    if nn(ap):
        rl = {'low': 'منخفضة', 'medium': 'متوسطة', 'high': 'عالية'}.get(rec.get('rd_risk_key'), 'متوسطة')
        rl_en = {'low': 'low', 'medium': 'medium', 'high': 'high'}.get(rec.get('rd_risk_key'), 'medium')
        tfw_ar = 'أسبوعياً' if rec.get('rd_tf') == 'W' else 'يومياً'          # 🆕 v5.2: الصياغة تطابق إطار الأسلوب
        tfw_en = 'per week' if rec.get('rd_tf') == 'W' else 'per day'
        ar.append(f'المخاطرة {rl} (ATR = {ap:.1f}% من السعر {tfw_ar}، معايَرة على نوع الأصل وإطار الأسلوب).')
        en.append(f'Risk is {rl_en} (ATR = {ap:.1f}% of price {tfw_en}, calibrated to the asset class and style timeframe).')
    # بيانات الفتح
    if rec.get('gap_ok') is False:   # 🆕 v5.2: تنبيه شفاف بدل فجوة 0% زائفة
        ar.append('⚠ بيانات أسعار الفتح من المزود غير موثوقة لهذا السهم (الفتح يُساوي إغلاق الأمس) — فتعطّلت فلاتر الفجوة وأنماط الشموع المعتمدة على الفتح؛ بقية المؤشرات سليمة.')
        en.append('⚠ Open prices from the data provider are unreliable for this symbol (open equals prior close) — gap filters and open-based candle patterns are disabled; other indicators are unaffected.')
    # أصل غير سهمي
    if rec.get('asset') and rec.get('asset') != 'Stock':
        ar.append('هذا الأصل غير سهمي — التحليل المالي العميق ونماذج القيمة العادلة المالية (P/E/جراهام) غير منطبقة عليه، والتقييم يعتمد على البديل الفني المحسوب ومعايرة المخاطرة الخاصة بفئته.')
        en.append('This is a non-equity asset — deep financial analysis and P/E/Graham models do not apply; valuation uses the computed technical composite with risk calibrated to its asset class.')
    # استبعاد قطاعي
    if rec.get('sector_note_ar'):
        ar.append(rec['sector_note_ar'])
        en.append(rec.get('sector_note_en', ''))
    # السوق العام
    mc = rec.get('mkt_class')
    mc_ar = MKT_TXT.get(mc, ('', ''))[1].replace('🟢 ', '').replace('🔴 ', '').replace('🔻 ', '').replace('↗ ', '').replace('🩸 ', '').replace('⚪ ', '').replace('🐻 ', '').replace('🔵 ', '')
    mc_en = MKT_TXT.get(mc, ('', ''))[0].replace('🟢 ', '').replace('🔴 ', '').replace('🔻 ', '').replace('↗ ', '').replace('🩸 ', '').replace('⚪ ', '').replace('🐻 ', '').replace('🔵 ', '')
    ar.append(f'المؤشر العام الذي يتبعه السهم ({rec.get("bench", "")}) حالته: {mc_ar}.')
    en.append(f'The general index this stock follows ({rec.get("bench", "")}) is: {mc_en}.')
    # القيمة العادلة
    fv, up = rec.get('fv_fair'), rec.get('fv_upside')
    if nn(fv) and nn(up):
        ar.append(f'القيمة العادلة المقدّرة {fv:,.2f} أي {("أعلى" if up >= 0 else "أدنى")} من السعر بنسبة {abs(up):.1f}% ({rec.get("fv_verdict", "")}).')
        en.append(f'Estimated fair value is {fv:,.2f}, {abs(up):.1f}% {"above" if up >= 0 else "below"} the current price ({rec.get("fv_verdict_en", rec.get("fv_verdict", ""))}).')
    if nn(fv) and nn(rec.get('fv_conf')):
        cf_ = rec['fv_conf']; lo_, hi_ = rec.get('fv_low'), rec.get('fv_high')
        rng_ar = f' نطاق النماذج الأساسية {lo_:,.2f}–{hi_:,.2f}.' if nn(lo_) and nn(hi_) else ''
        rng_en = f' Core-model range {lo_:,.2f}–{hi_:,.2f}.' if nn(lo_) and nn(hi_) else ''
        ar.append(f'ثقة التقدير {cf_:.0f}% (النماذج: {rec.get("fv_models", "")}؛ مضاعف P/E العادل {rec.get("fv_pe_x", NaN):.1f}×).' + rng_ar + (' ثقة منخفضة: أثر القيمة العادلة في القرار مخفَّض.' if cf_ < P['fvMinConf'] else ''))
        en.append(f'Estimate confidence {cf_:.0f}% (models: {rec.get("fv_models", "")}; fair P/E {rec.get("fv_pe_x", NaN):.1f}x).' + rng_en + (' Low confidence: its influence on the verdict is reduced.' if cf_ < P['fvMinConf'] else ''))
    # التحليل المالي العميق
    dst = rec.get('dp_status')
    if dst not in (None, '—'):
        st_ar = TR['dp_status'].get(dst, (dst, dst))[1]
        st_en = TR['dp_status'].get(dst, (dst, dst))[0]
        if dst != 'INSUFFICIENT_DATA':
            ar.append(f'التحليل المالي العميق: جودة {rec.get("dp_qual", 0):.0f} · نمو {rec.get("dp_growth", 0):.0f} · تقييم {rec.get("dp_valscore", 0):.0f} → {st_ar}.')
            en.append(f'Deep financial analysis: quality {rec.get("dp_qual", 0):.0f} · growth {rec.get("dp_growth", 0):.0f} · valuation {rec.get("dp_valscore", 0):.0f} → {st_en}.')
        else:
            ar.append('البيانات المالية غير كافية لإصدار حكم مالي واضح.')
            en.append('Financial data is insufficient for a clear fundamental verdict.')
        fl = rec.get('dp_flags')
        if nn(fl) and fl > 0:
            ar.append(f'⚠️ يوجد {fl:.0f} علم/أعلام مالية حمراء (Altman/Beneish) — راجع القوائم المالية بنفسك.')
            en.append(f'⚠️ {fl:.0f} red financial flag(s) detected (Altman/Beneish) — review the statements yourself.')
        pe = rec.get('dp_pe')
        if nn(pe):
            ar.append(f'مكرر الربحية P/E = {pe:.1f} (أقل من 15 يُعد رخيصاً نسبياً وأكثر من 40 غالياً).')
            en.append(f'P/E = {pe:.1f} (below 15 is relatively cheap, above 40 is expensive).')
    # تحليل الشارت
    bp, sp_ = rec.get('px_buy_pct'), rec.get('px_sell_pct')
    if nn(bp) and nn(sp_):
        ar.append(f'تحليل الشارت متعدد الفئات: قوة الشراء {bp:.0f}% مقابل البيع {sp_:.0f}% ({rec.get("px_buy_grade", "")}).')
        en.append(f'Multi-category chart analysis: buy strength {bp:.0f}% vs sell {sp_:.0f}% ({rec.get("px_buy_grade", "")}).')
    # خطة مقترحة
    if nn(rec.get('zb_entry')):
        ar.append(f'خطة مقترحة: نطاق دخول {rec.get("zb_low"):,.2f}–{rec.get("zb_high"):,.2f}، وقف {rec.get("zb_stop"):,.2f} ({rec.get("zb_stop_pct"):+.1f}%)، هدف {rec.get("zb_target"):,.2f} ({rec.get("zb_target_pct"):+.1f}%)، عائد/مخاطرة 1:{rec.get("zb_rr"):,.1f}.')
        en.append(f'Suggested plan: entry zone {rec.get("zb_low"):,.2f}–{rec.get("zb_high"):,.2f}, stop {rec.get("zb_stop"):,.2f} ({rec.get("zb_stop_pct"):+.1f}%), target {rec.get("zb_target"):,.2f} ({rec.get("zb_target_pct"):+.1f}%), R:R 1:{rec.get("zb_rr"):,.1f}.')
    # خلاصة
    tail = {
        'STRONG BUY': ('الخلاصة: بنية وتوقيت قويان — الدخول التدريجي مع الالتزام الصارم بالوقف هو الأنسب.',
                       'Bottom line: strong structure and timing — gradual entries with strict stop discipline fit best.'),
        'BUY DIP': ('الخلاصة: الاتجاه إيجابي لكن الأفضل انتظار تراجع قرب نطاق الدخول ثم الشراء التدريجي.',
                    'Bottom line: the setup is positive but waiting for a pullback into the entry zone suits better.'),
        'WATCH': ('الخلاصة: ضع السهم على قائمة المراقبة وانتظر تحسن الإشارات قبل أي قرار.',
                  'Bottom line: keep the stock on a watchlist and wait for signals to improve before acting.'),
        'AVOID': ('الخلاصة: يُنصح بتجنّب السهم حالياً حتى تتحسن المؤشرات بشكل واضح.',
                  'Bottom line: better to avoid this stock for now until the indicators clearly improve.'),
        'SELL': ('الخلاصة: إشارات بيع واضحة — الابتعاد أو تقليل المراكز مع وقف صارم هو الأنسب.',
                 'Bottom line: clear sell signals — stepping aside or trimming with a strict stop fits best.'),
    }
    if dec in tail:
        ar.append(tail[dec][0]); en.append(tail[dec][1])
    return ' '.join(ar), ' '.join(en)


# %% [الخلية 4]
# -----------------------------------------------------------------------------
# 11) تحليل رمز واحد → سجل مسطّح (كل النتائج)
# -----------------------------------------------------------------------------
def fnum(x, d=2):
    return '—' if not nn(x) else (f'{x:,.{d}f}' if not (isinstance(x, float) and math.isinf(x)) else '∞')

def pick_style(base, fm, price, p):
    """🆕 v7.0: نوع الاستثمار التلقائي (Auto) لكل سهم: قاعدة v6.6 الفنية + الأساسيات (P/E · P/B · نمو الأرباح · ROE). يعيد (الأسلوب, السبب)."""
    trend, cmf, rsi, vol, vr = base['trend'], base['cmf'], base['rsi'], base['vol_ann'], base['vol_ratio']
    if vol > 35 and nn(vr) and vr > 1.5: return 'Swing', 'vol'
    if trend >= 66 and nn(cmf) and cmf > 0.05: return 'Growth', 'trend'
    if rsi < 45 and nn(cmf) and cmf > 0: return 'Value', 'dip'
    if p.get('autoStyleFund', True):
        eps, bv, eg, roe = fm.get('eps'), fm.get('bvps'), fm.get('eps_g'), fm.get('roe')
        pe = price / eps if (nn(eps) and eps > 0 and nn(price)) else NaN
        pb = price / bv if (nn(bv) and bv > 0 and nn(price)) else NaN
        g_ = fm.get('eps_ttm_g') if nn(fm.get('eps_ttm_g')) else eg
        if nn(g_) and g_ >= 15 and nn(roe) and roe >= 12 and trend >= 33: return 'Growth', 'earnings'
        if (nn(pe) and 0 < pe <= 10) or (nn(pb) and 0 < pb <= 1.0): return 'Value', 'multiples'
    if trend >= 66: return 'Medium Term', 'trend'
    return 'Long Term', 'default'

def analyze_symbol(sym, df, ctx):
    p = ctx['p']; fund = ctx['fund'].get(sym, {}); mk = market_of(sym)
    bench_sym = ctx['bench_map'].get(mk); bdf = ctx['bench_data'].get(bench_sym)
    # 🆕 v6 (إصلاح 8): الأصل المرجعي نفسه (ذهب/بيتكوين/مؤشر كمرجع لنفسه) — بلا قوة نسبية ولا مقارنة زائفة
    self_bench = (bench_sym == sym) or (asset_class(sym) in ('index', 'commodity') and bench_sym == sym)
    if self_bench:
        bdf = None
    price = float(df['Close'].iloc[-1]); prev = float(df['Close'].iloc[-2]) if len(df) > 1 else price
    base = base_engine(df, bdf, p)
    tvu = (ctx.get('tvf') or {}).get(mk) or {}
    tv_row = (tvu.get('rows') or {}).get(tv_key(sym, mk))
    fm = fund_metrics(fund, price, sym, p, tvf=tv_row)      # 🆕 v7.0: قيمة سوقية/EPS TTM مصحّحان
    sug_style, sug_why = pick_style(base, fm, price, p)      # 🆕 v7.0: اقتراح Auto
    style = sug_style if ctx['style'] == 'Auto' else ctx['style']      # 🆕 v7.0: أسلوب محدد = حصري لكل الأسهم
    sess_closed = session_closed(sym, df.index[-1])
    _e_, _s_ = s_ema(df['Close'], p['emaFast']).iloc[-1], s_sma(df['Close'], p['smaSlow']).iloc[-1]      # 🆕 v6.6: يعرف حالة التعادل (currentBias = 0 في Pine)
    bias = 1 if _e_ > _s_ else -1 if _e_ < _s_ else 0
    mtf = mtf_info(sym, df, ctx.get('intraday'), p, bias, ctx.get('monthly', {}).get(sym))
    hb, hs = hist_htf_arrays(df, p)
    corr_v, corr_ok_b, corr_ok_s = NaN, True, True
    dxy = ctx.get('dxy')
    if dxy is not None and len(dxy) > p['corrLen'] + 5:
        # 🆕 v5.2: الارتباط يُحسب على العوائد اليومية لا على الأسعار (الأسعار غير المستقرة تُطفئ الارتباط زوراً)
        # 🆕 v6.6: مع pineParity الارتباط على الأسعار الخام كما في Pine: ta.correlation(close, corrClose, len)
        if p.get('pineParity', True):
            ra = df['Close'].tail(p['corrLen'])
            rb = dxy['Close'].reindex(ra.index, method='ffill')
        else:
            ra = df['Close'].tail(p['corrLen'] + 1).pct_change()
            rb = dxy['Close'].reindex(ra.index, method='ffill').pct_change()
        m_ = ra.notna() & rb.notna()
        if m_.sum() > 10: corr_v = float(ra[m_].corr(rb[m_]))
        if p['useCorr'] and nn(corr_v) and abs(corr_v) >= p['corrThresh']:
            up_ = ema_sma_state(dxy, p) == 1
            corr_ok_b = (corr_v >= p['corrThresh'] and up_) or (corr_v <= -p['corrThresh'] and not up_)
            corr_ok_s = (corr_v >= p['corrThresh'] and not up_) or (corr_v <= -p['corrThresh'] and up_)
    px = prime_x_engine(df, p, hb, hs, dict(htf_buy=mtf['buy_ok'], htf_sell=mtf['sell_ok'], corr_buy=corr_ok_b, corr_sell=corr_ok_s))
    if px is None: return None
    ac = asset_class(sym)
    if ac != 'stock':   # 🆕 v5.2: أصول غير سهمية — لا قوائم مالية، يُعرض نوع الأصل بوضوح في عمود القطاع
        fm['sector'] = {'crypto': 'عملات رقمية (Crypto)', 'forex': 'عملات أجنبية (Forex)',
                        'commodity': 'معادن وسلع (Commodities)', 'index': 'مؤشر (Index)'}.get(ac, '')
        fm['industry'] = ''
    atr = px['atr']
    res_n, sup_n, res_l, sup_l = auto_sr(df, p, price)
    pdh, pdl = (float(df['High'].iloc[-2]), float(df['Low'].iloc[-2])) if len(df) > 2 else (NaN, NaN)
    vpoc = calc_vpoc(df)
    rs = rs_multi(df, bdf)
    bm = None if self_bench else bench_metrics(bdf, style_params(style, p), p)
    rd = radar_row(sym, df, style, p, bm, fm['sector'], sess_closed)
    deep = deep_analysis(fm, rd['price'], rd.get('prevC', NaN), rd.get('ema20', NaN), rd.get('rsiV', NaN), rd.get('atr', NaN), style, p, mk=mk) if (ctx['deep'] and ac == 'stock' and rd['state'] in (0, 3)) else None
    wma52 = px['wma']; sma120 = float(df['Close'].tail(120).mean())
    # 🆕 v7.0: مضاعف نسبي (وسيط القطاع ثم السوق من ماسح TradingView) + هدف خارجي من المستخدم
    rel = None
    stt = tvu.get('stats') or {}
    if tv_row and stt:
        sc_ = tv_row.get('sector') or ''
        sp_ = (stt.get('sector') or {}).get(sc_)
        if sp_ and sp_[1] >= int(p.get('fvRelMinPeers', 5)): rel = dict(pe=sp_[0], n=sp_[1], scope='Sector')
        elif nn(stt.get('market_pe')) and stt.get('n_market', 0) >= 15: rel = dict(pe=stt['market_pe'], n=stt['n_market'], scope='Market')
    ext_t = None
    for _k in (sym.upper(), tv_key(sym, mk), sym.upper().split('.')[0]):
        if _k in (p.get('fvExt') or {}): ext_t = float(p['fvExt'][_k]); break
    fv = fair_value(fm, price, style, [vpoc, wma52, sma120], p, ref_price=float(df['Close'].tail(int(p.get('fvRefLookback', 252))).median()), mk=mk, rel=rel, ext=ext_t)   # 🆕 v6.3/6.4/7.0
    # ---- حجم الصفقة ----
    slD = atr * p['slATR'] if nn(atr) else NaN
    risk_amt = p['capital'] * p['riskPct'] / 100
    pos_units = risk_amt / slD if nn(slD) and slD > 0 else NaN
    # ---- سجل ----
    chg = (price - prev) / prev * 100
    rec = dict(symbol=sym, name=fm['name'] or sym, market=mk, currency=fm['currency'], sector=fm['sector'], industry=fm['industry'],
               price=price, chg=chg, last_date=str(df.index[-1].date()), bars=len(df), sess_closed=sess_closed, bench=bench_sym,
               w52h=fm['w52h'] if nn(fm['w52h']) else float(df['High'].tail(252).max()), w52l=fm['w52l'] if nn(fm['w52l']) else float(df['Low'].tail(252).min()),
               mcap=fm['mcap'], beta=fm['beta'], div_yield=fm['div_yield'])
    # الدرجة الأساسية
    rec.update(base_score=base['score'], base_rating=base['rating'], base_decision=base['decision'], auto_style=style, style_suggest=sug_style, style_why=sug_why,
               base_trend=base['trend'], base_cmf=base['cmf'], base_rsi=base['rsi'], base_rs=base['rs'], base_vwap=base['vwap_pos'],
               base_support=base['support'], base_resistance=base['resistance'], vol_ann=base['vol_ann'], style_used=style)
    # تحليل الشارت الفني
    cb, cs_ = px['catB'], px['catS']
    regime = '🚀 Strong Trend' if px['chop'] < p['chopTrend'] else '🌊 Choppy' if px['chop'] > p['chopChoppy'] else '😴 Calm'
    vr = px['volRatio']
    mstate = '⚪ N/A' if not nn(vr) else f'{vr:.2f}x ' + ('🔥 High Activity' if vr >= p['msHigh'] else '💤 Low Liquidity' if vr <= p['msLow'] else '⚖️ Normal Activity')
    struct_conf = 'Bullish' if px['msConf'] == 1 else 'Bearish' if px['msConf'] == -1 else 'Neutral'
    struct_live = 'Bullish' if px['msEff'] == 1 else 'Bearish' if px['msEff'] == -1 else 'Neutral'
    zone = '🔴 Premium' if px['inPrem'] else '🟢 Discount' if px['inDisc'] else '🟡 Equilibrium'
    near = []
    tol = atr * 0.5
    for (t_, b_) in px['bullOB']:
        if b_ - tol <= price <= t_ + tol: near.append('🟦OB↑')
    for (t_, b_) in px['bearOB']:
        if b_ - tol <= price <= t_ + tol: near.append('🟪OB↓')
    for (isb, t_, b_, lv) in px['fvgs']:
        if b_ - tol <= price <= t_ + tol: near.append('🟢FVG↑' if isb else '🟠FVG↓')
    near = ' '.join(dict.fromkeys(near)) or 'No Nearby Zones'
    divtxt = px['divLast'][1] if (px['i'] - px['divLast'][0]) <= 10 else 'None'
    eqtxt = px['eqLast'][1] if (px['i'] - px['eqLast'][0]) <= 10 else ''        # 🆕 v6: EQH/EQL للشرح والعمود
    sq_txt = '⚠️ Active Squeeze' if px['squeeze'] else ('Release' if px['sqRelease'] else 'Normal')
    sc_ema = '🟢' if px['emaF'] > px['smaS'] else '🔴'
    sc_rsi = '🟢' if px['rsiS'] > 50 else '🔴'
    sc_st = '🟢' if px['stD'] < 0 else '🔴'
    # 🆕 v6.6: الماسح يعرف STANDBY (bull>=2 وbull>bear شراء · bear>=2 وbear>bull بيع · وإلا انتظار) — int() لأن جمع np.bool_ يتصرّف كـOR
    g_ = int(px['emaF'] > px['smaS']) + int(px['rsiS'] > 50) + int(px['stD'] < 0)
    r_ = int(px['emaF'] < px['smaS']) + int(px['rsiS'] < 50) + int(px['stD'] > 0)
    sc_sig = '🟢 BUY' if (g_ >= 2 and g_ > r_) else '🔴 SELL' if (r_ >= 2 and r_ > g_) else '⏳ STANDBY'
    # 🆕 v5.0: قرار تحليل الشارت — بدون «IN TRADE» عندما تكون الصفقة الافتراضية مطفأة
    if px['final'] == 'IN TRADE' and not p['vtOn']:
        mc_ = p['minCats']
        px_disp = ('ENTRY BUY' if px['isBuy'] else 'ENTRY SELL' if px['isSell'] else
                   'WATCH' if (px['buyAg'] >= mc_ or px['sellAg'] >= mc_) else
                   'WAIT' if (px['buyAg'] >= max(mc_ - 2, 1) or px['sellAg'] >= max(mc_ - 2, 1)) else 'NO TRADE')
    else:
        px_disp = px['final']
    # 🆕 v6: أكواد القرار الفني بنفس تسميات التصميم (T_*) مع الميل صعودي/هبوطي عند «متابعة»
    px_code = {'ENTRY BUY': 'T_BUY', 'ENTRY SELL': 'T_SELL', 'IN TRADE': 'IN TRADE'}.get(px_disp)
    if px_code is None:
        px_code = 'T_WATCH_UP' if px_disp == 'WATCH' and px['buyP'] >= px['sellP'] else \
                  'T_WATCH_DOWN' if px_disp == 'WATCH' else \
                  'T_WAIT' if px_disp == 'WAIT' else 'T_AVOID'
    rec.update(
        px_regime=regime, px_chop=px['chop'], px_buy_score=px['buyS'], px_buy_pct=px['buyP'], px_buy_grade=px['buyGrade'], px_buy_cats=px['buyAg'],
        px_sell_score=px['sellS'], px_sell_pct=px['sellP'], px_sell_grade=px['sellGrade'], px_sell_cats=px['sellAg'],
        px_max_score=px['maxS'], px_signal='BUY' if px['isBuy'] else 'SELL' if px['isSell'] else 'None',
        px_signal_age=min([a for a in (px['lastBuyAge'], px['lastSellAge']) if a is not None], default=None),
        px_final=px_code, px_state=mstate, px_mtf_mode=mtf['mode'],
        px_h1=('⚪' if mtf['h1'] is None else '🟢' if mtf['h1'] == 1 else '🔴'), px_h4=('⚪' if mtf['h2'] is None else '🟢' if mtf['h2'] == 1 else '🔴'),
        px_matrix=mtf['matrix'], px_matrix_frames='/'.join(mtf['frames']), px_mtf_label=mtf['label'],
        px_vwap=('🟢 Above' if price > px['vwap'] else '🔴 Below') if nn(px['vwap']) else '⚪', px_vwap_val=px['vwap'], px_vpoc=vpoc,
        px_support=sup_n, px_resistance=res_n, px_pdh=pdh, px_pdl=pdl, px_rs_label=rs['label'], px_rs_detail=rs['detail'],
        px_sweep=px['sweep'], px_div=divtxt, px_squeeze=sq_txt, px_cmf=px['cmf'], px_zone=zone,
        px_location=f"{zone} | VWAP:{'Above' if price > px['vwap'] else 'Below'} | VPOC:{'Above' if price > vpoc else 'Below'} | WMA:{'Above' if price > px['wma'] else 'Below'}",
        px_near=near, px_struct_conf=struct_conf, px_struct_live=struct_live, px_last_break=px['smcLast'] or '—',
        px_smc_counts=f"BOS↑:{px['smcCnt']['bb']} CHoCH↑:{px['smcCnt']['bc']} BOS↓:{px['smcCnt']['sb']} CHoCH↓:{px['smcCnt']['sc']}",
        px_fib=('✅ Fib Confirmed' if px['fibConfirmed'] else '⚠️ Fib Fallback'), px_fibH=px['fibH'], px_fibL=px['fibL'],
        px_corr=corr_v, px_macd_hist=px['macdHist'], px_pos_units=pos_units, px_risk_amt=risk_amt, px_atr=atr,
        px_ema=px['emaF'], px_sma=px['smaS'], px_wma=px['wma'], px_st=px['stV'], px_st_dir='🟢 Up' if px['stD'] < 0 else '🔴 Down',
        px_rsi_f=px['rsiF'], px_rsi_s=px['rsiS'], px_stoch=px['stK'], px_ao=px['ao'], px_patterns=', '.join(px['pat']) or '—',
        px_cat_buy=' '.join(f'{k}:{v}' for k, v in cb.items()), px_cat_sell=' '.join(f'{k}:{v}' for k, v in cs_.items()),
        px_regime_mult=' '.join(f'{k}×{v}' for k, v in px['rg'].items()), px_grades_ok=px['gradesOK'],
        # 🆕 v6: حقول إضافية موجودة في التصميم المرفق (MACD/Stoch التفصيلية + الشمعة + الحجم + الهيكل)
        px_macd=px['macd'], px_macd_sig=px['macdSig'], px_stoch_k=px['stK'], px_stoch_d=px['stD_'],
        px_bar_chg=px['barChg'], px_vol_ratio=vr, px_eq=eqtxt, px_dist=('Dist' if px['isDist'] else ''), px_sq_on=bool(px['squeeze']),
        px_smc_bias=int(px['smcBias']) if nn(px['smcBias']) else 0)
    # البطاقة الافتراضية (تُحسب دائماً داخلياً — تُعرض فقط عند تفعيل الخيار)
    cnt1 = int(round(px['reach1'] * px['opened'] / 100)) if (nn(px['reach1']) and px['opened']) else 0
    cnt2 = int(round(px['reach2'] * px['opened'] / 100)) if (nn(px['reach2']) and px['opened']) else 0
    cnt3 = int(round(px['reach3'] * px['opened'] / 100)) if (nn(px['reach3']) and px['opened']) else 0
    rec.update(
        vt_state=px['trade_state'], vt_dir=px['trade_dir'], vt_entry=px['entry'], vt_sl=px['sl'], vt_tp1=px['tp1'], vt_tp2=px['tp2'], vt_tp3=px['tp3'],
        vt_hit=('✅' if px['hit1'] else '') + ('✅' if px['hit2'] else '') + ('✅' if px['hit3'] else ''), vt_be=px['be'], vt_mfe=px['mfe'], vt_mae=px['mae'],
        vt_record=f"W{px['W']} • L{px['L']} • BE{px['BE']} • AMB{px['AMB']}", vt_w=px['W'], vt_l=px['L'], vt_be_n=px['BE'], vt_amb=px['AMB'],
        vt_closed=px['closed'], vt_opened=px['opened'], vt_win_rate=px['win_rate'], vt_pf=px['pf'], vt_avg_r=px['avg_r'],
        # «الوصول» = نسبة الصفقات المفتوحة التي لمست كل هدف في أي لحظة (وليس نسبة الربح النهائي — الربح عند الهدف الثالث)
        vt_reached=f"TP1 {fnum(px['reach1'], 0)}% ({cnt1}/{px['opened']}) • TP2 {fnum(px['reach2'], 0)}% ({cnt2}/{px['opened']}) • TP3 {fnum(px['reach3'], 0)}% ({cnt3}/{px['opened']})",
        vt_r1=px['reach1'], vt_r2=px['reach2'], vt_r3=px['reach3'],
        vt_last_outcome=px['last_outcome'] or '—', vt_last_r=px['last_r'])
    # Radar
    rec.update(rd_style=style, rd_tf=rd['tf'], rd_score=rd.get('score', -1), rd_inv=rd.get('inv', NaN), rd_entry=rd.get('entryScore', NaN),
               rd_rating=rd.get('rating', ''), rd_tech=rd.get('tech', '—'), rd_reasons=rd.get('reasons', ''), rd_sig=rd.get('sig', ''),
               rd_tags=rd.get('reason_tags', []), rd_risk_key=rd.get('risk_key', 'medium'), rd_trend=rd.get('trendPct', NaN),
               rd_rsi=rd.get('rsiV', NaN), rd_macdL=rd.get('macdL', NaN), rd_macdS=rd.get('macdS', NaN), rd_ema50=rd.get('ema50', NaN),
               rd_risk=rd.get('riskLevel', ''), rd_atr_pct=rd.get('atrPct', NaN), rd_stop=rd.get('stop', NaN), rd_target=rd.get('target', NaN),
               rd_tgt_src=rd.get('tgtSrc', ''), rd_rr=rd.get('rr', NaN), rd_rr_mkt=rd.get('rr', NaN), rd_qty=rd.get('qty', NaN), rd_adx=rd.get('adx', NaN), rd_bbpb=rd.get('bbPB', NaN),
               rd_gap=rd.get('gapPct', NaN), rd_state=rd['state'], rd_confirmed=rd.get('confirmedNow', False), rd_traded=rd.get('tradedVal', NaN),
               rd_dist_sup=rd.get('distSup', NaN), rd_peer=NaN, rd_peer_src='', rd_sc_chg=rd.get('scChg', NaN), rd_atr=rd.get('atr', NaN),
               gap_ok=rd.get('open_ok', True),
               chg20=float((df['Close'].iloc[-1] / df['Close'].iloc[-21] - 1) * 100) if len(df) > 21 else NaN)
    # 🆕 أهداف فيبوناتشي حسب الأسلوب (تُستخدم كمرشحات لأهداف الاستثمار tg_*)
    fib = fib_targets(df, style, p, price, rec['w52h'], rec['w52l'])
    fibL, fibH = (fib['fib_lo'], fib['fib_hi']) if fib else (NaN, NaN)
    # العميق (+ الحارس بنفس شروط TradingView)
    if deep:
        dec_ = deep['status']; gk = []
        if p['guardOn'] and dec_ == 'STRONG_BUY':
            if p['guardRiskMax'] > 0 and deep['risk'] >= p['guardRiskMax']: gk.append('risk')
            if p['guardChase'] > 0 and nn(rec['chg']) and rec['chg'] >= p['guardChase']: gk.append('chase')
            if p['guardNeedTech'] and rd.get('tech') != '🟢 Conf': gk.append('tech')
            if p['guardOnCorr'] and bm and bm.get('stress', bm['state'] == 3): gk.append('correction')      # 🆕 v7.0: يشمل التراجع/التصحيح/الهابط/الانهيار
            if gk: dec_ = 'BUY_DIP'
        rec.update(dp_status=dec_, dp_guard_keys=gk,
                   dp_guard_ar=('الحارس: ' + ' + '.join(GUARD_TXT[x][1] for x in gk)) if gk else '',
                   dp_guard_en=('Guard: ' + ' + '.join(GUARD_TXT[x][0] for x in gk)) if gk else '',
                   # 🆕 v6: توكنات الحارس بصيغة التصميم المرفق (MktCorrection / Risk≥80 / Chase≥6 / Tech≠Conf)
                   dp_guard=(' + '.join({'correction': 'MktCorrection', 'risk': f"Risk≥{int(p['guardRiskMax'])}",
                                         'chase': f"Chase≥{int(p['guardChase'])}", 'tech': 'Tech≠Conf'}[x] for x in gk)) if gk else '',
                   dp_align=align_code(rd.get('tech', '—'), dec_), dp_inv=deep['inv'], dp_ent=deep['ent'],
                   dp_conf=deep['conf'], dp_pe=deep['pe'], dp_pb=deep['pb'], dp_flags=deep['flags'], dp_risk=deep['risk'], dp_qual=deep['qual'],
                   dp_growth=deep['growth'], dp_valscore=deep['valscore'])
    else:
        rec.update(dp_status='—', dp_guard='', dp_guard_keys=[], dp_guard_ar='', dp_guard_en='', dp_align=9, dp_inv=NaN, dp_ent=NaN, dp_conf=NaN,
                   dp_pe=fm['pe_info'], dp_pb=fm['pb_info'], dp_flags=NaN, dp_risk=NaN, dp_qual=NaN, dp_growth=NaN, dp_valscore=NaN)
    rec.update(dp_eps_ttm_g=fm['eps_ttm_g'], dp_roe=fm['roe'], dp_piotroski=fm['pio'], dp_altman=fm['altman'], dp_beneish=fm['beneish'], dp_eps_g=fm['eps_g'],
               dp_eps=fm['eps'], dp_bvps=fm['bvps'], dp_fcf=fm['fcfm'], dp_fwd_pe=fm['fwd_pe'])
    # 🆕 v5.2: ملاحظة شفافة عند استبعاد مقاييس غير معبّرة عن القطاع (بنوك/تأمين/مرافق/عقار) + إخفاء قيمها من الأعمدة
    if ac == 'stock' and p.get('sectorAware', True) and not (fm.get('altman_ok', True) and fm.get('fcf_ok', True)):
        exl_en, exl_ar = [], []
        if not fm.get('altman_ok', True): exl_en.append('Altman Z'); exl_ar.append('Altman Z'); rec['dp_altman'] = NaN
        if not fm.get('fcf_ok', True): exl_en.append('FCF margin'); exl_ar.append('هامش FCF'); rec['dp_fcf'] = NaN
        rec['sector_note_ar'] = f"قطاع «{fm['sector']}»: {' و'.join(exl_ar)} لا يُطبَّق/تُطبَّق على هذا القطاع لأنه غير معبّر عنه (بنوك/تأمين/مرافق/عقار) — التقييم اعتمد على بقية المقاييس."
        rec['sector_note_en'] = f"Sector “{fm['sector']}”: {' and '.join(exl_en)} do(es) not apply to this sector (banks/insurance/utilities/real estate) — the rest of the metrics were used."
    rec['fm_flags'] = ','.join(fm.get('fm_flags') or [])
    rec.update(fv_fair=fv['fair'], fv_upside=fv['upside'], fv_mos=fv['mos'], fv_verdict=fv['verdict'], fv_source=fv['source'], fv_models=fv['used'],
               fv_pe=fv['pe_model'], fv_pe_x=fv['pe_x'], fv_graham=fv['graham'], fv_grahamG=fv['grahamG'], fv_analyst=fv['analyst'],
               fv_pb=fv['pb_model'], fv_rel=fv['rel_model'], fv_rel_pe=fv['rel_pe'], fv_ext=fv['ext_model'], fv_conf=fv['conf'], fv_low=fv['low'], fv_high=fv['high'],
               fv_growth=fv['growth'], fv_quality=fv['quality'], fv_eps_src=fm.get('eps_src', ''), mcap_src=fm.get('mcap_src', ''),
               fv_rel_scope=(rel['scope'] + f" ({rel['n']})") if rel else '',
               fv_an_hi=fm['analyst_hi'], fv_an_lo=fm['analyst_lo'], fv_an_n=fm['analyst_n'])
    fv_verd_en = fv['verdict']
    rec['fv_verdict_en'] = fv_verd_en
    # الماسح
    rec.update(sc_ema=sc_ema, sc_rsi=sc_rsi, sc_st=sc_st, sc_chop=px['chop'],
               sc_regime='Trending' if px['chop'] < p['chopTrend'] else 'Choppy' if px['chop'] > p['chopChoppy'] else 'Neutral',
               sc_signal=sc_sig, sc_str=f'{max(g_, r_)}/3', sc_sync='')
    # الحالة العامة للسوق + القرار الموحد + خطة الدخول
    mst = (3 if bm.get('stress') else bm['state']) if bm else 0      # 🆕 v7.0: تشديد الحارس في كل حالات الضغط المؤسسية
    mcls = market_class(bm, p)
    uscore, ugrade, udec, ureas_ar, ureas_en = unified_decision(rec, mst, p, no_short=(mk in NO_SHORT_MARKETS))
    plan = zb_plan(price, atr, sup_n if nn(sup_n) else base['support'], res_n if nn(res_n) else base['resistance'], udec, p)
    rec.update(uni_score=uscore, uni_grade=ugrade, uni_decision=udec, uni_signal=udec,
               uni_reasons=ureas_en, uni_reasons_ar=ureas_ar, uni_reasons_en=ureas_en,
               uni_notes=rec.get('uni_note_codes', ''),
               mkt_state_n=mst, mkt_state=int(mst) if nn(mst) else 0, mkt_class=mcls, mkt_rebound=bool(bm and bm.get('rebound')))
    rec.update(plan)
    # 🆕 v6: أهداف الاستثمار (فيبو + قمة 52 أسبوع + المحللين + القيمة العادلة) حسب الأسلوب — كما في التصميم المرفق
    rec.update(invest_targets(price, style, fibL, fibH, rec['w52h'], fm['analyst'], fm['analyst_hi'], fv['fair'], atr))
    # 🆕 v6: حالة المؤشر العام التفصيلية للعرض (مثل الملف المرفق) — label/tf/bench/dd/vs20/vs50/chg1/ret5
    mdet = (ctx.get('mkt_detail') or {}).get((bench_sym, 'W' if style == 'Long Term' else 'D'))
    if mdet is not None:
        rec.update(mkt_label=mdet['label'], mkt_tf=mdet['tf'], mkt_bench=bench_sym, mkt_dd=float(mdet['dd']),
                   mkt_vs20=float(mdet['vs20']), mkt_vs50=float(mdet['vs50']), mkt_chg1=float(mdet['chg1']), mkt_ret5=float(mdet['ret5']))
    else:
        rec.update(mkt_label='M_NA', mkt_tf='D', mkt_bench=bench_sym, mkt_dd=NaN, mkt_vs20=NaN, mkt_vs50=NaN, mkt_chg1=NaN, mkt_ret5=NaN)
    rec['_mdet'] = mdet
    # 🆕 v6 (إصلاح 7): الأسباب الكاملة تُبنى الآن وبقيت تُترجم لكل لغة عند العرض (بلا سياق عام _LOC_CTX)
    if nn(rec.get('dp_risk')):
        rec['rd_reasons_full'] = rec['rd_reasons'] + f" | Risk: {rec['dp_risk']:.1f}" + (f" | Guard: {rec['dp_guard']}" if rec.get('dp_guard') else '')
    else:
        rec['rd_reasons_full'] = rec['rd_reasons']
    # قرار التحليل العميق معاً مع درع الحارس (كما في التصميم المرفق)
    rec['dp_decision'] = rec['dp_status'] + ('+SHIELD' if rec.get('dp_guard_keys') else '')
    # 🆕 الشرح النصي (عربي + إنجليزي) — يُستخدم في التفاصيل والأعمدة المساعدة
    ex_ar, ex_en = build_explain(rec, p)
    rec['explain_ar'], rec['explain_en'] = ex_ar, ex_en
    rec['_px'] = dict(signals=px['signals'], trades=px['trades'])
    rec['_mkt'] = bm
    return rec

# -----------------------------------------------------------------------------
# 13) تشغيل الفحص الكامل
# -----------------------------------------------------------------------------
def run_scan(symbols_text, market='AUTO', bench_choice='AUTO', style='Auto', capital=10000.0, risk_pct=1.0, deep=True,
             intraday=False, require_htf=True, use_corr=True, guard=True, vt=True, lang='عربي', progress=None, p_over=None,
             be_next_bar=False):
    """يعيد dict: df (DataFrame), recs, meta. (vt: إظهار الصفقة الافتراضية — be_next_bar: الوقف من الشمعة التالية)
    🆕 v6.6: الافتراضيات use_corr=True وbe_next_bar=False مطابقة لـPine."""
    p = dict(P); p.update(capital=float(capital), riskPct=float(risk_pct), requireHTF=bool(require_htf), useCorr=bool(use_corr),
                          guardOn=bool(guard), vtOn=bool(vt), beNextBar=bool(be_next_bar))
    if p_over:
        for _k, _v in p_over.items():      # 🆕 v7.0: دمج القواميس (أوزان القيمة العادلة/الأهداف الخارجية) بدل استبدالها كلياً
            p[_k] = {**p[_k], **_v} if (isinstance(_v, dict) and isinstance(p.get(_k), dict) and _k not in ('fvCoe',)) else _v
    syms, dropped = parse_symbols(symbols_text, market)
    if not syms: raise ValueError('لم يتم إدخال رموز صالحة.')
    t0 = time.time(); log = []
    if dropped: log.append(f'⚠️ تم تجاهل {dropped} رمز زائد (الحد الأقصى {MAX_SYMBOLS}).')
    prices, alias = fetch_prices_with_fallback(syms, market, progress)
    fill_tv_history(prices, [alias.get(s, s) for s in syms], log, p)      # 🆕 v6.4/6.5: تاريخ ناقص (مصر/السعودية) → TradingView
    egx_info = apply_live(prices, 'EGX', log)      # 🆕 v6.2: سعر اليوم/اللحظي لأسهم البورصة المصرية بدل شمعة ياهو المتأخرة
    tasi_info = apply_live(prices, 'TASI', log)      # 🆕 v6.5: نفس الإصلاح لأسهم السعودية (.SR)
    _FV_ACTIVE.clear(); _FV_ACTIVE.update(p.get('fvCoe') or {})
    log.extend(fv_inputs_log(p, {market_of(t) for t in prices}))      # 🆕 v6.5: المضاعف المستخدم + تحذير قِدم المدخلات
    syms_ok = [alias.get(s, s) for s in syms if alias.get(s, s) in prices]
    failed = [s for s in syms if alias.get(s, s) not in prices]
    short = [s for s in syms_ok if len(prices[s]) < 60]
    syms_ok = [s for s in syms_ok if len(prices[s]) >= 60]
    if failed: log.append('❌ لا بيانات لـ: ' + ', '.join(failed))
    for f_ in [x for x in failed if x.endswith('.CA') or x.endswith('.SR')]:      # 🆕 v6.3/6.5: سهم مصري/سعودي بلا تاريخ على ياهو — نعرض سعره الحالي من TradingView للعلم
        _m = 'EGX' if f_.endswith('.CA') else 'TASI'
        q_ = (live_snapshot(_m) or {}).get(f_[:-len(LIVE_MKT[_m]['suf'])].upper())
        log.append(f"ℹ️ {f_}: ياهو لا يوفر له أي بيانات تاريخية (غير مغطّى على ياهو) فلا يمكن تحليله فنياً/مالياً هنا" +
                   (f" — سعره الحالي على TradingView {q_['close']:g}" + (f" ({q_['chg']:+.2f}%)" if nn(q_['chg']) else '') if q_ else '') + '.')
    if short: log.append('⏳ تاريخ قصير (<60 شمعة) تم استبعاده: ' + ', '.join(short))
    if not syms_ok: raise ValueError('تعذر تحميل بيانات أي رمز.\n' + '\n'.join(log))
    mk_used = sorted({market_of(s) for s in syms_ok})
    bench_map = {m: (BENCH_BY_MARKET[m] if bench_choice == 'AUTO' else bench_choice) for m in mk_used}
    bench_data = fetch_prices(sorted(set(bench_map.values()) | {'DX-Y.NYB'}), period='2y')
    if any(m_ in mk_used for m_ in ('EGX', 'TASI')):
        fill_tv_index(bench_data, list(bench_map.values()), log, p)      # 🆕 v6.4/6.5
        apply_index_live(bench_data, log)      # 🆕 v6.2/6.5
    # 🆕 v5.1: بديل تلقائي عندما يرجع ياهو تاريخاً غير كافٍ لمؤشر السوق (يحدث حالياً مع ^CASE30 و ^TASI.SR
    #    صف واحد فقط) فيظهر «غير متاح» لحالة السوق العام والقوة النسبية لكل أسهم مصر/السعودية.
    # 🆕 v6 (طلب 4): مؤشرات مصر الأخرى تُجرَّب مرشحاتها بالترتيب قبل البديل (EGX70/EGX100/Shariah).
    bench_proxy = {}
    for m, bs in list(bench_map.items()):
        b0 = bench_data.get(bs)
        if b0 is not None and len(b0) >= 25:
            bench_proxy[m] = False
            continue
        alt, src_lbl = None, ''
        cands = [c for c in _EGX_INDICES.values() if bs in c]
        for cl in cands:                      # 🆕 v6: مرشحات إضافية لنفس المؤشر (مثل ^CCSI لـEGX70)
            for c in cl:
                if c == bs: continue
                alt = fetch_prices([c], period='2y').get(c)
                if alt is not None and len(alt) >= 25:
                    src_lbl = f'رمز بديل ({c})'; break
            if alt is not None and len(alt) >= 25: break
        if alt is None or len(alt) < 25:
            px_ = _BENCH_PROXY.get(m)
            if px_:
                alt = fetch_prices([px_], period='2y').get(px_)
                if alt is not None and len(alt) >= 25:
                    src_lbl = f'ETF بديل ({px_})'
        if alt is None or len(alt) < 25:
            alt = _synthetic_index([prices[t] for t in syms_ok if market_of(t) == m])
            if alt is not None and len(alt) >= 25:
                src_lbl = 'مؤشر تركيبي متساوي الأوزان من أسهم السوق المفحوصة'
        if alt is not None and len(alt) >= 25:
            bench_data[bs] = alt
            bench_proxy[m] = True
            log.append(f'ℹ️ مؤشر {bs} لا يوفر ياهو تاريخاً كاملاً له حالياً — حُسبت حالة السوق العام والقوة النسبية بـ{src_lbl}.')
        else:
            bench_proxy[m] = False
    # 🆕 v5.2: بيانات شهرية 10 سنوات — يجعل إطار M1 في مصفوفة الأطر متاحًا دائمًا (كان يحتاج 34 شهرًا من سنتين فيبقى ⚪)
    mo_data = fetch_prices(syms_ok, period='10y', interval='1mo', chunk=25) if p.get('monthlyData', True) else {}
    # 🆕 v5.2: القوائم المالية تُجلب للأسهم فقط (رقمية/عملات/معادن بلا قوائم — توفير وقت وطلبات)
    stock_syms = [s for s in syms_ok if asset_class(s) == 'stock']
    fund = fetch_fundamentals(stock_syms, deep=deep, progress=progress) if stock_syms else {}
    intr = fetch_intraday_all(syms_ok, progress) if intraday else None
    # 🆕 v7.0: بيانات TradingView الأساسية (EPS TTM + قيمة سوقية حية + وسيط P/E للقطاع/السوق) — الفشل لا يوقف التحليل
    tvf = {}
    if p.get('fvTvFund', True) and stock_syms:
        for _m in sorted({market_of(s) for s in stock_syms} & set(TV_FUND_MKT)):
            try:
                _d = tv_fund_universe(_m)
            except Exception:
                _d = {}
            if _d: tvf[_m] = _d
            else: log.append(f'ℹ️ بيانات TradingView الأساسية غير متاحة لسوق {_m} الآن — يُكمل التحليل ببيانات ياهو (قد تتأخر EPS والقيمة السوقية).')
    # 🆕 v6: حالة المؤشر العام التفصيلية للعرض (صاعد/ضعف/ارتداد/هبوط/تصحيح/انهيار) على اليومي والأسبوعي
    mkt_detail = {(b_, tf_): market_detail(bench_data.get(b_), p, tf_) for b_ in set(bench_map.values()) for tf_ in ('D', 'W')}
    ctx = dict(p=p, fund=fund, tvf=tvf, bench_map=bench_map, bench_data=bench_data, style=style, deep=deep, intraday=intr,
               dxy=bench_data.get('DX-Y.NYB'), monthly=mo_data, mkt_detail=mkt_detail)
    recs = []
    for k, s in enumerate(syms_ok):
        try:
            r = analyze_symbol(s, prices[s], ctx)
            if r: r['_df'] = prices[s]; recs.append(r)
        except Exception as e:
            log.append(f'❌ خطأ في تحليل {s}: {type(e).__name__}: {e}')
        if progress: progress(k + 1, len(syms_ok), 'التحليل')
    if not recs: raise ValueError('فشل تحليل كل الرموز.\n' + '\n'.join(log))
    # الأقران + المزامنة — 🆕 v5.2: المقارنة على نافذة موحّدة (20 شمعة يومية) لكل الأسهم
    # 🆕 v6.6: مع pineParity الأقران على scChg (نافذة الأسلوب) وحالة 0 فقط كما في f_computePeer في Pine
    PAR = p.get('pineParity', True); PK = 'rd_sc_chg' if PAR else 'chg20'
    ok = [r for r in recs if ((r['rd_state'] == 0) if PAR else (r['rd_state'] in (0, 3))) and nn(r.get(PK))]
    for r in ok:
        others = [x for x in ok if x is not r]
        sec = [x[PK] for x in others if r['sector'] and x['sector'] == r['sector']]
        if len(sec) >= 2: r['rd_peer'] = r[PK] - float(np.mean(sec)); r['rd_peer_src'] = 'Sec'
        elif len(others) >= 2: r['rd_peer'] = r[PK] - float(np.mean([x[PK] for x in others])); r['rd_peer_src'] = 'All'
    mx = max(pd.Timestamp(r['last_date']) for r in recs)
    for r in recs:
        lag = (mx - pd.Timestamp(r['last_date'])).days
        r['sc_sync'] = '✅' if lag == 0 else f'⏳{lag}d'
        r['sc_chg'] = r['chg']
    if p.get('sortByDecision', True):      # 🆕 v7.0: الترتيب حسب قرار الشراء ثم الدرجة
        _rk = {'STRONG BUY': 0, 'BUY DIP': 1, 'WATCH': 2, 'AVOID': 3, 'SELL': 4}
        recs.sort(key=lambda r: (_rk.get(r['uni_decision'], 5), -(r['uni_score'] if nn(r['uni_score']) else -1)))
    else:
        recs.sort(key=lambda r: (-(r['uni_score'] if nn(r['uni_score']) else -1)))
    df = pd.DataFrame([{k: v for k, v in r.items() if not k.startswith('_')} for r in recs])
    if not p['vtOn']:   # 🆕 v5.0: عند إيقاف الصفقة الافتراضية تُحذف أعمدتها من كل النتائج
        df = df.drop(columns=[c for c in df.columns if c.startswith('vt_')])
    banners = {}
    for r in recs:
        if r.get('_mdet') is not None and r['market'] not in banners:
            banners[r['market']] = (r['bench'], r['_mdet'], r.get('mkt_state_n', 0))
    meta = dict(generated=dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'), n=len(recs), requested=len(syms), failed=failed, log=log,
                banners=banners, style=style, deep=deep, intraday=intraday, secs=time.time() - t0, lang=lang, p=p, as_of=str(mx.date()),
                vtOn=bool(p['vtOn']), guardOn=bool(p['guardOn']), bench_proxy=bench_proxy, egx_live=egx_info)
    return dict(df=df, recs=recs, meta=meta)

# -----------------------------------------------------------------------------
# 8b) 🆕 v6: حالة المؤشر العام التفصيلية + أهداف الاستثمار حسب الأسلوب (من الكود الأساسي v2.0)
# -----------------------------------------------------------------------------
def market_detail(bdf, p, tf='D'):
    """🆕 v7.0: حالة المؤشر العام التفصيلية للعرض — مراحل مؤسسية مطابقة لمؤشر Pine v4.2 (انهيار · سوق هابط · تصحيح · تراجع · ضعف · صحي · تعافٍ)
    + وسوم: قمة جديدة · ارتداد غير مؤكد · ارتداد تحت EMA20 · حركة ذعر."""
    if bdf is not None and tf == 'W': bdf = resample_ohlc(bdf, 'W-FRI')
    if bdf is None or len(bdf) < 60: return None
    ph = mkt_phase_calc(bdf['Close'], p, tf)
    if ph is None: return None
    lab = {6: 'M_CRASH', 5: 'M_BEAR', 4: 'M_CORR', 3: 'M_DOWN', 7: 'M_RECOVERY', 2: 'M_WEAK', 1: 'M_UP'}.get(ph['phase'], 'M_NA')
    tags = []
    if ph['phase'] == 6: tags.append('PANIC')
    if ph['at_high']: tags.append('NEW_HIGH')
    if ph['bounce_tag']: tags.append('BOUNCE')
    if ph['below20_up']: tags.append('REBOUND20')
    if ph['phase'] == 7: tags.append('RECOVERY_OK')
    return dict(tf=tf, label=lab, dd=ph['dd20'], vs20=ph['vs20'], vs50=ph['vs50'], chg1=ph['chg1'], ret5=ph['chg5'], bounce=ph['bounce'], close=ph['close'],
                in_corr=ph['state'] == 3, phase=ph['phase'], stress=ph['stress'], dd_ref=ph['dd_ref'], long_len=ph['long_len'], tags=tags,
                crash_day=ph['crash_day'], crash_win=ph['crash_win'], hi_long_ok=nn(ph['hi_long']))

# -----------------------------------------------------------------------------
# أهداف الاستثمار (فيبوناتشي + قمم + المحللين + القيمة العادلة) حسب أسلوب الاستثمار
# -----------------------------------------------------------------------------
STYLE_MIN_GAIN = {'Swing': 8.0, 'Growth': 20.0, 'Value': 25.0, 'Medium Term': 30.0, 'Long Term': 40.0}
def invest_targets(price, style, fibL, fibH, w52h, an_mean, an_hi, fair, atr):
    out = {}
    if not (nn(price) and price > 0): return out
    floor_ = price * 1.02; cands = []
    if nn(fibL) and nn(fibH) and fibH > fibL:
        R = fibH - fibL
        for ext, code in ((1.0, 'FIB1000'), (1.272, 'FIB1272'), (1.618, 'FIB1618'), (2.0, 'FIB2000'), (2.618, 'FIB2618'), (3.618, 'FIB3618')):
            lv = fibL + R * ext
            if lv > floor_: cands.append((lv, code))
    fibs = [x for x in cands]
    for lv, code in ((w52h, 'HIGH52'), (an_mean, 'ANALYST'), (an_hi, 'ANALYST_HI'), (fair, 'FAIR')):
        if nn(lv) and lv > floor_: cands.append((lv, code))
    cands.sort(key=lambda x: x[0])
    for k in range(3):
        if k < len(fibs):
            out[f'tg_fib{k + 1}'] = fibs[k][0]; out[f'tg_fib{k + 1}_pct'] = (fibs[k][0] / price - 1) * 100
            out[f'tg_fib{k + 1}_lvl'] = fibs[k][1]
        else:
            out[f'tg_fib{k + 1}'] = NaN; out[f'tg_fib{k + 1}_pct'] = NaN; out[f'tg_fib{k + 1}_lvl'] = ''
    mg = STYLE_MIN_GAIN.get(style, 20.0)
    def pick(minpct):
        thr = price * (1 + minpct / 100)
        for lv, code in cands:
            if lv >= thr: return lv, code
        return thr, 'PCT'
    t1, c1 = pick(mg); t2, c2 = pick(mg * 1.6)
    if t2 <= t1 * 1.01: t2, c2 = t1 * 1.25, 'PCT'
    out.update(tg_inv=t1, tg_inv_pct=(t1 / price - 1) * 100, tg_inv_src=c1, tg_stretch=t2, tg_stretch_pct=(t2 / price - 1) * 100, tg_stretch_src=c2, tg_min_pct=mg)
    out['tg_text'] = ' | '.join(f"{code}:{lv:,.2f} ({(lv / price - 1) * 100:+.0f}%)" for lv, code in cands[:6])
    return out


# -----------------------------------------------------------------------------
# 12) الأعمدة (إنجليزي | عربي) والمجموعات — مطابقة تماماً لتصميم ملف الـHTML المرفق + حقول v6 الجديدة
# -----------------------------------------------------------------------------
COLS = {
 'symbol': ('Symbol', 'الرمز'),
 'name': ('Name', 'الاسم'),
 'market': ('Market', 'السوق'),
 'currency': ('Cur.', 'العملة'),
 'sector': ('Sector', 'القطاع'),
 'industry': ('Industry', 'النشاط'),
 'price': ('Price', 'السعر'),
 'chg': ('Chg%', 'التغير%'),
 'last_date': ('Last bar', 'آخر شمعة'),
 'bars': ('Bars', 'عدد الشموع'),
 'w52h': ('52W High', 'أعلى 52أسبوع'),
 'w52l': ('52W Low', 'أدنى 52أسبوع'),
 'mcap': ('Mkt Cap', 'القيمة السوقية'),
 'beta': ('Beta', 'بيتا'),
 'div_yield': ('Div %', 'العائد %'),
 'uni_score': ('Score', 'الدرجة'),
 'uni_grade': ('Grade', 'التقييم'),
 'uni_decision': ('Final Verdict', 'القرار النهائي'),
 'uni_signal': ('Signal', 'الإشارة'),
 'uni_notes': ('Verdict notes', 'ملاحظات القرار'),
 'auto_style': ('Investment type', 'نوع الاستثمار'),
 'style_used': ('Style used', 'الأسلوب المستخدم'),
 'explain': ('Explanation', 'شرح النتيجة'),
 'mkt_label': ('Index state', 'حالة المؤشر العام'),
 'mkt_tf': ('Index frame', 'إطار المؤشر'),
 'mkt_bench': ('Index', 'المؤشر'),
 'mkt_dd': ('Index vs 20d high %', 'المؤشر عن قمة 20 يوم %'),
 'mkt_vs20': ('Index vs EMA20 %', 'المؤشر عن EMA20 %'),
 'mkt_vs50': ('Index vs EMA50 %', 'المؤشر عن EMA50 %'),
 'mkt_chg1': ('Index day %', 'تغير المؤشر اليوم %'),
 'mkt_ret5': ('Index 5d %', 'المؤشر 5 أيام %'),
 'fv_fair': ('Fair Value', 'القيمة العادلة'),
 'fv_upside': ('Upside to fair %', 'الفرق عن العادلة %'),
 'fv_mos': ('Margin of safety %', 'هامش الأمان %'),
 'fv_verdict': ('Valuation', 'تقييم السعر'),
 'fv_source': ('FV source', 'مصدر التقدير'),
 'fv_models': ('FV models', 'النماذج المستخدمة'),
 'fv_pe': ('P/E model', 'نموذج P/E'),
 'fv_pe_x': ('Fair P/E (x)', 'مضاعف P/E العادل'),
 'fv_graham': ('Graham', 'جراهام'),
 'fv_grahamG': ('Graham-Growth', 'جراهام-نمو'),
 'fv_analyst': ('Analyst target', 'هدف المحللين'),
 'fv_an_hi': ('Analyst high', 'أعلى هدف'),
 'fv_an_lo': ('Analyst low', 'أدنى هدف'),
 'fv_an_n': ('# analysts', 'عدد المحللين'),
 'fv_pb': ('P/B model', 'نموذج P/B (ROE)'),
 'fv_rel': ('Relative model', 'النموذج النسبي'),
 'fv_rel_pe': ('Peer P/E (x)', 'مضاعف الأقران (x)'),
 'fv_rel_scope': ('Peer basis', 'أساس الأقران'),
 'fv_ext': ('External target', 'الهدف الخارجي'),
 'fv_conf': ('FV confidence %', 'ثقة القيمة العادلة %'),
 'fv_low': ('FV range low', 'أدنى القيمة العادلة'),
 'fv_high': ('FV range high', 'أعلى القيمة العادلة'),
 'fv_growth': ('Expected EPS growth %', 'نمو EPS المتوقع %'),
 'fv_quality': ('Quality factor', 'عامل الجودة'),
 'fv_eps_src': ('EPS source', 'مصدر EPS'),
 'mcap_src': ('Mkt cap source', 'مصدر القيمة السوقية'),
 'style_suggest': ('Auto-suggested type', 'النوع المقترح تلقائياً'),
 'style_why': ('Why this type', 'سبب التصنيف'),
 'dp_eps_ttm_g': ('EPS TTM vs FY %', 'نمو EPS (TTM مقابل السنة) %'),
 'zb_low': ('Buy zone low', 'بداية نطاق الدخول'),
 'zb_high': ('Buy zone high', 'نهاية نطاق الدخول'),
 'zb_entry': ('Entry', 'الدخول'),
 'zb_stop': ('Stop', 'الوقف'),
 'zb_stop_pct': ('Stop %', 'الوقف %'),
 'zb_target': ('Target', 'الهدف'),
 'zb_target_pct': ('Target %', 'الهدف %'),
 'zb_rr': ('R:R (1:x)', 'العائد/المخاطرة (1:x)'),
 'zb_dir': ('Direction', 'الاتجاه'),
 'tg_fib1': ('Fib target 1 (1.272)', 'هدف فيبو 1'),
 'tg_fib1_pct': ('Fib 1 %', 'فيبو 1 %'),
 'tg_fib2': ('Fib target 2', 'هدف فيبو 2'),
 'tg_fib2_pct': ('Fib 2 %', 'فيبو 2 %'),
 'tg_fib3': ('Fib target 3', 'هدف فيبو 3'),
 'tg_fib3_pct': ('Fib 3 %', 'فيبو 3 %'),
 'tg_inv': ('Investment target', 'هدف الاستثمار (حسب الأسلوب)'),
 'tg_inv_pct': ('Inv. target %', 'هدف الاستثمار %'),
 'tg_inv_src': ('Target source', 'مصدر الهدف'),
 'tg_stretch': ('Extended target', 'الهدف الممتد'),
 'tg_stretch_pct': ('Extended %', 'الهدف الممتد %'),
 'tg_stretch_src': ('Ext. source', 'مصدر الممتد'),
 'tg_min_pct': ('Min. goal % (style)', 'الحد الأدنى المطلوب % (للأسلوب)'),
 'tg_text': ('All target levels', 'كل مستويات الأهداف'),
 'base_score': ('Quick score', 'درجة الفحص السريع'),
 'base_rating': ('Quick rating', 'التصنيف السريع'),
 'base_decision': ('Quick decision', 'القرار السريع'),
 'base_trend': ('Trend%', 'الاتجاه%'),
 'base_cmf': ('CMF', 'CMF'),
 'base_rsi': ('RSI(14)', 'RSI(14)'),
 'base_rs': ('RS Score', 'القوة النسبية'),
 'base_vwap': ('VWAP Position', 'موقع VWAP'),
 'base_support': ('Support (20)', 'دعم (20)'),
 'base_resistance': ('Resistance (20)', 'مقاومة (20)'),
 'vol_ann': ('Volatility %', 'التذبذب السنوي %'),
 'px_final': ('Technical decision', 'القرار الفني'),
 'px_signal': ('Signal now', 'إشارة الآن'),
 'px_signal_age': ('Bars since signal', 'شموع منذ الإشارة'),
 'px_regime': ('Regime', 'نظام السوق'),
 'px_chop': ('Chop Zone', 'Chop'),
 'px_regime_mult': ('Regime mult.', 'معاملات النظام'),
 'px_buy_score': ('BUY points', 'نقاط الشراء'),
 'px_buy_pct': ('BUY %', 'نسبة الشراء%'),
 'px_buy_grade': ('BUY Grade', 'تقييم الشراء'),
 'px_buy_cats': ('BUY cats /7', 'فئات الشراء /7'),
 'px_sell_score': ('SELL points', 'نقاط البيع'),
 'px_sell_pct': ('SELL %', 'نسبة البيع%'),
 'px_sell_grade': ('SELL Grade', 'تقييم البيع'),
 'px_sell_cats': ('SELL cats /7', 'فئات البيع /7'),
 'px_max_score': ('Max points', 'الحد الأقصى'),
 'px_cat_buy': ('Buy cats T/M/V/S/L/SMC/P', 'فئات الشراء'),
 'px_cat_sell': ('Sell cats T/M/V/S/L/SMC/P', 'فئات البيع'),
 'px_state': ('Market activity', 'نشاط السوق'),
 'px_mtf_mode': ('MTF mode', 'وضع الأطر'),
 'px_h1': ('H1 (or D1)', 'H1 (أو D1)'),
 'px_h4': ('H4 (or W1)', 'H4 (أو W1)'),
 'px_matrix': ('MTF matrix', 'مصفوفة الأطر'),
 'px_matrix_frames': ('Frames', 'الأطر'),
 'px_mtf_label': ('MTF verdict', 'حكم الأطر'),
 'px_vwap': ('VWAP', 'VWAP'),
 'px_vwap_val': ('VWAP value', 'قيمة VWAP'),
 'px_vpoc': ('VPOC (approx)', 'VPOC (تقريبي)'),
 'px_support': ('Support', 'أقرب دعم'),
 'px_resistance': ('Resistance', 'أقرب مقاومة'),
 'px_pdh': ('PDH', 'PDH'),
 'px_pdl': ('PDL', 'PDL'),
 'px_rs_label': ('Relative Strength', 'القوة النسبية'),
 'px_rs_detail': ('RS Detail', 'تفاصيل RS'),
 'px_sweep': ('Liquidity sweep', 'اصطياد السيولة'),
 'px_div': ('Divergence', 'الدايفرجنس'),
 'px_squeeze': ('Squeeze', 'انكماش بولينجر'),
 'px_cmf': ('CMF', 'CMF'),
 'px_location': ('Location', 'الموقع'),
 'px_near': ('Near Zones', 'مناطق قريبة'),
 'px_struct_conf': ('Structure (confirmed)', 'الهيكل (مؤكد)'),
 'px_struct_live': ('Structure (live)', 'الهيكل (لحظي)'),
 'px_last_break': ('Last BOS/CHoCH', 'آخر كسر هيكل'),
 'px_smc_counts': ('Structure breaks', 'عدّادات كسر الهيكل'),
 'px_fib': ('Fib status', 'حالة فيبو'),
 'px_fibH': ('Fib swing high', 'قمة الموجة'),
 'px_fibL': ('Fib swing low', 'قاع الموجة'),
 'px_corr': ('Correlation (DXY)', 'الارتباط (DXY)'),
 'px_macd_hist': ('MACD Hist', 'MACD Hist'),
 'px_pos_units': ('Position size (units)', 'حجم الصفقة'),
 'px_risk_amt': ('Risk amount', 'مبلغ المخاطرة'),
 'px_atr': ('ATR', 'ATR'),
 'px_ema': ('EMA fast', 'EMA السريع'),
 'px_sma': ('SMA slow', 'SMA البطيء'),
 'px_wma': ('WMA 52', 'WMA 52'),
 'px_st': ('SuperTrend', 'SuperTrend'),
 'px_st_dir': ('ST dir', 'اتجاه ST'),
 'px_rsi_f': ('RSI fast', 'RSI السريع'),
 'px_rsi_s': ('RSI slow', 'RSI البطيء'),
 'px_stoch': ('Stoch K', 'Stoch K'),
 'px_ao': ('AO', 'AO'),
 'px_patterns': ('Candle patterns', 'أنماط الشموع'),
 'vt_state': ('Trade state', 'حالة الصفقة'),
 'vt_dir': ('Dir', 'الاتجاه'),
 'vt_entry': ('Entry', 'الدخول'),
 'vt_sl': ('SL', 'الوقف'),
 'vt_tp1': ('TP1', 'الهدف1'),
 'vt_tp2': ('TP2', 'الهدف2'),
 'vt_tp3': ('TP3', 'الهدف3'),
 'vt_hit': ('Targets hit', 'أهداف محققة'),
 'vt_be': ('Stop at breakeven', 'الوقف عند التعادل'),
 'vt_mfe': ('MFE', 'أقصى ربح عائم'),
 'vt_mae': ('MAE', 'أقصى خسارة عائمة'),
 'vt_record': ('Record', 'السجل'),
 'vt_opened': ('Opened trades', 'صفقات مفتوحة'),
 'vt_closed': ('Closed trades', 'صفقات مغلقة'),
 'vt_win_rate': ('Win rate %', 'نسبة الربح%'),
 'vt_pf': ('PF', 'PF'),
 'vt_avg_r': ('Avg R', 'متوسط R'),
 'vt_reached': ('Targets reached', 'الوصول للأهداف'),
 'vt_last_outcome': ('Last result', 'آخر نتيجة'),
 'vt_last_r': ('Last R', 'آخر R'),
 'rd_style': ('Style', 'الأسلوب'),
 'rd_tf': ('TF', 'الإطار'),
 'rd_score': ('Score', 'الدرجة'),
 'rd_inv': ('Invest score', 'درجة الاستثمار'),
 'rd_entry': ('Entry score', 'درجة الدخول'),
 'rd_tech': ('Tech', 'فني'),
 'rd_rating': ('Rating', 'التقييم'),
 'rd_reasons': ('Reasons', 'الأسباب'),
 'rd_reasons_full': ('Reasons/Risk', 'الأسباب/المخاطر'),
 'rd_sig': ('Sig', 'إشارة'),
 'rd_stop': ('Stop', 'وقف'),
 'rd_target': ('Target', 'هدف'),
 'rd_tgt_src': ('Target src', 'مصدر الهدف'),
 'rd_rr': ('R:R', 'R:R'),
 'rd_qty': ('Size', 'الكمية'),
 'rd_peer': ('vsPeer', 'نسبي/أقران'),
 'rd_peer_txt': ('vsPeer', 'نسبي/أقران'),
 'rd_peer_src': ('Peer src', 'مصدر الأقران'),
 'rd_adx': ('ADX', 'ADX'),
 'rd_bbpb': ('BB %B', 'BB %B'),
 'rd_gap': ('Gap %', 'فجوة %'),
 'rd_atr_pct': ('ATR %', 'ATR %'),
 'rd_risk': ('Risk', 'المخاطرة'),
 'rd_traded': ('Avg traded value', 'متوسط قيمة التداول'),
 'rd_dist_sup': ('Dist. from support %', 'البعد عن الدعم %'),
 'dp_align': ('Align', 'توافق'),
 'dp_inv': ('Inv%', 'استثمار%'),
 'dp_ent': ('Ent%', 'دخول%'),
 'dp_conf': ('Conf%', 'ثقة%'),
 'dp_pe': ('P/E', 'P/E'),
 'dp_pb': ('P/B', 'P/B'),
 'dp_flags': ('Flags', 'أعلام'),
 'dp_status': ('Deep decision', 'قرار التحليل العميق'),
 'dp_decision': ('Decision', 'القرار'),
 'dp_guard': ('Guard', 'الحارس'),
 'dp_risk': ('Deep risk', 'مخاطرة التحليل العميق'),
 'dp_qual': ('Quality', 'الجودة'),
 'dp_growth': ('Growth', 'النمو'),
 'dp_valscore': ('Value score', 'درجة التقييم'),
 'dp_roe': ('ROE %', 'ROE %'),
 'dp_piotroski': ('Piotroski', 'Piotroski'),
 'dp_altman': ('Altman Z', 'Altman Z'),
 'dp_beneish': ('Beneish M', 'Beneish M'),
 'dp_eps_g': ('EPS growth %', 'نمو EPS %'),
 'dp_eps': ('EPS (TTM)', 'EPS'),
 'dp_bvps': ('BVPS', 'القيمة الدفترية'),
 'dp_fcf': ('FCF margin %', 'هامش FCF %'),
 'dp_fwd_pe': ('Fwd P/E', 'P/E المتوقع'),
 'sc_ema': ('EMA/SMA', 'EMA/SMA'),
 'sc_rsi': ('RSI', 'RSI'),
 'sc_st': ('ST', 'ST'),
 'sc_chop': ('Chop', 'Chop'),
 'sc_regime': ('Regime', 'النظام'),
 'sc_signal': ('Signal', 'الإشارة'),
 'sc_str': ('Str', 'القوة'),
 'sc_sync': ('Sync', 'المزامنة'),
 'zb_rr_mkt': ('R:R at market price', 'R:R عند سعر السوق'),
 'rd_rr_mkt': ('R:R at market', 'R:R عند سعر السوق'),
 'rd_fib': ('Fib targets', 'أهداف فيبو'),
}

GROUPS = {
 'summary': ('Summary', 'الملخص', ['symbol', 'name', 'market', 'price', 'chg', 'uni_score', 'uni_grade', 'uni_decision', 'mkt_label', 'fv_fair', 'fv_upside', 'fv_verdict', 'fv_conf', 'zb_low', 'zb_high', 'zb_entry', 'zb_stop', 'zb_stop_pct', 'zb_target', 'zb_target_pct', 'zb_rr', 'zb_rr_mkt', 'tg_inv', 'tg_inv_pct', 'px_final', 'rd_rating', 'dp_decision', 'auto_style', 'uni_notes']),
 'radar': ('Investment Radar', 'الرادار الاستثماري', ['symbol', 'price', 'chg', 'rd_score', 'rd_tech', 'rd_rating', 'rd_reasons_full', 'rd_sig', 'rd_stop', 'rd_target', 'rd_rr', 'rd_rr_mkt', 'rd_qty', 'rd_peer_txt', 'dp_align', 'dp_inv', 'dp_ent', 'dp_conf', 'dp_pe', 'dp_pb', 'dp_flags', 'dp_decision', 'rd_style', 'rd_tf', 'rd_inv', 'rd_entry', 'rd_tgt_src', 'rd_peer', 'rd_peer_src', 'rd_adx', 'rd_bbpb', 'rd_gap', 'rd_atr_pct', 'rd_risk', 'rd_traded', 'rd_dist_sup']),
 'technical': ('Technical Analysis', 'التحليل الفني', ['symbol', 'price', 'px_final', 'px_signal', 'px_signal_age', 'px_regime', 'px_chop', 'px_regime_mult', 'px_buy_score', 'px_buy_pct', 'px_buy_grade', 'px_buy_cats', 'px_sell_score', 'px_sell_pct', 'px_sell_grade', 'px_sell_cats', 'px_max_score', 'px_cat_buy', 'px_cat_sell', 'px_state', 'px_mtf_mode', 'px_h1', 'px_h4', 'px_matrix', 'px_matrix_frames', 'px_mtf_label', 'px_vwap', 'px_vwap_val', 'px_vpoc', 'px_support', 'px_resistance', 'px_pdh', 'px_pdl', 'px_rs_label', 'px_rs_detail', 'px_sweep', 'px_div', 'px_squeeze', 'px_cmf', 'px_location', 'px_near', 'px_struct_conf', 'px_struct_live', 'px_last_break', 'px_smc_counts', 'px_fib', 'px_fibH', 'px_fibL', 'px_corr', 'px_macd_hist', 'px_pos_units', 'px_risk_amt', 'px_atr', 'px_ema', 'px_sma', 'px_wma', 'px_st', 'px_st_dir', 'px_rsi_f', 'px_rsi_s', 'px_stoch', 'px_ao', 'px_patterns']),
 'fair': ('Fair Value & Deep Analysis', 'القيمة العادلة والتحليل العميق', ['symbol', 'price', 'fv_fair', 'fv_upside', 'fv_mos', 'fv_verdict', 'fv_source', 'fv_models', 'fv_pe', 'fv_pe_x', 'fv_graham', 'fv_grahamG', 'fv_analyst', 'fv_pb', 'fv_rel', 'fv_rel_pe', 'fv_rel_scope', 'fv_ext', 'fv_an_hi', 'fv_an_lo', 'fv_an_n', 'fv_conf', 'fv_low', 'fv_high', 'fv_growth', 'fv_quality', 'fv_eps_src', 'mcap_src', 'dp_align', 'dp_inv', 'dp_ent', 'dp_conf', 'dp_pe', 'dp_pb', 'dp_fwd_pe', 'dp_flags', 'dp_decision', 'dp_guard', 'dp_risk', 'dp_qual', 'dp_growth', 'dp_valscore', 'dp_roe', 'dp_piotroski', 'dp_altman', 'dp_beneish', 'dp_eps_g', 'dp_eps_ttm_g', 'dp_eps', 'dp_bvps', 'dp_fcf', 'mcap', 'beta', 'div_yield', 'w52h', 'w52l']),
 'targets': ('Targets', 'الأهداف', ['symbol', 'price', 'uni_decision', 'style_used', 'zb_entry', 'zb_stop', 'zb_target', 'zb_target_pct', 'zb_rr_mkt', 'rd_target', 'tg_fib1', 'tg_fib1_pct', 'tg_fib2', 'tg_fib2_pct', 'tg_fib3', 'tg_fib3_pct', 'tg_min_pct', 'tg_inv', 'tg_inv_pct', 'tg_inv_src', 'tg_stretch', 'tg_stretch_pct', 'tg_stretch_src', 'fv_fair', 'fv_analyst', 'fv_an_hi', 'w52h', 'tg_text']),
 'market': ('Index State', 'حالة المؤشر العام', ['symbol', 'market', 'mkt_bench', 'mkt_label', 'mkt_tf', 'mkt_dd', 'mkt_vs20', 'mkt_vs50', 'mkt_chg1', 'mkt_ret5']),
 'simulated': ('Simulated Trade', 'الصفقة الافتراضية', ['symbol', 'price', 'vt_state', 'vt_dir', 'vt_entry', 'vt_sl', 'vt_tp1', 'vt_tp2', 'vt_tp3', 'vt_hit', 'vt_be', 'vt_mfe', 'vt_mae', 'vt_record', 'vt_opened', 'vt_closed', 'vt_win_rate', 'vt_pf', 'vt_avg_r', 'vt_reached', 'vt_last_outcome', 'vt_last_r']),
 'scanner': ('Quick Scanner', 'الماسح السريع', ['symbol', 'price', 'chg', 'sc_ema', 'sc_rsi', 'sc_st', 'sc_chop', 'sc_regime', 'sc_signal', 'sc_str', 'sc_sync']),
 'original': ('Quick Scan', 'الفحص السريع', ['symbol', 'price', 'chg', 'base_score', 'base_rating', 'base_decision', 'auto_style', 'style_suggest', 'style_why', 'base_trend', 'base_cmf', 'base_rsi', 'base_rs', 'base_vwap', 'base_support', 'base_resistance', 'vol_ann']),
 'explain': ('Explanation', 'شرح النتائج', ['symbol', 'name', 'uni_decision', 'uni_score', 'explain']),
}
GROUP_ORDER = ['summary', 'radar', 'technical', 'fair', 'targets', 'market', 'simulated', 'scanner', 'original', 'explain']

def active_groups(res):
    sim = res['meta']['p'].get('vtOn', True)
    return [g for g in GROUP_ORDER if g != 'simulated' or sim]

def hdr(key, lang):
    en, ar = COLS.get(key, (key, key))
    return ar if lang == 'عربي' else en

DEC_COLOR = {'STRONG BUY': '#00c853', 'BUY DIP': '#2979ff', 'WATCH': '#ffb300', 'AVOID': '#9e9e9e', 'SELL': '#e53935'}
DEC_NAME = {'STRONG BUY': ('Strong Buy', 'شراء قوي'), 'BUY DIP': ('Buy on dip', 'شراء عند التراجع'), 'WATCH': ('Watch', 'متابعة'),
            'AVOID': ('Avoid', 'تجنّب'), 'SELL': ('Sell / Avoid', 'بيع / تجنّب')}
TECH_NAME = {'T_BUY': ('BUY signal', 'شراء (إشارة دخول)'), 'T_SELL': ('SELL signal', 'بيع (إشارة خروج)'), 'T_WATCH_UP': ('Watch – bullish bias', 'متابعة – ميل صعودي'),
             'T_WATCH_DOWN': ('Watch – bearish bias', 'متابعة – ميل هبوطي'), 'T_WAIT': ('Wait', 'انتظار'), 'T_AVOID': ('Avoid', 'تجنّب'), 'IN TRADE': ('Running virtual trade', 'صفقة افتراضية جارية')}
MKT_NAME = {'M_UP': ('Healthy / uptrend', 'صحي / صعود'), 'M_NEUTRAL': ('Sideways / neutral', 'عرضي / محايد'), 'M_WEAK': ('Weak (below EMA20)', 'ضعف (تحت EMA20)'),
            'M_REBOUND': ('Rebound (unconfirmed)', 'ارتداد (غير مؤكد)'), 'M_DOWN': ('Pullback / downtrend', 'تراجع / اتجاه هابط'), 'M_CORR': ('Correction', 'تصحيح'),
            'M_BEAR': ('Bear market', 'سوق هابط'), 'M_RECOVERY': ('Recovery', 'تعافٍ'),
            'M_CRASH': ('Market crash', 'انهيار السوق'), 'M_NA': ('N/A', 'غير متاح')}
MKT_ICON = {'M_UP': '🟢', 'M_NEUTRAL': '🟡', 'M_WEAK': '🟡', 'M_REBOUND': '🟠', 'M_DOWN': '🟠', 'M_CORR': '🔴', 'M_BEAR': '🐻', 'M_RECOVERY': '🔵', 'M_CRASH': '🚨', 'M_NA': '⚪'}
MKT_COLOR = {'M_UP': '#e6f9ee', 'M_NEUTRAL': '#fff9e0', 'M_WEAK': '#fff6d6', 'M_REBOUND': '#fff1dc', 'M_DOWN': '#ffe9cf', 'M_CORR': '#ffe3e3', 'M_BEAR': '#ffd6dc', 'M_RECOVERY': '#e1f1ff', 'M_CRASH': '#ffc9c9', 'M_NA': '#eeeeee'}
MKT_TAG = {'PANIC': ('⚡ Panic move', '⚡ حركة ذعر'), 'NEW_HIGH': ('🚀 New high', '🚀 قمة جديدة'), 'BOUNCE': ('↗ Bounce — unconfirmed (below EMA50, dead-cat risk)', '↗ ارتداد غير مؤكد (تحت EMA50 — خطر Dead-cat)'),
           'REBOUND20': ('↗ Rebound below EMA20 — unconfirmed', '↗ ارتداد تحت EMA20 — غير مؤكد'), 'RECOVERY_OK': ('✔ Back above EMA50 after a ≥ correction-size drawdown', '✔ عاد فوق EMA50 بعد هبوط بحجم التصحيح')}
BENCH_NAME = {'^NDX': ('Nasdaq 100', 'ناسداك 100'), '^GSPC': ('S&P 500', 'S&P 500'), '^DJI': ('Dow Jones', 'داو جونز'), '^IXIC': ('Nasdaq Composite', 'ناسداك المركب'),
              '^CASE30': ('EGX 30', 'EGX 30'), '^TASI.SR': ('TASI', 'تاسي'), 'BTC-USD': ('Bitcoin', 'بيتكوين'), 'GC=F': ('Gold', 'الذهب'), 'DX-Y.NYB': ('DXY', 'مؤشر الدولار'), '^EGX70EWI.CA': ('EGX 70 EWI', 'EGX 70'), '^EGX100EWI.CA': ('EGX 100 EWI', 'EGX 100'),
              '^EGXSHARIAH.CA': ('EGX Shariah', 'EGX الشريعة'), '^CCSI': ('EGX 70 (alt)', 'EGX 70 (بديل)'),
              'KSA': ('iShares MSCI Saudi', 'صندوق السعودية'), 'EGPT': ('VanEck Egypt', 'صندوق مصر')}
MARKET_NAME = {'US': ('US', 'أمريكا'), 'EGX': ('Egypt', 'مصر'), 'TASI': ('Saudi', 'السعودية'),
               'CRYPTO': ('Crypto', 'عملات رقمية'), 'FX': ('Forex', 'فوركس'), 'CMDTY': ('Commodities', 'معادن وسلع')}
SECTOR_AR = {'Technology': 'التقنية', 'Financial Services': 'الخدمات المالية', 'Energy': 'الطاقة', 'Healthcare': 'الرعاية الصحية', 'Consumer Cyclical': 'السلع الاستهلاكية الدورية',
             'Consumer Defensive': 'السلع الاستهلاكية الأساسية', 'Industrials': 'الصناعة', 'Basic Materials': 'المواد الأساسية', 'Real Estate': 'العقارات', 'Utilities': 'المرافق',
             'Communication Services': 'خدمات الاتصالات'}
STYLE_NAME = {'Value': ('Value', 'قيمة'), 'Growth': ('Growth', 'نمو'), 'Swing': ('Swing', 'مضاربة'), 'Medium Term': ('Medium Term', 'مدى متوسط'), 'Long Term': ('Long Term', 'مدى طويل')}
STYLE_ICON = {'Value': '💰', 'Growth': '📈', 'Swing': '⚡', 'Medium Term': '📊', 'Long Term': '🏛️'}
TGT_SRC = {'FIB1000': ('Swing high (Fib 1.0)', 'قمة الموجة (فيبو 1.0)'), 'FIB1272': ('Fib 1.272', 'فيبو 1.272'), 'FIB1618': ('Fib 1.618', 'فيبو 1.618'), 'FIB2000': ('Fib 2.0', 'فيبو 2.0'),
           'FIB2618': ('Fib 2.618', 'فيبو 2.618'), 'FIB3618': ('Fib 3.618', 'فيبو 3.618'), 'HIGH52': ('52-week high', 'أعلى 52 أسبوع'), 'ANALYST': ('Analyst mean', 'متوسط المحللين'),
           'ANALYST_HI': ('Analyst high', 'أعلى هدف للمحللين'), 'FAIR': ('Fair value', 'القيمة العادلة'), 'PCT': ('Style goal %', 'نسبة هدف الأسلوب')}
NOTE_NAME = dict(NOTE_CODE)   # 🆕 v6: نفس رموز الملاحظات الموحدة (تُترجم للعرض)

ALIGN_TXT2 = {2: ('✅ Full', '✅ توافق كامل'), 1: ('🟡 Partial', '🟡 جزئي'), -1: ('⚠️ Conflict', '⚠️ تعارض'), -2: ('⛔ Both negative', '⛔ سلبي معاً'), 5: ('⚪ Tech only', '⚪ فني فقط'), 9: ('—', '—')}

# رموز النص → (إنجليزي، عربي)
TOK = {
 'STRONG BUY': ('STRONG BUY', 'شراء قوي'), 'BUY DIP': ('BUY DIP', 'شراء عند التراجع'), 'WATCH / WAIT': ('WATCH / WAIT', 'متابعة / انتظار'), 'WATCH': ('WATCH', 'متابعة'), 'AVOID': ('AVOID', 'تجنّب'),
 'BUY': ('BUY', 'شراء'), 'SELL': ('SELL', 'بيع'), 'None': ('None', 'لا يوجد'), 'N/A': ('N/A', 'غير متاح'),
 'STRONG_BUY': ('🟢 STRONG BUY', '🟢 شراء قوي'), 'BUY_DIP': ('🔵 BUY DIP', '🔵 شراء عند التراجع'), 'WATCHLIST': ('🟡 WATCH', '🟡 متابعة'), 'INSUFFICIENT_DATA': ('⚪ NO DATA', '⚪ بيانات ناقصة'),
 'WAIT_ENTRY': ('🟠 WAIT ENTRY', '🟠 انتظر الدخول'), 'AVOID_': ('🔴 AVOID', '🔴 تجنّب'),
 'Strong Trend': ('Strong Trend', 'اتجاه قوي'), 'Choppy': ('Choppy', 'متذبذب'), 'Calm': ('Calm', 'هادئ'), 'Trending': ('Trending', 'اتجاهي'), 'Neutral': ('Neutral', 'محايد'),
 'High Activity': ('High Activity', 'نشاط عالٍ'), 'Low Liquidity': ('Low Liquidity', 'سيولة ضعيفة'), 'Normal Activity': ('Normal Activity', 'نشاط طبيعي'),
 'STRONG CONFIRMED': ('STRONG CONFIRMED', 'تأكيد قوي'), 'AGAINST TREND': ('AGAINST TREND', 'عكس الاتجاه'), 'MIXED': ('MIXED', 'متباين'),
 'Above': ('Above', 'فوق'), 'Below': ('Below', 'تحت'), 'Premium': ('Premium', 'منطقة غالية'), 'Discount': ('Discount', 'منطقة رخيصة'), 'Equilibrium': ('Equilibrium', 'توازن'),
 'No Nearby Zones': ('No Nearby Zones', 'لا مناطق قريبة'), 'Bullish': ('Bullish', 'صاعد'), 'Bearish': ('Bearish', 'هابط'),
 'Fib Confirmed': ('Fib Confirmed', 'فيبو مؤكد'), 'Fib Fallback': ('Fib Fallback', 'فيبو بديل (50 شمعة)'),
 'Bull Sweep': ('Bull Sweep', 'اصطياد سيولة صاعد'), 'Bear Sweep': ('Bear Sweep', 'اصطياد سيولة هابط'), 'Bull Div': ('Bull Div', 'دايفرجنس صاعد'), 'Bear Div': ('Bear Div', 'دايفرجنس هابط'),
 'Active Squeeze': ('Active Squeeze', 'انكماش نشط'), 'Release': ('Release', 'انفلات'), 'Normal': ('Normal', 'طبيعي'),
 'Stronger': ('Stronger', 'أقوى من المرجع'), 'Weaker': ('Weaker', 'أضعف من المرجع'), 'Up': ('Up', 'صاعد'), 'Down': ('Down', 'هابط'),
 'RUNNING': ('RUNNING', 'جارية'), 'CLOSED': ('CLOSED', 'مغلقة'), 'WAITING': ('WAITING', 'بانتظار إشارة'), 'WIN': ('WIN', 'ربح'), 'LOSS': ('LOSS', 'خسارة'), 'BE': ('BE', 'تعادل'), 'AMBIGUOUS': ('AMBIGUOUS', 'غامض'),
 'TP1': ('TP1', 'الهدف1'), 'TP2': ('TP2', 'الهدف2'), 'TP3': ('TP3', 'الهدف3'), 'LONG': ('LONG', 'شراء'), 'SHORT': ('SHORT', 'بيع'),
 'Strong Inv.': ('Strong Inv.', 'استثمار قوي'), 'High Pot.': ('High Pot.', 'إمكانات عالية'), 'Watchlist': ('Watchlist', 'قائمة مراقبة'), 'Weak Str.': ('Weak Str.', 'هيكل ضعيف'), 'Avoid': ('Avoid', 'تجنّب'),
 'Conf': ('Conf', 'مؤكد'), 'Dev': ('Dev', 'قيد التكوّن'), 'No': ('No', 'لا'),
 'Trend↑': ('Trend↑', 'اتجاه↑'), 'RS+': ('RS+', 'قوة نسبية+'), 'CMF+': ('CMF+', 'سيولة+'), 'Vol+': ('Vol+', 'حجم+'), 'NearSup': ('NearSup', 'قرب دعم'), 'Accum': ('Accum', 'تجميع'),
 'ADX+': ('ADX+', 'اتجاه قوي+'), 'BB-Low': ('BB-Low', 'بولينجر سفلي'), 'BB-High': ('BB-High', 'بولينجر علوي'), 'GapUp': ('GapUp', 'فجوة صاعدة'), 'GapDn': ('GapDn', 'فجوة هابطة'),
 'Crash': ('Crash', 'انهيار'), 'Break': ('Break', 'كسر'), 'Dip?': ('Dip?', 'تراجع محتمل؟'), 'LowLiq': ('LowLiq', 'سيولة ضعيفة'),
 'Low': ('Low', 'منخفضة'), 'Medium': ('Medium', 'متوسطة'), 'High': ('High', 'عالية'), 'Risk:': ('Risk:', 'المخاطرة:'), 'Guard:': ('Guard:', 'الحارس:'),
 'MktCorrection': ('MktCorrection', 'تصحيح السوق'), 'Tech≠Conf': ('Tech≠Conf', 'الفني غير مؤكد'), 'Risk≥': ('Risk≥', 'مخاطرة≥'), 'Chase≥': ('Chase≥', 'مطاردة≥'),
 'Sec': ('Sec', 'القطاع'), 'All': ('All', 'الكل'), 'Fundamental': ('Fundamental', 'مالي'), 'Technical estimate': ('Technical estimate', 'تقدير فني'),
 'Undervalued': ('Undervalued', 'رخيص'), 'Fair': ('Fair', 'عادل'), 'Overvalued': ('Overvalued', 'مرتفع'),
 'Analysts': ('Analysts', 'المحللين'), 'INTRADAY': ('INTRADAY', 'لحظي'), 'PROXY': ('PROXY', 'بديل يومي/أسبوعي/شهري'), 'Rating': ('Rating', 'التقييم'),
 'Hammer': ('Hammer', 'مطرقة'), 'InvHammer': ('InvHammer', 'مطرقة مقلوبة'), 'BullEngulf': ('BullEngulf', 'ابتلاع صاعد'), 'MorningStar': ('MorningStar', 'نجمة الصباح'),
 'HangingMan': ('HangingMan', 'الرجل المشنوق'), 'ShootingStar': ('ShootingStar', 'الشهاب'), 'BearEngulf': ('BearEngulf', 'ابتلاع هابط'), 'EveningStar': ('EveningStar', 'نجمة المساء'),
 'Doji': ('Doji', 'دوجي'), 'Marubozu': ('Marubozu', 'ماروبوزو'), 'EQH': ('EQH', 'قمم متساوية'), 'EQL': ('EQL', 'قيعان متساوية'),
 'Value': ('Value', 'قيمة'), 'Growth': ('Growth', 'نمو'), 'Swing': ('Swing', 'مضاربة'), 'Medium Term': ('Medium Term', 'مدى متوسط'), 'Long Term': ('Long Term', 'مدى طويل'),
 'Strong Buy': ('Strong Buy', 'شراء قوي'), 'Buy Dip': ('Buy Dip', 'شراء عند التراجع'), 'Fib': ('Fib', 'فيبو'),
 'NoVol': ('NoVol', 'بلا حجم تداول'), 'ShortHist': ('ShortHist', 'تاريخ أقل من 200 شمعة'), 'Dist': ('Dist', 'تصريف'),
 'N_GUARD_RISK': NOTE_CODE['N_GUARD_RISK'], 'N_GUARD_CHASE': NOTE_CODE['N_GUARD_CHASE'], 'N_GUARD_TECH': NOTE_CODE['N_GUARD_TECH'],
 'N_SELL_VS_SCORE': NOTE_CODE['N_SELL_VS_SCORE'],
}
for _k, (_e, _a) in list(TECH_NAME.items()): TOK[_k] = (_e, _a)
for _k, (_e, _a) in list(MKT_NAME.items()): TOK[_k] = (_e, _a)
for _k, (_e, _a) in list(TGT_SRC.items()): TOK[_k] = (_e, _a)
for _k, (_e, _a) in list(NOTE_NAME.items()): TOK[_k] = (_e, _a)
TOK['STANDBY'] = ('STANDBY', 'انتظار')
TOK['Deep Value'] = ('Deep Value', 'خصم كبير'); TOK['Rich'] = ('Rich', 'غالٍ جداً'); TOK['External'] = ('External', 'خارجي'); TOK['External+Fundamental'] = ('External+Fundamental', 'خارجي + مالي'); TOK['Relative'] = ('Relative', 'نسبي')      # 🆕 v6.6: حالة الماسح «انتظار»
_TOK_RX = {}
HIDDEN = ('rd_tags', 'rd_risk_key', 'mkt_class', 'mkt_state_n', 'uni_note_codes', 'dp_guard_keys', 'guard_keys', 'fv_verdict_en',
        'explain_ar', 'explain_en', 'explain_short_ar', 'explain_short_en', 'explain_mid_ar', 'explain_mid_en', 'uni_reasons',
        'uni_reasons_ar', 'uni_reasons_en', 'gap_ok', 'fib_src', 'fib_lo', 'fib_hi', 'fib_n', 'fib_m1', 'fib_m2', 'fib_m3',
        'rd_fib', 'rd_fib1', 'rd_fib1_pct', 'rd_fib2', 'rd_fib2_pct', 'rd_fib3', 'rd_fib3_pct', 'sector_note_ar', 'sector_note_en', 'asset',
        'chg20', 'dp_guard_ar', 'dp_guard_en', 'mkt_rebound', 'rd_atr', 'rd_ema50', 'rd_macdL', 'rd_macdS', 'rd_rsi', 'rd_trend', 'sc_chg')
_TOK_RX = {}
def _tok_regex(lang):
    if lang in _TOK_RX: return _TOK_RX[lang]
    idx = 1 if lang == 'عربي' else 0
    keys = [k for k in TOK if (lang == 'عربي' or TOK[k][0] != k)]
    keys.sort(key=len, reverse=True)
    rx = re.compile('(?<![A-Za-z_])(' + '|'.join(re.escape(k) for k in keys) + r')(?![A-Za-z_])') if keys else None
    _TOK_RX[lang] = (rx, idx); return _TOK_RX[lang]
def trtext(s, lang):
    if not isinstance(s, str) or not s: return s
    rx, idx = _tok_regex(lang)
    return rx.sub(lambda m: TOK[m.group(1)][idx], s) if rx else s

# -----------------------------------------------------------------------------
# تنسيق الأرقام + تحويل أي خلية إلى نص معروض باللغة المختارة
# -----------------------------------------------------------------------------
PCT_SIGNED = {'chg', 'zb_stop_pct', 'zb_target_pct', 'fv_upside', 'rd_peer', 'rd_gap', 'mkt_dd', 'mkt_vs20', 'mkt_vs50', 'mkt_chg1', 'mkt_ret5', 'tg_fib1_pct', 'tg_fib2_pct', 'tg_fib3_pct', 'tg_inv_pct', 'tg_stretch_pct'}
PCT_PLAIN = {'fv_conf', 'fv_growth', 'dp_eps_ttm_g', 'fv_mos', 'vt_win_rate', 'rd_atr_pct', 'dp_eps_g', 'dp_roe', 'vol_ann', 'dp_fcf', 'div_yield', 'tg_min_pct', 'px_buy_pct', 'px_sell_pct', 'dp_inv', 'dp_ent', 'dp_conf'}
PRICE_KEYS = {'price', 'zb_low', 'zb_high', 'zb_entry', 'zb_stop', 'zb_target', 'fv_fair', 'vt_entry', 'vt_sl', 'vt_tp1', 'vt_tp2', 'vt_tp3', 'rd_stop', 'rd_target', 'px_support', 'px_resistance',
              'px_pdh', 'px_pdl', 'px_vpoc', 'px_vwap_val', 'px_fibH', 'px_fibL', 'px_st', 'px_ema', 'px_sma', 'px_wma', 'fv_pe', 'fv_graham', 'fv_grahamG', 'fv_analyst', 'fv_an_hi', 'fv_an_lo', 'fv_low', 'fv_high', 'fv_pb', 'fv_rel', 'fv_ext',
              'base_support', 'base_resistance', 'w52h', 'w52l', 'px_atr', 'tg_fib1', 'tg_fib2', 'tg_fib3', 'tg_inv', 'tg_stretch', 'dp_eps', 'dp_bvps'}
def fmt_cell(key, v):
    if v is None: return '—'
    if isinstance(v, (bool, np.bool_)): return '✔' if v else '—'
    if isinstance(v, (int, np.integer)): return str(v)
    if isinstance(v, (float, np.floating)):
        if math.isinf(v): return '∞'
        if v != v: return '—'
        if key in ('mcap', 'rd_traded'): return f'{v / 1e9:,.2f}B' if abs(v) >= 1e9 else f'{v / 1e6:,.1f}M' if abs(v) >= 1e6 else f'{v:,.0f}'
        if key in PCT_SIGNED: return f'{v:+.2f}%'
        if key in PCT_PLAIN: return f'{v:.1f}%'
        if key in PRICE_KEYS: return f'{v:,.2f}' if abs(v) >= 1 else f'{v:,.4f}'
        return f'{v:,.2f}'
    return str(v)

def disp(key, v, lang, row=None):
    """القيمة النهائية المعروضة (نص) — كل النصوص تتبع اللغة المختارة."""
    ar = lang == 'عربي'; i = 1 if ar else 0
    if key == 'uni_decision': return DEC_NAME.get(v, (v, v))[i]
    if key == 'uni_signal': return DEC_NAME.get(v, (v, v))[i]
    if key == 'px_final': return TECH_NAME.get(v, (v, v))[i]
    if key == 'mkt_label': return MKT_ICON.get(v, '⚪') + ' ' + MKT_NAME.get(v, (v, v))[i]
    if key == 'mkt_bench': return BENCH_NAME.get(v, (v, v))[i]
    if key == 'mkt_tf': return {'D': ('Daily', 'يومي'), 'W': ('Weekly', 'أسبوعي')}.get(v, (v, v))[i]
    if key == 'market': return MARKET_NAME.get(v, (v, v))[i]
    if key == 'sector': return SECTOR_AR.get(v, v) if (ar and v) else v
    if key in ('auto_style', 'style_used', 'rd_style', 'style_suggest'):
        return (STYLE_ICON.get(v, '') + ' ' + STYLE_NAME.get(v, (v, v))[i]).strip()
    if key in ('tg_inv_src', 'tg_stretch_src'): return TGT_SRC.get(v, (v, v))[i] if v else '—'
    if key == 'uni_notes': return ('، ' if ar else ', ').join(NOTE_NAME[c][i] for c in str(v).split('|') if c in NOTE_NAME) or '—'
    if key == 'dp_align':
        try: return ALIGN_TXT2.get(int(v), ('—', '—'))[i]
        except Exception: return '—'
    if key == 'fv_verdict': return TOK.get(v, (v, v))[i]
    if key == 'rd_peer_txt': return '—'
    if key == 'style_why':
        return ({'vol': ('High volatility + volume surge', 'تذبذب عالٍ مع قفزة حجم'), 'trend': ('Strong trend', 'اتجاه قوي'), 'dip': ('Pullback with positive money flow', 'تراجع مع تدفق سيولة موجب'),
                 'earnings': ('Strong earnings growth + ROE', 'نمو أرباح قوي + عائد على الملكية'), 'multiples': ('Low P/E or P/B', 'مضاعفات منخفضة (P/E أو P/B)'),
                 'default': ('Default (no stronger signal)', 'افتراضي (لا إشارة أقوى)')}.get(v, (v, v))[i] if v else '—')
    if key == 'fv_eps_src':
        return ({'TV-TTM': ('TradingView TTM', 'تريدنغ فيو TTM'), 'Yahoo-TTM': ('Yahoo TTM', 'ياهو TTM'), 'Quarterly-sum': ('Sum of last 4 quarters', 'مجموع آخر 4 أرباع'),
                 'FY': ('Last fiscal year (may be stale)', 'آخر سنة مالية (قد تكون قديمة)'), 'Price/PE': ('Price ÷ Yahoo P/E (currency-safe)', 'السعر ÷ مضاعف ياهو (آمن للعملة)')}.get(v, (v, v))[i] if v else '—')
    if key == 'mcap_src':
        return ({'TradingView': ('TradingView (live)', 'تريدنغ فيو (حي)'), 'Yahoo': ('Yahoo', 'ياهو'), 'Price×Shares': ('Price × shares (Yahoo cap was stale)', 'السعر × الأسهم (قيمة ياهو قديمة)')}.get(v, (v, v))[i] if v else '—')
    if key == 'fv_rel_scope':
        m_ = re.match(r'(Sector|Market) \((\d+)\)', str(v))
        return (((('Sector' if m_[1] == 'Sector' else 'Market') if not ar else ('القطاع' if m_[1] == 'Sector' else 'السوق')) + f' ({m_[2]})') if m_ else '—')
    if key == 'vt_record' and isinstance(v, str):
        m = re.match(r'W(\d+) • L(\d+) • BE(\d+) • AMB(\d+)', v)
        if m: return (f'ربح {m[1]} • خسارة {m[2]} • تعادل {m[3]} • غامض {m[4]}' if ar else f'Win {m[1]} • Loss {m[2]} • BE {m[3]} • Amb {m[4]}')
    if key == 'rd_tgt_src' and isinstance(v, str):
        if isinstance(v, str) and v.startswith('E') and v[1:].isdigit():   # 🆕 v6: مصدر الهدف متوسط متحرك (E20/E50)
            return ('متوسط ' + v[1:] if ar else 'EMA ' + v[1:])
        return {'H': ('قمة الفترة' if ar else 'Period high')}.get(v, v) or '—'
    if key == 'px_signal_age': return '—' if v is None or (isinstance(v, float) and v != v) else str(int(v))
    if key in ('vt_dir', 'zb_dir'): return TOK.get(v, (v, v))[i] if v else '—'
    if isinstance(v, str):
        if key == 'dp_decision':   # 🆕 v6: درع الحارس 🛡 يظهر بجوار القرار كما في التصميم المرفق
            sh = v.endswith('+SHIELD')
            vv = v[:-7] if sh else v
            return trtext(vv.replace('AVOID', 'AVOID_') if vv.startswith('AVOID') else vv, lang) + (' 🛡' if sh else '')
        if key == 'dp_status': return trtext('AVOID_' if v == 'AVOID' else v, lang)
        if key in ('sc_sync',):
            return re.sub(r'⏳(\d+)d', (r'⏳\1 يوم' if ar else r'⏳\1d'), v)
        if 'Insufficient history' in v:
            v = re.sub(r'⏳ Insufficient history \(needs (\d+)\+ bars\)', (r'⏳ تاريخ غير كافٍ (يحتاج \1+ شمعة)' if ar else r'⏳ Insufficient history (needs \1+ bars)'), v)
        return trtext(v, lang) if v else '—'
    return fmt_cell(key, v)

def row_display(r, lang):
    """dict كامل: key → نص معروض (يشمل الشرح ونص نسبي/أقران).
    🆕 v6 (إصلاح 7): الترجمة تعمل لكل صف على حدة بمُدخلاته فقط — لا سياق عام _LOC_CTX فيتعطل تعريب الأسباب."""
    out = {k: disp(k, v, lang) for k, v in r.items() if not str(k).startswith('_') and k not in HIDDEN}
    pv, ps = r.get('rd_peer'), r.get('rd_peer_src')
    out['rd_peer_txt'] = (f"{pv:+.1f} ({trtext(ps, lang)})" if nn(pv) else '—')
    out['explain'] = explain(r, lang)
    return out

# -----------------------------------------------------------------------------
# شرح نصي مبسّط لكل سهم (سبب القرار)
# -----------------------------------------------------------------------------
def explain(r, lang):
    ar = lang == 'عربي'; L = (lambda en, a: a if ar else en); I = 1 if ar else 0
    f1 = lambda x: f'{x:.1f}'; f2 = lambda x: f'{x:,.2f}'
    dec = r['uni_decision']; P_ = []
    dname = DEC_NAME[dec][I]
    s1 = L(f"Verdict: {dname} — overall score {r['uni_score']:.0f}/100 (grade {r['uni_grade']}).", f"القرار: {dname} — الدرجة الكلية {r['uni_score']:.0f} من 100 (التقييم {r['uni_grade']}).")
    notes = [NOTE_NAME[c][I] for c in str(r.get('uni_notes', '')).split('|') if c in NOTE_NAME]
    if notes: s1 += L(' Adjusted by: ', ' تم تعديل القرار بسبب: ') + (' ، ' if ar else ', ').join(notes) + '.'
    P_.append(s1)
    # حالة المؤشر العام
    lab = r.get('mkt_label', 'M_NA')
    if lab != 'M_NA' and nn(r.get('mkt_dd')):
        bn = BENCH_NAME.get(r.get('mkt_bench'), (r.get('mkt_bench'),) * 2)[I]
        extra = {'M_CRASH': L('Extreme caution: broad selling pressure.', 'حذر شديد: ضغط بيع واسع على السوق.'),
                 'M_BEAR': L('Bear market: capital preservation first — new entries only with strong confirmation.', 'سوق هابط: الأولوية لحماية رأس المال — الدخول الجديد بتأكيد قوي فقط.'),
                 'M_RECOVERY': L('Recovery: the index is back above EMA50 after a deep drawdown; confirmation is improving.', 'تعافٍ: عاد المؤشر فوق EMA50 بعد هبوط عميق والتأكيد يتحسن.'),
                 'M_CORR': L('Even good stocks tend to fall with the index in a correction, so new entries need extra confirmation.', 'في التصحيح تميل حتى الأسهم الجيدة للهبوط مع المؤشر، لذا تحتاج الدخولات الجديدة إلى تأكيد إضافي.'),
                 'M_DOWN': L('The market trend is against new long positions.', 'اتجاه السوق ضد الدخول الشرائي الجديد.'),
                 'M_REBOUND': L('A bounce is not yet a confirmed recovery.', 'الارتداد لا يعني تعافياً مؤكداً بعد.'),
                 'M_WEAK': L('Market momentum is soft.', 'زخم السوق ضعيف.'),
                 'M_UP': L('The market backdrop supports buying.', 'حالة السوق داعمة للشراء.'), 'M_NEUTRAL': ''}.get(lab, '')
        tfw = L(' (weekly basis)', ' (على الإطار الأسبوعي)') if r.get('mkt_tf') == 'W' else ''
        P_.append(L(f"Market backdrop: {bn}{tfw} is in {MKT_NAME[lab][0]} ({r['mkt_dd']:+.1f}% from its 20-day high, {r['mkt_vs50']:+.1f}% vs EMA50). {extra}",
                    f"حالة المؤشر العام: {bn}{tfw} في حالة {MKT_NAME[lab][1]} ({r['mkt_dd']:+.1f}% عن قمة 20 يوماً و{r['mkt_vs50']:+.1f}% عن EMA50). {extra}"))
    # الاتجاه
    up_short = r['px_ema'] > r['px_sma']; st_up = r['px_st_dir'].endswith('Up'); above_wma = r['price'] > r['px_wma']
    t = []
    t.append(L('the fast average is above the slow one' if up_short else 'the fast average is below the slow one', 'المتوسط السريع فوق البطيء' if up_short else 'المتوسط السريع تحت البطيء'))
    t.append(L('the trend line (SuperTrend) is green' if st_up else 'the trend line (SuperTrend) is red', 'خط الاتجاه (SuperTrend) أخضر' if st_up else 'خط الاتجاه (SuperTrend) أحمر'))
    t.append(L('price is above the 52-bar weighted average' if above_wma else 'price is below the 52-bar weighted average', 'السعر فوق المتوسط المرجح 52' if above_wma else 'السعر تحت المتوسط المرجح 52'))
    sc = r.get('px_struct_conf'); mtf = r.get('px_mtf_label', '')
    sc_t = L({'Bullish': 'market structure is making higher highs/lows', 'Bearish': 'market structure is making lower highs/lows', 'Neutral': 'market structure is undecided'}.get(sc, ''),
             {'Bullish': 'هيكل السوق صاعد (قمم وقيعان أعلى)', 'Bearish': 'هيكل السوق هابط (قمم وقيعان أدنى)', 'Neutral': 'هيكل السوق غير محسوم'}.get(sc, ''))
    if sc_t: t.append(sc_t)
    mt = ('STRONG CONFIRMED' in mtf, 'AGAINST' in mtf, 'MIXED' in mtf)
    if mt[0]: t.append(L('higher timeframes confirm the trend', 'الأطر الزمنية الأكبر تؤكد الاتجاه'))
    elif mt[1]: t.append(L('higher timeframes are against the trend', 'الأطر الزمنية الأكبر عكس الاتجاه'))
    elif mt[2]: t.append(L('higher timeframes are mixed', 'الأطر الزمنية الأكبر متباينة'))
    trend_good = up_short and st_up
    P_.append(L('Trend: ', 'الاتجاه: ') + ('، ' if ar else '; ').join(t) + '.')
    # الزخم
    rsi = r['px_rsi_s']; mh = r['px_macd_hist']
    if rsi >= 70: rt = L(f'RSI {rsi:.0f} is overbought, so the rise may pause', f'مؤشر القوة النسبية RSI عند {rsi:.0f} أي تشبع شرائي وقد يتوقف الصعود')
    elif rsi >= 50: rt = L(f'RSI {rsi:.0f} is healthy (above 50)', f'مؤشر RSI عند {rsi:.0f} وهو صحي (فوق 50)')
    elif rsi >= 30: rt = L(f'RSI {rsi:.0f} is weak (below 50)', f'مؤشر RSI عند {rsi:.0f} وهو ضعيف (تحت 50)')
    else: rt = L(f'RSI {rsi:.0f} is oversold; a bounce is possible but the trend is still down', f'مؤشر RSI عند {rsi:.0f} أي تشبع بيعي وقد يحدث ارتداد لكن الاتجاه ما زال هابطاً')
    mt_ = L('MACD momentum is positive' if (nn(mh) and mh > 0) else 'MACD momentum is negative', 'زخم MACD إيجابي' if (nn(mh) and mh > 0) else 'زخم MACD سلبي')
    P_.append(L('Momentum: ', 'الزخم: ') + rt + ('، ' if ar else '; ') + mt_ + '.')
    # السيولة والشمعة
    s = []
    cm = r['px_cmf']
    if nn(cm): s.append(L(f'money flow (CMF {cm:+.2f}) shows ' + ('buying' if cm > 0 else 'selling') + ' pressure', f'تدفق السيولة (CMF {cm:+.2f}) يدل على ضغط ' + ('شراء' if cm > 0 else 'بيع')))
    vr = r.get('px_vol_ratio')
    if nn(vr): s.append(L(f'volume is {vr:.2f}x its average (' + ('strong' if vr >= 1.5 else 'weak' if vr <= 0.7 else 'normal') + ')', f'الحجم {vr:.2f} ضعف المتوسط (' + ('قوي' if vr >= 1.5 else 'ضعيف' if vr <= 0.7 else 'عادي') + ')'))
    sw = r.get('px_sweep')
    if sw == 'Bull Sweep': s.append(L('a bullish liquidity sweep occurred (stops below a low were hunted then price recovered)', 'حدث اصطياد سيولة صاعد (كُسر قاع لاصطياد الوقف ثم عاد السعر للأعلى)'))
    elif sw == 'Bear Sweep': s.append(L('a bearish liquidity trap occurred (a high was broken then rejected)', 'حدثت مصيدة سيولة هابطة (كُسرت قمة ثم رُفض السعر)'))
    if r.get('px_eq'): s.append(L('equal ' + ('highs' if r['px_eq'] == 'EQH' else 'lows') + ' nearby can act as a liquidity pool', 'وجود ' + ('قمم' if r['px_eq'] == 'EQH' else 'قيعان') + ' متساوية قريبة قد تعمل كمصيدة سيولة'))
    if r.get('px_dist'): s.append(L(f"the last candle dropped {r['px_bar_chg']:.1f}% (distribution candle)", f"آخر شمعة هبطت {r['px_bar_chg']:.1f}% (شمعة تصريف)"))
    pats = [p_ for p_ in str(r.get('px_patterns', '')).split(', ') if p_ and p_ != '—']
    if pats: s.append(L('candle pattern: ' + ', '.join(pats), 'نمط الشمعة: ' + '، '.join(TOK.get(p_, (p_, p_))[I] for p_ in pats)))
    if r.get('px_sq_on'): s.append(L('Bollinger bands are squeezed (a sharp move may follow, direction unknown)', 'نطاق بولينجر منضغط (قد تتبعه حركة قوية دون تحديد الاتجاه)'))
    if r.get('px_div') in ('Bull Div', 'Bear Div'): s.append(L('RSI divergence: ' + ('bullish' if r['px_div'] == 'Bull Div' else 'bearish'), 'دايفرجنس RSI: ' + ('صاعد' if r['px_div'] == 'Bull Div' else 'هابط')))
    if s: P_.append(L('Liquidity & candle: ', 'السيولة والشمعة: ') + ('، ' if ar else '; ').join(s) + '.')
    # المخاطرة والقوة النسبية
    s = []
    if nn(r.get('rd_atr_pct')): s.append(L(f"daily volatility (ATR) is {r['rd_atr_pct']:.1f}% of price (risk: {trtext(r['rd_risk'], lang)})", f"التذبذب (ATR) {r['rd_atr_pct']:.1f}% من السعر (المخاطرة: {trtext(r['rd_risk'], lang)})"))
    if r.get('px_rs_label') and 'N/A' not in r['px_rs_label']: s.append(L('relative to its index it is ' + ('stronger' if 'Stronger' in r['px_rs_label'] else 'weaker'), 'مقارنةً بمؤشره هو ' + ('أقوى' if 'Stronger' in r['px_rs_label'] else 'أضعف')))
    if nn(r.get('rd_peer')): s.append(L(f"{r['rd_peer']:+.1f} pts vs peers", f"{r['rd_peer']:+.1f} نقطة مقابل الأقران"))
    if s: P_.append(L('Risk & relative strength: ', 'المخاطرة والقوة النسبية: ') + ('، ' if ar else '; ').join(s) + '.')
    # التقييم والقوائم المالية
    s = []
    if nn(r.get('fv_fair')):
        s.append(L(f"fair value ≈ {f2(r['fv_fair'])} ({TOK.get(r['fv_verdict'], (r['fv_verdict'],) * 2)[0]}, {r['fv_upside']:+.0f}% vs price; source: {r['fv_source']})",
                   f"القيمة العادلة ≈ {f2(r['fv_fair'])} ({TOK.get(r['fv_verdict'], (r['fv_verdict'],) * 2)[1]}، {r['fv_upside']:+.0f}% عن السعر؛ المصدر: {trtext(r['fv_source'], lang)})"))
    if nn(r.get('dp_piotroski')): s.append(L(f"Piotroski {r['dp_piotroski']:.0f}/9 ({'strong' if r['dp_piotroski'] >= 7 else 'average' if r['dp_piotroski'] >= 5 else 'weak'} financial health)", f"درجة Piotroski {r['dp_piotroski']:.0f} من 9 (صحة مالية {'قوية' if r['dp_piotroski'] >= 7 else 'متوسطة' if r['dp_piotroski'] >= 5 else 'ضعيفة'})"))
    if nn(r.get('dp_altman')) and r['dp_altman'] < 1.8: s.append(L('Altman Z signals bankruptcy risk', 'مؤشر Altman Z يدل على خطر تعثر'))
    if nn(r.get('dp_beneish')) and r['dp_beneish'] > -1.8: s.append(L('Beneish M hints at earnings-quality risk', 'مؤشر Beneish M يشير إلى مخاطرة في جودة الأرباح'))
    if nn(r.get('dp_roe')): s.append(f"ROE {r['dp_roe']:.0f}%")
    if s: P_.append(L('Valuation & quality: ', 'التقييم والجودة: ') + ('، ' if ar else '; ').join(s) + '.')
    if r.get('dp_guard'): P_.append(L('Safety guard: the strong-buy decision was reduced (' + trtext(r['dp_guard'], lang) + ').', 'نظام الحماية: خُفّض قرار الشراء القوي (' + trtext(r['dp_guard'], lang) + ').'))
    # الخطة
    if dec in ('STRONG BUY', 'BUY DIP') and nn(r.get('zb_entry')):
        pl = L(f"Plan: buy zone {f2(r['zb_low'])}–{f2(r['zb_high'])}, entry ≈ {f2(r['zb_entry'])}, stop {f2(r['zb_stop'])} ({r['zb_stop_pct']:+.1f}%), first target {f2(r['zb_target'])} ({r['zb_target_pct']:+.1f}%, R:R 1:{r['zb_rr']:.1f}).",
               f"الخطة: نطاق الشراء {f2(r['zb_low'])}–{f2(r['zb_high'])} والدخول ≈ {f2(r['zb_entry'])} والوقف {f2(r['zb_stop'])} ({r['zb_stop_pct']:+.1f}%) والهدف الأول {f2(r['zb_target'])} ({r['zb_target_pct']:+.1f}%) بعائد/مخاطرة 1:{r['zb_rr']:.1f}.")
        if nn(r.get('tg_inv')):
            pl += L(f" For a {STYLE_NAME.get(r['style_used'], ('',) * 2)[0]} investment aim for ≈ {f2(r['tg_inv'])} ({r['tg_inv_pct']:+.0f}%, {TGT_SRC.get(r['tg_inv_src'], ('',) * 2)[0]}) and extended ≈ {f2(r['tg_stretch'])} ({r['tg_stretch_pct']:+.0f}%).",
                    f" وللاستثمار بأسلوب {STYLE_NAME.get(r['style_used'], ('', '')) [1]} الهدف ≈ {f2(r['tg_inv'])} ({r['tg_inv_pct']:+.0f}%، المصدر: {TGT_SRC.get(r['tg_inv_src'], ('', ''))[1]}) والهدف الممتد ≈ {f2(r['tg_stretch'])} ({r['tg_stretch_pct']:+.0f}%).")
    elif dec == 'SELL':
        pl = L('Plan: avoid new buying; existing holders may consider reducing or tightening stops.', 'الخطة: تجنّب الشراء الجديد؛ ومن يملك السهم قد يفكر في التخفيف أو رفع الوقف.')
    elif dec == 'WATCH':
        pl = L('Plan: no entry yet — wait for a clearer signal (higher grade, confirmation from higher timeframes, or a pullback into the buy zone).', 'الخطة: لا دخول الآن — انتظر إشارة أوضح (تقييم أعلى أو تأكيد من الأطر الأكبر أو تراجع إلى نطاق الشراء).')
    else:
        pl = L('Plan: stay away for now; the evidence is weak or negative.', 'الخطة: الابتعاد حالياً؛ الأدلة ضعيفة أو سلبية.')
    P_.append(pl)
    return '\n'.join(P_)


# -----------------------------------------------------------------------------
# 14) تقرير HTML ثابت (للـ PDF / PNG / عرض كولاب) — جداول مقسّمة بعرض ثابت + عزل اتجاه الأرقام (تصميم v2.0)
# -----------------------------------------------------------------------------
NOTE_AR = 'أداة مساعدة في قراءة وفحص الأسهم والمساعدة في القرار الاستثماري، وليست توصية بالشراء أو البيع.'
NOTE_EN = 'A helper tool for reading and screening stocks and supporting investment decisions. It is not a recommendation to buy or sell.'
_AR_RX = re.compile(r'[\u0600-\u06FF]')
_ICON = {'🟢': '#00c853', '🔴': '#e53935', '🟡': '#ffb300', '🟠': '#fb8c00', '🔵': '#2979ff', '⚪': '#bdbdbd', '🟦': '#26c6da', '🟪': '#ab47bc'}
def hx(x, iso=True):
    raw = '' if x is None else str(x)
    has_ar = bool(_AR_RX.search(raw))
    s = _html.escape(raw)
    for k, col in _ICON.items():
        s = s.replace(k, f'<i class="dot" style="background:{col}"></i>')
    s = (s.replace('✅', '✔').replace('❌', '✖').replace('⚠️', '⚠').replace('🚀', '▲').replace('🌊', '≈').replace('😴', '–').replace('🔥', '▲').replace('💤', '▼')
           .replace('⚖️', '=').replace('🌱', '').replace('🔻', '▼').replace('🪤', '').replace('💰', '').replace('📈', '').replace('📊', '').replace('🏛️', '').replace('⚡', '').replace('🔸', '◆').replace('🛡', '🛡'))
    return f'<span dir="ltr" class="i">{s}</span>' if (iso and not has_ar and raw) else s

CSS = """
@page { size: A4 landscape; margin: 9mm 8mm 11mm; @bottom-center { content: counter(page) ' / ' counter(pages); font-size: 8pt; color:#777; direction: ltr; unicode-bidi: isolate } }
* { box-sizing: border-box; } body { font-family: 'Cairo','Noto Sans Arabic','Noto Sans','DejaVu Sans',Arial,sans-serif; font-size: 8.5pt; color:#1b1f2a; margin:0; }
.i { unicode-bidi: isolate; white-space: nowrap }
h1 { font-size: 18pt; margin: 0 0 2mm; color:#0d1b3d } h2 { font-size: 12pt; margin: 5mm 0 2mm; color:#0d1b3d; border-bottom: 2px solid #ffc400; padding-bottom: 1mm; page-break-after: avoid }
.hdr { background: linear-gradient(90deg,#0d1b3d,#1b2f63); background-color:#0d1b3d; color:#fff; padding: 5mm 6mm; border-radius: 3mm; margin-bottom: 3mm }
.hdr h1 { color:#fff } .hdr small { color:#cfd8ff } .banner { padding: 1.5mm 3mm; border-radius: 2mm; margin: 1mm 0; font-size: 8pt }
table.dt { border-collapse: collapse; width:100%; margin-bottom: 3mm; table-layout: fixed } table.dt th { background:#0d1b3d; color:#fff; padding: 1.2mm 1mm; font-size: 6.4pt; text-align:center; overflow-wrap: anywhere }
table.dt td { border-bottom: 1px solid #e3e6ee; padding: .9mm 1mm; text-align:center; font-size: 6.9pt; overflow-wrap: anywhere; word-break: break-word } table.dt tr:nth-child(even) td { background:#f6f8fc } table.dt td.l { text-align:start }
table.dt tr { page-break-inside: avoid }
.dot { display:inline-block; width:2.4mm; height:2.4mm; border-radius:50%; vertical-align:middle; margin: 0 .3mm }
.badge { display:inline-block; color:#fff; padding:.5mm 1.8mm; border-radius: 2mm; font-weight:700; font-size: 7pt; white-space: nowrap }
.pos { color:#00a152; font-weight:700 } .neg { color:#d32f2f; font-weight:700 }
table.grid { width:100%; border-collapse: separate; border-spacing: 3mm 0; margin: 0 -3mm 3mm; page-break-inside: avoid } table.grid > tbody > tr > td, table.grid > tr > td { width:50%; vertical-align: top; padding:0; border:0 }
.card { border:1px solid #d5dbea; border-radius:3mm; padding:2.5mm 3mm; background:#fbfcff; font-size:7.6pt }
table.t2, table.t2 td, table.t3, table.t3 td, table.fair, table.fair td { border:0; background:none; padding:0 } table.t2 { width:100% } table.t2 td.e { text-align:end }
.sym { font-size: 13pt; font-weight:800 } .nm { color:#566; font-size:7.5pt } .px { font-size: 14pt; font-weight:800 }
table.t3 { width:100%; border-spacing: 1.2mm 0; border-collapse: separate; margin:1.5mm -1.2mm 0 } td.box { width:33.3%; border-radius:2mm; padding:1mm 1.5mm; text-align:center; border:1px solid }
.box b { display:block; font-size: 9.5pt } .box span { font-size:6.6pt } td.stop { border-color:#ef9a9a; background:#fff1f1; color:#c62828 } td.entry { border-color:#90caf9; background:#eef6ff; color:#1565c0 } td.tgt { border-color:#a5d6a7; background:#eefbef; color:#2e7d32 } td.tg2 { border-color:#ffe082; background:#fffbea; color:#8a6500 }
table.fair { width:100%; border:1px solid #f5b5b5; background:#fff4f4; border-collapse:separate; border-radius:2mm; margin:1.2mm 0 } table.fair td { padding:1mm 2mm } table.fair.good { border-color:#a5d6a7; background:#f1fbf2 }
.note { font-size: 7.4pt; color:#444; line-height:1.5; margin-top:1.2mm }
.cols2 { column-count: 2; column-gap: 7mm } .ex { break-inside: avoid; page-break-inside: avoid; margin-bottom: 3mm; padding-bottom: 2mm; border-bottom: 1px dashed #cfd6e8 } .ex h3 { margin:0 0 1mm; font-size: 9pt; color:#0d1b3d } .ex p { margin: 0 0 1mm; font-size: 7.6pt; line-height: 1.55 }
.disc { background:#fff8e1; border:1px solid #ffe082; border-radius:2mm; padding:2mm 3mm; font-size: 8pt; margin-top:4mm }
.pb { page-break-before: always } .gl { font-size:7.4pt; line-height:1.6; color:#333 }
"""
LONG_W = {'name': 3, 'uni_notes': 3, 'rd_reasons_full': 5, 'px_location': 5, 'px_rs_detail': 4, 'auto_style': 2.4, 'px_near': 2.4, 'fv_models': 3, 'tg_text': 6,
          'px_cat_buy': 3.2, 'px_cat_sell': 3.2, 'px_smc_counts': 3.4, 'vt_reached': 5, 'vt_record': 3.5, 'px_regime_mult': 4, 'px_patterns': 2.6, 'px_state': 2.6, 'fv_verdict': 2, 'mkt_label': 2.6,
          'uni_decision': 2, 'px_final': 2.4, 'rd_rating': 2.2, 'dp_decision': 2.2, 'px_mtf_label': 2.4, 'px_regime': 2, 'rd_peer_txt': 1.6, 'px_matrix_frames': 2.4, 'dp_guard': 2.4, 'px_vwap': 1.6, 'px_zone': 2,
          'sector': 2.4, 'industry': 2.6, 'symbol': 1.5, 'zb_dir': 1.4, 'rd_sig': 2.4, 'px_struct_conf': 1.6, 'px_struct_live': 1.6, 'px_sweep': 2, 'px_div': 2, 'px_squeeze': 2, 'px_last_break': 1.6, 'fv_source': 1.8,
          'tg_inv_src': 2, 'tg_stretch_src': 2, 'mkt_bench': 1.6, 'vt_last_outcome': 1.6}
def chunk_keys(keys, budget=17.0):
    keys = [k for k in keys if k != 'explain']
    chunks, cur, w = [], [], 0.0
    for k in keys:
        kw = LONG_W.get(k, 1.0)
        if cur and w + kw > budget:
            chunks.append(cur); cur = ['symbol'] + ([k] if k != 'symbol' else []); w = LONG_W['symbol'] + (kw if k != 'symbol' else 0)
        else:
            cur.append(k); w += kw
    if cur: chunks.append(cur)
    return chunks

def dec_badge(dec, lang):
    return f'<span class="badge" style="background:{DEC_COLOR.get(dec, "#777")}">{_html.escape(DEC_NAME.get(dec, (dec, dec))[1 if lang == "عربي" else 0])}</span>'
def cls_num(v):
    return 'pos' if (nn(v) and v > 0) else 'neg' if (nn(v) and v < 0) else ''

def table_html(rows, raws, keys, lang):
    """rows: قائمة dict نصوص معروضة؛ raws: قائمة dict قيم خام (للتلوين)."""
    tw = sum(LONG_W.get(k, 1.0) for k in keys)
    h = '<table class="dt"><colgroup>' + ''.join(f'<col style="width:{LONG_W.get(k, 1.0) / tw * 100:.2f}%">' for k in keys) + '</colgroup><tr>'
    h += ''.join(f'<th>{_html.escape(hdr(k, lang))}</th>' for k in keys) + '</tr>'
    for d, rw in zip(rows, raws):
        h += '<tr>'
        for k in keys:
            v = d.get(k, '—')
            if k == 'uni_decision': h += f'<td>{dec_badge(rw["uni_decision"], lang)}</td>'
            elif k in PCT_SIGNED: h += f'<td class="{cls_num(rw.get(k))}">{hx(v)}</td>'
            elif k in ('name', 'uni_notes', 'rd_reasons_full', 'px_location', 'px_rs_detail', 'auto_style', 'px_near', 'fv_models', 'tg_text'): h += f'<td class="l">{hx(v)}</td>'
            else: h += f'<td>{hx(v)}</td>'
        h += '</tr>'
    return h + '</table>'

def card_html(r, d, lang):
    ar = lang == 'عربي'; L = (lambda en, a: a if ar else en); up = r['fv_upside']; dec = r['uni_decision']
    f = lambda k: hx(d.get(k, '—'))
    fair_cls = 'fair good' if (nn(up) and up >= 0) else 'fair'
    nm = str(r['name'])[:40]
    tg = ''
    if nn(r.get('tg_inv')):
        tg = (f'<table class="t3"><tr><td class="box tg2"><span>{L("Fib target 1", "هدف فيبو 1")}</span><b>{f("tg_fib1")}</b><span>{f("tg_fib1_pct")}</span></td>'
              f'<td class="box tg2"><span>{L("Investment target", "هدف الاستثمار")} · {hx(d.get("auto_style", ""))}</span><b>{f("tg_inv")}</b><span>{f("tg_inv_pct")} · {hx(d.get("tg_inv_src", ""))}</span></td>'
              f'<td class="box tg2"><span>{L("Extended target", "الهدف الممتد")}</span><b>{f("tg_stretch")}</b><span>{f("tg_stretch_pct")}</span></td></tr></table>')
    sim = ''
    if nn(r.get('vt_win_rate')) or 'vt_record' in r:
        sim = f' · {L("Sim. trades", "المحاكاة")}: {f("vt_record")}'
    return f"""<div class="card"><table class="t2"><tr><td><div class="sym">{hx(r['symbol'])}</div><div class="nm">{hx(nm)} · {hx(d.get('sector', ''))}</div></td>
<td class="e"><div class="px">{f('price')}</div><div class="{cls_num(r['chg'])}">{f('chg')}</div></td></tr></table>
<div style="margin:1mm 0">{dec_badge(dec, lang)} &nbsp; {L('Score','الدرجة')}: <b>{f('uni_score')}</b> ({r['uni_grade']}) &nbsp; {hx(d.get('auto_style', ''))} &nbsp; {L('Index','المؤشر')}: {hx(d.get('mkt_label', ''))}</div>
<table class="{fair_cls}"><tr><td>{L('Fair value','القيمة العادلة')}: <b>{f('fv_fair')}</b> <small>({hx(d.get('fv_source', ''))})</small></td><td style="text-align:end" class="{cls_num(up)}">{f('fv_upside')} · {hx(d.get('fv_verdict', ''))}</td></tr></table>
<table class="t3"><tr><td class="box stop"><span>{L('Stop','الوقف')}</span><b>{f('zb_stop')}</b><span>{f('zb_stop_pct')}</span></td>
<td class="box entry"><span>{L('Entry','الدخول')}</span><b>{f('zb_entry')}</b><span>{f('zb_low')} – {f('zb_high')}</span></td>
<td class="box tgt"><span>{L('Target','الهدف')}</span><b>{f('zb_target')}</b><span>{f('zb_target_pct')}</span></td></tr></table>{tg}
<div class="note">R:R 1:{f('zb_rr')} · {L('Technical','الفني')}: <b>{hx(d.get('px_final', ''))}</b> ({L('Buy','شراء')} {f('px_buy_pct')} / {L('Sell','بيع')} {f('px_sell_pct')}) · {L('Rating','التقييم')}: {hx(d.get('rd_rating', ''))} · {L('Deep','العميق')}: {hx(d.get('dp_decision', ''))}{sim}</div></div>"""

def mkt_banner_text(md, lang):
    """🆕 v7.0: سطر لافتة السوق المؤسسية (مطابق لمحتوى لافتة Pine v4.2)."""
    ar = lang == 'عربي'; I = 1 if ar else 0
    f1 = lambda v: '—' if not nn(v) else f'{v:+.1f}%'
    t = [(f"{'عن قمة 20 شمعة' if ar else 'vs 20-bar high'}: {f1(md['dd'])}"), f"vs EMA20: {f1(md['vs20'])}", f"vs EMA50: {f1(md['vs50'])}",
         f"{'تغيّر الشمعة' if ar else 'Bar chg'}: {f1(md['chg1'])}"]
    if nn(md.get('dd_ref')) and md.get('hi_long_ok'): t.append(f"{'عن قمة ' if ar else 'vs '}{md['long_len']}{'-شمعة' if ar else '-bar high'}: {f1(md['dd_ref'])}")
    if nn(md.get('bounce')): t.append(f"{'فوق أدنى 20 شمعة' if ar else 'Off 20-bar low'}: +{md['bounce']:.1f}%")
    for tg in md.get('tags', []): t.append(MKT_TAG[tg][I])
    return ' | '.join(t)

def banners_html(meta, lang):
    ar = lang == 'عربي'; I = 1 if ar else 0; ban = ''
    for m, (bs, md, bm) in meta['banners'].items():
        lab = md['label']
        state = MKT_ICON[lab] + ' ' + MKT_NAME[lab][I]
        ban += (f'<div class="banner" style="background:{MKT_COLOR[lab]}">🧭 {hx(MARKET_NAME.get(m, (m, m))[I])} · {hx(BENCH_NAME.get(bs, (bs, bs))[I])}: <b>{hx(state)}</b> | {hx(mkt_banner_text(md, lang))}</div>')
    return ban

def build_html(res, lang='عربي', cards_top=30, only_head=False):
    meta, recs = res['meta'], res['recs']; ar = lang == 'عربي'; L = (lambda en, a: a if ar else en); dirn = 'rtl' if ar else 'ltr'
    rows = [row_display(r, lang) for r in recs]; raws = recs
    cnt = {}
    for r in recs: cnt[r['uni_decision']] = cnt.get(r['uni_decision'], 0) + 1
    chips = ' '.join(f'{dec_badge(k, lang)} <b>{v}</b>' for k, v in cnt.items())
    h = f'<html dir="{dirn}" lang="{"ar" if ar else "en"}"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
    h += (f'<div class="hdr"><h1>ER1991 Smart Investment Radar PRO — {L("Stock Analysis Report", "تقرير تحليل الأسهم")}</h1><small>{hx(meta["generated"])} · {L("Data as of","البيانات حتى")} {hx(meta["as_of"])} · '
          f'{meta["n"]} {L("symbols","رمز")} · {L("Style","الأسلوب")}: {hx(disp("style_used", meta["style"], lang) if meta["style"] != "Auto" else L("Auto per stock", "تلقائي لكل سهم"))}</small></div>')
    h += banners_html(meta, lang) + f'<div style="margin:2mm 0">{chips}</div>'
    first = True
    for g in active_groups(res):
        if g == 'explain': continue
        title = GROUPS[g][1] if ar else GROUPS[g][0]
        for ci, ks in enumerate(chunk_keys(GROUPS[g][2])):
            cls = ' class="pb"' if (not first and ci == 0) else ''
            sub = f' ({ci + 1})' if ci else ''
            h += f'<h2{cls}>{_html.escape(title)}{sub}</h2>' + table_html(rows, raws, ks, lang)
        first = False
        if only_head: break
    if only_head: return h + '</body></html>'
    n_cards = min(cards_top, len(recs))
    if n_cards:
        h += f'<h2 class="pb">{L("Stock cards (top","بطاقات الأسهم (أفضل")} {n_cards})</h2>'
        for k in range(0, n_cards, 2):
            pair = [card_html(recs[j], rows[j], lang) for j in range(k, min(k + 2, n_cards))]
            h += '<table class="grid"><tr>' + ''.join(f'<td>{c}</td>' for c in pair) + ('<td></td>' if len(pair) == 1 else '') + '</tr></table>'
    h += f'<h2 class="pb">{L("Explanation of results","شرح النتائج")}</h2><div class="cols2">'
    for r, d in zip(recs, rows):
        paras = ''.join(f'<p>{hx(x, iso=False)}</p>' for x in d['explain'].split('\n'))
        h += f'<div class="ex"><h3>{hx(r["symbol"])} · {dec_badge(r["uni_decision"], lang)}</h3>{paras}</div>'
    h += '</div>'
    h += f'<h2 class="pb">{L("Methodology & reading guide","المنهجية ودليل القراءة")}</h2>' + methodology_html(res, lang)
    return h + '</body></html>'

def methodology_points(res, lang):
    ar = lang == 'عربي'; sim = res['meta']['p'].get('simulate', True)
    if ar:
        pts = [
         '<b>الدرجة النهائية</b> = متوسط مرجّح: تقييم الرادار الاستثماري 35% · قوة الإشارة الفنية 30% · القيمة العادلة 20% · التحليل العميق 15% (يُعاد توزيع الأوزان إن غاب مكوّن).',
         '<b>القرار النهائي</b>: ≥75 شراء قوي · ≥60 شراء عند التراجع · ≥45 متابعة · أقل من ذلك تجنّب. ويتحول إلى «بيع / تجنّب» عند إشارة بيع فنية.',
         '<b>نظام الحماية</b>: يخفّض «شراء قوي» إلى «شراء عند التراجع» عند أي شرط: مخاطرة التحليل العميق ≥ 80، أو ارتفاع اليوم ≥ 6% (مطاردة الشمعة الخضراء)، أو الفني غير مؤكد، أو تصحيح المؤشر العام. ويظهر سببه في عمود الأسباب وعلامة 🛡 بجوار القرار.',
         '<b>حالة المؤشر العام</b> (مراحل مؤسسية مطابقة لمؤشر Pine): <b>انهيار</b> (هبوط شمعة المرجع ≥7% أو ≥10% خلال 5 شموع) · <b>سوق هابط</b> (≥20% عن قمة السنة) · <b>تعافٍ</b> (عاد فوق EMA50 بعد هبوط بحجم التصحيح وارتفاع ≥5% عن القاع) · <b>تصحيح</b> (≥10% عن القمة) · <b>تراجع/اتجاه هابط</b> (≥5% عن قمة 20 شمعة أو تحت EMA50 مع EMA20 تحته) · <b>ضعف</b> (تحت EMA20) · <b>صحي</b>. وسوم: قمة جديدة · ارتداد غير مؤكد (خطر Dead-cat) · ارتداد تحت EMA20. في كل حالات الضغط (تراجع/تصحيح/هابط/انهيار) يُخفَّض «شراء قوي» تلقائياً بواسطة الحارس. العتبات قابلة للتعديل من لوحة الإعدادات.',
         '<b>القيمة العادلة (v2)</b>: مزيج مرجّح من نماذج مستقلة: P/E عادل بمضاعف جوردون (1+g)÷(r−g) حيث r = الفائدة الخالية + علاوة المخاطر وg = (1+التضخم)×(1+النمو الحقيقي)−1 (' + _pe_table_txt('ar') + '؛ مقيّد 5–20) مع علاوة/خصم نمو وجودة · P/B عادل بـROE (الأساس للبنوك) · رقم جراهام مُعايَر لمضاعف السوق · جراهام-نمو بالنمو الحقيقي · مضاعف نسبي من وسيط القطاع/السوق (TradingView) · هدف المحللين · هدف خارجي تُدخله أنت. للقطاع المالي وزن P/B أعلى. تُحسب <b>ثقة</b> 0–100 (عدد النماذج + اكتمال البيانات − تباعدها − الخسائر) ويقل أثر القيمة العادلة في القرار عند ضعفها. EPS: الأولوية لـTTM من TradingView ثم ياهو ثم الأرباع ثم السنة، والقيمة السوقية تُصحَّح إن كانت قديمة. النتائج حساسة جداً لفائدة/تضخم السوق (خصوصاً مصر) فراجع مدخلاتها من لوحة الإعدادات، وهي تقدير لا حقيقة مطلقة وقد تختلف عن أهداف بنوك الاستثمار المبنية على نماذج DCF ومعدلات خصم مختلفة.',
         '<b>الخطة والأهداف</b>: نطاق الشراء بين أقرب دعم (أو السعر − ATR) والسعر، الدخول عند ثلث النطاق، الوقف تحت النطاق بنصف ATR، والهدف = السعر + 1.5 × المخاطرة. بجانبها <b>أهداف فيبوناتشي</b> (امتدادات 1.272 / 1.618 / 2.618 من آخر موجة مؤكدة) و<b>هدف الاستثمار حسب الأسلوب</b>: يُختار أقرب مستوى (فيبو أو قمة 52 أسبوعاً أو المحللين أو القيمة العادلة) يحقق الحد الأدنى المطلوب: مضاربة 8% · نمو 20% · قيمة 25% · مدى متوسط 30% · مدى طويل 40%، وإن لم يوجد يُستخدم الحد نفسه. والهدف الممتد = 1.6 ضعف ذلك الحد.',
         '<b>التحليل الفني</b>: 7 فئات (اتجاه/زخم/سيولة/هيكل/استباقية/مفاهيم المال الذكي/شموع) × معاملات نظام السوق (Chop)، بشروط: حد أدنى 9 نقاط و3 فئات وتوافق الأطر العليا وتبريد 5 شموع وفلتر الشمعة الحادة والفجوة. <b>القرار الفني</b> لا يرتبط بالصفقة الافتراضية: شراء/بيع عند ظهور إشارة، متابعة عند تجمّع الأدلة (مع الميل صعودي أو هبوطي)، انتظار، أو تجنّب.',
        ]
        if sim: pts.append('<b>الصفقة الافتراضية (اختيارية)</b>: محاكاة على بيانات الشارت: وقف 1×ATR وأهداف 0.5/1.5/3×ATR، ويُنقل الوقف للتعادل بعد الهدف الأول (خيار فحص الوقف من الشمعة التالية مُتاح؛ الافتراضي مطابق لـPine: نفس الشمعة). <b>كيف تقرأ «الوصول للأهداف»</b>: مثال TP1 74% (32/43) يعني أنه من 43 صفقة فُتحت لمس السعر الهدف الأول في 32 منها مرة واحدة على الأقل (شمعة AMBIGUOUS لا تُحتسب). الهدف الأول قريب لذا نسبته مرتفعة دائماً، أما <b>نسبة الربح</b> فتحتسب الصفقة رابحة فقط إذا بلغت الهدف الثالث دون العودة لسعر الدخول، لذلك تكون أقل بكثير (وتقارب نسبة وصول TP3). فرق النسب لا يعني خللاً: يعني أن كثيراً من الصفقات تتحرك في اتجاهك ثم ترجع وتنتهي بتعادل. استخدمه لمعرفة هل يناسب الرمز الخروج الجزئي عند الهدف الأول أو الثاني.')
        pts.append('<b>فروقات عن منصات الرسم</b>: بيانات يومية من yfinance وقد تتأخر. VWAP على الفريم اليومي يُحسب متحركاً 20 يوماً. المحاكاة التاريخية تستبدل فلتر H1/H4 باتجاه الأسبوع السابق (وللحالة الحالية يمكن تفعيل الأطر اللحظية). مؤشرات Piotroski وAltman وBeneish تُحسب من القوائم المتاحة وقد تغيب لبعض الأسواق.')
        pts.append('<b>🆕 R:R عند سعر السوق</b>: إلى جانب R:R المحسوب من سعر دخول الخطة يظهر عمود «R:R عند سعر السوق» الذي يفترض الشراء الفوري بالسعر الحالي — فلا تبدو نسبة الخطة أفضل من الواقع فقط لأن الدخول المفترض أعمق في النطاق.')
        pts.append('<b>🆕 أصول بلا حجم (فوركس/مؤشرات) وبيانات قصيرة</b>: عندما يكون حجم التداول صفراً تُستبعد فئة الحجم من متوسط الدرجة بإعادة توزيع الأوزان، وعندما يكون التاريخ أقل من 200 شمعة يُحسب الاتجاه على المتوسطات المتاحة فقط — فلا تنخفض الدرجات زوراً. والرموز المتقاطعة مع أسهم (DASH/STX/SOL…) تُعامل كسهم إلا إذا أُلحق بها -USD/USDT.')
        pts.append('<b>🆕 تعيين ذكي للرموز</b>: يمكنك كتابة الاسم أو الرمز المختصر مباشرة (INTC أو INTEL، JUFO أو «جوهينة»، XAUUSD أو GOLD) فيتحول تلقائياً لصيغة ياهو الصحيحة، ومؤشرات مصر (EGX30/EGX70/EGX100/EGX Shariah) تُجرَّب مرشحاتها المتعددة ثم بديل ETF/تركيبي عند غياب البيانات.')
    else:
        pts = ['<b>Final score</b> = weighted mean: investment rating 35% · technical signal strength 30% · fair value 20% · deep analysis 15% (weights are re-normalised if a part is missing).',
               '<b>Final verdict</b>: ≥75 Strong Buy · ≥60 Buy on dip · ≥45 Watch · below = Avoid; becomes “Sell / Avoid” on a technical sell signal.',
               '<b>Safety guard</b>: reduces “Strong Buy” to “Buy on dip” when any condition holds: deep risk ≥ 80, day gain ≥ 6% (chasing), technical not confirmed, or index in correction. The reason shows in the reasons column with a 🛡 mark next to the decision.',
               '<b>Index state</b> (institutional phases matching the Pine indicator): <b>Crash</b> (index bar ≤ −7% or ≤ −10% in 5 bars) · <b>Bear market</b> (≥20% below the yearly high) · <b>Recovery</b> (back above EMA50 after a correction-size drawdown and ≥5% off the low) · <b>Correction</b> (≥10% below the high) · <b>Pullback/downtrend</b> (≥5% below the 20-bar high or below EMA50 with EMA20 under it) · <b>Weak</b> (below EMA20) · <b>Healthy</b>. Tags: new high · unconfirmed bounce (dead-cat risk) · rebound below EMA20. In every stress state the guard caps “Strong Buy”. Thresholds are editable in the settings panel.',
               '<b>Fair value (v2)</b>: weighted blend of independent models: justified P/E using Gordon (1+g)÷(r−g) with r = risk-free + equity premium and g = (1+inflation)×(1+real growth)−1 (' + _pe_table_txt('en') + '; clamped 5–20) with growth/quality premium · ROE-justified P/B (primary for banks) · market-calibrated Graham number · real-growth Graham-growth · relative multiple from sector/market median (TradingView) · analyst target · optional external target you enter. Financials weigh P/B higher. A 0–100 <b>confidence</b> (model count + data completeness − dispersion − losses) scales the influence on the verdict. EPS priority: TradingView TTM, Yahoo, quarters, fiscal year; a stale market cap is corrected. Results are very sensitive to the market rate/inflation inputs (especially Egypt) — review them in the settings panel; this is an estimate, and can differ from investment-bank DCF targets that use other discount rates.',
               '<b>Plan & targets</b>: buy zone from nearest support (or price − ATR) to price, entry at 1/3 of the zone, stop 0.5 ATR below it, target = price + 1.5 × risk. Alongside: <b>Fibonacci targets</b> (1.272 / 1.618 / 2.618 extensions of the last confirmed swing) and a <b>style-based investment target</b>: the nearest level (Fib, 52-week high, analysts, fair value) that meets the minimum goal: Swing 8% · Growth 20% · Value 25% · Medium 30% · Long 40%, otherwise the minimum itself. Extended target = 1.6× that minimum.',
               '<b>Technical analysis</b>: 7 categories × market-regime multipliers (Chop) with conditions: ≥9 points, ≥3 categories, higher-timeframe agreement, 5-bar cooldown, sharp-candle and gap filters. The <b>technical decision</b> does not depend on the simulated trade: Buy/Sell on a signal, Watch when evidence builds (bullish or bearish bias), Wait, or Avoid.']
        if sim: pts.append('<b>Simulated trade (optional)</b>: simulation on chart data: stop 1×ATR, targets 0.5/1.5/3×ATR, stop moved to breakeven after TP1 (an option to check the stop from the next bar is available; the default matches Pine: same bar). <b>Reading “Targets reached”</b>: TP1 74% (32/43) means that of 43 opened trades, 32 touched the first target at least once (an AMBIGUOUS bar is not counted). The first target is close, so its rate is always high; the <b>win rate</b> counts a trade as a win only if it reaches TP3 without returning to entry, so it is much lower (and close to the TP3 rate). The gap is not a bug: many trades move your way and then fall back to breakeven. Use it to judge whether partial exits at TP1/TP2 suit the symbol.')
        pts.append('<b>Differences vs charting platforms</b>: daily yfinance data (may be delayed); VWAP on daily bars is a rolling 20-day VWAP; the historical simulation replaces the H1/H4 filter with the previous week trend (live intraday frames can be enabled for the current state); Piotroski/Altman/Beneish come from available statements and may be missing for some markets.')
        pts.append('<b>🆕 R:R at market price</b>: beside the plan-entry R:R a new column shows the R:R assuming an immediate market buy — so the plan number no longer looks better than reality only because the assumed entry sits deeper in the zone.')
        pts.append('<b>🆕 No-volume assets & short history</b>: when volume is zero (forex/indices) the volume category is excluded with re-normalised weights; below 200 bars the trend is computed on the available averages only. Ambiguous tickers (DASH/STX/SOL…) are treated as stocks unless a -USD/USDT suffix is given.')
        pts.append('<b>🆕 Smart symbol mapping</b>: type a brand name or short code (INTC or INTEL, JUFO, XAUUSD or GOLD) and it resolves automatically; Egyptian indices (EGX30/EGX70/EGX100/EGX Shariah) try multiple Yahoo candidates then an ETF/synthetic fallback.')
    return pts

def methodology_html(res, lang):
    ar = lang == 'عربي'
    log = ''.join(f'<li>{_html.escape(x)}</li>' for x in res['meta']['log'])
    return ('<div class="gl">' + ''.join(f'<p>• {x}</p>' for x in methodology_points(res, lang)) + (f'<ul>{log}</ul>' if log else '') + '</div>'
            + f'<div class="disc">{NOTE_AR if ar else NOTE_EN}</div>')


# -----------------------------------------------------------------------------
# 15) HTML تفاعلي (ملف واحد مستقل يعمل بدون إنترنت) — نفس تصميم الملف المرفق تماماً: جدول + بطاقة + رسم + لغتان
# -----------------------------------------------------------------------------
def _jclean(o):
    if isinstance(o, dict): return {str(k): _jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_jclean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        o = float(o); return None if (o != o or math.isinf(o)) else o
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o

def chart_data(r, bars=130):
    df = r['_df']; p = P; c = df['Close']
    ema = s_ema(c, p['emaFast']); sma = s_sma(c, p['smaSlow']); wma = s_wma(c, p['wmaLen'])
    t = df.tail(bars); dec = 2 if r['price'] >= 1 else 4
    rd = lambda s: [None if (x != x) else round(float(x), dec) for x in s.tail(bars).values]
    lv = {'stop': r.get('zb_stop'), 'entry': r.get('zb_entry'), 'target': r.get('zb_target'), 'fair': r.get('fv_fair'), 'sup': r.get('px_support'),
          'res': r.get('px_resistance'), 'inv': r.get('tg_inv')}
    return dict(o=rd(t['Open']), h=rd(t['High']), l=rd(t['Low']), c=rd(t['Close']), ema=rd(ema), sma=rd(sma), wma=rd(wma),
                d0=str(t.index[0].date()), d1=str(t.index[-1].date()), lv={k: (None if not nn(v) else round(float(v), dec)) for k, v in lv.items()})

UI_TXT = {
 'ar': dict(
  title='ER1991 Smart Investment Radar PRO',
  sub='تقرير تفاعلي',
  search='🔍 بحث بالرمز أو الاسم',
  all_dec='كل القرارات',
  all_mkt='كل الأسواق',
  lang='English',
  csv='⬇ CSV',
  print='🖨 طباعة',
  close='✕',
  prev='‹ السابق',
  next='التالي ›',
  overview='نظرة عامة',
  fair='القيمة العادلة',
  stop='الوقف',
  entry='الدخول',
  target='الهدف',
  zone='نطاق الشراء',
  score='الدرجة',
  inv='هدف الاستثمار',
  ext='الهدف الممتد',
  fib1='هدف فيبو 1',
  expl='شرح النتيجة',
  guide='دليل القراءة والمنهجية',
  index='المؤشر العام',
  none='لا نتائج مطابقة',
  hint='اضغط على أي سهم أو أي قيمة لفتح بطاقته وتفاصيله',
  sup='دعم',
  res='مقاومة',
  count='نتيجة',
  price='السعر',
  symbols='رمز',
  data_as='البيانات حتى',
  style='الأسلوب',
  auto='تلقائي لكل سهم',
  all_sty='كل أنواع الاستثمار',
  k_total='عدد الأسهم',
  k_avg='متوسط الدرجة',
  k_best='الأعلى درجة',
  conf='الثقة',
 ),
 'en': dict(
  title='ER1991 Smart Investment Radar PRO',
  sub='Interactive report',
  search='🔍 Search symbol or name',
  all_dec='All verdicts',
  all_mkt='All markets',
  lang='عربي',
  csv='⬇ CSV',
  print='🖨 Print',
  close='✕',
  prev='‹ Prev',
  next='Next ›',
  overview='Overview',
  fair='Fair value',
  stop='Stop',
  entry='Entry',
  target='Target',
  zone='Buy zone',
  score='Score',
  inv='Investment target',
  ext='Extended target',
  fib1='Fib target 1',
  expl='Explanation',
  guide='Reading guide & methodology',
  index='Market index',
  none='No matching results',
  hint='Click any symbol or value to open its card and details',
  sup='Support',
  res='Resistance',
  count='results',
  price='Price',
  symbols='symbols',
  data_as='Data as of',
  style='Style',
  auto='Auto per stock',
  all_sty='All investment types',
  k_total='Symbols',
  k_avg='Avg score',
  k_best='Top score',
  conf='Confidence',
 ),
}

def build_payload(res, default_lang='عربي'):
    recs, meta = res['recs'], res['meta']; groups = active_groups(res)
    rows = []
    for r in recs:
        raw = {k: float(v) for k, v in r.items() if not str(k).startswith('_') and isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, (bool, np.bool_))
               and v == v and not (isinstance(v, float) and math.isinf(v))}
        rows.append(dict(sym=r['symbol'], name=str(r['name']), dec=r['uni_decision'], mkt=r['market'], sty=r.get('style_used', ''), raw=raw, ar=row_display(r, 'عربي'), en=row_display(r, 'English'), chart=chart_data(r)))
    gl = []
    for g in groups:
        keys = [k for k in GROUPS[g][2] if not (g == 'summary' and k == 'explain')]
        gl.append(dict(id=g, title=[GROUPS[g][0], GROUPS[g][1]], keys=keys))
    hdrs = {'ar': {k: hdr(k, 'عربي') for k in COLS}, 'en': {k: hdr(k, 'English') for k in COLS}}
    ban = []
    for m, (bs, md, bm) in meta['banners'].items():
        ban.append(dict(mkt=[MARKET_NAME.get(m, (m, m))[0], MARKET_NAME.get(m, (m, m))[1]], bench=list(BENCH_NAME.get(bs, (bs, bs))), label=[MKT_ICON[md['label']] + ' ' + MKT_NAME[md['label']][0], MKT_ICON[md['label']] + ' ' + MKT_NAME[md['label']][1]],
                        color=MKT_COLOR[md['label']], phase=md['label'], dd=md['dd'], v20=md['vs20'], v50=md['vs50'],
                        text=[mkt_banner_text(md, 'English'), mkt_banner_text(md, 'عربي')]))
    guide = {'ar': ''.join(f'<p>• {x}</p>' for x in methodology_points(res, 'عربي')), 'en': ''.join(f'<p>• {x}</p>' for x in methodology_points(res, 'English'))}
    style_txt = {'ar': (disp('style_used', meta['style'], 'عربي') if meta['style'] != 'Auto' else UI_TXT['ar']['auto']), 'en': (disp('style_used', meta['style'], 'English') if meta['style'] != 'Auto' else UI_TXT['en']['auto'])}
    styleNames = {'ar': {k: STYLE_ICON[k] + ' ' + STYLE_NAME[k][1] for k in STYLES}, 'en': {k: STYLE_ICON[k] + ' ' + STYLE_NAME[k][0] for k in STYLES}}
    return dict(defLang='ar' if default_lang == 'عربي' else 'en', styleNames=styleNames, rows=rows, groups=gl, hdrs=hdrs, ui=UI_TXT, banners=ban, guide=guide, decColor=DEC_COLOR,
                decNames={'ar': {k: v[1] for k, v in DEC_NAME.items()}, 'en': {k: v[0] for k, v in DEC_NAME.items()}}, signed=sorted(PCT_SIGNED),
                note={'ar': NOTE_AR, 'en': NOTE_EN}, meta=dict(gen=meta['generated'], asof=meta['as_of'], n=meta['n'], style=style_txt, log=meta['log']), sim=bool(meta['p'].get('vtOn', True)))

HTML_TPL = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ER1991 Smart Investment Radar PRO</title>
<style>
__FONT__
:root{--navy:#0d1b3d;--navy2:#1b2f63;--gold:#ffc400;--bg:#f4f6fb;--line:#e3e6ee;--ink:#1b1f2a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:'Cairo','Noto Sans Arabic','Noto Sans','Segoe UI',Tahoma,Arial,sans-serif;font-size:14px}
.i{unicode-bidi:isolate;white-space:nowrap}.pos{color:#00a152;font-weight:700}.neg{color:#d32f2f;font-weight:700}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;vertical-align:middle;margin:0 2px}
.hdr{background:#0d1b3d;background:linear-gradient(90deg,#0d1b3d,#1b2f63);color:#fff;padding:16px 22px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
.hdr h1{margin:0 0 4px;font-size:22px}.hdr small{color:#cfd8ff}.hb button{margin:0 4px}
button{font-family:inherit;cursor:pointer;border:0;border-radius:8px;padding:8px 14px;background:var(--gold);color:var(--navy);font-weight:700;font-size:13px}
button:hover{filter:brightness(1.07)}
.wrap{padding:12px 18px}.banner{padding:7px 12px;border-radius:8px;margin:5px 0;font-size:13px}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0}
.tools input,.tools select{padding:8px 10px;border:1px solid #cdd5e6;border-radius:8px;font-family:inherit;font-size:13px;background:#fff}.tools input{min-width:240px}
.badge{display:inline-block;color:#fff;padding:2px 10px;border-radius:10px;font-weight:700;font-size:12px;white-space:nowrap}
.chip{cursor:pointer;margin:0 3px;user-select:none}
.tabs{display:flex;flex-wrap:wrap;gap:4px;border-bottom:2px solid var(--gold);margin-top:6px}
.tabs button{background:#e6eaf5;color:var(--navy);border-radius:8px 8px 0 0}.tabs button.on{background:var(--navy);color:#fff}
.tw{overflow:auto;max-height:66vh;background:#fff;border:1px solid #d5dbea;border-radius:0 0 10px 10px}
table#tbl{border-collapse:collapse;width:100%;min-width:900px}
#tbl th{background:var(--navy);color:#fff;padding:8px 8px;font-size:12px;position:sticky;top:0;z-index:2;cursor:pointer;white-space:nowrap;user-select:none}
#tbl td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:center;font-size:12.5px;cursor:pointer}
#tbl tr:nth-child(even) td{background:#f6f8fc}#tbl tr:hover td{background:#fff4cc}
#tbl td.l{text-align:start;min-width:220px;white-space:normal}#tbl td.s{font-weight:800;color:var(--navy);text-align:start}
.hint{color:#667;font-size:12px;margin:6px 0}
details.guide{background:#fff;border:1px solid #d5dbea;border-radius:10px;padding:8px 14px;margin:12px 0}details.guide summary{cursor:pointer;font-weight:700;color:var(--navy)}
.gl p{margin:6px 0;line-height:1.7;font-size:13px}.foot{background:#fff8e1;border:1px solid #ffe082;border-radius:8px;padding:8px 12px;font-size:13px;margin:10px 0 24px}
.mbg{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(8,15,35,.62);display:none;z-index:50;overflow:auto;padding:3vh 2vw}
.mbg.on{display:block}.modal{background:#fff;border-radius:14px;max-width:1080px;margin:0 auto;padding:16px 18px;box-shadow:0 20px 60px rgba(0,0,0,.4)}
.mh{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap}.sym{font-size:26px;font-weight:800;color:var(--navy)}.nm{color:#566;font-size:13px}
.px{font-size:26px;font-weight:800}.mnav{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}.mnav button.x{background:#e53935;color:#fff}
.row{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0}.box{flex:1;min-width:130px;border-radius:10px;padding:8px 10px;text-align:center;border:1px solid}
.box b{display:block;font-size:19px}.box span{display:block;font-size:12px;line-height:1.5}.b-stop{border-color:#ef9a9a;background:#fff1f1;color:#c62828}.b-entry{border-color:#90caf9;background:#eef6ff;color:#1565c0}
.b-tgt{border-color:#a5d6a7;background:#eefbef;color:#2e7d32}.b-tg2{border-color:#ffe082;background:#fffbea;color:#8a6500}
.fair{border:1px solid #f5b5b5;background:#fff4f4;border-radius:10px;padding:8px 12px;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}.fair.good{border-color:#a5d6a7;background:#f1fbf2}
.cv{background:#0f1730;border-radius:10px;overflow:hidden;margin:10px 0}canvas{display:block}
.ex p{margin:6px 0;line-height:1.8;overflow-wrap:anywhere;word-break:break-word;max-width:100%}.modal{overflow-wrap:anywhere}.ex{background:#f9fbff;border:1px solid #dfe6f6;border-radius:10px;padding:8px 14px}
.mtabs{display:flex;flex-wrap:wrap;gap:4px;border-bottom:2px solid var(--gold);margin:10px 0 8px}.mtabs button{background:#e6eaf5;color:var(--navy);border-radius:8px 8px 0 0;padding:6px 12px}.mtabs button.on{background:var(--navy);color:#fff}
table.kv{width:100%;border-collapse:collapse}table.kv td{border-bottom:1px solid var(--line);padding:6px 8px;font-size:13px}table.kv td:first-child{color:#667;width:38%}table.kv tr:nth-child(even) td{background:#f6f8fc}
@media(max-width:700px){.px,.sym{font-size:20px}.tools input{min-width:100%}}

:root{--navy:#0b1736;--navy2:#16295c;--gold:#f5b700;--bg:#eef2f9;--line:#e1e7f2;--ink:#17203a;--up:#00a152;--dn:#d32f2f;--card:#fff;--shadow:0 6px 22px rgba(11,23,54,.10)}
body{background:linear-gradient(180deg,#eef2f9 0,#f6f8fc 320px);font-size:14px}
button,input,select,table{font-family:'Cairo',inherit}
.hdr{background:linear-gradient(120deg,#0b1736 0,#16295c 60%,#1f3a7d 100%);border-bottom:3px solid var(--gold);box-shadow:var(--shadow)}
.hdr h1{font-weight:800;letter-spacing:.2px}.hdr h1::before{content:"\1F4E1  "}
button{border-radius:10px;box-shadow:0 1px 0 rgba(0,0,0,.08);transition:transform .08s,filter .15s}button:active{transform:translateY(1px)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:10px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:10px 14px;box-shadow:var(--shadow);border-inline-start:5px solid var(--gold)}
.kpi span{display:block;font-size:12px;color:#5a6682}.kpi b{display:block;font-size:22px;color:var(--navy);line-height:1.3}.kpi small{color:#7a859e}
.kpi.g{border-inline-start-color:#00c853}.kpi.b{border-inline-start-color:#2979ff}.kpi.r{border-inline-start-color:#e53935}
.banner{border-radius:12px;border:1px solid rgba(0,0,0,.06);font-weight:600;line-height:1.7}
.tools{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:10px;box-shadow:var(--shadow)}
.tools input,.tools select{border-radius:10px;border:1px solid #cdd7ea}
.tabs{border-bottom:3px solid var(--gold)}.tabs button{border-radius:10px 10px 0 0;box-shadow:none}
.tw{border-radius:0 0 14px 14px;box-shadow:var(--shadow)}
#tbl th{background:linear-gradient(180deg,#16295c,#0b1736);font-weight:700}
#tbl tr:nth-child(even) td{background:#f5f8fe}#tbl tr:hover td{background:#fff2c2}
#tbl td.s{font-weight:800}
.sc{display:inline-block;min-width:70px;position:relative;text-align:center;border-radius:8px;background:#e9eef8;overflow:hidden;font-weight:700}
.sc i{position:absolute;inset:0 auto 0 0;opacity:.28;border-radius:8px}.sc b{position:relative;padding:1px 6px;font-weight:700}
.badge{box-shadow:0 1px 3px rgba(0,0,0,.2)}
.modal{border-radius:18px;border-top:5px solid var(--gold)}
.mtabs button.on,.tabs button.on{background:linear-gradient(180deg,#16295c,#0b1736);color:#fff}
.box{box-shadow:0 2px 8px rgba(11,23,54,.06)}
.fair small{color:#6b7790}
.chipc{display:inline-block;border-radius:10px;padding:0 8px;font-size:12px;font-weight:700;background:#e8eefc;color:#16295c;margin-inline-start:6px}
@media(max-width:700px){.kpi b{font-size:18px}}
@media print{.tools,.tabs,.hb,.mbg,.hint{display:none!important}.tw{max-height:none}body{background:#fff}}
</style></head><body>
<div class="hdr"><div><h1 id="ttl"></h1><small id="sub"></small></div><div class="hb"><button id="bLang"></button><button id="bCsv"></button><button id="bPrint"></button></div></div>
<div class="wrap">
<div id="ban"></div>
<div class="kpis" id="kpis"></div>
<div class="tools"><input id="q" type="search"><select id="fd"></select><select id="fm"></select><select id="fs"></select><span id="chips"></span><span id="cnt" class="hint"></span></div>
<div class="tabs" id="tabs"></div>
<div class="tw"><table id="tbl"></table></div>
<div class="hint" id="hint"></div>
<details class="guide"><summary id="gs"></summary><div class="gl" id="gb"></div></details>
<div class="foot" id="note"></div>
</div>
<div class="mbg" id="mbg"><div class="modal" id="modal"></div></div>
<script>
(function(){
var D=__DATA__;
var S={lang:D.defLang,group:'summary',sk:'',sd:1,q:'',fd:'',fm:'',fs:'',cur:-1,tab:'overview'};
var AR=/[\u0600-\u06FF]/;
var ICON={'\uD83D\uDFE2':'#00c853','\uD83D\uDD34':'#e53935','\uD83D\uDFE1':'#ffb300','\uD83D\uDFE0':'#fb8c00','\uD83D\uDD35':'#2979ff','\u26AA':'#bdbdbd','\uD83D\uDFE6':'#26c6da','\uD83D\uDFEA':'#ab47bc'};
var LONGK={name:1,uni_notes:1,rd_reasons_full:1,px_location:1,px_rs_detail:1,auto_style:1,px_near:1,fv_models:1,tg_text:1,explain:1};
function $(id){return document.getElementById(id);}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function ic(h){for(var k in ICON){if(ICON.hasOwnProperty(k)){h=h.split(k).join('<i class="dot" style="background:'+ICON[k]+'"></i>');}}return h;}
function U(k){return D.ui[S.lang][k]||k;}
function txt(r,k){var v=r[S.lang][k];return(v===undefined||v===null||v==='')?'\u2014':String(v);}
function fx(t){var h=ic(esc(t));return AR.test(t)?h:'<span dir="ltr" class="i">'+h+'</span>';}
function H(k){return D.hdrs[S.lang][k]||k;}
function cellHtml(r,k){
  var t=txt(r,k);
  if(k==='uni_decision'){return '<span class="badge" style="background:'+(D.decColor[r.dec]||'#777')+'">'+esc(t)+'</span>';}
  if((k==='uni_score'||k==='rd_score'||k==='fv_conf')&&r.raw[k]!==undefined){var sv=Math.max(0,Math.min(100,r.raw[k])),sc=sv>=75?'#00c853':(sv>=60?'#2979ff':(sv>=45?'#ffb300':'#9e9e9e'));return '<span class="sc"><i style="width:'+sv+'%;background:'+sc+'"></i><b>'+esc(t)+'</b></span>';}
  var cls='';if(D.signed.indexOf(k)>=0){var rv=r.raw[k];cls=rv>0?'pos':(rv<0?'neg':'');}
  return '<span class="'+cls+'">'+fx(t)+'</span>';
}
function grp(id){for(var i=0;i<D.groups.length;i++){if(D.groups[i].id===id){return D.groups[i];}}return D.groups[0];}
function visible(){
  var out=[],i,r,q=S.q.toLowerCase();
  for(i=0;i<D.rows.length;i++){r=D.rows[i];
    if(S.fd&&r.dec!==S.fd){continue;}if(S.fm&&r.mkt!==S.fm){continue;}if(S.fs&&r.sty!==S.fs){continue;}
    if(q&&(r.sym+' '+r.name+' '+(r.ar.name||'')).toLowerCase().indexOf(q)<0){continue;}
    out.push(i);}
  if(S.sk){var k=S.sk,d=S.sd;out.sort(function(a,b){var ra=D.rows[a].raw[k],rb=D.rows[b].raw[k];
    if(ra!==undefined&&rb!==undefined){return(ra-rb)*d;}
    var ta=txt(D.rows[a],k),tb=txt(D.rows[b],k);return(ta<tb?-1:(ta>tb?1:0))*d;});}
  return out;
}
function renderTable(){
  var g=grp(S.group),idx=visible(),h='<thead><tr>',i,j,k;
  for(j=0;j<g.keys.length;j++){k=g.keys[j];h+='<th data-k="'+k+'">'+esc(H(k))+(S.sk===k?(S.sd>0?' \u25B2':' \u25BC'):'')+'</th>';}
  h+='</tr></thead><tbody>';
  for(i=0;i<idx.length;i++){var r=D.rows[idx[i]];h+='<tr>';
    for(j=0;j<g.keys.length;j++){k=g.keys[j];var c=(k==='symbol')?'s':(LONGK[k]?'l':'');
      h+='<td class="'+c+'" data-i="'+idx[i]+'" data-k="'+k+'">'+(k==='symbol'?'<span dir="ltr" class="i">'+esc(r.sym)+'</span>':cellHtml(r,k))+'</td>';}
    h+='</tr>';}
  if(!idx.length){h+='<tr><td colspan="'+g.keys.length+'">'+esc(U('none'))+'</td></tr>';}
  $('tbl').innerHTML=h+'</tbody>';
  $('cnt').textContent=idx.length+' '+U('count');
}
function renderTabs(){
  var h='',i;for(i=0;i<D.groups.length;i++){var g=D.groups[i];h+='<button data-g="'+g.id+'" class="'+(g.id===S.group?'on':'')+'">'+esc(S.lang==='ar'?g.title[1]:g.title[0])+'</button>';}
  $('tabs').innerHTML=h;
}
function renderChips(){
  var cnt={},i;for(i=0;i<D.rows.length;i++){cnt[D.rows[i].dec]=(cnt[D.rows[i].dec]||0)+1;}
  var h='',k;for(k in cnt){if(cnt.hasOwnProperty(k)){h+='<span class="chip" data-d="'+k+'"><span class="badge" style="background:'+D.decColor[k]+'">'+esc(D.decNames[S.lang][k])+'</span> <b>'+cnt[k]+'</b></span>';}}
  $('chips').innerHTML=h;
}
function renderBanners(){
  var h='',i,b,L=S.lang==='ar'?1:0;
  for(i=0;i<D.banners.length;i++){b=D.banners[i];
    h+='<div class="banner" style="background:'+b.color+'">\uD83E\uDDED '+esc(b.mkt[L])+' \u00B7 '+esc(b.bench[L])+': <b>'+ic(esc(b.label[L]))+'</b> | <span dir="ltr" class="i" style="white-space:normal">'+ic(esc(b.text[L]))+'</span></div>';}
  $('ban').innerHTML=h;
}
function renderKpis(){
  var n=D.rows.length,c={},i,sum=0,best=null,bs=-1,L=S.lang;
  for(i=0;i<n;i++){var r=D.rows[i];c[r.dec]=(c[r.dec]||0)+1;var v=r.raw.uni_score;if(v!==undefined){sum+=v;if(v>bs){bs=v;best=r;}}}
  function k(cls,lab,val,sub){return '<div class="kpi '+cls+'"><span>'+esc(lab)+'</span><b>'+val+'</b><small>'+esc(sub||'')+'</small></div>';}
  var h=k('',U('k_total'),n,D.meta.style[L])+k('g',D.decNames[L]['STRONG BUY'],c['STRONG BUY']||0,'')+k('b',D.decNames[L]['BUY DIP'],c['BUY DIP']||0,'')+k('',D.decNames[L]['WATCH'],c['WATCH']||0,'')+k('r',D.decNames[L]['AVOID'],(c['AVOID']||0)+(c['SELL']||0),'')+k('',U('k_avg'),n?(sum/n).toFixed(1):'\u2014','')+(best?k('g',U('k_best'),'<span dir="ltr" class="i">'+esc(best.sym)+'</span>',bs.toFixed(1)):'');
  $('kpis').innerHTML=h;
}
function renderFilters(){
  var f=$('fd'),m=$('fm'),h='<option value="">'+esc(U('all_dec'))+'</option>',k,seen={},i;
  for(k in D.decNames[S.lang]){if(D.decNames[S.lang].hasOwnProperty(k)){h+='<option value="'+k+'"'+(S.fd===k?' selected':'')+'>'+esc(D.decNames[S.lang][k])+'</option>';}}
  f.innerHTML=h;
  var sf=$('fs'),sh='<option value="">'+esc(U('all_sty'))+'</option>',ss={},j;
  for(j=0;j<D.rows.length;j++){var sy=D.rows[j].sty;if(sy&&!ss[sy]){ss[sy]=1;sh+='<option value="'+sy+'"'+(S.fs===sy?' selected':'')+'>'+esc((D.styleNames[S.lang]||{})[sy]||sy)+'</option>';}}
  sf.innerHTML=sh;
  h='<option value="">'+esc(U('all_mkt'))+'</option>';
  for(i=0;i<D.rows.length;i++){var mk=D.rows[i].mkt;if(!seen[mk]){seen[mk]=1;h+='<option value="'+mk+'"'+(S.fm===mk?' selected':'')+'>'+esc(D.rows[i][S.lang].market)+'</option>';}}
  m.innerHTML=h;
}
function applyUi(){
  document.documentElement.lang=S.lang;document.documentElement.dir=S.lang==='ar'?'rtl':'ltr';
  $('ttl').textContent=U('title');$('sub').innerHTML=esc(U('sub'))+' \u00B7 <span dir="ltr" class="i">'+esc(D.meta.gen)+'</span> \u00B7 '+esc(U('data_as'))+' <span dir="ltr" class="i">'+esc(D.meta.asof)+'</span> \u00B7 '+D.meta.n+' '+esc(U('symbols'))+' \u00B7 '+esc(U('style'))+': '+esc(D.meta.style[S.lang]);
  $('bLang').textContent=U('lang');$('bCsv').textContent=U('csv');$('bPrint').textContent=U('print');$('q').placeholder=U('search');
  $('gs').textContent=U('guide');$('gb').innerHTML=D.guide[S.lang];$('note').textContent=D.note[S.lang];$('hint').textContent=U('hint');
  renderBanners();renderKpis();renderFilters();renderChips();renderTabs();renderTable();if(S.cur>=0){renderModal();}
}
function tabFor(k){
  if(k.indexOf('dp_')===0||k.indexOf('fv_')===0){return 'fair';}if(k.indexOf('px_')===0){return 'technical';}
  if(k.indexOf('tg_')===0||k.indexOf('zb_')===0){return 'targets';}if(k.indexOf('vt_')===0){return D.sim?'simulated':'overview';}
  if(k.indexOf('mkt_')===0){return 'market';}if(k.indexOf('rd_')===0){return 'radar';}if(k.indexOf('base_')===0){return 'original';}return 'overview';
}
function box(cls,label,val,sub){return '<div class="box '+cls+'"><span>'+esc(label)+'</span><b>'+fx(val)+'</b><span>'+fx(sub||'')+'</span></div>';}
function overview(r){
  var d=r[S.lang],h='',up=r.raw.fv_upside,good=(up!==undefined&&up>=0);
  h+='<div class="fair'+(good?' good':'')+'"><span>'+esc(U('fair'))+': <b>'+fx(d.fv_fair)+'</b> <small>('+esc(d.fv_source)+')</small></span><span class="'+(good?'pos':'neg')+'">'+fx(d.fv_upside)+' \u00B7 '+esc(d.fv_verdict)+'</span><span><small>'+esc(U('conf'))+'</small> <span class="chipc">'+fx(d.fv_conf)+'</span> <small>'+fx(d.fv_low)+' \u2013 '+fx(d.fv_high)+'</small></span></div>';
  h+='<div class="row">'+box('b-stop',U('stop'),d.zb_stop,d.zb_stop_pct)+box('b-entry',U('entry'),d.zb_entry,d.zb_low+' \u2013 '+d.zb_high)+box('b-tgt',U('target'),d.zb_target,d.zb_target_pct+' \u00B7 R:R 1:'+d.zb_rr)+'</div>';
  if(r.raw.tg_inv!==undefined){h+='<div class="row">'+box('b-tg2',U('fib1'),d.tg_fib1,d.tg_fib1_pct)+box('b-tg2',U('inv')+' \u00B7 '+d.auto_style,d.tg_inv,d.tg_inv_pct+' \u00B7 '+d.tg_inv_src)+box('b-tg2',U('ext'),d.tg_stretch,d.tg_stretch_pct)+'</div>';}
  h+='<div class="cv"><canvas id="cv"></canvas></div>';
  var ps=String(d.explain).split('\n'),i,e='';for(i=0;i<ps.length;i++){e+='<p>'+fx(ps[i]).replace(/^<span dir="ltr" class="i">(.*)<\/span>$/,'$1')+'</p>';}
  h+='<h3>'+esc(U('expl'))+'</h3><div class="ex">'+e+'</div>';
  return h;
}
function kv(r,id){
  var g=grp(id),h='<table class="kv">',i,k;
  for(i=0;i<g.keys.length;i++){k=g.keys[i];if(k==='symbol'){continue;}h+='<tr><td>'+esc(H(k))+'</td><td>'+cellHtml(r,k)+'</td></tr>';}
  return h+'</table>';
}
function renderModal(){
  var r=D.rows[S.cur],d=r[S.lang],tabs=['overview','radar','technical','fair','targets','market'],i;
  if(D.sim){tabs.push('simulated');}tabs.push('original');
  var h='<div class="mnav"><button id="mPrev">'+esc(U('prev'))+'</button><button id="mNext">'+esc(U('next'))+'</button><button class="x" id="mClose">'+esc(U('close'))+'</button></div>';
  h+='<div class="mh"><div><div class="sym"><span dir="ltr" class="i">'+esc(r.sym)+'</span></div><div class="nm">'+fx(d.name)+' \u00B7 '+fx(d.sector||'')+'</div></div><div style="text-align:end"><div class="px">'+fx(d.price)+'</div><div class="'+(r.raw.chg>0?'pos':(r.raw.chg<0?'neg':''))+'">'+fx(d.chg)+'</div></div></div>';
  h+='<div style="margin:8px 0"><span class="badge" style="background:'+D.decColor[r.dec]+'">'+esc(d.uni_decision)+'</span> &nbsp; '+esc(U('score'))+': <b>'+fx(d.uni_score)+'</b> ('+esc(d.uni_grade)+') &nbsp; '+fx(d.auto_style)+' &nbsp; '+esc(U('index'))+': '+fx(d.mkt_label)+'</div>';
  h+='<div class="mtabs">';
  for(i=0;i<tabs.length;i++){var g=tabs[i],lab=(g==='overview')?U('overview'):(S.lang==='ar'?grp(g).title[1]:grp(g).title[0]);h+='<button data-t="'+g+'" class="'+(g===S.tab?'on':'')+'">'+esc(lab)+'</button>';}
  h+='</div><div id="mbody">'+(S.tab==='overview'?overview(r):kv(r,S.tab))+'</div>';
  $('modal').innerHTML=h;$('mbg').className='mbg on';
  if(S.tab==='overview'){drawChart($('cv'),r.chart);}
}
var LVC={stop:'#ef5350',entry:'#42a5f5',target:'#66bb6a',fair:'#ba68c8',sup:'#26a69a',res:'#ff7043',inv:'#ffd54f'};
function drawChart(cv,ch){
  if(!cv||!ch||!ch.c||!ch.c.length){return;}
  var par=cv.parentNode,w=par.clientWidth||700,h=310,dpr=window.devicePixelRatio||1;
  cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr);cv.style.width=w+'px';cv.style.height=h+'px';
  var g=cv.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);g.fillStyle='#0f1730';g.fillRect(0,0,w,h);
  var n=ch.c.length,pl=6,pr=82,pt=12,pb=20,cw=(w-pl-pr)/n,lo=1e18,hi=-1e18,i,k;
  for(i=0;i<n;i++){if(ch.l[i]<lo){lo=ch.l[i];}if(ch.h[i]>hi){hi=ch.h[i];}}
  var rng0=hi-lo,use={};
  for(k in ch.lv){if(ch.lv.hasOwnProperty(k)&&ch.lv[k]!==null&&ch.lv[k]>lo-rng0*0.6&&ch.lv[k]<hi+rng0*0.6){use[k]=ch.lv[k];if(ch.lv[k]<lo){lo=ch.lv[k];}if(ch.lv[k]>hi){hi=ch.lv[k];}}}
  var pad=(hi-lo)*0.04;lo-=pad;hi+=pad;
  function Y(p){return pt+(hi-p)/(hi-lo)*(h-pt-pb);}
  g.font='11px Cairo,sans-serif';g.lineWidth=1;g.strokeStyle='#243055';g.fillStyle='#8fa0cc';
  for(i=0;i<=4;i++){var pv=lo+(hi-lo)*i/4,yy=Y(pv);g.beginPath();g.moveTo(pl,yy);g.lineTo(w-pr,yy);g.stroke();g.textAlign='left';g.fillText(pv.toFixed(pv>=1?2:4),w-pr+4,yy+4);}
  for(i=0;i<n;i++){var x=pl+i*cw+cw/2,up=ch.c[i]>=ch.o[i],col=up?'#26a69a':'#ef5350';
    g.strokeStyle=col;g.fillStyle=col;g.beginPath();g.moveTo(x,Y(ch.h[i]));g.lineTo(x,Y(ch.l[i]));g.stroke();
    var yt=Y(Math.max(ch.o[i],ch.c[i])),yb=Y(Math.min(ch.o[i],ch.c[i]));g.fillRect(x-cw*0.35,yt,Math.max(cw*0.7,1),Math.max(yb-yt,1));}
  function line(arr,col){g.strokeStyle=col;g.lineWidth=1.3;g.beginPath();var st=false,j;for(j=0;j<n;j++){if(arr[j]===null){continue;}var xx=pl+j*cw+cw/2;if(!st){g.moveTo(xx,Y(arr[j]));st=true;}else{g.lineTo(xx,Y(arr[j]));}}g.stroke();}
  line(ch.ema,'#29b6f6');line(ch.sma,'#ec407a');line(ch.wma,'#fdd835');g.lineWidth=1;
  var names={stop:U('stop'),entry:U('entry'),target:U('target'),fair:U('fair'),sup:U('sup'),res:U('res'),inv:U('inv')};
  var order=[];for(k in use){if(use.hasOwnProperty(k)){order.push(k);}}
  order.sort(function(a,b){return Y(use[a])-Y(use[b]);});
  var lastY=-99;
  for(i=0;i<order.length;i++){k=order[i];var yy2=Y(use[k]);g.strokeStyle=LVC[k];g.fillStyle=LVC[k];if(g.setLineDash){g.setLineDash([5,4]);}g.beginPath();g.moveTo(pl,yy2);g.lineTo(w-pr,yy2);g.stroke();if(g.setLineDash){g.setLineDash([]);}
    var ly=Math.max(yy2+4,lastY+12);lastY=ly;g.textAlign='left';g.fillText(names[k]+' '+use[k].toFixed(use[k]>=1?2:4),w-pr+4,ly);}
  g.fillStyle='#8fa0cc';g.textAlign='left';g.fillText(ch.d0,pl,h-5);g.textAlign='right';g.fillText(ch.d1,w-pr,h-5);
}
function openModal(i,tab){S.cur=i;S.tab=tab||'overview';renderModal();try{history.replaceState(null,'','#'+D.rows[i].sym);}catch(e){}}
function closeModal(){S.cur=-1;$('mbg').className='mbg';try{history.replaceState(null,'',location.pathname);}catch(e){}}
function step(dlt){var idx=visible(),p=idx.indexOf(S.cur);if(p<0){p=0;}p=(p+dlt+idx.length)%idx.length;if(idx.length){S.tab='overview';openModal(idx[p],S.tab);}}
function up(el,tag){while(el&&el.nodeName!==tag){el=el.parentNode;}return el;}
$('tbl').onclick=function(e){
  var el=e.target||e.srcElement,th=up(el,'TH');
  if(th){var k=th.getAttribute('data-k');if(S.sk===k){S.sd=-S.sd;}else{S.sk=k;S.sd=1;}renderTable();return;}
  var td=up(el,'TD');if(td&&td.getAttribute('data-i')!==null){openModal(parseInt(td.getAttribute('data-i'),10),tabFor(td.getAttribute('data-k')));}
};
$('tabs').onclick=function(e){var b=up(e.target||e.srcElement,'BUTTON');if(b){S.group=b.getAttribute('data-g');S.sk='';renderTabs();renderTable();}};
$('chips').onclick=function(e){var c=e.target||e.srcElement;while(c&&!(c.getAttribute&&c.getAttribute('data-d'))){c=c.parentNode;}if(c){S.fd=(S.fd===c.getAttribute('data-d'))?'':c.getAttribute('data-d');renderFilters();renderTable();}};
$('q').oninput=function(){S.q=this.value;renderTable();};
$('fd').onchange=function(){S.fd=this.value;renderTable();};$('fm').onchange=function(){S.fm=this.value;renderTable();};$('fs').onchange=function(){S.fs=this.value;renderTable();};
$('bLang').onclick=function(){S.lang=S.lang==='ar'?'en':'ar';applyUi();};
$('bPrint').onclick=function(){window.print();};
$('bCsv').onclick=function(){
  var g=grp(S.group),idx=visible(),rows=[],i,j,line=[];
  for(j=0;j<g.keys.length;j++){line.push('"'+H(g.keys[j]).replace(/"/g,'""')+'"');}rows.push(line.join(','));
  for(i=0;i<idx.length;i++){line=[];for(j=0;j<g.keys.length;j++){line.push('"'+(g.keys[j]==='symbol'?D.rows[idx[i]].sym:txt(D.rows[idx[i]],g.keys[j])).replace(/"/g,'""')+'"');}rows.push(line.join(','));}
  var blob=new Blob(['\uFEFF'+rows.join('\n')],{type:'text/csv;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='ER1991_'+S.group+'.csv';document.body.appendChild(a);a.click();document.body.removeChild(a);
};
$('modal').onclick=function(e){var el=e.target||e.srcElement,b=up(el,'BUTTON');if(!b){return;}
  if(b.id==='mClose'){closeModal();}else if(b.id==='mPrev'){step(-1);}else if(b.id==='mNext'){step(1);}else if(b.getAttribute('data-t')){S.tab=b.getAttribute('data-t');renderModal();}};
$('mbg').onclick=function(e){if((e.target||e.srcElement)===$('mbg')){closeModal();}};
document.onkeydown=function(e){e=e||window.event;if(S.cur<0){return;}if(e.keyCode===27){closeModal();}else if(e.keyCode===37){step(S.lang==='ar'?1:-1);}else if(e.keyCode===39){step(S.lang==='ar'?-1:1);}};
window.onresize=function(){if(S.cur>=0&&S.tab==='overview'){drawChart($('cv'),D.rows[S.cur].chart);}};
applyUi();
var hs=decodeURIComponent((location.hash||'').replace('#','')),hp=hs.split('/');
if(hp[0]){for(var z=0;z<D.rows.length;z++){if(D.rows[z].sym===hp[0]){openModal(z,hp[1]||'overview');break;}}}
})();
</script></body></html>'''

_CAIRO_URL = 'https://github.com/google/fonts/raw/main/ofl/cairo/Cairo%5Bslnt%2Cwght%5D.ttf'
_CAIRO_CSS = {'v': None}
def _cairo_font_css():
    """🆕 v7.0: خط Cairo — يُحمَّل مرة واحدة ويُضمَّن في ملف HTML (base64) ليعمل دون إنترنت؛ وإن تعذّر التحميل يُستخدم رابط Google Fonts + خط Cairo المحلي إن وُجد."""
    if _CAIRO_CSS['v'] is not None: return _CAIRO_CSS['v']
    import base64
    path = os.path.join(OUT_DIR, 'Cairo-VF.ttf'); data = None
    try:
        if os.path.exists(path) and os.path.getsize(path) > 50000:
            data = open(path, 'rb').read()
        else:
            req = urllib.request.Request(_CAIRO_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as r_: data = r_.read()
            if len(data) > 50000: open(path, 'wb').write(data)
            else: data = None
    except Exception:
        data = None
    if data:
        css = "@font-face{font-family:'Cairo';font-style:normal;font-weight:200 1000;font-display:swap;src:url(data:font/ttf;base64," + base64.b64encode(data).decode('ascii') + ") format('truetype')}"
    else:
        css = "@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');@font-face{font-family:'Cairo';src:local('Cairo')}"
    _CAIRO_CSS['v'] = css
    return css

def export_html(res, lang, cards_top=30):
    """HTML تفاعلي: جدول قابل للفرز والتصفية، نافذة بطاقة لكل سهم، رسم بياني، تبديل لغة — ملف واحد يعمل دون إنترنت."""
    payload = _jclean(build_payload(res, lang))
    data = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    path = f'{OUT_DIR}/ER1991_interactive_{_stamp()}.html'
    open(path, 'w', encoding='utf-8').write(HTML_TPL.replace('__FONT__', _cairo_font_css()).replace('__DATA__', data))
    return path


# -----------------------------------------------------------------------------
# 16) التصدير: Excel / CSV / PDF / PNG / Google Sheet (تصميم v2.0)
# -----------------------------------------------------------------------------
def _stamp(): return dt.datetime.now().strftime('%Y%m%d_%H%M')
_TEXT_NUM = {'dp_align', 'px_signal_age'}
def xl_val(k, v, dsp):
    """الأرقام تبقى أرقاماً (للفرز/الصيغ) والنصوص تُعرض باللغة المختارة."""
    if isinstance(v, (bool, np.bool_)): return dsp
    if isinstance(v, (int, float, np.integer, np.floating)) and k not in _TEXT_NUM:
        if isinstance(v, (float, np.floating)):
            if v != v: return None
            if math.isinf(v): return '∞'
            return float(v)
        return int(v)
    return dsp

def sheet_table(res, g, lang):
    keys = [k for k in GROUPS[g][2]]
    rows = []
    for r in res['recs']:
        d = row_display(r, lang)
        rows.append([xl_val(k, r.get(k), d.get(k, '—')) for k in keys])
    return keys, rows

def export_csv(res, lang):
    path = f'{OUT_DIR}/ER1991_results_{_stamp()}.csv'
    cols = []
    for g in active_groups(res):
        for k in GROUPS[g][2]:
            if k not in cols: cols.append(k)
    data = []
    for r in res['recs']:
        d = row_display(r, lang); data.append([xl_val(k, r.get(k), d.get(k, '—')) for k in cols])
    pd.DataFrame(data, columns=[hdr(c, lang) for c in cols]).to_csv(path, index=False, encoding='utf-8-sig'); return path

def export_excel(res, lang):
    path = f'{OUT_DIR}/ER1991_results_{_stamp()}.xlsx'; ar = lang == 'عربي'
    with pd.ExcelWriter(path, engine='xlsxwriter') as xw:
        wb = xw.book
        f_h = wb.add_format(dict(bold=True, font_color='#FFFFFF', bg_color='#0D1B3D', align='center', valign='vcenter', text_wrap=True, border=1))
        f_t = wb.add_format(dict(bold=True, font_size=14, font_color='#0D1B3D'))
        f_n = wb.add_format(dict(num_format='#,##0.00', align='center')); f_c = wb.add_format(dict(align='center', valign='top'))
        f_p = wb.add_format(dict(num_format='+0.00;-0.00;0.00', align='center')); f_w = wb.add_format(dict(text_wrap=True, valign='top'))
        green = wb.add_format(dict(bg_color='#C8F7D4', font_color='#006100')); blue = wb.add_format(dict(bg_color='#D6E6FF', font_color='#0B3D91'))
        yellow = wb.add_format(dict(bg_color='#FFF3C4', font_color='#7A5B00')); red = wb.add_format(dict(bg_color='#FFD6D6', font_color='#9C0006')); gray = wb.add_format(dict(bg_color='#E6E6E6'))
        for g in active_groups(res):
            en, arn = GROUPS[g][0], GROUPS[g][1]
            keys, rows = sheet_table(res, g, lang)
            sn = (arn if ar else en)[:31].replace('/', '-')
            ws = wb.add_worksheet(sn); xw.sheets[sn] = ws
            if ar: ws.right_to_left()
            ws.write(0, 0, f"ER1991 Smart Investment Radar PRO — {arn if ar else en} — {res['meta']['generated']}", f_t)
            for j, k in enumerate(keys):
                ws.write(1, j, hdr(k, lang), f_h)
                wide = k in ('name', 'uni_reasons', 'uni_notes', 'rd_reasons_full', 'px_location', 'px_rs_detail', 'px_near', 'fv_models', 'px_cat_buy', 'px_cat_sell', 'px_smc_counts', 'auto_style', 'tg_text', 'vt_reached')
                w = 110 if k == 'explain' else 36 if wide else 13
                is_num = any(isinstance(rw[j], (int, float)) and not isinstance(rw[j], bool) for rw in rows)
                ws.set_column(j, j, w, f_w if k == 'explain' else (f_p if k in PCT_SIGNED else f_n if is_num else f_c))
            for i, rw in enumerate(rows):
                for j, v in enumerate(rw):
                    k = keys[j]
                    if v is None: continue
                    ws.write(i + 2, j, v, f_w if k == 'explain' else (f_p if (k in PCT_SIGNED and isinstance(v, (int, float))) else f_n if (isinstance(v, float)) else f_c))
            ws.set_row(1, 34); ws.freeze_panes(2, 1); ws.autofilter(1, 0, len(rows) + 1, len(keys) - 1)
            for j, k in enumerate(keys):
                rng = (2, j, len(rows) + 1, j)
                if k in ('uni_decision', 'base_decision', 'px_final', 'dp_decision', 'sc_signal', 'fv_verdict', 'rd_rating', 'uni_signal', 'mkt_label'):
                    for txt, fm_ in (('Deep Value', green), ('خصم كبير', green), ('Rich', red), ('غالٍ جداً', red), ('Bear', red), ('سوق هابط', red), ('Recovery', blue), ('تعافٍ', blue), ('Healthy', green), ('صحي', green), ('STRONG BUY', green), ('Strong Buy', green), ('شراء قوي', green), ('BUY DIP', blue), ('Buy on dip', blue), ('شراء عند التراجع', blue), ('High Pot', blue), ('إمكانات عالية', blue),
                                     ('SELL', red), ('Sell', red), ('بيع', red), ('AVOID', gray), ('Avoid', gray), ('تجنّب', gray), ('Overvalued', red), ('مرتفع', red), ('Crash', red), ('انهيار', red), ('Correction', red), ('تصحيح', red),
                                     ('Downtrend', red), ('هبوط', red), ('WATCH', yellow), ('Watch', yellow), ('متابعة', yellow), ('Weak', yellow), ('ضعف', yellow), ('Rebound', yellow), ('ارتداد', yellow), ('Fair', yellow), ('عادل', yellow),
                                     ('Uptrend', green), ('صاعد', green), ('Undervalued', green), ('رخيص', green), ('BUY', green), ('شراء', green)):
                        ws.conditional_format(*rng, dict(type='text', criteria='containing', value=txt, format=fm_, stop_if_true=True))
                if k in ('uni_score', 'rd_score', 'base_score', 'px_buy_pct', 'dp_inv', 'dp_ent'):
                    ws.conditional_format(*rng, dict(type='3_color_scale', min_color='#F8696B', mid_color='#FFEB84', max_color='#63BE7B', min_type='num', min_value=0, mid_type='num', mid_value=50, max_type='num', max_value=100))
                if k in ('chg', 'fv_upside', 'zb_target_pct', 'tg_inv_pct'):
                    ws.conditional_format(*rng, dict(type='cell', criteria='>', value=0, format=green)); ws.conditional_format(*rng, dict(type='cell', criteria='<', value=0, format=red))
        sh = wb.add_worksheet('Guide'); sh.set_column(0, 0, 150)
        if ar: sh.right_to_left()
        sh.write(0, 0, 'دليل القراءة والمنهجية' if ar else 'Reading guide & methodology', f_t)
        lines = [re.sub(r'<[^>]+>', '', x) for x in methodology_points(res, lang)] + ['', NOTE_AR if ar else NOTE_EN] + [''] + res['meta']['log']
        for i, l_ in enumerate(lines): sh.write(i + 2, 0, l_, f_w)
    return path

def export_pdf(res, lang, cards_top=30):
    path = f'{OUT_DIR}/ER1991_report_{_stamp()}.pdf'
    html = build_html(res, lang, cards_top)
    try:
        from weasyprint import HTML
        HTML(string=html).write_pdf(path)
        return path
    except Exception as e:
        print('⚠️ تعذّر WeasyPrint (', type(e).__name__, ') — سأستخدم بديل matplotlib للـPDF.')
        return _matplotlib_report(res, lang, path, pdf=True)

def export_png(res, lang, cards_top=30, dpi=110):
    """يحوّل صفحات الـPDF إلى صور PNG ويضغطها في ZIP. يعيد (zip, أول صفحة)."""
    pdf = export_pdf(res, lang, cards_top); base = pdf.rsplit('.', 1)[0]
    pngs = []
    try:
        from pdf2image import convert_from_path
        for i, im in enumerate(convert_from_path(pdf, dpi=dpi), 1):
            fp = f'{base}_p{i:02d}.png'; im.save(fp); pngs.append(fp)
    except Exception as e:
        print('⚠️ تعذّر pdf2image:', e); pngs = [_matplotlib_report(res, lang, base + '_summary.png', pdf=False)]
    zp = base + '_png.zip'
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for f_ in pngs: z.write(f_, os.path.basename(f_))
    return zp, pngs[0]

def _matplotlib_report(res, lang, path, pdf=False):
    """بديل بسيط: جدول ملخص بالصورة/PDF عبر matplotlib (يدعم العربية إن توفر arabic_reshaper+bidi)."""
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    try:
        import arabic_reshaper; from bidi.algorithm import get_display
        fx = (lambda s: get_display(arabic_reshaper.reshape(str(s)))) if lang == 'عربي' else str
    except Exception:
        fx = str; lang = 'English'
    keys = ['symbol', 'price', 'chg', 'uni_score', 'uni_decision', 'fv_fair', 'fv_upside', 'zb_entry', 'zb_stop', 'zb_target', 'zb_rr', 'px_final', 'rd_rating']
    cell = []
    for r in res['recs'][:60]:
        d = row_display(r, lang); cell.append([fx(re.sub(r'[^\x00-\u06FF ]', '', str(d.get(k, '—'))) or '—') for k in keys])
    fig, ax = plt.subplots(figsize=(16, 0.32 * len(cell) + 1.4)); ax.axis('off')
    t = ax.table(cellText=cell, colLabels=[fx(hdr(k, lang)) for k in keys], loc='center', cellLoc='center'); t.auto_set_font_size(False); t.set_fontsize(7); t.scale(1, 1.25)
    for (i, j), c in t.get_celld().items():
        if i == 0: c.set_facecolor('#0D1B3D'); c.get_text().set_color('white')
    ax.set_title('ER1991 Smart Investment Radar PRO', fontsize=13)
    fig.savefig(path, bbox_inches='tight', dpi=130); plt.close(fig); return path

def export_gsheet(res, lang):
    """ينشئ Google Sheet جديداً في حسابك (يتطلب تسجيل الدخول داخل كولاب)."""
    from google.colab import auth; auth.authenticate_user()
    import gspread; from google.auth import default
    creds, _ = default(); gc = gspread.authorize(creds)
    title = f'ER1991 Report {_stamp()}'; sh = gc.create(title); ar = lang == 'عربي'
    first = True
    for g in active_groups(res):
        en, arn = GROUPS[g][0], GROUPS[g][1]
        keys, rows = sheet_table(res, g, lang)
        data = [[hdr(k, lang) for k in keys]] + [[('' if v is None else v) for v in row] for row in rows]
        name = (arn if ar else en)[:90]
        ws = sh.sheet1 if first else sh.add_worksheet(title=name, rows=len(data) + 5, cols=len(keys) + 2)
        if first: ws.update_title(name); first = False
        ws.update(range_name='A1', values=data, value_input_option='USER_ENTERED')
        sid = ws.id
        reqs = [dict(repeatCell=dict(range=dict(sheetId=sid, startRowIndex=0, endRowIndex=1),
                     cell=dict(userEnteredFormat=dict(backgroundColor=dict(red=.05, green=.1, blue=.24), horizontalAlignment='CENTER', wrapStrategy='WRAP',
                               textFormat=dict(bold=True, foregroundColor=dict(red=1, green=1, blue=1)))), fields='userEnteredFormat(backgroundColor,horizontalAlignment,wrapStrategy,textFormat)')),
                dict(updateSheetProperties=dict(properties=dict(sheetId=sid, gridProperties=dict(frozenRowCount=1, frozenColumnCount=1), rightToLeft=ar), fields='gridProperties(frozenRowCount,frozenColumnCount),rightToLeft')),
                dict(setBasicFilter=dict(filter=dict(range=dict(sheetId=sid, startRowIndex=0, endRowIndex=len(data), startColumnIndex=0, endColumnIndex=len(keys))))),
                dict(autoResizeDimensions=dict(dimensions=dict(sheetId=sid, dimension='COLUMNS', startIndex=0, endIndex=len(keys))))]
        for j, k in enumerate(keys):
            if k in ('uni_decision', 'px_final', 'base_decision', 'dp_decision'):
                for txt, col in (('STRONG', (.78, .97, .83)), ('شراء قوي', (.78, .97, .83)), ('BUY', (.84, .9, 1)), ('شراء', (.84, .9, 1)), ('WATCH', (1, .95, .77)), ('Watch', (1, .95, .77)), ('متابعة', (1, .95, .77)),
                                 ('SELL', (1, .84, .84)), ('Sell', (1, .84, .84)), ('بيع', (1, .84, .84)), ('AVOID', (.9, .9, .9)), ('Avoid', (.9, .9, .9)), ('تجنّب', (.9, .9, .9))):
                    reqs.append(dict(addConditionalFormatRule=dict(index=0, rule=dict(ranges=[dict(sheetId=sid, startRowIndex=1, endRowIndex=len(data), startColumnIndex=j, endColumnIndex=j + 1)],
                                booleanRule=dict(condition=dict(type='TEXT_CONTAINS', values=[dict(userEnteredValue=txt)]), format=dict(backgroundColor=dict(red=col[0], green=col[1], blue=col[2])))))))
        try: sh.batch_update(dict(requests=reqs))
        except Exception as e: print('تنبيه تنسيق الورقة', name, ':', e)
    return sh.url

def plot_symbol(rec, bars=200):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    df = rec['_df']; p = P; n0 = max(0, len(df) - bars)
    c = df['Close']
    ema = s_ema(c, p['emaFast']); sma = s_sma(c, p['smaSlow']); wma = s_wma(c, p['wmaLen']); st, sd = s_supertrend(df, p['stPeriod'], p['stMult'])
    d = df.iloc[n0:]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.78, 0.22], vertical_spacing=0.02)
    fig.add_trace(go.Candlestick(x=d.index, open=d.Open, high=d.High, low=d.Low, close=d.Close, name=rec['symbol'],
                                 increasing_line_color='#26a69a', decreasing_line_color='#ef5350'), 1, 1)
    for s_, nm, col in ((ema, f"EMA{p['emaFast']}", '#29b6f6'), (sma, f"SMA{p['smaSlow']}", '#ec407a'), (wma, f"WMA{p['wmaLen']}", '#fdd835')):
        fig.add_trace(go.Scatter(x=d.index, y=s_.iloc[n0:], name=nm, line=dict(width=1.3, color=col)), 1, 1)
    stu = st.iloc[n0:].where(sd.iloc[n0:] < 0); std = st.iloc[n0:].where(sd.iloc[n0:] > 0)
    fig.add_trace(go.Scatter(x=d.index, y=stu, name='SuperTrend ↑', line=dict(width=1.5, color='#00c853')), 1, 1)
    fig.add_trace(go.Scatter(x=d.index, y=std, name='SuperTrend ↓', line=dict(width=1.5, color='#e53935')), 1, 1)
    sg = [(i, dr, g) for (i, dr, g) in rec['_px']['signals'] if i >= n0]
    if sg:
        fig.add_trace(go.Scatter(x=[df.index[i] for i, _, _ in sg], y=[df.Low.iloc[i] * 0.985 if dr == 'BUY' else df.High.iloc[i] * 1.015 for i, dr, _ in sg],
                                 mode='markers+text', text=[f'{dr} {g}' for _, dr, g in sg], textposition='bottom center',
                                 marker=dict(symbol=['triangle-up' if dr == 'BUY' else 'triangle-down' for _, dr, _ in sg], size=11,
                                             color=['#00c853' if dr == 'BUY' else '#e53935' for _, dr, _ in sg]), name='Signals'), 1, 1)
    lines = [(rec.get('zb_stop'), 'Stop', '#e53935', 'dash'), (rec.get('zb_entry'), 'Entry', '#1e88e5', 'dash'), (rec.get('zb_target'), 'Target', '#00c853', 'dash'),
             (rec.get('fv_fair'), 'Fair value', '#ab47bc', 'dot'), (rec.get('px_support'), 'Support', '#43a047', 'dot'), (rec.get('px_resistance'), 'Resistance', '#e53935', 'dot'),
             (rec.get('px_vpoc'), 'VPOC', '#8e24aa', 'dot'), (rec.get('px_fibH'), 'Fib 100%', '#ffa726', 'dot'), (rec.get('px_fibL'), 'Fib 0%', '#9e9e9e', 'dot')]
    for y, nm, col, ds in lines:
        if nn(y): fig.add_hline(y=y, line=dict(color=col, dash=ds, width=1), annotation_text=f'{nm} {y:,.2f}', annotation_position='right', row=1, col=1)
    colors = np.where(d.Close >= d.Open, '#26a69a', '#ef5350')
    fig.add_trace(go.Bar(x=d.index, y=d.Volume, marker_color=colors, name='Volume'), 2, 1)
    fig.update_layout(template='plotly_dark', height=640, xaxis_rangeslider_visible=False, margin=dict(l=10, r=70, t=40, b=10),
                      title=f"{rec['symbol']} — {DEC_NAME[rec['uni_decision']][0]} | Score {rec['uni_score']:.1f}", legend=dict(orientation='h', y=1.02))
    return fig

# -----------------------------------------------------------------------------
# 17) الواجهة التفاعلية (Colab)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# 🆕 v7.0: مخطط لوحة الإعدادات الخارجية (شبيهة بإعدادات مؤشرات TradingView) — كل مفتاح موجود في P، والتجاوز يُمرَّر كـp_over فلا حاجة لتعديل الكود
# -----------------------------------------------------------------------------
SETTINGS_SCHEMA = [
 ('🎯 الأسلوب والترتيب', [('autoStyleFund', 'تصنيف Auto يستعين بالأساسيات (P/E · P/B · نمو)'), ('sortByDecision', 'الترتيب: قرار الشراء ثم الدرجة'),
                          ('stabilize', 'استقرار الترتيب (إغلاق مؤكد)'), ('closedAsConfirmed', 'اعتبار شمعة اليوم مؤكدة بعد انتهاء الجلسة')]),
 ('⚖️ القيمة العادلة', [('fvTvFund', 'بيانات TradingView (EPS TTM + قيمة سوقية + أقران)'), ('fvRelOn', 'النموذج النسبي (وسيط القطاع/السوق)'), ('fvRelMinPeers', 'أقل عدد شركات للقطاع'),
                        ('fvMinConf', 'أدنى ثقة لتأثير كامل في القرار'), ('fvGrowthW', 'وزن نمو الشركة الفعلي (0–1)'), ('fvPeHardCap', 'سقف مضاعف P/E بعد العلاوة'),
                        ('fvPbMin', 'أدنى P/B عادل'), ('fvPbMax', 'أعلى P/B عادل'), ('fvBand', 'نطاق «عادل» ± %'), ('fvDeepBand', 'حد الخصم/العلاوة الكبيرة %'),
                        ('fvGrahamScale', 'معايرة رقم جراهام لمضاعف السوق'), ('fvGuardLo', 'حارس النماذج: الحد الأدنى × السعر'), ('fvGuardHi', 'حارس النماذج: الحد الأعلى × السعر'),
                        ('fvSingleAnalystW', 'وزن هدف محلل واحد')]),
 ('🧮 أوزان النماذج', [('fvW.pe', 'P/E'), ('fvW.pb', 'P/B'), ('fvW.graham', 'جراهام'), ('fvW.grahamG', 'جراهام-نمو'), ('fvW.rel', 'نسبي'), ('fvW.analyst', 'المحللون'), ('fvW.ext', 'الهدف الخارجي'),
                       ('fvWFin.pe', 'مالي: P/E'), ('fvWFin.pb', 'مالي: P/B'), ('fvWFin.graham', 'مالي: جراهام'), ('fvWFin.rel', 'مالي: نسبي'), ('fvWFin.analyst', 'مالي: المحللون'), ('fvWFin.ext', 'مالي: خارجي')]),
 ('🧭 حالة السوق', [('mktCorrPct', 'حد التراجع: هبوط عن قمة 20 شمعة %'), ('mktCorrDD', 'تصحيح: هبوط عن القمة ≥ %'), ('mktBearDD', 'سوق هابط: هبوط عن القمة ≥ %'),
                    ('mktCrashDay', 'انهيار: هبوط شمعة المرجع ≥ %'), ('mktCrashWin', 'انهيار: هبوط 5 شموع ≥ %'), ('mktBounceMin', 'ارتداد: صعود من القاع ≥ %'), ('fibMktDDCrash', 'انهيار (فيبو): هبوط ≤ %')]),
 ('📡 الرادار والمخاطرة', [('riskLow', 'مخاطرة منخفضة: ATR% <'), ('riskHigh', 'مخاطرة عالية: ATR% >'), ('crashCandle', 'هبوط شمعة جبري %'), ('gapThresh', 'فجوة كبيرة %'), ('gapAware', 'تعويض الفجوة'),
                           ('minTradedValue', 'أدنى قيمة تداول يومية (0 = معطّل)'), ('lookbackManual', 'نطاق الدعم/المقاومة (Medium)'), ('cmfManual', 'فترة CMF (Medium)')]),
 ('🛡 الحارس', [('guardRiskMax', 'مخاطرة Deep ≥'), ('guardChase', 'ارتفاع اليوم ≥ %'), ('guardNeedTech', 'يتطلب Tech = Conf'), ('guardOnCorr', 'تشديد عند ضغط السوق')]),
 ('📐 الخطة والأهداف', [('stopAtr', 'مضاعف ATR للوقف'), ('targetAtr', 'مضاعف ATR للهدف'), ('capAtRes', 'قصّ الهدف عند القمة'), ('capAtEma', 'قصّ الهدف عند EMA'),
                        ('zbTargetR', 'هدف الخطة (× المخاطرة)'), ('zbStopATR', 'وقف الخطة (× ATR)'), ('slATR', 'وقف الصفقة الافتراضية ×ATR'), ('tp1ATR', 'TP1 ×ATR'), ('tp2ATR', 'TP2 ×ATR'), ('tp3ATR', 'TP3 ×ATR')]),
 ('🏁 أوزان الدرجة الموحدة', [('wUniRadar', 'الرادار'), ('wUniPrime', 'الإشارة الفنية'), ('wUniFair', 'القيمة العادلة'), ('wUniDeep', 'التحليل العميق')]),
]

def _p_get(key, base=None):
    cur = base if base is not None else P
    for part in key.split('.'): cur = cur[part]
    return cur

def parse_ext_targets(text):
    """«SWDY=115.6» أو «EGX:SWDY: 115.6» (سطر/فاصلة) → {'SWDY': 115.6}. الرمز بلا لاحقة ياهو."""
    out = {}
    for part in re.split(r'[\n,;]+', str(text or '')):
        m_ = re.match(r'\s*([^=:\s]+(?::[^=:\s]+)?)\s*[=:]\s*([0-9][0-9.,]*)\s*$', part)
        if not m_: continue
        sym_ = m_[1].upper().split(':')[-1].split('.')[0]
        try: out[sym_] = float(m_[2].replace(',', ''))
        except Exception: pass
    return out

STATE = {'res': None}
SAMPLE = 'AAPL, INTC, NVDA, PYPL, EGX:COMI, JUFO, TADAWUL:2222, XAUUSD, EURUSD, BTC'   # 🆕 v6: أمثلة التعيين الذكي

def _iframe(html, height=620):
    return f'<iframe srcdoc="{_html.escape(html, quote=True)}" width="100%" height="{height}" style="border:1px solid #2a3350;border-radius:8px;background:#fff"></iframe>'

def _download(path):
    """🆕 v6.1 (إصلاح التصدير): تنزيل موثوق في كولاب — حالة واضحة + حجم الملف، وإرشاد فوري عندما يمنع المتصفح التنزيل التلقائي
    (كروم يحجب التنزيلات التلقائية بعد الأولى ما لم يسمح المستخدم بتنزيل «ملفات متعددة» من أيقونة القفل)."""
    ok = False
    try:
        from google.colab import files
        files.download(path); ok = True
    except Exception:
        pass
    try: sz = os.path.getsize(path)
    except Exception: sz = 0
    size_txt = (f'{sz/1048576:.1f} MB' if sz >= 1048576 else f'{max(round(sz/1024), 0)} KB')
    print(('⬇️' if ok else '📁'), path, f'({size_txt})')
    if not ok:
        print('   ℹ️ لم يبدأ التنزيل التلقائي — الملف محفوظ في مجلد التقارير: افتح شجرة الملفات (يسار) ← content ← ER1991_Reports وانقر نقراً مزدوجاً على الملف لتنزيله.')

def detail_html(r, lang):
    d = row_display(r, lang)
    paras = ''.join(f'<p>{hx(x, iso=False)}</p>' for x in d['explain'].split('\n'))
    return (f'<html dir="{"rtl" if lang == "عربي" else "ltr"}"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<table class="grid"><tr><td>{card_html(r, d, lang)}</td></tr></table><div class="ex">{paras}</div></body></html>')

def build_ui():
    import ipywidgets as W
    from IPython.display import display, HTML, clear_output
    lay = W.Layout(width='100%'); sty = {'description_width': '150px'}
    t_syms = W.Textarea(value=SAMPLE, description='الرموز (حتى 100):', layout=W.Layout(width='100%', height='110px'), style=sty,
                        placeholder='افصل بفاصلة أو سطر جديد. أمثلة: AAPL, EGX:COMI, TADAWUL:2222, COMI.CA, 2222.SR')
    d_mkt = W.Dropdown(options=[('تلقائي (Auto)', 'AUTO'), ('🇺🇸 أمريكا', 'US'), ('🇪🇬 مصر — أضف .CA للرموز المجردة', 'EGX'), ('🇸🇦 السعودية — أضف .SR', 'TASI')],
                       value='AUTO', description='سوق الرموز المجردة:', layout=lay, style=sty)
    d_bm = W.Dropdown(options=BENCH_OPTIONS, value='AUTO', description='المؤشر المرجعي:', layout=lay, style=sty)
    d_style = W.Dropdown(options=[('تلقائي لكل سهم (Auto)', 'Auto'), ('قيمة (Value)', 'Value'), ('نمو (Growth)', 'Growth'), ('مضاربة (Swing)', 'Swing'),
                                  ('مدى متوسط (Medium Term)', 'Medium Term'), ('مدى طويل (Long Term)', 'Long Term')], value='Auto', description='أسلوب الاستثمار:', layout=lay, style=sty)
    d_lang = W.Dropdown(options=['عربي', 'English'], value='عربي', description='لغة النتائج والتقارير:', layout=lay, style=sty)
    f_cap = W.FloatText(value=10000.0, description='رأس المال:', style=sty); f_risk = W.FloatText(value=1.0, description='المخاطرة %:', style=sty)
    c_deep = W.Checkbox(value=True, description='التحليل المالي العميق (أبطأ لكن يحسب Piotroski/Altman/Beneish)', layout=lay)
    c_vt = W.Checkbox(value=True, description='🆕 إظهار الصفقة الافتراضية في النتائج (بطاقة + جدول + سجل الوصول للأهداف)', layout=lay)
    c_be = W.Checkbox(value=False, description='فحص وقف التعادل من الشمعة التالية (الافتراضي مغلق = مطابق لـPine؛ فعّله لإزالة انحياز الشارت اليومي)', layout=lay)
    c_intra = W.Checkbox(value=False, description='أطر لحظية حقيقية 15م/30م/1س/4س لمصفوفة الأطر (أبطأ؛ وإلا تُستخدم D1/W1/M1)', layout=lay)
    c_htf = W.Checkbox(value=True, description='اشتراط توافق الأطر العليا (H1/H4) لظهور الإشارة', layout=lay)
    c_corr = W.Checkbox(value=True, description='تفعيل فلتر الارتباط مع DXY (مفعّل افتراضياً مطابقةً لـPine؛ يؤثر عند ارتباط ≥ 0.3 فقط)', layout=lay)
    c_guard = W.Checkbox(value=True, description='نظام الحماية: يخفض «شراء قوي» إلى «شراء عند التراجع» عند تصحيح السوق/مخاطرة عالية/مطاردة', layout=lay)
    i_cards = W.IntSlider(value=30, min=5, max=100, step=5, description='عدد البطاقات بالتقرير:', style=sty, layout=lay)
    # 🆕 v7.0: لوحة الإعدادات الخارجية (تبويبات) + مدخلات السوق للقيمة العادلة + الأهداف الخارجية + تصدير/استيراد JSON
    sw = {}
    def _mk(key, lab):
        d = _p_get(key)
        if isinstance(d, bool): w = W.Checkbox(value=d, description=lab, indent=False, layout=W.Layout(width='96%'))
        elif isinstance(d, int): w = W.IntText(value=d, description=lab, style={'description_width': '230px'}, layout=W.Layout(width='96%'))
        else: w = W.FloatText(value=float(d), step=0.1, description=lab, style={'description_width': '230px'}, layout=W.Layout(width='96%'))
        sw[key] = w; return w
    tab_children, tab_titles = [], []
    for title, items in SETTINGS_SCHEMA:
        tab_children.append(W.VBox([_mk(k, lab) for k, lab in items])); tab_titles.append(title)
    _mk_names = [('EGX', '🇪🇬 مصر'), ('TASI', '🇸🇦 السعودية'), ('US', '🇺🇸 أمريكا')]
    _coe_fields = (('rf', 'فائدة خالية %'), ('g', 'تضخم %'), ('gr', 'نمو حقيقي %'), ('erp', 'علاوة مخاطر %'))
    coe_w = {m: {k: W.FloatText(value=float(FV_COE[m].get(k, FV_GR_DEFAULT)), description=lab, step=0.1, style={'description_width': '95px'}, layout=W.Layout(width='185px'))
                 for k, lab in _coe_fields} for m, _ in _mk_names}
    ext_ta = W.Textarea(value='', placeholder='هدف خارجي لكل سهم، سطر لكل سهم أو مفصول بفاصلة. مثال: SWDY=115.6 ، COMI=130', layout=W.Layout(width='96%', height='70px'))
    coe_box = W.VBox([W.HBox([W.HTML(f'<b style="display:inline-block;width:80px">{nm_}</b>')] + list(coe_w[m].values())) for m, nm_ in _mk_names] +
                     [W.HTML(f'<div style="color:#888;font-size:12px">r = فائدة + علاوة · النمو الاسمي g = (1+تضخم)(1+نمو حقيقي)−1 · المضاعف = (1+g)÷(r−g) بين 5 و20. مراجعة {FV_COE_ASOF} — تقديرية وشديدة الحساسية (خصوصاً مصر).</div>'),
                      W.HTML('<b>🎯 أهداف خارجية (مثل متوسط بنوك الاستثمار) — تدخل كنموذج مستقل بوزن fvW.ext:</b>'), ext_ta])
    tab_children.append(coe_box); tab_titles.append('🌍 مدخلات السوق والأهداف')
    ta_json = W.Textarea(value='', placeholder='الصق هنا إعدادات JSON ثم اضغط «استيراد»', layout=W.Layout(width='96%', height='120px'))
    b_exp = W.Button(description='⬆ تصدير الإعدادات', layout=W.Layout(width='170px')); b_imp = W.Button(description='⬇ استيراد', layout=W.Layout(width='120px')); b_rst = W.Button(description='↺ إعادة الضبط', button_style='warning', layout=W.Layout(width='140px'))
    tab_children.append(W.VBox([W.HBox([b_exp, b_imp, b_rst]), ta_json])); tab_titles.append('💾 حفظ/استيراد')
    tabs_w = W.Tab(children=tab_children)
    for i_, t_ in enumerate(tab_titles): tabs_w.set_title(i_, t_)
    acc = W.Accordion(children=[tabs_w]); acc.set_title(0, '⚙️ لوحة الإعدادات (القيمة العادلة · السوق · الرادار · الحارس · الخطة · الأوزان)'); acc.selected_index = None
    def _val(key, w):
        d = _p_get(key); v = w.value
        return bool(v) if isinstance(d, bool) else int(v) if isinstance(d, int) else float(v)
    def settings_flat():
        out = {}
        for k, w in sw.items():
            v = _val(k, w)
            if v != _p_get(k): out[k] = v
        coe = {m: {k: float(w.value) for k, w in coe_w[m].items()} for m, _ in _mk_names}
        if any(abs(coe[m][k] - float(FV_COE[m].get(k, FV_GR_DEFAULT))) > 1e-9 for m, _ in _mk_names for k in coe[m]): out['fvCoe'] = coe
        ext_ = parse_ext_targets(ext_ta.value)
        if ext_: out['fvExt'] = ext_
        return out
    def coe_over():
        flat = settings_flat(); over = {}
        for k, v in flat.items():
            if '.' in k: a_, b_ = k.split('.'); over.setdefault(a_, {})[b_] = v
            else: over[k] = v
        return over or None
    def _on_exp(_): ta_json.value = json.dumps(settings_flat(), ensure_ascii=False, indent=1)
    def _on_imp(_):
        try: d_ = json.loads(ta_json.value)
        except Exception as e_: ta_json.value = f'❌ JSON غير صالح: {e_}'; return
        for k, v in d_.items():
            if k in sw:
                try: sw[k].value = type(sw[k].value)(v)
                except Exception: pass
            elif k == 'fvCoe':
                for m, dd in v.items():
                    for kk, vv in dd.items():
                        if m in coe_w and kk in coe_w[m]: coe_w[m][kk].value = float(vv)
            elif k == 'fvExt': ext_ta.value = ', '.join(f'{a_}={b_}' for a_, b_ in v.items())
    def _on_rst(_):
        for k, w in sw.items(): w.value = _p_get(k)
        for m, _n in _mk_names:
            for k, w in coe_w[m].items(): w.value = float(FV_COE[m].get(k, FV_GR_DEFAULT))
        ext_ta.value = ''
    b_exp.on_click(_on_exp); b_imp.on_click(_on_imp); b_rst.on_click(_on_rst)
    b_run = W.Button(description='🚀 بدء الفحص والتحليل الشامل', button_style='success', layout=W.Layout(width='340px', height='44px'))
    prog = W.IntProgress(value=0, min=0, max=100, bar_style='info', layout=W.Layout(width='340px')); plab = W.Label('')
    out = W.Output(); detail_out = W.Output(); det_dd = W.Dropdown(options=[], description='تفاصيل سهم:', layout=lay, style=sty)
    mk_btn = lambda txt, st_: W.Button(description=txt, button_style=st_, layout=W.Layout(width='190px', height='38px'), disabled=True)
    b_xlsx, b_pdf, b_png, b_gs, b_csv, b_html = (mk_btn('📊 Excel', 'info'), mk_btn('📄 PDF', 'info'), mk_btn('🖼️ صور PNG', 'info'),
                                                   mk_btn('🟢 Google Sheet', 'warning'), mk_btn('🧾 CSV', ''), mk_btn('🌐 HTML تفاعلي', 'success'))
    exp_out = W.Output(); btns = [b_xlsx, b_pdf, b_png, b_gs, b_csv, b_html]

    def progress(i, n, label):
        prog.max = max(n, 1); prog.value = i; plab.value = f'{label}: {i}/{n}'
    def run(_):
        for b in btns: b.disabled = True
        with out:
            clear_output(); print('⏳ جاري التحميل والتحليل... (قد يستغرق 1–5 دقائق لـ100 سهم)')
        try:
            res = run_scan(t_syms.value, d_mkt.value, d_bm.value, d_style.value, f_cap.value, f_risk.value, c_deep.value, c_intra.value, c_htf.value,
                           c_corr.value, c_guard.value, vt=c_vt.value, lang=d_lang.value, progress=progress, be_next_bar=c_be.value, p_over=coe_over())
        except Exception as e:
            with out: clear_output(); print('❌', e)
            return
        STATE['res'] = res; plab.value = f"✅ اكتمل في {res['meta']['secs']:.0f} ثانية"
        with out:
            clear_output(); m = res['meta']
            print(f"✅ تم تحليل {m['n']} من {m['requested']} رمز | البيانات حتى {m['as_of']}")
            for l_ in m['log']: print(l_)
            display(HTML(_iframe(build_html(res, d_lang.value, 0, only_head=True), 640)))
        det_dd.options = [(f"{r['symbol']} — {DEC_NAME[r['uni_decision']][1 if d_lang.value == 'عربي' else 0]} ({r['uni_score']:.0f})", i) for i, r in enumerate(res['recs'])]
        for b in btns: b.disabled = False
        show_detail(None)
    def show_detail(_):
        res = STATE['res']
        if not res or det_dd.value is None: return
        r = res['recs'][det_dd.value]
        with detail_out:
            clear_output(wait=True)
            display(HTML(_iframe(detail_html(r, d_lang.value), 820)))
            try: plot_symbol(r).show()
            except Exception as e: print('تعذّر الرسم:', e)
    det_dd.observe(show_detail, names='value')
    def exporter(fn, label):
        def h(_):
            res = STATE['res']
            if not res: return
            with exp_out:
                clear_output(); print(f'⏳ {label}...')
                try:
                    r = fn(res)
                    if isinstance(r, tuple):
                        for x in r:
                            _download(x); time.sleep(1.2)   # 🆕 v6.1: مهلة بين الملفات — كولاب/كروم يحجب التنزيلات المتتالية السريعة
                        print('   💡 إن لم يظهر تنزيل كل الملفات: اسمح لهذا الموقع بتنزيل «ملفات متعددة» من أيقونة القفل أعلى المتصفح، أو حمّلها يدوياً من مجلد ER1991_Reports.')
                    elif isinstance(r, str) and r.startswith('http'): print('✅ تم إنشاء الملف في Google Drive:', r)
                    else: _download(r)
                    print(f'✅ {label}: تم بنجاح.')
                except Exception as e: print('❌', type(e).__name__, e)
        return h
    L = lambda: d_lang.value
    b_run.on_click(run)
    b_xlsx.on_click(exporter(lambda r: export_excel(r, L()), 'تجهيز Excel'))
    b_pdf.on_click(exporter(lambda r: export_pdf(r, L(), i_cards.value), 'تجهيز PDF'))
    b_png.on_click(exporter(lambda r: export_png(r, L(), i_cards.value), 'تجهيز صور PNG'))
    b_gs.on_click(exporter(lambda r: export_gsheet(r, L()), 'إنشاء Google Sheet'))
    b_csv.on_click(exporter(lambda r: export_csv(r, L()), 'تجهيز CSV'))
    b_html.on_click(exporter(lambda r: export_html(r, L(), i_cards.value), 'تجهيز HTML التفاعلي'))
    head = W.HTML('<h2 style="margin:4px 0">🛠️ ER1991 Smart Investment Radar PRO</h2><div style="color:#888;font-size:12px">تحليل فني + تحليل عميق + قيمة عادلة + أهداف + شرح نصي للقرار | أداة مساعدة في قراءة وفحص الأسهم وليست توصية بالشراء أو البيع</div>')
    ui = W.VBox([head, t_syms, d_mkt, d_bm, d_style, d_lang, W.HBox([f_cap, f_risk]), c_deep, c_vt, c_be, c_intra, c_htf, c_corr, c_guard, acc,
                 W.HBox([b_run, W.VBox([prog, plab])]), out, W.HTML('<b>التصدير والتحميل:</b>'), W.HBox(btns[:3]), W.HBox(btns[3:]), i_cards, exp_out,
                 W.HTML('<hr><b>تفاصيل سهم + رسم بياني:</b>'), det_dd, detail_out])
    return ui

def scan(symbols, **kw):
    """استخدام برمجي بدون واجهة: res = scan('AAPL, MSFT'); export_excel(res,'عربي')"""
    res = run_scan(symbols if isinstance(symbols, str) else ','.join(symbols), **kw); STATE['res'] = res; return res

# -----------------------------------------------------------------------------
# 18) 🆕 v6.6: اختبار ذاتي — شغّله بعد أي تعديل: selftest()
# -----------------------------------------------------------------------------
def selftest(seed=7, n=420):
    """فحص ثوابت: لا استثناءات، الدرجات 0–100، reach3 ≤ reach2 ≤ reach1، W+L+BE = closed، بذر EMA، VPOC بلا حجم."""
    rng = np.random.default_rng(seed)
    c = 100 * np.exp(np.cumsum(rng.normal(0.0004, 0.015, n)))
    o = np.r_[c[0], c[:-1]] * (1 + rng.normal(0, 0.004, n))
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.006, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.006, n)))
    df = pd.DataFrame(dict(Open=o, High=h, Low=l, Close=c, Volume=rng.integers(10**5, 10**6, n).astype(float)),
                      index=pd.bdate_range('2023-01-02', periods=n))
    p = dict(P)
    e = s_ema(df['Close'], 20)
    assert e.first_valid_index() == df.index[19], 'بذر EMA يجب أن يبدأ عند الشمعة 20'
    assert abs(float(e.iloc[19]) - float(df['Close'].iloc[:20].mean())) < 1e-9, 'البذر ليس SMA'
    px = prime_x_engine(df, p)
    assert px is not None
    assert px['W'] + px['L'] + px['BE'] == px['closed'], 'عدّادات الصفقات غير متسقة'
    if px['opened']:
        r1, r2, r3 = px['reach1'], px['reach2'], px['reach3']
        assert 0 <= r3 <= r2 <= r1 <= 100, f'ترتيب الوصول للأهداف خاطئ: {r1},{r2},{r3}'
    for st_ in STYLES:
        r = radar_row('TEST', df, st_, p, None)
        assert r['state'] in (0, 2, 3)
        if r['state'] == 0:
            assert 0 <= r['score'] <= 100, (st_, r['score'])
    nov = df.copy(); nov['Volume'] = 0.0
    assert not nn(calc_vpoc(nov)), 'VPOC بلا حجم يجب أن يكون NaN'
    sup_res = auto_sr(df, p, float(df['Close'].iloc[-1]))
    assert len(sup_res[2]) <= p['srMax'] and len(sup_res[3]) <= p['srMax']
    # ── 🆕 v7.0 ──
    # 1) القيمة السوقية القديمة تُصحَّح (SWDY: 102B قديمة ⇒ ≈260B) + EPS TTM من TradingView له الأولوية
    f1 = fund_metrics(dict(info=dict(trailingEps=7.13, bookValue=32.88, marketCap=102.03e9, impliedSharesOutstanding=2.14e9, currency='EGP', financialCurrency='EGP')), 121.46, 'SWDY.CA', p)
    assert abs(f1['mcap'] / 1e9 - 259.9) < 1.0 and f1['mcap_src'] == 'Price×Shares', f1['mcap']
    f2 = fund_metrics(dict(info=dict(trailingEps=7.13, bookValue=32.88)), 121.46, 'SWDY.CA', p, tvf=dict(eps_ttm=8.97, mcap=259.85e9))
    assert f2['eps'] == 8.97 and f2['eps_src'] == 'TV-TTM' and f2['mcap_src'] == 'TradingView'
    f3 = fund_metrics(dict(info=dict(trailingEps=3.0, trailingPE=20.0, bookValue=10.0, priceToBook=5.0, currency='USD', financialCurrency='TWD')), 100.0, 'ADR', p)
    assert abs(f3['eps'] - 5.0) < 1e-9 and abs(f3['bvps'] - 20.0) < 1e-9, 'حماية عملة ADR'
    # 2) القيمة العادلة: ثقة 0–100 · مضاعف مصر > 8.6 · هدف خارجي يرفع القيمة
    fm = dict(eps=8.97, bvps=32.88, eps_g=-1.2, eps_ttm_g=25.8, eps_fwd=NaN, analyst=NaN, analyst_n=NaN, roe=25.9, pio=3, fcfm=-0.3, altman=1.9, beneish=-2.11, altman_ok=True, fcf_ok=True, is_fin=False, eps_src='TV-TTM')
    assert market_fair_pe('EGX', p) > 11, market_fair_pe('EGX', p)
    v0 = fair_value(fm, 121.46, 'Medium Term', [], p, ref_price=110, mk='EGX')
    v1 = fair_value(fm, 121.46, 'Medium Term', [], p, ref_price=110, mk='EGX', ext=115.6)
    assert 0 <= v0['conf'] <= 100 and v1['fair'] > v0['fair'] and v0['verdict'] in ('Deep Value', 'Undervalued', 'Fair', 'Overvalued', 'Rich')
    # 3) مراحل السوق
    up = pd.Series(np.linspace(100, 200, 300)); ph = mkt_phase_calc(up, p, 'D'); assert ph['phase'] == 1 and ph['at_high'] and not ph['stress']
    cr = pd.concat([up, pd.Series([200 * 0.92])], ignore_index=True); ph = mkt_phase_calc(cr, p, 'D'); assert ph['phase'] == 6 and ph['stress']
    bear = pd.concat([up, pd.Series(np.linspace(199, 150, 60))], ignore_index=True); ph = mkt_phase_calc(bear, p, 'D'); assert ph['phase'] == 5, ph['phase']
    # 4) كل مفاتيح لوحة الإعدادات موجودة في P
    for _t, _items in SETTINGS_SCHEMA:
        for _k, _l in _items: _p_get(_k)
    assert parse_ext_targets('SWDY=115.6, EGX:COMI: 130') == {'SWDY': 115.6, 'COMI': 130.0}
    print('✅ selftest OK | opened=%s closed=%s W/L/BE=%s/%s/%s | v7.0: mcap/eps/fv/market-phases/settings OK' % (px['opened'], px['closed'], px['W'], px['L'], px['BE']))

if __name__ == '__main__' or 'google.colab' in sys.modules:
    try:
        from IPython.display import display
        display(build_ui())
    except Exception as _e:
        print('الواجهة تتطلب Jupyter/Colab:', _e)
