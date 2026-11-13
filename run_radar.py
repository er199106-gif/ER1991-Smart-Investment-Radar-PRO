#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ER1991 Smart Investment Radar PRO — مشغّل سطر الأوامر (GitHub Actions / Codespaces / جهازك).
لا يغيّر أي منطق في er1991_radar.py: يقرأ الإعدادات من config.json (أو متغيرات البيئة/الخيارات) ثم يستدعي run_scan ودوال التصدير نفسها.

أمثلة:
  python run_radar.py                                  # يقرأ config.json
  python run_radar.py --symbols "EGX:COMI,EGX:SWDY" --style Growth --exports html,excel
  python run_radar.py --selftest
"""
import argparse, importlib, json, os, re, shutil, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ALL_EXPORTS = ('html', 'excel', 'csv', 'pdf', 'png')

def load_module():
    sys.path.insert(0, HERE)
    return importlib.import_module('er1991_radar')

def flat_to_over(flat):
    """نفس صيغة تصدير لوحة الإعدادات: {'fvW.pe': 0.5, 'fvCoe': {...}, 'fvExt': {...}} → p_over متداخل."""
    over = {}
    for k, v in (flat or {}).items():
        if k.startswith('_'): continue
        if '.' in k:
            a, b = k.split('.', 1); over.setdefault(a, {})[b] = v
        else:
            over[k] = v
    return over or None

def read_symbols(cfg, mod):
    """الأولوية: متغير البيئة RADAR_SYMBOLS ← config.symbols (نص/قائمة) ← الملف config.symbols_file."""
    env = os.environ.get('RADAR_SYMBOLS', '').strip()
    if env: return env
    s = cfg.get('symbols')
    if isinstance(s, list): s = ','.join(s)
    if s and str(s).strip(): return str(s)
    f = cfg.get('symbols_file')
    if f and os.path.exists(os.path.join(HERE, f)):
        txt = open(os.path.join(HERE, f), encoding='utf-8').read()
        return re.sub(r'#.*', '', txt)           # يدعم التعليقات بعد #
    return mod.SAMPLE

def _b(v, default):
    if v is None or str(v).strip() == '': return default
    return str(v).strip().lower() in ('1', 'true', 'yes', 'y', 'on', 'نعم')

def run(cfg, mod=None, out_dir=None, exports=None):
    mod = mod or load_module()
    out_dir = os.path.abspath(out_dir or cfg.get('out_dir') or os.path.join(HERE, 'ER1991_Reports'))
    os.makedirs(out_dir, exist_ok=True)
    mod.OUT_DIR = out_dir                      # دوال التصدير تقرأ OUT_DIR وقت الاستدعاء
    lang = os.environ.get('RADAR_LANG') or cfg.get('lang', 'عربي')
    style = os.environ.get('RADAR_STYLE') or cfg.get('style', 'Auto')
    market = os.environ.get('RADAR_MARKET') or cfg.get('market', 'AUTO')
    deep = _b(os.environ.get('RADAR_DEEP'), bool(cfg.get('deep', True)))
    exports = exports or [x.strip().lower() for x in (os.environ.get('RADAR_EXPORTS') or ','.join(cfg.get('exports', ['html', 'excel', 'csv']))).split(',') if x.strip()]
    bad = [x for x in exports if x not in ALL_EXPORTS]
    if bad: raise SystemExit(f'❌ تصدير غير معروف: {bad} — المتاح: {ALL_EXPORTS}')
    syms = read_symbols(cfg, mod)
    p_over = flat_to_over(cfg.get('settings'))
    print(f'▶ الرموز: {syms[:200]}{"…" if len(syms) > 200 else ""}\n▶ السوق={market} · الأسلوب={style} · عميق={deep} · اللغة={lang} · التصدير={exports}')
    t0 = time.time()
    res = mod.run_scan(syms, market, cfg.get('benchmark', 'AUTO'), style, float(cfg.get('capital', 10000.0)), float(cfg.get('risk_pct', 1.0)), deep,
                       bool(cfg.get('intraday', False)), bool(cfg.get('require_htf', True)), bool(cfg.get('use_corr', True)), bool(cfg.get('guard', True)),
                       vt=bool(cfg.get('virtual_trade', True)), lang=lang, progress=None, p_over=p_over, be_next_bar=bool(cfg.get('be_next_bar', False)))
    m = res['meta']
    print(f"✅ تم تحليل {m['n']} من {m['requested']} رمز | البيانات حتى {m['as_of']} | {time.time() - t0:.0f}ث")
    for l_ in m['log']: print(l_)
    files = {}
    cards = int(cfg.get('cards', 30))
    for kind in exports:
        try:
            if kind == 'html': files['html'] = mod.export_html(res, lang, cards)
            elif kind == 'excel': files['excel'] = mod.export_excel(res, lang)
            elif kind == 'csv': files['csv'] = mod.export_csv(res, lang)
            elif kind == 'pdf': files['pdf'] = mod.export_pdf(res, lang, cards)
            elif kind == 'png': files['png'] = mod.export_png(res, lang, cards)[0]
            print(f'📁 {kind}: {files[kind]}')
        except Exception as e:                  # فشل تصدير واحد لا يُسقط البقية
            print(f'⚠️ تعذّر تصدير {kind}: {type(e).__name__}: {e}')
    # ملفات مساعدة للنشر: index.html (آخر تقرير) + ملخص Markdown
    if 'html' in files:
        shutil.copyfile(files['html'], os.path.join(out_dir, 'index.html'))
    open(os.path.join(out_dir, 'summary.md'), 'w', encoding='utf-8').write(summary_md(res, mod, lang))
    return res, files

def summary_md(res, mod, lang):
    ar = lang == 'عربي'; I = 1 if ar else 0
    m = res['meta']
    L = [f"## 📡 ER1991 Smart Investment Radar PRO — {m['generated']}", f"{m['n']} / {m['requested']} · {'البيانات حتى' if ar else 'Data as of'} {m['as_of']}", '',
         '| # | ' + ('الرمز' if ar else 'Symbol') + ' | ' + ('القرار' if ar else 'Verdict') + ' | ' + ('الدرجة' if ar else 'Score') + ' | ' + ('نوع الاستثمار' if ar else 'Type') +
         ' | ' + ('السعر' if ar else 'Price') + ' | ' + ('القيمة العادلة' if ar else 'Fair value') + ' | ' + ('الثقة' if ar else 'Conf.') + ' |', '|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(res['recs'][:40], 1):
        fv = '—' if r['fv_fair'] != r['fv_fair'] else f"{r['fv_fair']:,.2f} ({r['fv_upside']:+.0f}%)"
        cf = '—' if r['fv_conf'] != r['fv_conf'] else f"{r['fv_conf']:.0f}%"
        L.append(f"| {i} | {r['symbol']} | {mod.DEC_NAME[r['uni_decision']][I]} | {r['uni_score']:.0f} | {mod.disp('style_used', r['style_used'], lang)} | {r['price']:,.2f} | {fv} | {cf} |")
    if m['log']:
        L += ['', '<details><summary>' + ('سجل التشغيل' if ar else 'Run log') + '</summary>', ''] + [f'- {x}' for x in m['log']] + ['', '</details>']
    L += ['', mod.NOTE_AR if ar else mod.NOTE_EN]
    return '\n'.join(L)

def main(argv=None):
    ap = argparse.ArgumentParser(description='ER1991 Smart Investment Radar PRO')
    ap.add_argument('--config', default=os.path.join(HERE, 'config.json'))
    ap.add_argument('--symbols'); ap.add_argument('--style'); ap.add_argument('--market'); ap.add_argument('--lang')
    ap.add_argument('--exports', help='html,excel,csv,pdf,png'); ap.add_argument('--out-dir'); ap.add_argument('--no-deep', action='store_true')
    ap.add_argument('--selftest', action='store_true', help='اختبار ذاتي بلا إنترنت')
    a = ap.parse_args(argv)
    mod = load_module()
    if a.selftest:
        mod.selftest(); return 0
    cfg = json.load(open(a.config, encoding='utf-8')) if os.path.exists(a.config) else {}
    if a.symbols: os.environ['RADAR_SYMBOLS'] = a.symbols
    if a.style: os.environ['RADAR_STYLE'] = a.style
    if a.market: os.environ['RADAR_MARKET'] = a.market
    if a.lang: os.environ['RADAR_LANG'] = a.lang
    if a.no_deep: os.environ['RADAR_DEEP'] = 'false'
    try:
        res, files = run(cfg, mod, out_dir=a.out_dir, exports=[x.strip() for x in a.exports.split(',')] if a.exports else None)
    except ValueError as e:                    # لا رموز/لا بيانات: رسالة واضحة وكود خروج 1
        print('❌', e); return 1
    return 0 if files else 2

if __name__ == '__main__':
    sys.exit(main())
