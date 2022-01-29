import smtplib
import ssl


class Sender:

    def __init__(self):
        self.EMAIL_MESSAGES = {
            'last_watered': {
                'subject': 'Raspberry Pi: Plant Watering Time',
                'message': 'Your plant was last watered at'
            },
            'check_water_level': {
                'subject': 'Raspberry Pi: Check Water Level',
                'message': 'Check your water level!',
            }
        }

    def send_email(self, time_last_watered, subject, message):
        port = 465
        smtp_server = "smtp.gmail.com"
        FROM = TO = "YOUR_EMAIL@gmail.com"
        password = "YOUR_PASSWORD"

        complete_message = ''
        if not time_last_watered:
            complete_message = "Subject: {}\n\n{}".format(subject, message)
        else:
            complete_message = "Subject: {}\n\n{} {}".format(subject, message, time_last_watered)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(FROM, password)
            server.sendmail(FROM, TO, complete_message)

    def send_last_watered_email(self, time_last_watered):
        message = self.EMAIL_MESSAGES['last_watered']['message']
        subject = self.EMAIL_MESSAGES['last_watered']['subject']
        self.send_email(time_last_watered, subject, message)

    def send_check_water_level_email(self):
        message = self.EMAIL_MESSAGES['check_water_level']['message']
        subject = self.EMAIL_MESSAGES['check_water_level']['subject']
        self.send_email(False, subject, message)
