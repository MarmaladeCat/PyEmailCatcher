import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import json
import mimetypes
import email.encoders


class MIMEmail:

    def __init__(self):
        self.host = ""
        self.port = None
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

    def setSendinfo(self, sendinfo):
        self.host = sendinfo["host"]
        self.port = sendinfo["port"]
        self.authMail = sendinfo["authMail"]
        self.authPasswd = sendinfo["authPasswd"]

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

    def setSendinfo(self, sendinfo):
        self.host = sendinfo["host"]
        self.port = sendinfo["port"]
        self.authMail = sendinfo["authMail"]
        self.authPasswd = sendinfo["authPasswd"]
        self.mailFrom = sendinfo["fromMail"]
        receiver = []
        for i, addr in sendinfo["toMail"].items():
            receiver.append(addr)
        self.mailTo = receiver


    def peekInfo(self):
        print("host", self.host)
        print("port", self.port)
        print("authMail", self.authMail)
        print("authPasswd", self.authPasswd)
        print("msg:", self.msg.as_string())

    def loadConfigFromJson(self, jsonfile):
        with open(jsonfile, "r") as fd:
            MailConfig = json.load(fd)
        MIMEmail.setBasic(self, MailConfig["basic"])
        MIMEmail.setSendinfo(self, MailConfig["sendinfo"])
        MIMEmail.setContent(self, MailConfig["content"])
        MIMEmail.setAttachments(self, MailConfig["attachment"])

    def sendBySMTP(self):
        smtp = smtplib.SMTP()
        smtp.connect(self.host,self.port)
        smtp.login(self.authMail,self.authPasswd)
        smtp.sendmail(self.mailFrom,self.mailTo,self.msg.as_string())
        smtp.quit()



if __name__ == "__main__":
    with open("mail1.json", "r") as fd:
        MailConfig = json.load(fd)

    
    basic = MailConfig["basic"]
    sendinfo = MailConfig["sendinfo"]
    content = MailConfig["content"]
    attachment = MailConfig["attachment"]

    oneMail = MIMEmail()
    oneMail.loadConfigFromJson("./mail1.json")
    oneMail.peekInfo()
    oneMail.send2file("./a.txt")
    oneMail.sendBySMTP()

    # oneMail = MIMEmail()
    # oneMail.setBasic(basic)
    # oneMail.setContent(content)
    # oneMail.setAttachments(attachment)
    # oneMail.setSendinfo(sendinfo)
    # oneMail.peekInfo()

    

