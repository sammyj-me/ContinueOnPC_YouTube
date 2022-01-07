import email
import imaplib
import webbrowser
import re
import time
import urllib.request

from plyer import notification

def words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())

def application():
    #credentials
    username ="YOUR EMAIL HERE@gmail.com"        # Enter your Email username here!!!

    #generated app password
    app_password= "YOUR PASSWORD"                      # Enter Your Email password here!!!

    # Phone number
    phone_number = "1YOUR PHONE NUMBER"                   # Enter your Phone number here!!! 1(XXX)-(XXXX) No spaces or parenthesis.

    # Gmail API Hosting: https://www.systoolsgroup.com/imap/
    gmail_host= 'imap.gmail.com'

    #set connection
    mail = imaplib.IMAP4_SSL(gmail_host, 993)

    #login
    mail.login(username, app_password)

    #select inbox
    mail.select("INBOX")

    # count unread emails
    return_code, data = mail.search(None, 'UnSeen')
    mail_ids = data[0].decode()
    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    #select specific mails
    _, selected_mails = mail.search(None, '(FROM "+'+phone_number+'@mailmymobile.net ")', 'unseen')  # You may have to change this code to match the email address of your phone number 

    #total number of mails from specific user
    print("Total Unseen Messages from "+ phone_number, len(selected_mails[0].split()))

    for num in selected_mails[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        _, bytes_data = data[0]

        #convert the byte data to message
        email_message = email.message_from_bytes(bytes_data)
        print("\n===========================================")

        #access data
        print("Subject: ",email_message["subject"])
        print("To:", email_message["to"])
        print("From: ",email_message["from"])
        print("Date: ",email_message["date"])
        for part in email_message.walk():
            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                message = part.get_payload(decode=True)
                print("Message: \n", message.decode())
                print("==========================================\n")
                
                link_pattern = re.compile(r'(?P<url>https?://[^\s]+)')
                search = link_pattern.search(message.decode())

                link_pattern = re.compile(r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?')
                search2 = link_pattern.search(message.decode())

                if search is not None:
                    if search2 is not None: # Checks if it's a YouTube Link
                        title = 'YouTube Link received!'
                        message = search2.group(0)
                        notification.notify(title = title,
                                            message = message,
                                            app_icon = None,
                                            timeout = 4,
                                            toast = False)
                        
                        print("Link found! -> " + search2.group(0))

                        # url of the video
                        url = search2.group(0).replace('https://youtu.be/', '')
                        
                # *** OPEN IFRAME IN BROWSER ***
            
                        new_url = 'https://www.youtube.com/embed/'+url+'?autoplay=1'    # Add autoplay notation at the end of the URL.
                                                                                        # Make sure to change settings in your web browser to allow autoplay as well.
                        print(new_url) # Print the URL to the shell for confirmation.

                        index = open("web_iframe_youtube.html").read().format(video_url=new_url) # opens the HTML Document as a long string. Looks for the {video_url} tag.
                                                                                                 # Sets the {video_url} tag to the new URL as read from the email.
                        print(index)  #print new hyper-text-markup as confirmation.

                        file = open("web_iframe_youtube.html","w")      # Open the html file that hosts the video
                        file.write(index)                               # Write the new text (with the new video URL) to the web page.
                        file.close()

                        webbrowser.open("web_iframe_youtube.html", new = 0) # Open the video web page in a new browser tab

                        time.sleep(10)  # wait 10 seconds for web page to load. If the video URL variable resets (see following) before the page loads, the video will not play.

                        # Reset the video URL variable within the html file that hosts the video
                        html_str = """<!DOCTYPE html>
                        <html>
                                <body>
                                        <center>
                                        <iframe width="1280" height="720" src="{video_url}">
                                        </iframe>
                                        </center>

                                </body>
                        </html> """

                        # Open and write the new text
                        file = open("web_iframe_youtube.html","w")
                        file.write(html_str)
                        file.close()

                        # Shell Confirmation
                        print("html file has been reset")
                        
                    else:
                        title = 'Web Link received!'
                        message = search.group(0)
                        notification.notify(title = title,
                                            message = message,
                                            app_icon = None,
                                            timeout = 4,
                                            toast = False)
                        print("Link found! -> " + search.group(0))
                        webbrowser.open(search.group(0))
                    
                else:
                    print("No web links were found.")                

                break
            
while 1:
    application()
    time.sleep(10)
