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

# Destination of source files
dir_lardx="$HOME/.lardx"

# Get the absolute path of this script's directory
dir_origin=$(cd "$(dirname "$0")" && pwd)


if ! [ -d "$dir_origin/out" ]; then
    echo -e "\n\033[91mFailed. Missing output packages..\033[0m"
    exit
fi


# Make folder in home directory
if [ -d "$dir_lardx" ]; then
    echo -e "\033[95mReinstalling Lardx..\033[0m"
    rm -r $dir_lardx
else
    echo -e "\033[95mInstalling Lardx..\033[0m"
fi
mkdir $dir_lardx


# Function to handle keyboard interrupt
function handle_interrupt() {
    echo -e "\n\033[91mKeyboard interrupt. Performing cleanup..\033[0m"
    rm -r $dir_lardx
    exit 1
}
# Set up SIGINT trap before running the apt script
trap handle_interrupt SIGINT


# Copy source files
cp -r $dir_origin/out/* $dir_lardx

# Make shell script executable
dir_exec=$dir_lardx/dist/lardx
chmod +x $dir_exec/lardx


# Set the new environment variable
# Get the user's current shell
current_shell=$(basename "$SHELL")

# Get the corresponding shell configuration file
config_file="$HOME/.${current_shell}rc"

# Add the environment variable to the configuration file if it doesn't already exist
if ! grep -q "PATH=\$PATH:$dir_exec" "$config_file"; then
    echo -e "PATH=\$PATH:$dir_exec" >> "$config_file"
    echo -e "\033[94mAdded \$PATH:lardx to $config_file..\033[0m"
fi

# Define the formatted text with ANSI escape codes inside the read prompt
read -rp $'\nOpen a new terminal and run \033[95m lardx \033[0m to begin.'
echo -e "\033[92mSuccess! Lardx has been installed. \033[0m\n"