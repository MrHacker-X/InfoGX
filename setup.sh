# !/bin/bash
# Created by Alex Butler (MrHacker-X)
# Don't be a copy cat, Be original always

clear
echo -e "\033[1;97m██\033[1;91m╗\033[1;97m███\033[1;91m╗░░\033[1;97m██\033[1;91m╗\033[1;97m███████\033[1;91m╗░\033[1;97m█████\033[1;91m╗░░\033[1;97m██████\033[1;91m╗░\033[1;97m██\033[1;91m╗░░\033[1;97m██\033[1;91m╗"
echo -e "\033[1;97m██\033[1;91m║\033[1;97m████\033[1;91m╗░\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m╔════╝\033[1;97m██\033[1;91m╔══\033[1;97m██\033[1;91m╗\033[1;97m██\033[1;91m╔════╝░╚\033[1;97m██\033[1;91m╗\033[1;97m██\033[1;91m╔╝"
echo -e "\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m╔\033[1;97m██\033[1;91m╗\033[1;97m██\033[1;91m║\033[1;97m█████\033[1;91m╗░░\033[1;97m██\033[1;91m║░░\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m║░░\033[1;97m██\033[1;91m╗░░╚\033[1;97m███\033[1;91m╔╝░"
echo -e "\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m║╚\033[1;97m████\033[1;91m║\033[1;97m██\033[1;91m╔══╝░░\033[1;97m██\033[1;91m║░░\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m║░░╚\033[1;97m██\033[1;91m╗░\033[1;97m██\033[1;91m╔\033[1;97m██\033[1;91m╗░"
echo -e "\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m║░╚\033[1;97m███\033[1;91m║\033[1;97m██\033[1;91m║░░░░░╚\033[1;97m█████\033[1;91m╔╝╚\033[1;97m██████\033[1;91m╔╝\033[1;97m██\033[1;91m╔╝╚\033[1;97m██\033[1;91m╗"
echo -e "\033[1;91m╚═╝╚═╝░░╚══╝╚═╝░░░░░░╚════╝░░╚═════╝░╚═╝░░╚═╝"
echo -e "\033[1;91m░░░░░░░░\033[1;97m█ \033[1;91mCreated By: MrHacker-X \033[1;97m█\033[1;91m░░░\033[1;97mV_0.92\033[1;91m░░"
echo
echo
if [ -d "/data/data/com.termux/files" ];then
    echo '[*] Setting up it in your termux'
    apt update -y
    apt upgrade -y
    apt install python termux-tools -y
    pip install requests
    touch infogx
    echo 'python /data/data/com.termux/InfoGX/infogx.py' > infogx
    chmod +x infogx
    mv infogx /data/data/com.termux/files/usr/bin
    rm -rf /data/data/com.termux/InfoGX
    mkdir /data/data/com.termux/InfoGX
    chmod +x infogx.py
    mv infogx.py /data/data/com.termux/InfoGX
    rm -rf ../InfoGX

else
    sudo echo '[*] Setting up it in your Linux'
    sudo apt-get update -y
    sudo apt-get upgrade -y
    sudo apt-get install python3 python3-pip -y
    sudo pip install requests
    sudo touch infogx
    sudo echo 'python3 /usr/local/InfoGX/infogx.py' > infogx
    sudo chmod +x infogx 
    sudo mv infogx /usr/local/bin
    sudo rm -rf /usr/local/InfoGX
    sudo mkdir /usr/local/InfoGX
    chmod +x infogx.py 
    sudo mv .infogx.py /usr/local/InfoGX
    sudo rm -rf ../InfoGX

fi

echo
echo
echo -e "\033[1;91m[*] \033[1;97mInstallation is completed"
echo -e "\033[1;91m[*] \033[1;97mNote: You need to relaunch your terminal to work properly"
echo -e "\033[1;91m[*] \033[1;97mAfter relaunching InfoGX will work properly"
echo -e "\033[1;91m[*] \033[1;97mJust Close and Reopen Your terminal to relaunch it"
echo -e "\033[1;91m[*] \033[1;97mAnd booooooom"
echo -e "\033[1;91m[*] \033[1;97mNow you can launch InfoGX by command 'infogx'"
echo
echo
echo

