import os
import time
from datetime import datetime
from exchangelib import DELEGATE, Account, ServiceAccount, Configuration, NTLM
from plyer import notification
from dotenv import load_dotenv
import pygame

# load credentials
load_dotenv(".credentials")

password = os.environ.get("EXCHANGE_PASSWORD")
username = os.environ.get("EXCHANGE_USERNAME")
outgoing_email_address = os.environ.get("EXCHANGE_OUTGOING_ADDRESS")
soundfile = os.environ.get("NOTIFICATION_SOUND")
exchange_server = os.environ.get("EXCHANGE_SERVER")

if soundfile != "":
    # load a sound file
    pygame.mixer.init()
    print("Loading soundfile", soundfile)
    pygame.mixer.music.load(soundfile)  # can be any other format
else:
    print("Skipping loading of soundfile")

print("Initiating connection to exchange...")
# If you want to enable the fault tolerance, create credentials as a service account instead:
credentials = ServiceAccount(username=username, password=password)

# Set up a target account and do an autodiscover lookup to find the target EWS endpoint:
account = Account(primary_smtp_address=outgoing_email_address, credentials=credentials,
                  autodiscover=True, access_type=DELEGATE)

config = Configuration(server=exchange_server, credentials=credentials, auth_type=NTLM)

last_number_of_emails = account.inbox.unread_count

print("Waiting for emails... Press CTRL+C to stop")

try:
    while True:
        # Update the counters
        account.inbox.refresh()
        cur_number_of_emails = account.inbox.unread_count

        if cur_number_of_emails > last_number_of_emails:
            # we got a new mail, get the last view messages
            diff = cur_number_of_emails - last_number_of_emails
            bodytext = ""
            for item in account.inbox.all().order_by('-datetime_received')[:diff]:
                bodytext += "{folder}: {name} ({email}): {subject}\n".format(
                    name=item.author.name, email=item.author.email_address, subject=item.subject, folder=item.folder.name
                )

            print("{dt}: {n} new emails".format(dt=datetime.now(), n=diff))

            # play a sound
            if soundfile != "":
                pygame.mixer.music.play()
            # show notification
            notification.notify(title="{n} new emails".format(n=diff), message=bodytext)

        last_number_of_emails = cur_number_of_emails
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping.")
