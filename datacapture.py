import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# create a new Chrome browser instance
driver = webdriver.Chrome()

# navigate to the Google home page
driver.get("https://www.tripadvisor.com.au/Airline_Review-d8729133-Reviews-Qantas#REVIEWS")

page = 0
index = 0
while page < 3:
    page += 1
    time.sleep(5)

    # find the search box element by name
    search_box = driver.find_elements(By.CLASS_NAME, "WAllg._T")

    # click read more button
    read_more_button = search_box[0].find_element(By.CLASS_NAME, "TnInx")
    if read_more_button:
        read_more_button.click()
        wait = WebDriverWait(driver, 10)

    for element in search_box:
        # element.find_element(By.CLASS_NAME, "Hlmiy.F1").find_element(By.TAG_NAME,"span").get_attribute("class")
        # 1.	Rating
        rating = \
        element.find_element(By.CLASS_NAME, "Hlmiy.F1").find_element(By.TAG_NAME, "span").get_attribute("class")[-2]

        # 2.	Review title
        review_title = element.find_element(By.CLASS_NAME, "KgQgP.MC._S.b.S6.H5._a").find_element(By.TAG_NAME,
                                                                                                  "span").text
        # 3.	Review content
        review_content = element.find_element(By.CLASS_NAME, "QewHA.H4._a").find_element(By.TAG_NAME, "span").text

        # 4.    Date of travel
        data_of_travel = element.find_element(By.CLASS_NAME, "teHYY._R.Me.S4.H3").text

        # 5.	Ratings of individual criteria (Bonus)
        individual_criteria_dict = {}

        index += 1
        print("=============================", index, "====================================")
        print("Ratting:", rating)
        print("Review title:", review_title)
        print("Review content:", review_content)
        print("Date of travel:", data_of_travel)

        try:
            individual_criteria = element.find_element(By.CLASS_NAME, "ZzICe.Me.f").find_elements(By.CLASS_NAME, "Nd")
            if individual_criteria:
                individual_criteria_dict = {
                    "Legroom": individual_criteria[0].find_element(By.TAG_NAME, "span").get_attribute("class")[-2],
                    "Seat_comfort": individual_criteria[1].find_element(By.TAG_NAME, "span").get_attribute("class")[-2],
                    "In_flight_Entertainment":
                        individual_criteria[2].find_element(By.TAG_NAME, "span").get_attribute("class")[-2],
                    "Customer_service": individual_criteria[3].find_element(By.TAG_NAME, "span").get_attribute("class")[
                        -2],
                    "Value_for_money": individual_criteria[4].find_element(By.TAG_NAME, "span").get_attribute("class")[
                        -2],
                    "Cleanliness": individual_criteria[5].find_element(By.TAG_NAME, "span").get_attribute("class")[-2],
                    "Check_in_and_boarding":
                        individual_criteria[6].find_element(By.TAG_NAME, "span").get_attribute("class")[-2],
                    "Food_and_Beverage":
                        individual_criteria[7].find_element(By.TAG_NAME, "span").get_attribute("class")[-2]
                }
        except NoSuchElementException:
            continue

        print("individual criteria", individual_criteria_dict)
        print()

    pageNumbers = driver.find_element(By.CLASS_NAME, "pageNumbers").find_elements(By.XPATH, './/*')
    for i in range(0, len(pageNumbers)):
        if pageNumbers[i].get_attribute("class") == "pageNum current disabled":
            pageNumbers[i + 1].click()
            break

# type in a search term and submit the form
# search_box.send_keys("OpenAI" + Keys.RETURN)

# search_box.send_keys('ChromeDriver')

search_box.clear()

driver.quit()
