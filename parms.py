import os
import urllib.request
import smtplib

try:
    url = 'https://acfdata.coworks.be/cancerdrugsdb.txt'
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    text = data.decode('utf-8')  # a `str`; this step can vary depending on how the file is encoded

    # save to vscode files (for git)
    save_dir = os.path.join("C:", os.sep, "Users", "ayelet_tohar", "Documents", "GitHub",
                            "Towards-personalized-medicine-in-cancer", "backend", "src", "common")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open(os.path.join(save_dir, 'cancerdrugsdb.txt'), 'w') as f:
        f.write(text)

    print("VS code updated, starting to update server")
    # save to server files
    save_dir = os.path.join("C:", os.sep, "inetpub", "wwwroot", "Flask_IIS", "src", "common")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open(os.path.join(save_dir, 'cancerdrugsdb.txt'), 'w') as f:
        f.write(text)
    print("Server is update. Done")

except Exception as e:
    print(e)
    # Set the email details
    to = "avivelded@gmail.com"
    sender = "avivelded@gmail.com"
    subject = "DB update failed"
    body = "Please check the code and find what you did wrong"

    # Set the SMTP server and port
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Connect to the server and send the email
    server.connect("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("avivelded@gmail.com", "gdrozsakgcjzonef")

    # Construct the email message
    msg = f"Subject: {subject}\n\n{body}"

    # Send the email
    server.sendmail(sender, to, msg)

    # Disconnect from the server
    server.quit()
