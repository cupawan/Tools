import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import yaml
import re

class SendEmail:
    def __init__(self,config_file_path,is_html = False):
        self.config_file_path = config_file_path
        self.is_html = is_html
        self.config = self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_file_path,'r') as f:
                config = yaml.safe_load(f)
                return config
        except Exception as e:
            d = {}
            return d
    def send_email(self, rec_email, body,subject = "", file_paths = None):
        msg = MIMEMultipart()
        msg['From'] = self.config['MY_EMAIL_ADDRESS']
        msg['To'] = rec_email
        rec_name = rec_email.split("@")[0]
        match = re.search(r'([a-zA-Z]+)(\d+)', rec_name)
        rec_name = match.groups()[0] if match else rec_name
        today_date = datetime.now().strftime("%d-%m-%Y")
        msg['Subject'] = f"{today_date} {subject.strip()}"
        if not self.is_html:
            body2 = f"Hello {rec_name}\n\n{body}"
            msg.attach(MIMEText(body2, 'plain'))
        else:            
            body2 = f"<h3>Hello {rec_name}</h3>\n\n{body}"
            msg.attach(MIMEText(body2, 'html'))
        if file_paths and isinstance(file_paths,list):
            for file_path in file_paths:
                attachment = open(file_path, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= " + file_path.split("/")[-1])
                msg.attach(part)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.config['MY_EMAIL_ADDRESS'], self.config['MY_GMAIL_APP_PASSWORD'])
            server.sendmail(self.config['MY_EMAIL_ADDRESS'], rec_email, msg.as_string())
        return {'status': 'sent'}
    

if __name__ == "__main__":
    ins = SendEmail(config_file_path="tools_config.yaml")
    ins.send_email(rec_email='username@domain.com',body = "<email_body>", subject = "Test Email", file_paths=["file1,file2,file3..."])
    
    