#!/usr/bin/env bash
# 배포: build.py(캐시버스팅+버전스탬프) → commit → push. 항상 이걸로 배포해 캐시 문제 방지.
# 사용: bash deploy.sh "커밋 메시지"
set -e
cd "$(dirname "$0")"
python build.py
git add -A
if git diff --cached --quiet; then echo "변경 없음"; exit 0; fi
git -c user.name="jakeon32" -c user.email="airis327@gmail.com" commit -q -m "${1:-portal update}

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push origin master
echo "배포 완료 → https://jakeon32.github.io/claude-guide-portal/"
