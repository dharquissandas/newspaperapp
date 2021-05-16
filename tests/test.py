from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from newspaperapp.models import newsCategory, userInfo, newsArticle, Comment, subComment
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime

class TestProjectLoginReg(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome("tests/chromedriver.exe")
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
    
    #B1 Testing

    def test1(self):
        print("Incorrect Login Test")
        self.browser.get(self.live_server_url + reverse("login"))
        WebDriverWait(self.browser,20).until(lambda d: d.find_element_by_tag_name("body"))
        body = self.browser.find_element_by_tag_name('body')
        name = body.find_element_by_name('username')
        pass1 = body.find_element_by_name('password')
        name.send_keys('testuser')
        pass1.send_keys('Password123')
        body.find_element_by_class_name('form-signin').submit()
        try:
            self.assertEquals(self.browser.current_url,self.browser.current_url)
            print("TEST OK")
        except:
            print("TEST FAILED")


    def test2(self):
        print("Incorrect Register Test")
        self.browser.get(self.live_server_url + reverse("register"))
        body = self.browser.find_element_by_tag_name('body')
        name = body.find_element_by_name('username')
        email = body.find_element_by_name('email')
        dob = body.find_element_by_name('dob')
        pass1 = body.find_element_by_name('password1')
        pass2 = body.find_element_by_name('password2')
        name.send_keys('testuser')
        email.send_keys('test@test.com')
        dob.send_keys('28/05/2000')
        pass1.send_keys('Password1234')
        pass2.send_keys('Password123')
        body.find_element_by_class_name('form-signin').submit()
        time.sleep(3)
        try:
            self.assertEquals(self.browser.current_url,self.browser.current_url)
            print("TEST OK")
        except:
            print("TEST FAILED")
    
    def test3(self):
        print("Correct Register & Login Test")
        test_url = self.live_server_url + reverse("index")
        self.browser.get(self.live_server_url + reverse("register"))
        body = self.browser.find_element_by_tag_name('body')
        name = body.find_element_by_name('username')
        email = body.find_element_by_name('email')
        dob = body.find_element_by_name('dob')
        pass1 = body.find_element_by_name('password1')
        pass2 = body.find_element_by_name('password2')
        name.send_keys('testuser')
        email.send_keys('test@test.com')
        dob.send_keys('28/05/2000')
        pass1.send_keys('TestPass123')
        pass2.send_keys('TestPass123')
        body.find_element_by_class_name('form-signin').submit()
        time.sleep(3)
        self.browser.get(self.live_server_url + reverse("logout"))
        print("Correct Login Test")
        time.sleep(3)
        body = self.browser.find_element_by_tag_name('body')
        name = body.find_element_by_name('username')
        pass1 = body.find_element_by_name('password')
        name.send_keys('testuser')
        pass1.send_keys('TestPass123')
        body.find_element_by_class_name('form-signin').submit()
        time.sleep(3)
        try:
            self.assertEquals(self.browser.current_url,test_url)
            print("TEST OK")
        except:
            print("TEST FAILED")

    ##B4 Testing

    def test4(self):
        print("Like System Test")
        print("Register User")
        self.browser.get(self.live_server_url + reverse("register"))
        body = self.browser.find_element_by_tag_name('body')
        name = body.find_element_by_name('username')
        email = body.find_element_by_name('email')
        dob = body.find_element_by_name('dob')
        pass1 = body.find_element_by_name('password1')
        pass2 = body.find_element_by_name('password2')
        name.send_keys('testuser')
        email.send_keys('test@test.com')
        dob.send_keys('28/05/2000')
        pass1.send_keys('TestPass123')
        pass2.send_keys('TestPass123')
        body.find_element_by_class_name('form-signin').submit()
        time.sleep(3)
        print("Create Article")
        newsCategory.objects.create(
            name = "TestCat"
        )
        newsArticle.objects.create(
            headline = "TestHeadline",
            text = "TestText",
            category = newsCategory.objects.get(pk=1),
            date = datetime.datetime(2020, 5, 17)
        )
        self.browser.get(self.live_server_url + reverse("category", args=[1]))
        print("Like Article")
        self.browser.find_element_by_id("like1").click()
        time.sleep(3)
        self.browser.get(self.live_server_url + reverse("showLikes"))
        time.sleep(3)

        try:
            self.assertEquals(self.browser.find_element_by_class_name("card-title").text,"TestHeadline")
            print("TEST OK (Like)")
        except:
            print("TEST FAILED (Like)")
        
        self.browser.get(self.live_server_url + reverse("category", args=[1]))
        print("Unlike Article")
        self.browser.find_element_by_id("dislike1").click()
        time.sleep(3)
        self.browser.get(self.live_server_url + reverse("showLikes"))
        time.sleep(3)
        try:
            self.assertEquals(self.browser.find_element_by_class_name("card-title").text,"Your Likes are Empty")
            print("TEST OK (Unlike)")
        except:
            print("TEST FAILED (Unlike)")

    ##I2 Testing
    def test5(self):
        print("Comment System Test")
        print("Register User")
        self.browser.get(self.live_server_url + reverse("register"))
        body = self.browser.find_element_by_tag_name('body')
        name = body.find_element_by_name('username')
        email = body.find_element_by_name('email')
        dob = body.find_element_by_name('dob')
        pass1 = body.find_element_by_name('password1')
        pass2 = body.find_element_by_name('password2')
        name.send_keys('testuser')
        email.send_keys('test@test.com')
        dob.send_keys('28/05/2000')
        pass1.send_keys('TestPass123')
        pass2.send_keys('TestPass123')
        body.find_element_by_class_name('form-signin').submit()
        print("Create Article")
        newsCategory.objects.create(
            name = "TestCat"
        )
        newsArticle.objects.create(
            headline = "TestHeadline",
            text = "TestText",
            category = newsCategory.objects.get(pk=2),
            date = datetime.datetime(2020, 5, 17)
        )
        self.browser.get(self.live_server_url + reverse("viewArticle", args=[2]))
        time.sleep(3)
        self.browser.find_element_by_id("id_body").send_keys("Test Comment")
        print("Submit Comment")
        self.browser.find_element_by_id("submitComment").click()
        time.sleep(3)
        comment = self.browser.find_element_by_id("comment1")
        try:
            self.assertEquals(comment.find_element_by_class_name("card-text").text,"Test Comment")
            print("TEST OK (Comment)")
        except:
            print("TEST FAILED (Comment)")

        time.sleep(3)
        print("Delete Comment")
        comment.find_element_by_class_name("deletebutton").click()
        time.sleep(3)
        comments = self.browser.find_elements_by_id("comment1")
        try:
            self.assertEquals(len(comments),0)
            print("TEST OK (Uncomment)")
        except:
            print("TEST FAILED (Uncomment)")