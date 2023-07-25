#!/usr/bin/env bash


echo -e "
\033[96m
██╗      █████╗ ██████╗ ██████╗ ██╗  ██╗
██║     ██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝
██║     ███████║██████╔╝██║  ██║ ╚███╔╝ 
██║     ██╔══██║██╔══██╗██║  ██║ ██╔██╗ 
███████╗██║  ██║██║  ██║██████╔╝██╔╝ ██╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝
\033[0m
\U0001F916 Google Bard for the Linux Terminal
\U0001F530 Projects:\033[96m https://github.com/mihkuno \033[0m
"

# Get the absolute path of this script's directory
dir_origin=$(cd "$(dirname "$0")" && pwd)

cd $dir_origin/..

if [ -d "out" ]; then
    echo -e "\033[95mRebuilding Source..\033[0m"
    rm -r "out"
else
    echo -e "\033[95mBuilding Source..\033[0m"
fi

mkdir -p out

cp uninstall.sh out/

cd out/

pyinstaller ../src/lardx.py

cd $dir_origin

echo -e "\033[92mBuild Complete. \033[0m\n"