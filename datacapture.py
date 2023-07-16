from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# create a new Chrome browser instance
driver = webdriver.Chrome()

# navigate to the Google home page
driver.get("https://www.tripadvisor.com.au/Airline_Review-d8729133-Reviews-Qantas#REVIEWS")

# find the search box element by name
search_box = driver.find_elements(By.CLASS_NAME, "WAllg._T")

for element in search_box:
    # print(element.text)

    # click all read more button
    read_more_button = search_box[0].find_element(By.CLASS_NAME, "TnInx")
    if read_more_button:
        read_more_button.click()

    # set up a wait object with a timeout
    wait = WebDriverWait(driver, 10)

    #element.find_element(By.CLASS_NAME, "Hlmiy.F1").find_element(By.TAG_NAME,"span").get_attribute("class")
    # 1.	Rating
    #rating = element.find_element(By.XPATH, "//div[@data-test-target='review-rating']").find_element(By.TAG_NAME, "span").get_attribute("class")
    rating = element.find_element(By.CLASS_NAME, "Hlmiy.F1").find_element(By.TAG_NAME,"span").get_attribute("class")
    # 2.	Review title
    #review_title = element.find_element(By.XPATH, "//div[@data-test-target='review-title']").find_element(By.TAG_NAME, "span").text
    review_title = element.find_element(By.CLASS_NAME, "KgQgP.MC._S.b.S6.H5._a").find_element(By.TAG_NAME, "span").text
    # 3.	Review content
    review_content = element.find_element(By.CLASS_NAME, "QewHA.H4._a").find_element(By.TAG_NAME, "span").text

    # 4.    Date of travel
    data_of_travel = element.find_element(By.CLASS_NAME, "teHYY._R.Me.S4.H3").text

    # 5.	Ratings of individual criteria (Bonus)

    print("Ratting:", rating)
    print("Review title:", review_title)
    print("Review content:", review_content)
    print("Date of travel:", data_of_travel)
    print()

# type in a search term and submit the form
# search_box.send_keys("OpenAI" + Keys.RETURN)

#search_box.send_keys('ChromeDriver')

#search_box.submit()

driver.quit()

#https://blog.csdn.net/pcylzl1127/article/details/123952585?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522168940628616800225516334%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=168940628616800225516334&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-123952585-null-null.142^v88^control_2,239^v2^insert_chatgpt&utm_term=selenium.common.exceptions.NoSuchElementException%3A%20Message%3A%20no%20such%20element%3A%20Unable%20to%20locate%20element%3A%20&spm=1018.2226.3001.4187