1. 163邮箱的要求更为严格

2. 需要用MIMEMultipart

3. toMail不可以直接用list

4. msg中需要有subject、to、from等，否则  （163mail：）SMTPDataError：554 b'DT:SPM

5. 163邮箱对图片有奇怪的cid，不按照cid要求的为  SMTPDataError：554, b'DT:SPM

6. 邮箱需要开启SMTP服务，并获取授权码作为authPasswd

