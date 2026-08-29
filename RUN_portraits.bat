@echo off
chcp 65001 >nul
cd /d D:\AI\CODE\learning-curve-auto\JOSEON
echo ============================================
echo   character portraits - 10 images, 4:5
echo ============================================
echo.
echo   python generate_portraits.py --list
echo   python generate_portraits.py --only oki
echo   python generate_portraits.py --limit 3
echo.
python generate_portraits.py %*
echo.
pause
