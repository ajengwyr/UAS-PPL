from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest, sys

class ProfileTestCase(unittest.TestCase):

    @classmethod
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        server = 'http://localhost:4444'

        self.browser = webdriver.Remote(command_executor=server, options=options)

    def test_1_login_page(self):
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = "http://localhost"

        self.browser.get(url)
        self.browser.save_screenshot('screenshot.png')
        expected_result = "Login"
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)

    def test_2_login_with_database_credentials(self):
        
        # Masukkan username dan password
        self.browser.find_element(By.XPATH, "//*[@id='inputUsername']").send_keys("admin")
        self.browser.find_element(By.XPATH, "//*[@id='inputPassword']").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "/html/body/form/button").click()

        # Verifikasi bahwa login berhasil
        expected_result = "Halo, admin"
        actual_result = self.browser.find_element(By.XPATH, "/html/body/div[1]/h2").text
        self.assertIn(expected_result, actual_result)

    def test_3_profile_click(self):
        expected_result = "Profil"
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/a[1]").click()
        actual_result = self.browser.find_element(By.XPATH, "/html/body/div[1]/h2").text
        self.assertIn(expected_result, actual_result)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.connection.close()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
