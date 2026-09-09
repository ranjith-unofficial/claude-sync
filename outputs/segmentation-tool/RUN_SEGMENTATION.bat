@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Segmentation Typing Tool

rem ------------------------------------------------------------------
rem  Segmentation Typing Tool - Windows launcher
rem
rem  Use it either way:
rem    * drag an Excel typing tool onto this file, or
rem    * double-click it and type the path when asked.
rem
rem  Note: paths are always quoted below, because the source workbooks
rem  have spaces and brackets in their names - e.g. "... V1 (1).xlsm" -
rem  and an unquoted bracket will break a batch IF block.
rem ------------------------------------------------------------------

set "HERE=%~dp0"
set "ENGINE=%HERE%segmentation_tool.py"

echo ==============================================================
echo   SEGMENTATION TYPING TOOL
echo ==============================================================
echo.

if not exist "%ENGINE%" goto :no_engine

rem --- locate Python -------------------------------------------------
set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY where python3 >nul 2>&1 && set "PY=python3"
if not defined PY goto :no_python

rem A bare -V avoids nesting quotes and brackets inside a FOR /F command,
rem which is where batch quoting most often falls apart.
%PY% -V >nul 2>&1
if errorlevel 1 goto :no_python
for /f "tokens=1,2" %%a in ('%PY% -V 2^>^&1') do set "PYVER=%%b"
echo Python !PYVER! found.

rem --- make sure openpyxl is available -------------------------------
%PY% -c "import openpyxl" >nul 2>&1
if errorlevel 1 goto :install_dep
goto :have_dep

:install_dep
echo.
echo Installing the required 'openpyxl' package ...
%PY% -m pip install --quiet --disable-pip-version-check openpyxl
if errorlevel 1 goto :no_dep
echo Done.

:have_dep
echo.

rem --- inputs --------------------------------------------------------
set "MODEL=%~1"
set "DATA=%~2"

if not defined MODEL goto :ask_model
goto :got_model

:ask_model
set /p "MODEL=Path to the typing tool Excel file (or drag it here): "
set MODEL=!MODEL:"=!

:got_model
if not defined MODEL goto :nothing
if not exist "!MODEL!" goto :no_file

if defined DATA goto :run
echo.
echo --------------------------------------------------------------
echo  SCRIPT QUESTION NAMES
echo --------------------------------------------------------------
echo The script needs your survey's question names. They are numbered
echo per block, in the order the variables appear on the Formulas tab.
echo   e.g. rating items QS17_1..QS17_3, paired items QS16_1..QS16_10
echo.
set "QSCALE=TypingTool1DP"
set "QPAIR=TypingTool2DP"
set /p "QSCALE=Prefix for the rating/scale questions [%QSCALE%]: "
set /p "QPAIR=Prefix for the paired/MaxDiff questions [%QPAIR%]: "
set QSCALE=!QSCALE:"=!
set QPAIR=!QPAIR:"=!

echo.
echo If both blocks use the same answer style you must split them by hand,
echo in sheet order - for example  TT2:16,TT1:8  - otherwise leave blank.
set /p "QBLOCKS=Explicit block split (optional): "
set QBLOCKS=!QBLOCKS:"=!

echo.
set "HID=HIDSegment"
set /p "HID=Hidden question to check against [%HID%]: "
set HID=!HID:"=!

echo.
echo Extra options (press Enter to skip):
echo    1  audit    - print the step-by-step maths for the first respondent
echo    2  vars     - print the whole coefficient table
echo    3  ref      - add a zero-coefficient baseline segment
echo    4  ifelse   - write paired questions as If/Else instead of on^(...^)
echo    5  nodata   - assert the hidden question is empty (first deployment)
echo    6  round4   - round coefficients to 4 decimal places
set /p "OPTS=Choose any of 1 2 3 4 5 6: "

set "ARGS=--q-scale "!QSCALE!" --q-pair "!QPAIR!" --hid "!HID!""
if defined QBLOCKS set "ARGS=!ARGS! --q-blocks "!QBLOCKS!""
echo.!OPTS!| findstr /c:"1" >nul && set "ARGS=!ARGS! --audit"
echo.!OPTS!| findstr /c:"2" >nul && set "ARGS=!ARGS! --variables"
echo.!OPTS!| findstr /c:"3" >nul && set "ARGS=!ARGS! --reference-segment"
echo.!OPTS!| findstr /c:"4" >nul && set "ARGS=!ARGS! --pair-style ifelse"
echo.!OPTS!| findstr /c:"5" >nul && set "ARGS=!ARGS! --assert-style nodata"
echo.!OPTS!| findstr /c:"6" >nul && set "ARGS=!ARGS! --decimals 4"

echo.
echo --------------------------------------------------------------
if defined DATA goto :run_with_data

%PY% "%ENGINE%" "!MODEL!" !ARGS!
goto :done

:run_with_data
if not exist "!DATA!" goto :no_data
%PY% "%ENGINE%" "!MODEL!" "!DATA!" !ARGS!
goto :done

:done
echo --------------------------------------------------------------
echo.
echo Finished. Two files were written next to the Excel file:
echo    ^<name^>_results.xlsx        - Batch tab with the results
echo    ^<name^>_results_script.txt  - the segmentation script
goto :end

rem --- error exits ---------------------------------------------------
:no_engine
echo ERROR: segmentation_tool.py was not found in
echo    %HERE%
echo Keep this .bat file in the same folder as the Python script.
goto :end

:no_python
echo ERROR: Python was not found on this PC.
echo Install it from https://www.python.org/downloads/windows/
echo and tick "Add python.exe to PATH" during setup.
goto :end

:no_dep
echo ERROR: could not install 'openpyxl'.
echo Try running this by hand in a Command Prompt:
echo    %PY% -m pip install openpyxl
goto :end

:no_file
echo ERROR: that file does not exist:
echo    !MODEL!
goto :end

:no_data
echo ERROR: that data file does not exist:
echo    !DATA!
goto :end

:nothing
echo Nothing entered - closing.
goto :end

:end
echo.
pause
endlocal
