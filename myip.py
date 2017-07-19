from urllib import request
from email.mime.text import MIMEText
import smtplib,time

def get_ip():
    url=r'http://ifconfig.me/ip'
    try:
        with request.urlopen(url) as ipf:
            ip=ipf.read().decode('utf-8').strip('\n')
            print('Get ip correctly!',ip)
            return ip
    except:
        print('Get ip error!')
        time.sleep(60)
        print("Get ip again!")
        ip=get_ip()
        return ip

def send_ip(ip):
    mail_host='smtp.163.com'
    mail_user='shmild123'
    mail_pswd='gr**891106'
    try:
        server=smtplib.SMTP(mail_host,25)
        server.login(mail_user,mail_pswd)
        msg=MIMEText(ip,'plain','utf-8')
        server.sendmail('shmild123@163.com','shmild123@163.com',msg.as_string())
        server.close()
        print('Send email correctly!')
        return True
    except Exception as e:
        print('Send email error!',e)
        return False

if __name__=='__main__':
    ip=get_ip()
    if_send=send_ip(ip)
    ip_new=ip
    n=0
    while True:
        time.sleep(60)
        if not ip:
            print('Ip is none!')
            ip = get_ip()
            ip_new = ip
            if_send = send_ip(ip)
        elif ip!=ip_new:
            print('Ip renewed!')
            ip=ip_new
            if_send = send_ip(ip)
        elif not if_send:
            print('Send again!')
            if_send = send_ip(ip)
        else:
            print('Everything goes well,fall in sleep now!')
            time.sleep(1800)
            print('Awake,get ip again!')
            ip_new=get_ip()
        if n>=10:
            break
        else:
            n+=1