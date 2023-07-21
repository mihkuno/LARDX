#!/usr/bin/env zsh
# Or
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


# Flag if installation is successful
flag_success=0

# Destination of source files
dir_lardx="$HOME/.lardx"

# Get the absolute path of this script's directory
dir_origin=$(dirname "$(readlink -f "$0")")

# Check if python is installed on the system
is_python_installed=0


# Make folder in home directory
if [ -d "$dir_lardx" ]; then
    echo "\033[95mReinstalling Lardx..\033[0m"
    rm -r $dir_lardx
else
    echo "\033[95mInstalling Lardx..\033[0m"
fi
mkdir $dir_lardx


# Function to handle keyboard interrupt
function handle_interrupt() {
    echo -e "\n\033[91mKeyboard interrupt detected. Performing cleanup..\033[0m"
    rm -r $dir_lardx
    exit 1
}
# Set up SIGINT trap before running the apt script
trap handle_interrupt SIGINT


# Check if Python 3 and pip for Python 3 are installed
if which python3 >/dev/null 2>&1 && which pip3 >/dev/null 2>&1; then
  
    # Get the current Python version
    python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    package_name="python$python_version-venv"

    # Create virtual environment
    # Check if python3-venv is installed
    python3 -m venv $dir_lardx/venv > /dev/null 2>&1
    
    # Check the exit status using $? and act accordingly
    if [ $? -eq 0 ]; then
        is_python_installed=1
    else
        echo "\033[93m$package_name is not installed.\033[0m"

        if sudo apt update; then
            # Run apt install in the background and wait for 30 seconds
            if sudo apt install -y "$package_name"; then
                echo "\033[94m$package_name has been successfully installed.\033[0m"
                # Create virtual environment
                python3 -m venv $dir_lardx/venv > /dev/null 2>&1
                is_python_installed=1
            else
                echo "\n\033[93mFailed to install $package_name.\033[0m"
            fi
        else
            echo -e "\n\033[91mFailed to update package list..\033[0m"
            rm -r $dir_lardx
        fi
    fi

else
    echo "\n\033[93mEither Python3 or Pip is missing..\033[0m"
fi


if [ "$is_python_installed" -eq 1 ]; then

    # Copy source files
    cp $dir_origin/source/lardx* $dir_lardx

    # Activate virtual environment
    source "$dir_lardx/venv/bin/activate"

    # Install the required packages
    echo "\033[93mValidating Libraries..\033[0m"
    pip install -r "$dir_origin/requirements.txt"

    # Make shell script executable
    chmod +x $dir_lardx/lardx

    # Create env path for lardx
    # String to search for
    path_string="PATH=\$PATH:$dir_lardx"

    # For Zsh
    if [ -n "$ZSH_VERSION" ]; then
        # File to search in
        path_file="$HOME/.zshrc"
        # Check if the string does not exist in the file using grep
        if ! grep -q "$path_string" "$path_file"; then
            echo "\033[94mSetting up \$PATH to ~/.zshrc..\033[0m"
            printf "\n\n$path_string\n\n" >> $path_file
        else
            echo "\033[93mThe \$PATH in ~/.zshrc already exists..\033[0m"
        fi

    # For Bash
    elif [ -n "$BASH_VERSION" ]; then
        # File to search in
        path_file="$HOME/.bashrc"
        # Check if the string does not exist in the file using grep
        if ! grep -q "$path_string" "$path_file"; then
            echo "\033[94mSetting up \$PATH to ~/.bashrc..\033[0m"
            printf "\n\n$path_string\n\n" >> $path_file
        else
            echo "\033[93mThe \$PATH in ~/.bashrc already exists..\033[0m"
        fi

    else
        # Looks like both shells aren't installed
        echo -e "\n\033[91mOnly BASH and ZSH shells are supported.\033[0m"
        echo -e "\n\033[91mOtherwise, you have to manually set \$PATH for ~/.lardx \033[0m"
    fi    

    echo -e "\n\n\n\n\033[92mSuccess! Lardx has been installed. \033[0m"
    echo "Type \033[95m lardx \033[0m to start" 
    flag_success=1
fi


# Remove folder if installation failed, 
if [ "$flag_success" -eq 0 ]; then
    # TODO: remove the string in path
    echo -e "\n\033[91mFailed! Lardx was not installed. \033[0m"
    rm -r $dir_lardx
fi