import smtplib

from config import config


def send_email(to_addr, subject, body_text):
    host = config['email']['host']
    port = config['email']['port']

    login = config['email']['login']
    password = config['email']['password']

    from_addr = config['email']['login']

    BODY = "\r\n".join((
        "From: %s" % from_addr,
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "",
        body_text
    ))

    server = smtplib.SMTP_SSL(host, port)
    server.login(login, password)
    server.sendmail(from_addr, [to_addr], BODY)
    server.quit()
