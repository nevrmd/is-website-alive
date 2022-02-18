from time import sleep
import requests
import configparser
import smtplib
from email.mime.text import MIMEText

config = configparser.ConfigParser()
config.read("config.ini")
sender_email = config["From"]["email"]
sender_password = config["From"]["password"]
sender_host = config["From"]["host"]
sender_port = config["From"]["port"]
death = config["From"]["death"]
alive = config["From"]["alive"]
to_email = config["To"]["email"]
url = config["Website"]["url"]

try:
    requests.get(url)
except requests.exceptions.MissingSchema and requests.exceptions.ConnectionError:
    print(f"Invalid url '{url}'")
    exit()

input(f"Your email - '{sender_email}' and url that will be checked is '{url}'.\nAre you sure?")

is_email_sended = False

while True:
    res = requests.get(url)
    print("Checking website status...", end=" ")
    if res:
        if is_email_sended:
            print("website is brought to life, sending an email...")
            try:
                print("Trying to connect via secure connection...", end=" ")
                smtpObj = smtplib.SMTP(sender_host, sender_port)
                smtpObj.starttls()
                print("success!")
                print("Trying to send an email...", end=" ")
                smtpObj.login(sender_email, sender_password)
                smtpObj.sendmail(sender_email, to_email, f"{alive} ({res.status_code})")
                print("success!\n")
        
            # errors
            except smtplib.SMTPAuthenticationError:
                print("wrong email or password!")

            except smtplib.SMTPRecipientsRefused:
                print("invalid resiever's email")

            except UnicodeError:
                msg = MIMEText(alive, 'plain', 'utf-8')
                smtpObj.sendmail(sender_email, to_email, msg.as_string())
                print("success!")

            except:
                print("some error occured")
        
        elif not is_email_sended:
            print(f"website is alive ({res.status_code})!")
            is_email_sended = False
            sleep(15)
    
    elif not res:
        if is_email_sended:
            print("it still death!")
            sleep(15)
        elif not is_email_sended:
            print(f"website is dead ({res.status_code}), sending an email...\n")
            try:
                print("Trying to connect via secure connection...", end=" ")
                smtpObj = smtplib.SMTP(sender_host, sender_port)
                smtpObj.starttls()
                print("success!")
                print("Trying to send an email...", end=" ")
                smtpObj.login(sender_email, sender_password)
                smtpObj.sendmail(sender_email, to_email, f"{death} ({res.status_code})")
                print("success!\n")
                is_email_sended = True
        
            # errors
            except smtplib.SMTPAuthenticationError:
                print("wrong email or password!")

            except smtplib.SMTPRecipientsRefused:
                print("invalid resiever's email")

            except UnicodeError:
                msg = MIMEText(death, 'plain', 'utf-8')
                smtpObj.sendmail(sender_email, to_email, msg.as_string())
                print("success!")

            except:
                print("some error occured")