@echo off
chcp 65001 >nul
cd /d D:\AI\CODE\learning-curve-auto\WEBSITE
echo ============================================
echo   playlist video - 16:9, full tracklist
echo ============================================
echo.
echo   1. fill in tracklist.txt
echo   2. put playlist.mp3 next to this file
echo   3. run
echo.
echo   python generate_playlist_video.py --check
echo   python generate_playlist_video.py --preview 20
echo   python generate_playlist_video.py --frames-only
echo.
python generate_playlist_video.py %*
echo.
pause
