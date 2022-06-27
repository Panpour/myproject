from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from google import Google


# Get latest version of Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.implicitly_wait = 15

# Set url
url = "https://www.gmail.com"

try:
    # Open browser
    driver.get(url)

    # Create google object
    google = Google(driver)

    # Login
    google.login("ppourgias@gmail.com", "panpour13")

    try:
        # Check primary tab whether is selected
        assert google.primary_tab_is_selected(), "Primary tab is not selected"
        print("Primary tab is selected\n")
        print("\n-----------------------------------------\n\n")
    except:
        # If not, select primary tab
        google.click_primary_tab()

    # Get total emails in primary tab
    print("Total number of emails in primary tab: ", google.get_total_number_of_emails_in_primary_tab(), "\n")
    print("\n-----------------------------------------\n\n")

    # Get sender name and subject of nth email
    email_index = 5
    email_info = google.get_sender_name_and_subject_of_nth_email(email_index)
    print("5th email's sender name: ", email_info["sender_name"])
    print("5th email's subject: ", email_info["subject"], "\n")
    print("\n-----------------------------------------\n\n")

    # Get sender name and subject of all email in inbox
    emails_info = google.get_sender_name_and_subject_of_all_emails()
    for index, email_info in enumerate(emails_info):
        print(str(index + 1) + "th email info: \n")
        print("Sender name: ", email_info["sender_name"] + "\n")
        print("Subject: ", email_info["subject"] + "\n\n")
finally:
    driver.quit()




