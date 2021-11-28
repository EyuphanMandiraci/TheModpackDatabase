from requests import get



def send_email(e):
    get("https://mpdb.xyz/mail.php?e="+e)