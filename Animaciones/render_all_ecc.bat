@echo off
rem Wrapper to run render_all_ecc.ps1 with a permissive ExecutionPolicy.
rem Usage: render_all_ecc.bat      -> render all scenes
rem        render_all_ecc.bat 1    -> render only scene 1
rem        render_all_ecc.bat 20   -> render only scene 20
setlocal
set SCRIPT_DIR=%~dp0
set "SCENE_INDEX=%~1"

if not defined SCENE_INDEX set "SCENE_INDEX=0"

where pwsh >nul 2>&1
if %ERRORLEVEL%==0 (
  pwsh -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%render_all_ecc.ps1" -SceneIndex %SCENE_INDEX%
) else (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%render_all_ecc.ps1" -SceneIndex %SCENE_INDEX%
)

endlocal
exit /b %ERRORLEVEL%
