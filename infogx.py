# !/bin/python3

import requests
import os
import time
import signal

def load():

	def loadbar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
		percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
		filledLength = int(length * iteration // total)
		bar = fill * filledLength + '-' * (length - filledLength)
		print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
		if iteration == total:
			print()

	items = list(range(0, 30))
	l = len(items)

	loadbar(0, l, prefix='Progress:', suffix='Complete', length=l)
	for i, item in enumerate(items):
		time.sleep(0.08)
		loadbar(i + 1, l, prefix='Progress:', suffix='Complete', length=l)

banner = """\033[1;97m██\033[1;91m╗\033[1;97m███\033[1;91m╗░░\033[1;97m██\033[1;91m╗\033[1;97m███████\033[1;91m╗░\033[1;97m█████\033[1;91m╗░░\033[1;97m██████\033[1;91m╗░\033[1;97m██\033[1;91m╗░░\033[1;97m██\033[1;91m╗
\033[1;97m██\033[1;91m║\033[1;97m████\033[1;91m╗░\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m╔════╝\033[1;97m██\033[1;91m╔══\033[1;97m██\033[1;91m╗\033[1;97m██\033[1;91m╔════╝░╚\033[1;97m██\033[1;91m╗\033[1;97m██\033[1;91m╔╝
\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m╔\033[1;97m██\033[1;91m╗\033[1;97m██\033[1;91m║\033[1;97m█████\033[1;91m╗░░\033[1;97m██\033[1;91m║░░\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m║░░\033[1;97m██\033[1;91m╗░░╚\033[1;97m███\033[1;91m╔╝░
\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m║╚\033[1;97m████\033[1;91m║\033[1;97m██\033[1;91m╔══╝░░\033[1;97m██\033[1;91m║░░\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m║░░╚\033[1;97m██\033[1;91m╗░\033[1;97m██\033[1;91m╔\033[1;97m██\033[1;91m╗░
\033[1;97m██\033[1;91m║\033[1;97m██\033[1;91m║░╚\033[1;97m███\033[1;91m║\033[1;97m██\033[1;91m║░░░░░╚\033[1;97m█████\033[1;91m╔╝╚\033[1;97m██████\033[1;91m╔╝\033[1;97m██\033[1;91m╔╝╚\033[1;97m██\033[1;91m╗
\033[1;91m╚═╝╚═╝░░╚══╝╚═╝░░░░░░╚════╝░░╚═════╝░╚═╝░░╚═╝
\033[1;91m░░░░░░░░\033[1;97m█ \033[1;91mCreated By: MrHacker-X \033[1;97m█\033[1;91m░░░\033[1;97mV_0.92\033[1;91m░░
"""

main_mnu = """
\033[1;91m[?]\033[1;97m Select any Option

\033[1;91m[01]\033[1;97m Track IP Address
\033[1;91m[02]\033[1;97m E-mail Validatior
\033[1;91m[03]\033[1;97m Phone Number Validator
\033[1;91m[04]\033[1;97m Follow US
\033[1;91m[05]\033[1;97m WhoamI
\033[1;91m[00]\033[1;97m Quit

"""

soc = """\033[1;91m[*] \033[1;97mSelect any option

\033[1;91m[01] \033[1;97mInstagram
\033[1;91m[02] \033[1;97mFacebook
\033[1;91m[03] \033[1;97mGithub
\033[1;91m[04] \033[1;97mYouTube
\033[1;91m[05] \033[1;97mTelegram
\033[1;91m[06] \033[1;97mMy Website
\033[1;91m[99] \033[1;97mBack
\033[1;97m[00] \033[1;91mQuit

\033[1;97m[\033[1;91m??\033[1;97m] \033[1;91m>> \033[1;97m"""


about = """
\033[1;91m[*] Author: \033[1;97mAlex Butler (MrHacker-X)

\033[1;91m[*] Introduction: \033[1;97mHello guys I'm introducing on of best tool that is InfoGX. I've created this tool for linux and termux user, both user can use it. InfoGX tool can be for Gather information. You can gather information of different things. For now I'v added only 3 types of information Gathering features. That is given down below

\033[1;91m>> \033[1;97mPhoneNumber Validator
\033[1;91m>> \033[1;97mE-mail Validator
\033[1;91m>> \033[1;97mIP Tracking

\033[1;91m>>\033[1;97m In future I'll add more features in this tool. So you can follow me on github for Future updates Username is (MrHacker-X). 
\033[1;91m>>\033[1;97m If you have any Idea then you can tell me on Instagram  username is (0hacker_x0).

\033[1;91m[*] My Social media site:

\033[1;91m>> \033[1;97mInstagram   : 0hacker_x0
\033[1;91m>> \033[1;97mGithub      : MrHacker-X
\033[1;91m>> \033[1;97mYouTube     : Sololex
\033[1;91m>> \033[1;97mTelegram    : mrhackerxs
\033[1;91m>> \033[1;97mFacebook    : hackerxmr
\033[1;91m>> \033[1;97mMy Website  : hackwithalex.github.io

\033[1;91m>>\033[1;97m Thanks For Using InfoGX
"""


def ip():
    os.system('clear')
    print(banner)
    print()
    while True:
        ipad = input("\033[1;91m[?]\033[1;97m Enter target IP: ")

        if ipad == "":
            print()
            print("[!]No input detected")
            print()
            time.sleep(0.3)
        else:
            break

    ipr = requests.get("https://ipqualityscore.com/api/json/ip/pPiATkSdtLn3xgKW7a7HikZeZ4HMNa2R/" + ipad + "?strictness=0&allow_public_access_points=true&fast=true&lighter_penalties=true&mobile=true")
    print()
    load()
    time.sleep(1)
    print()
    print("\033[1;91m[~]\033[1;97m IP Details are given down below")
    print()
    print("\033[1;91m[*]\033[1;97m Target IP        : " + ipad )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m ASN              : " + str(ipr.json() ['ASN']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m ISP              : " + str(ipr.json() ['ISP']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Active TOR       : " + str(ipr.json() ['active_tor']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Active VPN       : " + str(ipr.json() ['active_vpn']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Country Code     : " + str(ipr.json() ['country_code']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Bot Status       : " + str(ipr.json() ['bot_status']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m City             : " + str(ipr.json() ['city']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Fraud Score      : " + str(ipr.json() ['fraud_score']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Host             : " + str(ipr.json() ['host']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Is Crawler       : " + str(ipr.json() ['is_crawler']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Latitude         : " + str(ipr.json() ['latitude']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Longitude        : " + str(ipr.json() ['longitude']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Message          : " + str(ipr.json() ['message']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Mobile           : " + str(ipr.json() ['mobile']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Organization     : " + str(ipr.json() ['organization']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Proxy            : " + str(ipr.json() ['proxy']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Recent Abuse     : " + str(ipr.json() ['recent_abuse']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Region           : " + str(ipr.json() ['region']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Request ID       : " + str(ipr.json() ['request_id']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Success          : " + str(ipr.json() ['success']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m TimeZone         : " + str(ipr.json() ['timezone']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m TOR              : " + str(ipr.json() ['tor']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m VPN              : " + str(ipr.json() ['vpn']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Zip Code         : " + str(ipr.json() ['zip_code']) )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Location         : \033[1;94mhttps://maps.google.com/?q=" + str(ipr.json() ['latitude']) + "," + str(ipr.json() ['longitude']) )
    print()
    time.sleep(0.1)
 
def mail():
    os.system('clear')
    print(banner)
    print()
    while True:
        em = input("\033[1;91m[?]\033[1;97m Enter target E-mail: ")
        if em == '':
            print()
            print("[!] No input detected")
            print()
            time.sleep(0.4)
        else:
            break

    eml = requests.get("https://ipqualityscore.com/api/json/email/pPiATkSdtLn3xgKW7a7HikZeZ4HMNa2R/" + em )
    print()
    load()
    time.sleep(1)
    print()
    print("\033[1;91m[~]\033[1;97m E-mail Details are given down below")
    print()
    print("\033[1;91m[*]\033[1;97m Target E-mail       : " + em )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Valid               : " + str(eml.json() ['valid']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Catch All           : " + str(eml.json() ['catch_all']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Common              : " + str(eml.json() ['common']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Deliverability      : " + str(eml.json() ['deliverability']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Disposable          : " + str(eml.json() ['disposable']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m DNS Valid           : " + str(eml.json() ['dns_valid']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Fraud Score         : " + str(eml.json() ['fraud_score']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Frequent Complainer : " + str(eml.json() ['frequent_complainer']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Generic             : " + str(eml.json() ['generic']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Honeypot            : " + str(eml.json() ['honeypot']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Leaked              : " + str(eml.json() ['leaked']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Message             : " + str(eml.json() ['message']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Over All Score      : " + str(eml.json() ['overall_score']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Recent Abuse        : " + str(eml.json() ['recent_abuse']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Request ID          : " + str(eml.json() ['request_id']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Sanitized E-mail    : " + str(eml.json() ['sanitized_email']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m SMTP Score          : " + str(eml.json() ['smtp_score']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Spam Trap Score     : " + str(eml.json() ['spam_trap_score']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Success             : " + str(eml.json() ['success']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Suggested Domain    : " + str(eml.json() ['suggested_domain']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Suspect             : " + str(eml.json() ['suspect']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Timed Out           : " + str(eml.json() ['timed_out']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m First Name          : " + str(eml.json() ['first_name']))
    time.sleep(0.1)
    print()
    print("\033[1;91m[~]\033[1;94m Domain Age")
    print()
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Human      : " + str(eml.json() ['domain_age'] ['human']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m ISO        : " + str(eml.json() ['domain_age'] ['iso']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Time Stamp : " + str(eml.json() ['domain_age'] ['timestamp']))
    time.sleep(0.1)
    print()
    print("\033[1;91m[~]\033[1;94m First Seen")
    print()
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Human      : " + str(eml.json() ['first_seen'] ['human']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m ISO        : " + str(eml.json() ['first_seen'] ['iso']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Time Stamp : " + str(eml.json() ['first_seen'] ['timestamp']))
    time.sleep(0.1)
    print()

def fonfo():
    os.system('clear')
    print(banner)
    print()
    while True:
        phn = input("\033[1;91m[?]\033[1;97m Enter Phone Number ( with country code ): ")
        if phn == '':
            print()
            print("[!] No input detected")
            print()
            time.sleep(0.4)
        else:
            break

    phe = requests.get("https://ipqualityscore.com/api/json/phone/pPiATkSdtLn3xgKW7a7HikZeZ4HMNa2R/" + phn )
    print()
    load()
    time.sleep(1)
    print()
    print("\033[1;91m[~]\033[1;97m Phone Number Details are given down below")
    print()
    print("\033[1;91m[*]\033[1;97m Target Number  : " + phn )
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Valid          : " + str(phe.json() ['valid']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m VOIP           : " + str(phe.json() ['VOIP']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Active         : " + str(phe.json() ['active']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Active Status  : " + str(phe.json() ['active_status']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Carrier        : " + str(phe.json() ['carrier']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m City           : " + str(phe.json() ['city']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Country        : " + str(phe.json() ['country']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Dialing Code   : " + str(phe.json() ['dialing_code']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Do Not Call    : " + str(phe.json() ['do_not_call']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Formatted      : " + str(phe.json() ['formatted']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Fraud Score    : " + str(phe.json() ['fraud_score']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Leaked         : " + str(phe.json() ['leaked']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Line Type      : " + str(phe.json() ['line_type']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Local Format   : " + str(phe.json() ['local_format']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m MCC            : " + str(phe.json() ['mcc']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Name           : " + str(phe.json() ['name']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Prepaid        : " + str(phe.json() ['prepaid']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Recent Abuse   : " + str(phe.json() ['recent_abuse']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Region         : " + str(phe.json() ['region']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Request ID     : " + str(phe.json() ['request_id']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Risky          : " + str(phe.json() ['risky']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m SMS Domain     : " + str(phe.json() ['sms_domain']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m SMS E-mail     : " + str(phe.json() ['sms_email']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Spammer        : " + str(phe.json() ['spammer']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Success        : " + str(phe.json() ['success']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m TimeZone       : " + str(phe.json() ['timezone']))
    time.sleep(0.1)
    print("\033[1;91m[*]\033[1;97m Zip Code       : " + str(phe.json() ['zip_code']))
    time.sleep(0.1)
    print()

## Main code begin from here

def hack():
    os.system('clear')
    print(banner)
    print(main_mnu)
    while True:
        os.system('clear')
        print(banner)
        print(main_mnu)
        mn = input("\033[1;91m[*]\033[1;97m infogx>> ")
        if mn == '':
            print()

        elif mn == '1' or mn == '01':
            print()
            print("\033[1;91m[*]\033[1;97m IP Tracing selected")
            time.sleep(1.1)
            os.system("clear")
            load()
            print(banner)
            print()
            ip()
            print()
            input("\033[1;94m Press ENTER To Continue")
            hack()

        elif mn == '2' or mn == '02':
            print()
            print("\033[1;91m[*]\033[1;97m E-mail Validator selected")
            time.sleep(1.1)
            os.system("clear")
            load()
            print(banner)
            print()
            mail()
            print()
            input("\033[1;94m Press ENTER To Continue")
            hack()

        elif mn == '3' or mn == '03':
            print()
            print("\033[1;91m[*]\033[1;97m Phone Number Validator selected")
            time.sleep(1.1)
            os.system("clear")
            load()
            print(banner)
            print()
            fonfo()
            print()
            input("\033[1;94m Press ENTER To Continue")
            hack()

        elif mn == '4' or mn == '04':
            print()
            print("\033[1;91m[*]\033[1;97m Follow US selected")
            time.sleep(1.1)
            os.system("clear")
            load()
            os.system("clear")
            print(banner)
            print()
            print("\033[1;91m[*] \033[1;97mThanks for using my tool 'InfoGX'. So you can follow me on various social media site. Link and options are given down below, So select here options where you want to follow me ")
            print()
            print()
            while True:
                fol = input(soc)
                if fol == '1' or fol == '01':
                    print()
                    print("\033[1;91m[*] \033[1;97mOpening my Instagram profile in your device \n")
                    time.sleep(1)
                    os.system("xdg-open https://instagram.com/0hacker_x0")
                
                elif fol == '2' or fol == '02':
                    print()
                    print("\033[1;91m[*] \033[1;97mOpening my Facebook page in your device \n")
                    time.sleep(1)
                    os.system("xdg-open https://facebook.com/hackerxmr")

                elif fol == '3' or fol == '03':
                    print()
                    print("\033[1;91m[*] \033[1;97mOpening my Github profile in your device \n")
                    time.sleep(1)
                    os.system("xdg-open https://github.com/MrHacker-X")

                elif fol == '4' or fol == '04':
                    print()
                    print("\033[1;91m[*] \033[1;97mOpening my YouTube channel in your device \n")
                    time.sleep(1)
                    os.system("xdg-open https://youtube.com/c/Sololex")
                
                elif fol == '5' or fol == '05':
                    print()
                    print("\033[1;91m[*] \033[1;97mOpening my Telegram Channel in your device \n")
                    time.sleep(1)
                    os.system("xdg-open https://t.me/mrhackersx")

                elif fol == '6' or fol == '06':
                    print()
                    print("\033[1;91m[*] \033[1;97mOpening my Website in your device \n")
                    time.sleep(1)
                    os.system("xdg-open https://hackwithalex.github.io")

                elif fol == '99':
                    print()
                    print("\033[1;91m[*]\033[1;97m Getting back ...\n")
                    time.sleep(1)
                    break

                elif fol == '0' or fol == '00':
                    print()
                    print("\033[1;91m[*]\033[1;97m Thanks for using InfoGX\n")
                    print("\033[1;91m[*]\033[1;97m Quiting ...\n")
                    time.sleep(1)
                    exit()
                    

                else:
                    print()
                    print("\033[1;91mInvalid Input")
                    print()

        elif mn == '5' or mn == '05':
            print()
            print("\033[1;91m[*]\033[1;97m WhoamI selected")
            print()
            time.sleep(1)
            os.system('clear')
            load()
            os.system('clear')
            print(banner)
            print()
            print(about)
            print()
            input("\033[1;94mPress ENTER For Continue")


        elif mn == '0' or mn == '00':
            print()
            print("\033[1;91m[*]\033[1;97m Thanks for using InfoGX\n")
            print("\033[1;91m[*]\033[1;97m Quitting.....")
            print()
            time.sleep(1)
            exit()
            
        else:
            print()
            print("\033[1;91m[!] Invalid input")
            time.sleep(1)
            print()
            
hack()
