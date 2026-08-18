@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================================
REM  publish.bat  —  push the Joseon story pages to GitHub
REM  demosaii
REM ============================================================
REM  Put this file in the same folder as the .html pages
REM  and double-click it. That's all.
REM
REM  Repo: https://github.com/DemosLady/joseon-universe
REM ============================================================

REM ---- already set for your repo, nothing to edit ----
set "REPO_URL=https://github.com/DemosLady/joseon-universe.git"
set "BRANCH=main"
REM ------------------------------

cd /d "%~dp0"

echo.
echo ============================================
echo   Joseon Universe - publish to GitHub
echo   folder: %cd%
echo ============================================
echo.

REM ---- check git is installed ----
where git >nul 2>nul
if errorlevel 1 (
  echo [ERROR] git is not installed or not in PATH.
  echo Download it from https://git-scm.com/download/win
  echo.
  pause
  exit /b 1
)

REM ---- check the html files are here ----
set FOUND=0
for %%F in (*.html) do set /a FOUND+=1
if !FOUND!==0 (
  echo [ERROR] No .html files found in this folder.
  echo Put publish.bat in the same folder as your chapter pages.
  echo.
  pause
  exit /b 1
)
echo Found !FOUND! html file(s).
echo.

REM ---- first run: init repo ----
if not exist ".git" (
  echo First run - setting up the repository...
  git init
  git branch -M %BRANCH%
  git remote add origin %REPO_URL%
  echo.
  REM a .nojekyll file makes GitHub Pages serve the files as-is
  if not exist ".nojekyll" type nul > .nojekyll
) else (
  REM make sure the remote still matches
  git remote set-url origin %REPO_URL% 2>nul
)

REM ---- commit message ----
set "MSG=%~1"
if "%MSG%"=="" (
  for /f "tokens=1-3 delims=/-. " %%a in ("%DATE%") do set "TODAY=%%a-%%b-%%c"
  set "MSG=update !TODAY!"
)

echo Staging files...
git add -A

REM ---- nothing changed? ----
git diff --cached --quiet
if not errorlevel 1 (
  echo.
  echo Nothing has changed since the last push. Done.
  echo.
  pause
  exit /b 0
)

echo Committing: "!MSG!"
git commit -m "!MSG!"

echo.
echo Pushing to %REPO_URL% ...
git push -u origin %BRANCH%
if errorlevel 1 (
  echo.
  echo [ERROR] Push failed.
  echo  - Check REPO_URL at the top of this file
  echo  - If GitHub asks for a password, use a Personal Access Token
  echo    ^(github.com - Settings - Developer settings - Tokens^)
  echo.
  pause
  exit /b 1
)

echo.
echo ============================================
echo   Done.
echo.
echo   If GitHub Pages is on, your pages are at:
echo   https://demoslady.github.io/joseon-universe/
echo   ...^/tistory_ch1_blood_and_fog.html
echo ============================================
echo.
pause
