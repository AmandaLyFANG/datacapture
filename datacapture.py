import csv
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By


def data_capture(commentNum: int) -> list:
    if commentNum < 1:
        return []

    final_page = int(commentNum / 5) + 1 if commentNum % 5 > 0 else int(commentNum / 5)

    comments_csv = []
    comments_json = []
    # create a new Chrome browser instance
    driver = webdriver.Chrome()

    # navigate to the Google home page
    driver.get("https://www.tripadvisor.com.au/Airline_Review-d8729133-Reviews-Qantas#REVIEWS")

    page = 0
    index = 0
    while page < final_page:
        page += 1
        print("Page:", page)

        # wait for the page to load
        time.sleep(3)

        # find the search box element by name
        search_box = driver.find_elements(By.CLASS_NAME, "WAllg._T")

        # click read more button
        read_more_button = search_box[0].find_element(By.CLASS_NAME, "TnInx")
        if read_more_button:
            read_more_button.click()
            WebDriverWait(driver, 10)

        for element in search_box:
            # current comment
            index += 1

            if commentNum < index:
                break

            # element.find_element(By.CLASS_NAME, "Hlmiy.F1").find_element(By.TAG_NAME,"span").get_attribute("class")
            # 1.	Rating
            rating = \
                element.find_element(By.CLASS_NAME, "Hlmiy.F1").find_element(By.TAG_NAME, "span").get_attribute(
                    "class")[-2]

            # 2.	Review title
            review_title = element.find_element(By.CLASS_NAME, "KgQgP.MC._S.b.S6.H5._a").find_element(By.TAG_NAME,
                                                                                                      "span").text
            # 3.	Review content
            review_content = element.find_element(By.CLASS_NAME, "QewHA.H4._a").find_element(By.TAG_NAME, "span").text

            # 4.    Date of travel -- exist non value
            data_of_travel = ""
            if element.find_elements(By.CLASS_NAME, "teHYY._R.Me.S4.H3"):
                data_of_travel = element.find_element(By.CLASS_NAME, "teHYY._R.Me.S4.H3").text.replace("Date of travel: ", "")

            # 5.	Ratings of individual criteria (Bonus)
            individual_criteria_dict = {
                "Legroom": "",
                "Seat comfort": "",
                "In-flight Entertainment": "",
                "Customer service": "",
                "Value for money": "",
                "Cleanliness": "",
                "Check-in and boarding": "",
                "Food and Beverage": ""
            }

            outer_div = element.find_elements(By.CLASS_NAME, "ZzICe.Me.f")
            if outer_div and outer_div[0].find_elements(By.CLASS_NAME, "hemdC.S2.H2"):
                indi_cri_divs = outer_div[0].find_elements(By.CLASS_NAME, "hemdC.S2.H2")
                for indi_div in indi_cri_divs:
                    item_name = indi_div.text
                    item_value = \
                        indi_div.find_element(By.CLASS_NAME, "Nd").find_element(By.TAG_NAME, "span").get_attribute(
                            "class")[
                            -2]
                    individual_criteria_dict[item_name] = item_value

            cmt_json = {"Ratting": rating, "Review title": review_title, "Review content": review_content,
                        "Date of travel": data_of_travel, "Ratings of individual criteria": individual_criteria_dict}
            comments_json.append(cmt_json)

            cmt_csv = {"Ratting": rating, "Review title": review_title, "Review content": review_content,
                       "Date of travel": data_of_travel,
                       "Legroom": individual_criteria_dict.get("Legroom"),
                       "Seat comfort": individual_criteria_dict.get("Seat comfort"),
                       "In-flight Entertainment": individual_criteria_dict.get("In-flight Entertainment"),
                       "Customer service": individual_criteria_dict.get("Customer service"),
                       "Value for money": individual_criteria_dict.get("Value for money"),
                       "Cleanliness": individual_criteria_dict.get("Cleanliness"),
                       "Check-in and boarding": individual_criteria_dict.get("Check-in and boarding"),
                       "Food and Beverage": individual_criteria_dict.get("Food and Beverage")
                       }
            comments_csv.append(cmt_csv)
            # print("=============================", index, "====================================")
            # print("Ratting:", rating)
            # print("Review title:", review_title)
            # print("Review content:", review_content)
            # print("Date of travel:", data_of_travel)
            # print("individual criteria", individual_criteria_dict)
            # print()

        pageNumbers = driver.find_element(By.CLASS_NAME, "pageNumbers").find_elements(By.XPATH, './/*')
        for i in range(0, len(pageNumbers)):
            if pageNumbers[i].get_attribute("class") == "pageNum current disabled":
                pageNumbers[i + 1].click()
                break

    return {"comments_json": comments_json, "comments_csv": comments_csv}


def write_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


# Use the function to write the data to a CSV file

def write_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)


cmt_dict = data_capture(1000)

write_to_csv(cmt_dict.get("comments_csv"), 'reviews.csv')

write_to_json(cmt_dict.get("comments_json"), 'reviews.json')
