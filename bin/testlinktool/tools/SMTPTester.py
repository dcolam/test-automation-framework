from smtplib import SMTP, SMTPException
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from subprocess import check_output as check_result
from email import message_from_binary_file

class SMTPTesterConnectionError(RuntimeError):
    pass


class SMTPTester():
    _default_keys = {
        "mx": "127.0.0.1",
        "port": "25",
        "to": "test@test.org",
        "from": "test@test.org"}

    def _get_log_mail(self, server):
        return check_result("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' cat /var/log/mail.log | cut -d " " -f 7|cut -d ":" -f 1| egrep [0-9A-Z]{10}| tail -n 1',
                            shell=True).decode("ascii")
        
    def _get_mail_has_failed(self, server, mail_id):
        try:
            return check_result("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' grep ' + mail_id +' /var/log/mail.log | grep "status=def"',
                                shell=True).decode("ascii") != ''
        except Exception:
            return False

    def _get_mail_has_success(self, server, mail_id):
        try:
            print("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' grep ' + mail_id +' /var/log/mail.log | grep "status=sent"')
            return check_result("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' grep ' + mail_id +' /var/log/mail.log | grep "status=sent"',
                                shell=True).decode("ascii") != ''
        except:
            return False

    def _connection(self, **kwargs):
        try:
            server = SMTP(kwargs["mx"], kwargs["port"])
        except Exception:
            raise SMTPTesterConnectionError()
        try:
            if not isinstance(kwargs["to"], list):
                kwargs["to"] = [kwargs["to"]]
            result = server.sendmail(kwargs["from"], kwargs["to"], kwargs["msg"].as_string())
            if result != {}:
                raise SMTPException()
            
        except SMTPException:
            raise
        finally:
            server.close()
    
    def sendMessageMustSucceed(self, message, **kwargs):
        params = {}
        for key, value in self._default_keys.items():
            params[key] = kwargs.get(key, value)
        params["msg"] = message
        m_id = ""
        try:
            self._connection(**params)
            m_id = self._get_log_mail(params["mx"]).strip()
            return (self._get_mail_has_success(params['mx'], m_id), "Message sent:"+m_id)
        except SMTPTesterConnectionError:
            return (False, "Cannot connect to mail server {} at port {}".format(params["mx"], params["port"]))
        except SMTPException as e:
            return (False, "Message " + m_id + " was not delivered due to an error " + str(e))
    
    def sendMessageMustBeRejected(self, message, **kwargs):
        params = {}
        for key, value in self._default_keys.items():
            params[key] = kwargs.get(key, value)
        params["msg"] = message
        try:
            self._connection(**params)
            m_id = self._get_log_mail(param["mx"]).strip()
            return (self._get_mail_has_failed(param["mx"], m_id), "Message sent, error was expected")
        except SMTPTesterConnectionError:
            return (False, "Cannot connect to mail server {} at port {}".format(params["mx"], params["port"]))
        except SMTPException as e:
            return (True, "Message was rejected as expected " + str(e))


class MailBuilder:
    
    _current = None
    must_replace = True
    
    def add_attachment(self, byte_stream, attachement_name):
        if not self._current or not isinstance(self.current, MIMEMultipart):
            temp = self._current
            self._current = MIMEMultipart(Subject=temp["Subject"],
                                          To=temp["To"],
                                          From=temp["From"])
            if temp:
                self._current.attach(temp)
        attachment = MIMEApplication(byte_stream)
        attachment.add_header("Content-Disposition",
                              'attachment',
                              filename=attachement_name)
        self._current.attach(attachment)
        return self
    
    def with_sender(self, sender):
        self._current["From"] = sender
        return self
    
    def with_recipients(self, *args):
        self._current["To"] = COMMASPACE.join([str(a) for a in args])
        return self
    
    def with_subject(self, subject):
        self._current["Subject"] = subject
        return self
    
    def with_html_part(self, html_code):
        html_part = MIMEText(html_code, "html")
        if not self._current:
            self._current = html_part
        elif not isinstance(self._current, MIMEMultipart):
            temp = self._current
            if not self.must_replace:
                self._current = MIMEMultipart(Subject=temp["Subject"],
                                              To=temp["To"],
                                              From=temp["From"],
                                              Date=temp["Date"])

                self._current.attach(temp)
                self._current.attach(html_part)
            else:
                self._current = html_part
                self.must_replace = False
        else:
            self._current.attach(html_part)
        return self
    
    def with_plain_text_part(self, text):
        txt_part = MIMEText(text, "plan")
        if not self._current:
            self._current = txt_part
        elif not isinstance(self._current, MIMEMultipart):
            temp = self._current
            if not self.must_replace:
                self._current = MIMEMultipart(Subject=temp["Subject"],
                                              To=temp["To"],
                                              From=temp["From"],
                                              Date=temp["Date"])
                self._current.attach(temp)
                self._current.attach(txt_part)
            else:
                self._current = txt_part
                self.must_replace = False
        else:
            self._current.attach(txt_part)
        return self

    def __enter__(self):
        if self.must_replace:
            self._current = MIMEText("")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._current = None

    def __str__(self):
        return self.build().as_string()

    def __init__(self, from_file=None):
        if from_file is not None:
            with open(from_file, 'rb') as f:
                self._current = message_from_binary_file(f)
    
    def build(self):
        self._current["Date"] = formatdate(localtime=True)
        return self._current
