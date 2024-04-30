from scrapy.http import FormRequest
from pathlib import Path
from scrapy import Spider, Request
import scrapy
from scrapy.selector import Selector
# from fb_comments_crawler.items import FbCommentsCrawlerItem


class timelineSpider(Spider):
    name = 'timeline'
    login_url = 'https://mbasic.facebook.com/login.php'
    target_url = 'https://mbasic.facebook.com/tintucvtv24?v=timeline'
    email = 'phamthaihuy94.yersin@gmail.com'
    password = '123Vnu##'

    def start_requests(self):
        yield scrapy.Request(url=self.login_url, callback=self.login)

    # login
    def login(self, response):
        print("parse-" * 10)
        # Extract CSRF token and other necessary fields from the login form
        csrf_token = response.css('input[name="fb_dtsg"]::attr(value)').get()
        # Assuming 'email' and 'pass' are the input names for the username and password fields
        return FormRequest.from_response(
            response,
            formdata={
                # 'email': 'idahcmus227nvc@gmail.com',
                # 'pass': 'VNUhcmus227#',
                'email': self.email,
                'pass': self.password,
                'fb_dtsg': csrf_token,
            },
            callback=self.after_login
        )

    def after_login(self, response):
        print("after_login+" * 10)
        # Check login success before scraping
        if "login_error" in response.url:
            self.log("Login failed", level=scrapy.logging.ERROR)
        else:
            self.log("Login succeeded")
        # Proceed with scraping after successful login
        # For example, navigate to the target page
        yield Request(url=self.target_url, callback=self.parse_content)

        return

    # for the first page load
    def parse_content(self, response):

        if response.status == 200:
            print("Received a valid response from the URL.")
        # Now you can proceed with extracting data using XPath or other methods
        else:
            print("Failed to receive a valid response from the URL. Status code:", response.status)


        content = Selector(response).xpath('//*[@id="structured_composer_async_container"]')

        filename = 'content.html'

        with open(filename,'w',encoding='utf-8') as f:
            f.write('\n'.join(content.getall()))
        print("-done" * 10)

        return