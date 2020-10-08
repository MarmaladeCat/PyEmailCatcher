import smtplib,time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from poplib import POP3
import json,re
import mimetypes
import email.encoders


class MIMEmail:

    def __init__(self):
        self.smtp = ""
        self.pop3 = ""
        
        self.port_smtp = None
        self.port_pop3 = None
        self.authMail = ""
        self.authPasswd = ""
        self.mailFrom = ""
        self.mailTo = []
        self.msg = MIMEMultipart("mixed")  # main MIME message

    def setBasic(self, basic):
        # subject to from
        self.msg['Subject'] = basic["subject"]
        receiver = []
        for i, addr in basic["toMail"].items():
            receiver.append(addr)
        self.msg["To"] = Header(','.join(receiver))
        self.msg['From'] = basic["fromMail"]
        Cc = []
        for i, addr in basic["Cc"].items():
            Cc.append(addr)
        self.msg["Cc"] = Header(','.join(Cc))

    # def setSendinfo(self, sendinfo):
    #     self.host_smtp = sendinfo["host_smtp"]
    #     self.host_pop3 = sendinfo["host_pop3"]
        
    #     self.port_smtp = sendinfo["port_smtp"]
    #     self.port_pop3 = sendinfo["port_pop3"]

    #     self.authMail = sendinfo["authMail"]
    #     self.authPasswd = sendinfo["authPasswd"]

    def setContent(self, content):
        part = MIMEMultipart("related")
        if content["contentNum"] != 0:
            for id, path in content["contentPath"].items():
                ctype, encoding = mimetypes.guess_type(path)
                with open(path, "r") as fp:
                    partTmp = MIMEText(fp.read(), _subtype=ctype.split("/")
                                       [-1], _charset=encoding)
                    part.attach(partTmp)
        if content["imageNum"] != 0:
            for id, path in content["imagePath"].items():
                ctype, encoding = mimetypes.guess_type(path["path"])
                with open(path["path"], "rb") as fp:
                    partTmp = MIMEImage(fp.read(), _subtype=ctype.split(
                        "/")[-1], _encoder=email.encoders.encode_base64)
                    partTmp.add_header("Content-ID", path["desc"])
                    part.attach(partTmp)
        self.msg.attach(part)

    def setAttachments(self, attachs):
        if attachs["attachNum"] != 0:
            for id, path in attachs["attachPath"].items():
                ctype, encoding = mimetypes.guess_type(path["path"])
                with open(path["path"], "rb") as fp:
                    partTmp = MIMEText(fp.read(), "base64", "UTF-8")
                    partTmp.add_header("Content-ID", path["desc"])
                    partTmp.add_header("Content-Type", ctype)
                    partTmp.add_header("Content-Disposition",
                                       "attachment; filename="+path["filename"])

                    self.msg.attach(partTmp)

    def send2file(self, filename):
        with open(filename, "w+") as fd:
            fd.write(self.msg.as_string())

    def setHostinfo(self, sendinfo):
        self.host_smtp = sendinfo["host_smtp"]
        self.host_pop3 = sendinfo["host_pop3"]

        self.port_smtp = sendinfo["port_smtp"]
        self.port_pop3 = sendinfo["port_pop3"]
        self.authMail = sendinfo["authMail"]
        self.authPasswd = sendinfo["authPasswd"]
        self.mailFrom = sendinfo["fromMail"]
        receiver = []
        for i, addr in sendinfo["toMail"].items():
            receiver.append(addr)
        self.mailTo = receiver

    def peekInfo(self):
        print("host_smtp", self.host_smtp)
        print("host_pop3", self.host_pop3)

        print("port_smtp", self.port_smtp)
        print("port_pop3", self.port_pop3)

        print("authMail", self.authMail)
        print("authPasswd", self.authPasswd)
        print("msg:", self.msg.as_string())

    def loadConfigFromJson(self, jsonfile):
        with open(jsonfile, "r") as fd:
            MailConfig = json.load(fd)
        MIMEmail.setBasic(self, MailConfig["basic"])
        MIMEmail.setHostinfo(self, MailConfig["sendinfo"])
        MIMEmail.setContent(self, MailConfig["content"])
        MIMEmail.setAttachments(self, MailConfig["attachment"])

    def sendBySMTP(self):
        smtp = smtplib.SMTP()
        smtp.connect(self.host_smtp, self.port_smtp)
        smtp.login(self.authMail, self.authPasswd)
        smtp.sendmail(self.mailFrom, self.mailTo, self.msg.as_string())
        smtp.quit()
    
    def load_pop3(self,jsonfile):
        with open(jsonfile, "r") as fd:
            PopConfig = json.load(fd)
        self.host_pop3 = PopConfig["host_pop3"]
        self.port_pop3 = PopConfig["port_pop3"]
        self.authMail = PopConfig["authMail"]
        self.authPasswd = PopConfig["authPasswd"]


    def getByPOP3(self):
        pop3server = POP3(self.host_pop3)
        print(pop3server.getwelcome().decode('utf-8'))
        # pop3server.set_debuglevel(1)

        # try:
        #     pop3server.user(self.authMail)
        #     pop3server.pass_(self.authPasswd+"as")
        # except BaseException as e:
        #     print(e)
        #     time.sleep(5)
        # else:
        #     pass

        try:
            pop3server.user(self.authMail)
            pop3server.pass_(self.authPasswd)
        except BaseException as e:
            print(e)
            time.sleep(5)
        else:
            pass

        try:
            print(pop3server.capa())
        except BaseException as e:
            print(e)
        else:
            pass

        # print(pop3server.capa())

        ret = pop3server.stat()
        print("stat:",ret)
        try:
            for i in range(1,ret[0]+2):
                print('Messages: %s. Size: %s' % tuple(re.findall(r"\d+",pop3server.list(i).decode("UTF-8"))))
        except BaseException as e:
            print(e)
        else:
            pass

        print(pop3server.list())

        pop3server.noop()

        time.sleep(3)
        print(pop3server.uidl())

        for i in range(1,ret[0]+1):
            print('Messages:{0[1]} uid: {0[2]}'.format(re.findall(r"^\d+|[0-9a-zA-Z\+]+",pop3server.uidl(i).decode("UTF-8"))))

        try:
            for i in range(1,ret[0]+2):
                response, lines, octets = pop3server.top(i , 10)
                print("response:",response)
                for j in lines:
                    print(j)
        except BaseException as e:
            print(e)
        else:
            pass

        try:
            for i in range(1,ret[0]+3):
                response, lines, octets = pop3server.retr(i)
                print("response:",response)
                for j in lines:
                    print(j)
        except BaseException as e:
            print(e)
        else:
            pass
        


        pop3server.quit()



if __name__ == "__main__":
    oneMail = MIMEmail()

    oneMail.loadConfigFromJson("mails_sina/mail1.json")
    # oneMail.peekInfo()
    # oneMail.send2file("./a.txt")
    oneMail.sendBySMTP()
    # oneMail.getByPOP3()


