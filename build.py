# -*- coding: utf-8 -*-
"""
build.py — 배포 전 실행. 캐시 때문에 업데이트가 안 보이는 문제 방지.
  1) shared.css / shared.js 참조에 콘텐츠 해시 기반 ?v= 자동 부여(변경 시에만 URL 바뀜)
  2) 각 페이지 <head>에 no-cache 메타 삽입(HTML 재검증 유도)
  3) 푸터 빌드 스탬프({{BUILD}} 또는 <span class="build">)를 '날짜 · 해시'로 갱신
사용: python build.py   (그 뒤 git commit && git push)
"""
import os, re, hashlib, glob, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

def read(p): return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

# 1) 공유 자산 콘텐츠 해시
css = read(os.path.join(ROOT, "shared.css"))
js  = read(os.path.join(ROOT, "shared.js"))
asset_ver = hashlib.md5((css + js).encode("utf-8")).hexdigest()[:8]
build_stamp = datetime.datetime.now().strftime("%Y-%m-%d") + " · " + asset_ver

NOCACHE = '<meta http-equiv="Cache-Control" content="no-cache, must-revalidate">'

def process(path):
    s = read(path)
    orig = s
    # shared.css / shared.js (../ 포함) 참조에 ?v=해시 부여(기존 ?v= 교체)
    s = re.sub(r'((?:\.\./)?shared\.(?:css|js))(\?v=[A-Za-z0-9]+)?', r'\1?v=' + asset_ver, s)
    # no-cache 메타 (charset 다음에 1회만)
    if 'http-equiv="Cache-Control"' not in s:
        s = re.sub(r'(<meta charset="[^"]+">)', r'\1\n' + NOCACHE, s, count=1)
    # 푸터 빌드 스탬프: {{BUILD}} 플레이스홀더 또는 기존 .build 스팬 갱신
    s = s.replace("{{BUILD}}", build_stamp)
    s = re.sub(r'(<span class="build"[^>]*>)[^<]*(</span>)', r'\g<1>' + build_stamp + r'\g<2>', s)
    if s != orig:
        write(path, s)
        return True
    return False

targets = [os.path.join(ROOT, "index.html")] + glob.glob(os.path.join(ROOT, "guides", "*.html"))
changed = [os.path.relpath(p, ROOT) for p in targets if process(p)]
print("asset version:", asset_ver, "| build:", build_stamp)
print("updated:", changed or "(none)")
