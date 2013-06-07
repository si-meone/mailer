__author__ = 'snasrallah'
import smtplib

# designed to be run via cron so crontab -e
# */15 * * * * python /home/username/scripts/mailer.py # JOB_ID_1

def mailer():
    fromaddr = ''
    toaddrs  = ''
    subject = "ip today"
    text = 'text'
    msg = 'Subject: %s\n\n%s' % (subject, get_ip_address())
    
    
    # Credentials (if needed)
    username = ''
    password = ''
    
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def get_ip_address():

    import socket
    # 1: Use the gethostname method

    ipaddr = socket.gethostbyname(socket.gethostname())
    if not( ipaddr.startswith('127') ) :
        print('Can use Method 1: ' + ipaddr)
        #return ipaddr

    # 2: Use outside connection
    '''
    Source:
    http://commandline.org.uk/python/how-to-find-out-ip-address-in-python/
    '''

    ipaddr=''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('google.com', 0))
        ipaddr=s.getsockname()[0]
        print('Can used Method 2: ' + ipaddr)
        return ipaddr
    except:
        pass


    # 3: Use OS specific command
    import subprocess , platform
    ipaddr=''
    os_str=platform.system().upper()

    if os_str=='LINUX' :

        # Linux:
        arg='ip route list'
        p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
        data = p.communicate()
        sdata = data[0].split()
        ipaddr = sdata[ sdata.index('src')+1 ]
        #netdev = sdata[ sdata.index('dev')+1 ]
        print('Can used Method 3: ' + ipaddr)
        #return ipaddr

    elif os_str=='WINDOWS' :

        # Windows:
        arg='route print 0.0.0.0'
        p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
        data = p.communicate()
        strdata=data[0].decode()
        sdata = strdata.split()

        while len(sdata)>0:
            if sdata.pop(0)=='Netmask' :
                if sdata[0]=='Gateway' and sdata[1]=='Interface' :
                    ipaddr=sdata[6]
                    break
        print('Can used Method 4: ' + ipaddr)
        #return ipaddr

def has_ip_address_changed(ip_address):
    try:
        with open ("ip_address", "r") as myfile:
            ip_in_file = myfile.read().replace('\n', '')
    except:
        print 'no ip set writing file'
        fw = open('ip_address', 'w')
        fw.write(ip_address)
        return True

    if ip_address == ip_in_file:
        print 'ip same'
        return False
    else :
        print 'ip different'
        fw = open('ip_address', 'w')
        fw.write(ip_address)
        return True


if __name__ == '__main__':
    ip = get_ip_address()
    if has_ip_address_changed(ip):
        mailer(ip)
