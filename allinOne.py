import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import json



def sendmail(configPath):
    with open(configPath, "r") as f:
        MailConfig = json.load(f)

    # print(len(MailConfig))

    basic = MailConfig["basic"]
    content = MailConfig["content"]
    image = MailConfig["image"]
    attachment = MailConfig["attachment"]

    # 邮件头
    msg = MIMEMultipart('alternative')


    msg["From"] = Header(basic["fromMail"])
    receiver = []
    for i, addr in basic["toMail"].items():
        receiver.append(addr)
    msg["To"] = Header(','.join(receiver))
    msg['Subject'] = Header(basic["subject"], "UTF-8")
    copy = []
    for i, addr in basic["Cc"].items():
        copy.append(addr)
    msg["Cc"] = Header(','.join(copy))
    msg["X-Priority"] = "3"
    
    # print infos
    # print("From:",msg["From"])
    # print("To:",msg["To"])
    # print("Subject:",msg["Subject"])
    # print("Cc:",msg["Cc"])

    # 正文内容
    # for i in range(content["contentNum"]):
    for id, part in content["contentPart"].items():
        with open(part["path"], "r") as f:
            partContent = MIMEText(f.read(), part["contentType"])
            # msg.set_payload
            msg.attach(partContent)

    # 添加图片
    if image["imageNum"]!=0:
        for id, path in image["imagePath"].items():
            with open(path["path"], "rb") as img:
                imageContent = MIMEImage(img.read())
                imageContent.add_header('Content-ID', path["desc"])
                msg.attach(imageContent)

    # 添加附件
    if attachment["attachNum"]!=0:
        for id, path in attachment["attachPath"].items():
            with open(path["path"], "rb") as attach:
                # print('attachment; filename="%s"' % path["desc"])
                attachContent = MIMEText(attach.read(), 'base64', 'utf-8')
                attachContent["Content-Type"] = 'application/octet-stream'
                attachContent["Content-Disposition"] = 'attachment; filename="%s"' % path["desc"]
                msg.attach(attachContent)


    # 发送模块
    smtp = smtplib.SMTP()
    smtp.connect(basic["host"],basic["port"])
    smtp.login(basic["authMail"], basic["authPasswd"])
    smtp.sendmail(basic["fromMail"], receiver, msg.as_string())
    smtp.quit()
    # print("send email OK! (config in %s)" % configPath)

if __name__ == "__main__":
    sendmail("./mails/mail1.json")