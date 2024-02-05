from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import pymysql
import os

class ProfileTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(10)  # Menunggu maksimal 10 detik untuk elemen muncul
        cls.connection = pymysql.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )

    def test_1_login_page(self):
        self.browser.get('http://localhost/BadCRUD/login.php')
        expected_result = "Login"
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)

    def test_2_login_with_database_credentials(self):
        # Path ke file database
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'your_database_file.sql'))

        # Ambil username dan password dari database
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT username, password FROM users WHERE id = 1")  # Ubah sesuai dengan skema tabel Anda
            result = cursor.fetchone()
            username, password = result

        # Masukkan username dan password
        self.browser.find_element(By.XPATH, "//*[@id='inputUsername']").send_keys(username)
        self.browser.find_element(By.XPATH, "//*[@id='inputPassword']").send_keys(password)
        self.browser.find_element(By.XPATH, "/html/body/form/button").click()

        # Verifikasi bahwa login berhasil
        expected_result = "Halo, admin"
        actual_result = self.browser.find_element(By.XPATH, "/html/body/div[1]/h2").text
        self.assertIn(expected_result, actual_result)

    def test_3_contact_click(self):           
        expected_result = "Add new contact"
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/a").click()
        actual_result = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/h5").text                

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.connection.close()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
