import datetime
import email
import imaplib

from win10toast import ToastNotifier


def print_email_details(email_message):
    print("From:", email_message["From"])
    print("Subject:", email_message["Subject"])
    print("Date:", email_message["Date"])
    print("Body:", email_message.get_payload(decode=True))
    print()


class EmailNotifier:
    def __init__(self, days_to_run, username, password, sender, subject, imap_server, imap_port):
        self.imap = None
        self.days_to_run = days_to_run
        self.username = username
        self.password = password
        self.sender = sender
        self.subject = subject
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.toaster = ToastNotifier()

    def connect_to_email(self):
        # Connect to the email account
        self.imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        print("Logging in to email account...")
        self.imap.login(self.username, self.password)
        self.imap.select("INBOX")

    def search_both_email_and_sender(self):
        today = datetime.datetime.today().weekday()
        if today not in self.days_to_run:
            return

            # Search for emails matching the search criteria
        print("Search for matching emails...")
        search_query = f'(FROM "{self.sender}" SUBJECT "{self.subject}")'
        result, data = self.imap.search(None, search_query)
        email_ids = data[0].split()

        # Print the details of the matching emails
        if email_ids:
            print(f"{len(email_ids)} matching emails found.")
            for email_id in email_ids:
                _, data = self.imap.fetch(email_id, "(RFC822)")
                email_message = email.message_from_bytes(data[0][1])
                print_email_details(email_message)

                # show a Windows toast notification
                self.toaster.show_toast("New email from the specified sender and subject",
                                        f"Sender: {email_message['From']}\nSubject: {email_message['Subject']}")

        else:
            print("No values found")

    def search_email_or_sender(self, sender=None, subject=None):
        # Search for emails matching the search criteria
        search_query = "All"
        if sender is not None:
            search_query = f'(FROM "{sender}")'
        elif subject is not None:
            search_query = f'(SUBJECT "{subject}")'
        print(f"Searching for matching emails with query: {search_query}")
        result, data = self.imap.search(None, search_query)
        email_ids = data[0].split()

        # Return a list of matching email messages
        message = []
        for email_id in email_ids:
            _, data = self.imap.fetch(email_id, "(RFC822)")
            email_message = email.message_from_bytes(data[0][1])
            message.append(email_message)
        return message

    def get_email_or_sender_notif(self, sender=None, subject=None):
        # Get the current day of the week (0 = Sunday, 1 = Monday, etc.)
        today = datetime.datetime.today().weekday()

        if today in self.days_to_run:
            # call search email function
            matching_emails = self.search_email_or_sender(sender=sender, subject=subject)
            if matching_emails:
                print(f"{len(matching_emails)} matching emails found.")
                # Print the details of the matching emails
                for email_message in matching_emails:
                    print_email_details(email_message)

                    # show a Windows toast notification
                    self.toaster.show_toast("New email from the specified sender and subject",
                                            f"Sender: {email_message['From']}\nSubject: {email_message['Subject']}")

    def set_days_to_run(self, days_to_run):
        self.days_to_run = days_to_run

    def set_email_account_credentials(self, username, password):
        self.username = username
        self.password = password
