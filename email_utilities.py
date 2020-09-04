import smtplib
from typing import Dict

EmailParameters = Dict[str, str]

def generate_text_from_template(template : str
                                 , params_dict : EmailParameters) -> str:
    return template.format(**params_dict)

def generate_email_message(from_user : str
                            , recipient : str
                            , subject : str
                            , body : str
                ) -> str:
    MESSAGE_TEMPLATE = """From: {from_user}\nTo: {recipient}\nSubject: {subject}\nMime-Version: 1.0;
Content-Type: text/html; charset="ISO-8859-1";
Content-Transfer-Encoding: 7bit;
\n
<html>
<body>
{body}
</body>
</html>
 """
    params_dict ={
                'from_user' : from_user
                , 'recipient' : recipient if isinstance(recipient, list) else [recipient]
                , 'subject' : subject
                , 'body' : body
                  }
    return generate_text_from_template(MESSAGE_TEMPLATE
                                       , params_dict)

def open_email_server(from_user : str
                      , pwd : str
                      , address : str = "smtp.gmail.com"
                      , port = 587):
    server = smtplib.SMTP(address
                          , port)
    server.ehlo()
    server.starttls()
    server.login(from_user, pwd)

    return server


def send_email(server
                , from_user
                , recipient
                , subject
                , body):
    recipient = recipient if isinstance(recipient, list) else [recipient]

    # Prepare actual message
    message = generate_email_message(from_user
                            , recipient
                            , subject
                            , body
                )

    success = True
    try:
        server.sendmail(from_user, recipient, message)
        #server.close()
    except:
        success = False

    return success

