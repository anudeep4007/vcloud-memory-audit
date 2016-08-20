A python sceript to ausdit memory usage in vCloud Director organizations. The script would check all the deployed vApps
in an organizations and report vApp having ram allocated above a defined limit.

The script assumes that you use AD for vCloud authetication. The AD details are required to fetch user details
while reporting.

Configuration Instructions
===========================
This is work in progreess. I plan to simplify configuration steps in subsequent versions.

mailerlist.py:

    Modify the foloiwng variables

        MAIL_SERVER = 'example@example.com'
        SENDER_EMAIL = 'example@example.com'

    Note: Things might need additional configuration dpending on your mail server configuration. More details here
    http://naelshiab.com/tutorial-send-email-python/

list_ad_objects.py:

    Change the following lines to add your AD sercer

        pyad.set_defaults(ldap_server="ad_server", username="username",password="password"

config.json:

    This is where you enter your org details. Multiple orgs can be listed in json format
