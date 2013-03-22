__author__ = 'snasrallah'
import smtplib

fromaddr = ''
toaddrs  = ''
msg = 'There was a terrible error that occured and I wanted you to know about'


# Credentials (if needed)
username = ''
password = ''

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
