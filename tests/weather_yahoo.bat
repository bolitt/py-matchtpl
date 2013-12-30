@echo off

echo Should have bin\curl installed
bin\curl "http://weather.yahoo.com/china/beijing/beijing-2151330/" | python stream.py -t weather_yahoo.xml > [out]weather_yahoo.out.txt