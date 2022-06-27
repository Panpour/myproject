from time import sleep

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Google:

    # Locators

    # Google account login locators
    LOG_IN_VIA_GOOGLE_BUTTON_LINK_TEXT = "Google"
    GOOGLE_EMAIL_INPUT_XPATH = "//input[@type='email']"
    GOOGLE_EMAIL_NEXT_BUTTON_DIV_ID = "identifierNext"
    GOOGLE_PASSWORD_INPUT_XPATH = "//input[@type='password']"
    GOOGLE_PASSWORD_NEXT_BUTTON_DIV_ID = "passwordNext"
    PRIMARY_TAB_CSS_SELECTOR = "div[aria-label=Primary]"
    PRIMARY_TAB_NUMBER_OF_EMAILS_SECTION_XPATH = "((//div[contains(@id, ':4r')]//span[@class='Dj'])[1]" \
                                                 "//span[@class='ts'])[3]"
    EMAIL_SENDER_NAME_CSS_SELECTOR = ".yX"
    EMAIL_SUBJECT_CSS_SELECTOR = ".zA .a4W"
    OLDER_ARROW_BUTTON = "div[aria-label=Older]"
    NEWER_ARROW_BUTTON = "div[aria-label=Newer]"
    LOADING_LABEL_CSS_SELECTOR = ".vX"

    def __init__(self, driver):
        self.driver = driver
        self.explicit_wait = 10

    def login(self, email, password):
        # Enter email
        self.enter_email(email)
        # Enter password
        self.enter_password(password)
        # Click "next" button
        self.click_login_button()

    def enter_email(self, email):
        element = (By.XPATH, self.GOOGLE_EMAIL_INPUT_XPATH)
        email_input = WebDriverWait(self.driver, self.explicit_wait).until(EC.visibility_of_element_located(element))
        email_input.send_keys(email)
        element = (By.ID, self.GOOGLE_EMAIL_NEXT_BUTTON_DIV_ID)
        next_button = WebDriverWait(self.driver, self.explicit_wait).until(EC.visibility_of_element_located(element))
        next_button.click()

    def enter_password(self, password):
        element = (By.XPATH, self.GOOGLE_PASSWORD_INPUT_XPATH)
        password_input = WebDriverWait(self.driver, self.explicit_wait).until(EC.visibility_of_element_located(element))
        password_input.click()
        password_input.send_keys(password)

    def click_login_button(self):
        element = (By.ID, self.GOOGLE_PASSWORD_NEXT_BUTTON_DIV_ID)
        next_button = WebDriverWait(self.driver, self.explicit_wait).until(EC.visibility_of_element_located(element))
        next_button.click()

    def primary_tab_is_selected(self):
        element = (By.CSS_SELECTOR, self.PRIMARY_TAB_CSS_SELECTOR)
        primary_tab = WebDriverWait(self.driver, self.explicit_wait).until(EC.visibility_of_element_located(element))
        aria_selected_attribute = primary_tab.get_attribute("aria-selected")
        return aria_selected_attribute == "true"

    def click_primary_tab(self):
        element = (By.CSS_SELECTOR, self.PRIMARY_TAB_CSS_SELECTOR)
        primary_tab = WebDriverWait(self.driver, self.explicit_wait).until(EC.visibility_of_element_located(element))
        primary_tab.click()

    def get_total_number_of_emails_in_primary_tab(self):
        element = (By.XPATH, self.PRIMARY_TAB_NUMBER_OF_EMAILS_SECTION_XPATH)
        total_number_of_emails_section = WebDriverWait(self.driver, self.explicit_wait)\
            .until(EC.visibility_of_element_located(element))
        return int(total_number_of_emails_section.text)

    def get_email_sender_names(self):
        element = (By.CSS_SELECTOR, self.EMAIL_SENDER_NAME_CSS_SELECTOR)
        names = WebDriverWait(self.driver, self.explicit_wait).until(EC.presence_of_all_elements_located(element))
        return names

    def get_email_subjects(self):
        element = (By.CSS_SELECTOR, self.EMAIL_SUBJECT_CSS_SELECTOR)
        subjects = WebDriverWait(self.driver, self.explicit_wait).until(EC.presence_of_all_elements_located(element))
        return subjects

    def get_sender_name_and_subject_of_nth_email(self, email_index):
        # Page related email index
        page_related_email_index = email_index % 50
        # If needed go to older pages
        times_to_move_to_older_page = int(email_index/50)
        for _ in range(times_to_move_to_older_page - 1):
            self.click_older_page_arrow_button()
        # Get sender names and subjects lists
        email_sender_names = self.get_email_sender_names()
        email_subjects = self.get_email_subjects()
        # Set desired email information
        email_obj = {
            "sender_name": email_sender_names[page_related_email_index].text,
            "subject": email_subjects[page_related_email_index].text
        }
        return email_obj

    def get_sender_name_and_subject_of_all_emails(self):
        total_emails_info = []
        # If needed go to older pages
        times_to_move_to_older_page = int(self.get_total_number_of_emails_in_primary_tab() / 50)
        while times_to_move_to_older_page >= 0:
            times_to_move_to_older_page -= 1
            # Get sender names and subjects lists
            email_sender_names = self.get_email_sender_names()
            email_subjects = self.get_email_subjects()
            for i in range(len(email_sender_names)):
                total_emails_info.append({
                    "sender_name": email_sender_names[i].text,
                    "subject": email_subjects[i].text
                })

            # Go to next page
            self.click_older_page_arrow_button()

        return total_emails_info

    def click_older_page_arrow_button(self):
        element = (By.CSS_SELECTOR, self.OLDER_ARROW_BUTTON)
        older_button = WebDriverWait(self.driver, self.explicit_wait).until(EC.visibility_of_element_located(element))
        older_button.click()
        self.wait_primary_tab_page_to_change()

    def click_newer_page_arrow_button(self):
        element = (By.CSS_SELECTOR, self.NEWER_ARROW_BUTTON)
        newer_button = WebDriverWait(self.driver, self.explicit_wait).until(EC.visibility_of_element_located(element))
        newer_button.click()
        self.wait_primary_tab_page_to_change()

    def wait_primary_tab_page_to_change(self):
        times = 5
        while times > 0:
            times -= 1
            if not self.loading_label_is_visible():
                break
            else:
                sleep(0.5)
        sleep(1)

    def loading_label_is_visible(self):
        try:
            element = (By.CSS_SELECTOR, self.LOADING_LABEL_CSS_SELECTOR)
            loading_label = WebDriverWait(self.driver, self.explicit_wait)\
                .until(EC.presence_of_element_located(element))
            style_attr = loading_label.get_attribute("style")
            return not style_attr.__contains__("display: none;")
        except:
            return False
