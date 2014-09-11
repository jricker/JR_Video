::Master BAT
if %~1 == metadataRED goto metadataRED
if %~1 == PRORES goto PRORES
if %~1 == H264 goto H264
if %~1 == REDH264 goto REDH264
if %~1 == IMG2MOV goto IMG2MOV
if %~1 == EXR2IMG goto EXR2IMG
if %~1 == EXR2IMG2MOV goto EXR2IMG2MOV
if %~1 == MOV2CUTDOWN goto MOV2CUTDOWN
if %~1 == EDL2MOV goto EDL2MOV
if %~1 == OPENFOLDER goto OPENFOLDER
::
:metadataRED
"%~2" --i %3 --printMeta 1 > %4
goto END
::
:PRORES
"%~2" -i "%~3" -y -acodec pcm_s24le -ac 2 -vcodec prores -profile:v %~5 -s hd1080 -bits_per_mb 8000 "%~4"
goto END
::
:H264
"%~2" -i %3 -y -vcodec libx264 -b:v 5000k -codec:a libvo_aacenc "%~4"
goto END
::
:REDH264
"%~2" --i %3 --outDir "%~4" -o "%~5" -w 1 -R 2 --colorSciVersion 1 --gpuPlatform 0
:: The --colorSciVersion is for the Mysterium X or later sensor which doens't corectly translate colors unless this is turned on. 
goto END
::
:IMG2MOV
::
"%~4" /i "%~3" %2 "%~6.avi" /x
if %errorlevel% == 0  goto ok
:err
echo Error %errorlevel% with %~nx1
goto theend
:ok
echo Ok, done
:theend
if %~8 == H264 goto convertH264
if %~8 == ProRes goto convertProRes
:convertProRes
%5 -i "%~6.avi" -y -vcodec prores -profile:v 0 -s %7 -bits_per_mb 8000 %6.mov
::del "%~6.avi"
goto END
::
:convertH264
%5 -i "%~6.avi" -y -vcodec libx264 -b:v 5000k -s %7 -codec:a libvo_aacenc %6.mp4
::del "%~6.avi"
goto END
::
::
:EXR2IMG
::%8 "%~6-10000.exr" "%6_temp.jpg" -resize 1280 720
%2 %3 %4 -resize 1920 1080
goto END
::
:EXR2IMG2MOV
%3 %4 %2 -resize %~5
goto END
::goto IMG2MOV
::
:MOV2CUTDOWN
"%~2" -i "%~3" -y -ss %~5 -to %~6 -y -vcodec prores -profile:v 0 -s hd1080 "%~4"
goto END
::
:EDL2MOV
"%~2" -oac pcm -ovc copy -o %~3
goto END
::
:OPENFOLDER
%SystemRoot%\explorer.exe %2
goto END
::
:END
echo DONE