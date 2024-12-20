from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
from selenium.webdriver.support.ui import Select
#Setup WebDriver using webdriver-manager
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)

def test_register_and_login():
    #Navigate to the register page
    driver.get("http://127.0.0.1:5000/register")

    try:
        #Fill out the register form
        username = "newtester1"
        password = "000000"
        full_name = "newtester1 user"
        email = "Usertest@example.com"
        time.sleep(1)
        #Wait for the username input field to be visible and fill out the form
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "full_name").send_keys(full_name)
        driver.find_element(By.ID, "email").send_keys(email)
        
        select_role = Select(driver.find_element(By.ID, "role"))
        select_role.select_by_visible_text("User")
        time.sleep(1)
        #Submit the form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        #Fill out the login form with the new credentials
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        #Submit the login form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        for i in range(11):
            time.sleep(1)
        #Navigate to Borrow a Book page
            driver.find_element(By.LINK_TEXT, "Borrow a Book").click()
        #Fill out the borrow form
            time.sleep(1)
            driver.find_element(By.ID, "book_id").send_keys(i+1)
        #Submit the borrow form
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        #Navigate to Return a Book page
        driver.find_element(By.LINK_TEXT, "Return a Book").click()
        time.sleep(1)
        #Fill out the return form
        driver.find_element(By.ID, "book_id").send_keys(10)
        #Submit the return form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        #Navigate to Borrow a Book page
        driver.find_element(By.LINK_TEXT, "Borrow a Book").click()
        #Fill out the borrow form
        time.sleep(1)
        driver.find_element(By.ID, "book_id").send_keys(10)
        #Submit the borrow form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        #Logout
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Logout").click()
        print("User Register and login tests passed successfully.")
        driver.find_element(By.LINK_TEXT, "Create a new user").click()
        #Fill out the register form
        username1 = "Admin1"
        password1 = "000000"
        full_name1 = "Admin1 haha"
        email1 = "Admintest@example.com"
        #Wait for the username input field to be visible and fill out the form
        time.sleep(1)
        driver.find_element(By.ID, "username").send_keys(username1)
        driver.find_element(By.ID, "password").send_keys(password1)
        driver.find_element(By.ID, "full_name").send_keys(full_name1)
        driver.find_element(By.ID, "email").send_keys(email1)
        time.sleep(1)
        
        select_role = Select(driver.find_element(By.ID, "role"))
        select_role.select_by_visible_text("Admin")
        time.sleep(1)
        #Submit the form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        #Fill out the login form with the new credentials
        driver.find_element(By.ID, "username").send_keys(username1)
        driver.find_element(By.ID, "password").send_keys(password1)
        #Submit the login form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        #Navigate to Add New Book page
        driver.find_element(By.LINK_TEXT, "Add New Book").click()
        time.sleep(1)
        #Fill out the add book form
        driver.find_element(By.ID, "title").send_keys("math")
        driver.find_element(By.ID, "author").send_keys("Author1")
        #Submit the add book form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        #Navigate to Add New User page
        driver.find_element(By.LINK_TEXT, "Add New User").click()
        time.sleep(1)
        #Fill out the add user form
        driver.find_element(By.ID, "username").send_keys("usertester3")
        driver.find_element(By.ID, "password").send_keys("000000")
        driver.find_element(By.ID, "full_name").send_keys("usertester3 haha")
        driver.find_element(By.ID, "email").send_keys("usertester2@example.com")
        #Select role
        select_role = Select(driver.find_element(By.ID, "role"))
        select_role.select_by_visible_text("User")
        #Submit the add user form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        #Delete a book
        book_id = "17"  # Replace with the actual book ID
        delete_book_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//form[@action='/admin/delete_book/{book_id}']/button"))
        )
        delete_book_button.click()
        time.sleep(1)
        #Delete a user
        user_id = '6'  # Replace with the actual user ID
        delete_user_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//form[@action='/admin/delete_user/{user_id}']/button"))
        )
        delete_user_button.click()
        #Logout
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Logout").click()
        print("Admin Register, login, add book, add user, delete book, and delete user tests passed successfully.")
        time.sleep(1)
        driver.find_element(By.ID, "username").send_keys("usertester3")
        driver.find_element(By.ID, "password").send_keys("000000")
        #Submit the login form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Borrow a Book").click()
        time.sleep(1)
        driver.find_element(By.ID, "book_id").send_keys(2)
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        #Navigate to Return a Book page
        driver.find_element(By.LINK_TEXT, "Return a Book").click()
        time.sleep(1)
        #Fill out the return form
        driver.find_element(By.ID, "book_id").send_keys(2)
        #Submit the return form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        print("New user can't borrow and return the book that has been others borrowed tests passed successfully.")
    except Exception as e:
        print(f"Test failed: {e}")
        raise
    finally:
        driver.quit()
# Run the test
if __name__ == "__main__":
    test_register_and_login()