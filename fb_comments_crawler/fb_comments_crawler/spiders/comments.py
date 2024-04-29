from scrapy.http import FormRequest
from pathlib import Path
from scrapy import Spider, Request
import scrapy
from scrapy.selector import Selector
from fb_comments_crawler.items import FbCommentsCrawlerItem
import numpy as np
import time



class cmtSpider(Spider):    

	visit_count = 0

	name = 'comments'
	allowed_domains = ["facebook.com", "www.facebook.com", "m.facebook.com", "mbasic.facebook.com"]
	# start_urls = [
	# 	'https://mbasic.facebook.com/login.php',
	# 	# "https://mbasic.facebook.com/photo?fbid=755415003461040&set=a.569288308740378",
	# ]

	post_urls = [
		"https://mbasic.facebook.com/photo?fbid=755415003461040&set=a.569288308740378",
		]

	login_url = 'https://mbasic.facebook.com/login.php'
	# target_url = 'https://mbasic.facebook.com/photo?fbid=755415003461040&set=a.569288308740378'
	email = 'testida1212@gmail.com'
	password = 'testtest111'

	# Adjust DOWNLOAD_DELAY in settings.py
	custom_settings = {
		'DOWNLOAD_DELAY': time.sleep(np.random.randint(2,5)) # Set a delay of 2 seconds between requests
	}

	def start_requests(self):
		yield scrapy.Request(url=self.login_url, callback=self.login)

	# login
	def login(self, response):
		print("parse-"*10)
		# Extract CSRF token and other necessary fields from the login form
		csrf_token = response.css('input[name="fb_dtsg"]::attr(value)').get()
		# Assuming 'email' and 'pass' are the input names for the username and password fields
		return FormRequest.from_response(
			response,
			formdata={
				'email':self.email,
				'pass':self.password,
				'fb_dtsg': csrf_token,
			},
			callback=self.after_login
		)

	def after_login(self, response):
		# print("after_login+"*10)
		# Check login success before scraping
		if "login_error" in response.url:
			self.log("Login failed", level=scrapy.logging.ERROR)
		else:
			self.log("Login succeeded")
		# Proceed with scraping after successful login
		# For example, navigate to the target page
		print("\n",self.post_urls[0],"\n")
		yield Request(url=self.post_urls[0],callback=self.parse_content)
		return

	# for the first page load
	def parse_content(self, response):

		print("=" * 100)
		print(response.css("title::text").get())


		# print("parse_content+" * 10)

		# if response.status == 200:
		# 	print("Received a valid response from the URL.")
		# # Now you can proceed with extracting data using XPath or other methods
		# else:
		# 	print("Failed to receive a valid response from the URL. Status code:", response.status)
		
		# print(response.css('title::text').get())

		# Đoạn vì lúc sang page thêm mục view-prev-comment nên cấu trúc đổi tăng thêm 1 bậc
		if self.visit_count == 0:
			content = Selector(response).xpath(
				# '//*[@id[starts-with(., "ufi")]]/div',
				'//*[@id="ufi_pfbid0aeH4A3rvR2vf6jFHVEHK2hxy6E5JFSYA1xVcqBz9X9CXf4YLc88Uv4cFqCFwZTqel"]/div/div[4]',
			)
			# print('\n1',content,'\n')
		else:
			content = Selector(response).xpath(
				# '//*[@id[starts-with(., "ufi")]]/div',
				'//*[@id="ufi_pfbid0aeH4A3rvR2vf6jFHVEHK2hxy6E5JFSYA1xVcqBz9X9CXf4YLc88Uv4cFqCFwZTqel"]/div/div[5]',
			)
			# print('\n2',content,'\n')
	
		print('So comment trong 1 page', len(content.xpath('./*')))

		# Lấy ra thông tin comment
		for ct in content.xpath('./*'):
			# Kiểm tra những id không phải tên người dùng thì loại (loại những nút xem thêm comment, xem comment trước) 
			if ct.xpath('@id').get().isnumeric() == False:
				continue
			yield{
				'name_people': ct.css("h3 a::text").get(),
				'content_comment': ct.css("div div::text").get(),
				'time_comment': ct.css('div abbr::text').get()
			}

		# Extracting the link for the "see next" page
		see_next = content.xpath('.//div[starts-with(@id,"see_next")]')
		see_next_link = see_next.xpath('a/@href').get()
		
		self.visit_count += 1
		
		# Còn comment thì chuyển sang page mới
		if see_next_link:
			# print(see_next_link)
			time.sleep(np.random.randint(5, 10))
			# If the link exists, yield a request to parse the next page
			yield response.follow(see_next_link, callback=self.parse_content)
		return
	