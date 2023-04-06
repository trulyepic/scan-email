import EmailNotifier


def main():
    email_notifier = EmailNotifier.EmailNotifier(
        days_to_run=[0, 1, 2, 3, 4],
        username="email",
        password="password",
        sender="jobs.uk@cloudworkers.company",
        subject="Cloudworkers Company- Your Application",
        imap_port=993,
        imap_server="imap.mail.yahoo.com"
    )

    email_notifier.connect_to_email()
    # Set the properties of the EmailNotifier class using the setters
    # email_notifier.search_both_email_and_sender()

    email_notifier.get_email_or_sender_notif(sender="bestbuyinfo@emailinfo.bestbuy.com")


if __name__ == "__main__":
    main()
