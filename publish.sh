#!/usr/bin/env bash
# ============================================================
#  publish.sh  —  push the Joseon story pages to GitHub
#  demosaii
#
#  First time:
#    1. create an empty repo on github.com (no README)
#    2. put its URL in REPO_URL below
#    3. chmod +x publish.sh
#    4. ./publish.sh
#
#  After that:  ./publish.sh "optional commit message"
# ============================================================

set -euo pipefail

# ---- EDIT THESE TWO LINES ----
REPO_URL="https://github.com/DemosLady/joseon-universe.git"
BRANCH="main"
# ------------------------------

cd "$(dirname "$0")"

echo
echo "============================================"
echo "  Joseon Universe - publish to GitHub"
echo "  folder: $(pwd)"
echo "============================================"
echo

command -v git >/dev/null 2>&1 || { echo "[ERROR] git is not installed."; exit 1; }

count=$(ls -1 *.html 2>/dev/null | wc -l | tr -d ' ')
if [ "$count" = "0" ]; then
  echo "[ERROR] No .html files in this folder."
  exit 1
fi
echo "Found $count html file(s)."
echo

if [ ! -d ".git" ]; then
  echo "First run - setting up the repository..."
  git init
  git branch -M "$BRANCH"
  git remote add origin "$REPO_URL"
  touch .nojekyll        # tell GitHub Pages to serve files as-is
else
  git remote set-url origin "$REPO_URL"
fi

MSG="${1:-update $(date +%Y-%m-%d)}"

echo "Staging files..."
git add -A

if git diff --cached --quiet; then
  echo
  echo "Nothing has changed since the last push. Done."
  exit 0
fi

echo "Committing: $MSG"
git commit -m "$MSG"

echo
echo "Pushing to $REPO_URL ..."
git push -u origin "$BRANCH"

echo
echo "============================================"
echo "  Done."
echo
echo "  If GitHub Pages is on, your pages are at:"
echo "  https://demoslady.github.io/joseon-universe/"
echo "============================================"
