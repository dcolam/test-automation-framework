from smtplib import SMTP, SMTPException, SMTPSenderRefused, SMTPRecipientsRefused, SMTPDataError
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
        a = check_result("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' cat /var/log/mail.log | grep qavrc|'
                                                                         'cut -d " " -f 6|cut -d ":" -f 1| '
                                                                         'egrep [0-9A-Z]{10}| tail -n 1',
                         shell=True).decode("ascii")

        return check_result("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' cat /var/log/mail.log | grep qavrc|'
                                                                            'cut -d " " -f 6|cut -d ":" -f 1| '
                                                                            'egrep [0-9A-Z]{10}| tail -n 1',
                            shell=True).decode("ascii")
        
    def _get_mail_has_failed(self, server, mail_id):
        try:
            return check_result("ssh -i ~/.ssh/id_rsa.pub sysadmin@" + server + ' grep ' + mail_id
                                + ' /var/log/mail.log | grep "status=def"',
                                shell=True).decode("ascii") != ''
        except Exception as e:
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

    def _send_no_esmtp_mail(self, **kwargs):
        """This command performs an entire mail transaction.

        The arguments are:
            - from_addr    : The address sending this mail.
            - to_addrs     : A list of addresses to send this mail to.  A bare
                             string will be treated as a list with 1 address.
            - msg          : The message to send.
            - mail_options : List of ESMTP options (such as 8bitmime) for the
                             mail command.
            - rcpt_options : List of ESMTP options (such as DSN commands) for
                             all the rcpt commands.

        msg may be a string containing characters in the ASCII range, or a byte
        string.  A string is encoded to bytes using the ascii codec, and lone
        \\r and \\n characters are converted to \\r\\n characters.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.  If the server does ESMTP, message size
        and each of the specified options will be passed to it.  If EHLO
        fails, HELO will be tried and ESMTP options suppressed.

        This method will return normally if the mail is accepted for at least
        one recipient.  It returns a dictionary, with one entry for each
        recipient that was refused.  Each entry contains a tuple of the SMTP
        error code and the accompanying error message sent by the server.

        This method may raise the following exceptions:

         SMTPHeloError          The server didn't reply properly to
                                the helo greeting.
         SMTPRecipientsRefused  The server rejected ALL recipients
                                (no mail was sent).
         SMTPSenderRefused      The server didn't accept the from_addr.
         SMTPDataError          The server replied with an unexpected
                                error code (other than a refusal of
                                a recipient).

        Note: the connection will be open even after an exception is raised.

        Example:

        In the above example, the message was accepted for delivery to three
        of the four addresses, and one was rejected, with the error code
        550.  If all addresses are accepted, then the method will return an
        empty dictionary.

        """
        try:
            server = SMTP(kwargs["mx"], kwargs["port"])
        except Exception:
            raise SMTPTesterConnectionError()
        server.helo()
        msg = kwargs["msg"].as_string()
        (code, resp) = server.mail(kwargs["from"], [])
        if code != 250:
            if code == 421:
                server.close()
            else:
                server._rset()
            raise SMTPSenderRefused(code, resp, kwargs["from"])
        senderrs = {}
        to_addrs = kwargs["to"]
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        for each in to_addrs:
            (code, resp) = server.rcpt(each, [])
            if (code != 250) and (code != 251):
                senderrs[each] = (code, resp)
            if code == 421:
                server.close()
                raise SMTPRecipientsRefused(senderrs)
        if len(senderrs) == len(to_addrs):
            # the server refused all our recipients
            server._rset()
            raise SMTPRecipientsRefused(senderrs)
        (code, resp) = server.data(msg)
        if code != 250:
            if code == 421:
                server.close()
            else:
                server._rset()
            raise SMTPDataError(code, resp)
        #if we got here then somebody got our mail
        return senderrs
    
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
    
    def sendMessageMustBeRejected(self, message, esmtp=True, **kwargs):
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
            if esmtp:
                self._connection(**params)
            else:
                self._send_no_esmtp_mail(**params)
            m_id = self._get_log_mail(params["mx"]).strip()
            if not m_id:
                raise Exception("message queue id not found")
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
        if not self._current or not isinstance(self._current, MIMEMultipart):
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
        elements = self._current.get("To", "").split(COMMASPACE) or []
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
            self.must_replace = False
    
    def build(self):
        """gather all data and generate the mail

        :return: the generated mail
        :rtype: str
        """
        self._current["Date"] = formatdate(localtime=True)
        return self._current
