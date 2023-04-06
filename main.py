import datetime
import email.message
import imaplib
import smtplib

from win10toast import ToastNotifier


def main():
    # Create a list of days on which you want to run the app
    days_to_run = [2]  # Sunday = 0, Monday = 1, Tuesday = 2, etc.

    # Get the current day of the week (0 = Sunday, 1 = Monday, etc.)
    today = datetime.datetime.today().weekday()

    # Set the email account credentials
    username = "email"
    password = "passowrd"

    # Set the email search criteria
    sender = "jobs.uk@cloudworkers.company"
    subject = "Cloudworkers Company- Your Application"

    # Set the notification parameters
    to_address = "k.nwoye@yahoo.com"
    from_address = "knwy@ymail.com"
    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587

    # Connect to the email account
    imap_server = "imap.mail.yahoo.com"
    imap_port = 993

    if today in days_to_run:
        toaster = ToastNotifier()
        with imaplib.IMAP4_SSL(imap_server, imap_port) as imap:
            print("Logging in to email account...")
            imap.login(username, password)
            imap.select("INBOX")

            # Search for emails matching the search criteria
            print("Searching for matching emails...")
            search_query = f'(FROM "{sender}" SUBJECT "{subject}")'
            result, data = imap.search(None, search_query)
            email_ids = data[0].split()

            # Send a notification if matching emails are found
            """if email_ids:
                print(f"{len(email_ids)} matching emails found.")
                message = email.message.Message()
                message["To"] = to_address
                message["From"] = from_address
                message["Subject"] = "Matching emails found"
                body = "The following emails match the search criteria:\n\n"
                for email_id in email_ids:
                    _, data = imap.fetch(email_id, "(RFC822)")
                    email_message = email.message_from_bytes(data[0][1])
                    body += f"From : {email_message['From']}\n"
                    body += f"Subject: {email_message['Subject']}\n\n"
                message.set_payload(body)
    
                with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                    print("Connecting to SMTP server...")
                    smtp.starttls()
                    smtp.login(username, password)
                    smtp.sendmail(from_address, to_address, message.as_string())
                    print("Notification sent.")
            else:
                print("No matching emails found")"""

            # Print the details of the matching emails
            if email_ids:
                print(f"{len(email_ids)} matching emails found.")
                for email_id in email_ids:
                    _, data = imap.fetch(email_id, "(RFC822)")
                    email_message = email.message_from_bytes(data[0][1])
                    print("From:", email_message["From"])
                    print("Subject:", email_message["Subject"])
                    print("Date:", email_message["Date"])
                    print("Body:", email_message.get_payload(decode=True))
                    print()

                    # show a Windows toast notification
                    toaster.show_toast("New email from the specified sender and subject",
                                       f"Sender: {email_message['From']}\nSubject: {email_message['Subject']}")


if __name__ == "__main__":
    main()
