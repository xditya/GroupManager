#!/bin/bash

# Add colors variables
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'
P='0'
#

#
bot_dir="/home/yacha/pKaraBot/"
script_q="${bot_dir}/Bot.sh"
cd $bot_dir
#

function logger(){
    date=$(date "+%Y/%m/%d %X")
    echo "${P} | ${date}: ${text}" >> script.log    #logging in file
    echo -e "${CYAN}${P} | ${date}:${NC} ${text}"   #show in terminal
    let "P=P+1"                                 
}

function run(){
    text="Creating tmux session..." && logger
    tmux kill-server #Kill all tmux sessions
    tmux new -d -s pKaraBot "bash $script_q load" # start new tmux session 
}
function stop(){
    text="Stopping bot!" && logger
    tmux kill-server #Kill all tmux sessions
}

function load(){
    text="Starting bot..." && logger
    for n in 99999; do python3 -m tg_bot; done
}

case "$1" in
    "run") run ;;
    "stop") stop ;;
    "load") load ;;
    "attach") tmux attach ;;
    *) echo other ;;
esac

