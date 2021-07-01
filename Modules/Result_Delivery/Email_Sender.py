import smtplib, ssl

from ..Constants.constants import SENDER_EMAIL, RECEIVER_EMAILS, EMAIL_PW

class Email_Sender:
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls

    def __init__(self):
        # Create a secure SSL context
        self.context = ssl.create_default_context()
    
    def send_message(self, msg: str, receiver_email: str="gazi.tony.trading@gmail.com"):
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(Email_Sender.smtp_server,Email_Sender.port)
            server.ehlo() # Can be omitted
            server.starttls(context=self.context) # Secure the connection
            server.ehlo() # Can be omitted  
            server.login(SENDER_EMAIL, EMAIL_PW)
            for receiver_email in RECEIVER_EMAILS:
                server.sendmail(SENDER_EMAIL, receiver_email, msg)

        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit() 





