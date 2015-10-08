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
    """
    Set of method that are useful to test SMTP fonctionality
    """
    _default_keys = {
        "mx": "127.0.0.1",
        "port": "25",
        "to": "test@test.org",
        "from": "test@test.org"}

    def _get_log_mail(self, server):
        return check_result("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' cat /var/log/mail.log | '
                                                                            'cut -d " " -f 7|cut -d ":" -f 1| '
                                                                            'egrep [0-9A-Z]{10}| tail -n 1',
                            shell=True).decode("ascii")
        
    def _get_mail_has_failed(self, server, mail_id):
        try:
            return check_result("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' grep ' + mail_id
                                + ' /var/log/mail.log | grep "status=def"',
                                shell=True).decode("ascii") != ''
        except Exception:
            return False

    def _get_mail_has_success(self, server, mail_id):
        try:
            return check_result("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' grep ' + mail_id +
                                ' /var/log/mail.log | grep "status=sent"',
                                shell=True).decode("ascii") != ''
        except Exception:
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
        """Send a e-mail to test server and check it was successful

        :param message: the full message
        :type message: str
        :param kwargs: a dictionary with "mx", "port", "to", et "from"
        :return: the result as a tuple with result[0] a bool and result[1] the message sent back by the server
        :rtype: tuple[bool,str]
        """
        params = {}
        for key, value in self._default_keys.items():
            params[key] = kwargs.get(key, value)
        params["msg"] = message
        m_id = ""
        try:
            self._connection(**params)
            m_id = self._get_log_mail(params["mx"]).strip()
            return self._get_mail_has_success(params['mx'], m_id), "Message sent:" + m_id
        except SMTPTesterConnectionError:
            return (False, "Cannot connect to mail server {} at port {}".format(params["mx"], params["port"]))
        except SMTPException as e:
            return (False, "Message " + m_id + " was not delivered due to an error " + str(e))
    
    def sendMessageMustBeRejected(self, message, **kwargs):
        """Send a e-mail to test server and check it was rejected

        :param message: the full message
        :type message: str
        :param kwargs: a dictionary with "mx", "port", "to", et "from"
        :return: the result as a tuple with result[0] a bool and result[1] the message sent back by the server
        :rtype: tuple[bool,str]
        """
        params = {}
        for key, value in self._default_keys.items():
            params[key] = kwargs.get(key, value)
        params["msg"] = message
        try:
            self._connection(**params)
            m_id = self._get_log_mail(params["mx"]).strip()
            return (self._get_mail_has_failed(params["mx"], m_id), "Message sent, error was expected")
        except SMTPTesterConnectionError:
            return (False, "Cannot connect to mail server {} at port {}".format(params["mx"], params["port"]))
        except SMTPException as e:
            return (True, "Message was rejected as expected " + str(e))


class MailBuilder:
    """
    A context-like object to build mail with a fluent api
    """
    _current = None
    must_replace = True
    
    def add_attachment(self, byte_stream, attachement_name):
        """add attachment to the mail

        :param byte_stream:
        :param attachement_name: the name that will be used in attachment
        :type attachement_name: str
        :return: a self instance to allow chaining
        :rtype: MailBuilder
        """
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
        """set the sender address

        :param sender: the address
        :type sender: str
        :return: a self instance to allow chaining
        :rtype: MailBuilder
        """
        self._current["From"] = sender
        return self
    
    def with_recipients(self, *args):
        """add addresses to the To header

        :param args: the list of all recipient addresses
        :return: a self instance to allow chaining
        :rtype: MailBuilder
        """
        elements = self._current.get("To").split(COMMASPACE) or []
        self._current["To"] = COMMASPACE.join(elements + [str(a) for a in args])
        return self

    def with_copy(self, *args):
        """add addresses to the CC header

        :param args: the list of all recipient addresses
        :return: a self instance to allow chaining
        :rtype: MailBuilder
        """
        elements = self._current.get("CC").split(COMMASPACE) or []
        self._current["CC"] = COMMASPACE.join(elements + [str(a) for a in args])
        return self

    def with_carbon_copy(self, *args):
        """add addresses to the CCp header

        :param args: the list of all recipient addresses
        :return: a self instance to allow chaining
        :rtype: MailBuilder
        """
        elements = self._current.get("CCp").split(COMMASPACE) or []
        self._current["CCp"] = COMMASPACE.join(elements + [str(a) for a in args])
        return self

    def with_subject(self, subject):
        """Set the Subject error

        :param subject:
        :type subject: str
        :return: a self instance to allow chaining
        :rtype: MailBuilder
        """
        self._current["Subject"] = subject
        return self
    
    def with_html_part(self, html_code):
        """add an html part to a MULTIPART mail or make it the only part

        :param html_code:
        :return: a self instance to allow chaining
        :rtype: MailBuilder
        """
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
        """add a text part

        :param text:
        :return: a self instance to allow chaining
        :rtype: MailBuilder
        """
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
        """

        :return:
        """
        if self.must_replace:
            self._current = MIMEText("")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self._current = None

    def __str__(self):
        return self.build().as_string()

    def __init__(self, from_file=None):
        if from_file is not None:
            with open(from_file, 'rb') as f:
                self._current = message_from_binary_file(f)
    
    def build(self):
        """gather all data and generate the mail

        :return: the generated mail
        :rtype: str
        """
        self._current["Date"] = formatdate(localtime=True)
        return self._current
