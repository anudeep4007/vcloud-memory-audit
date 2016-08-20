#in case you are looking for additional configuration for mail server check this
# http://naelshiab.com/tutorial-send-email-python/

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

class email_sent(object):

        def send_mail(self, to_email, subject, text, file_path_list):

            print to_email
            MAIL_SERVER = 'example@example.com'
            SENDER_EMAIL = 'example@example.com'
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            #msg['To'] = ", ".join(to_email)
            msg['To'] = to_email
            msg['Subject'] = subject
            print msg['To']

            msg.attach(MIMEText(text))

            #print file_path_list

            for f in file_path_list:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(f, 'rb').read())
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'\
                                % os.path.basename(f))
                msg.attach(part)

            mail_server = smtplib.SMTP(MAIL_SERVER)
            #mail_server.login(SENDER_USER, SENDER_PASSWORD)
            #split th and sent to multiple
            mail_server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
            mail_server.close()