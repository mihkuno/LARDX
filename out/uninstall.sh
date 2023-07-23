#!/usr/bin/env bash


# Inform the user about the action and ask for confirmation
read -rp "Are you sure you want to remove Lardx? (y/n): " answer

if [[ "$answer" == "y" || "$answer" == "Y" ]]; then


    # Destination of source files
    dir_lardx="$HOME/.lardx"

    # Remove the folder in home directory
    if [ -d "$dir_lardx" ]; then
        echo -e "\033[95mUninstalling Lardx..\033[0m"
        rm -rv $dir_lardx

        # Remove the env path in the shell config
    # Get the user's current shell
    current_shell=$(basename "$SHELL")

    # Get the corresponding shell configuration file
    config_file="$HOME/.${current_shell}rc"

    # Path string in the shell config 
    dir_exec=$dir_lardx/dist/lardx 

    # Define the line to remove
    line_to_remove="PATH=\$PATH:$dir_exec"

    # Use grep -v to exclude the matching line and create a temporary file
    grep -v "$line_to_remove" "$config_file" > "$config_file.tmp"

    # Replace the original file with the temporary file
    mv "$config_file.tmp" "$config_file"


    echo -e "
    \033[96m
    ██╗      █████╗ ██████╗ ██████╗ ██╗  ██╗
    ██║     ██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝
    ██║     ███████║██████╔╝██║  ██║ ╚███╔╝ 
    ██║     ██╔══██║██╔══██╗██║  ██║ ██╔██╗ 
    ███████╗██║  ██║██║  ██║██████╔╝██╔╝ ██╗
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝
    \033[0m
    \U0001F916 Thank you for using Lardx! \033[0m
    "

    echo -e "\033[92mSuccess! Lardx has been removed. \033[0m\n"
    else
        echo -e "\033[95mLardx is not installed..\033[0m"
        exit 1
    fi

else
    echo -e "\033[95mLardx was not removed.\033[0m"
    exit 1
fi
