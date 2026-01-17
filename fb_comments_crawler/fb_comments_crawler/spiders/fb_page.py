from scrapy.http import FormRequest
from pathlib import Path
from scrapy import Spider, Request
import scrapy
from scrapy.selector import Selector
import time
import numpy as np
from fb_comments_crawler.items import FbCommentsCrawlerItem

# from comments import cmtSpider

class timelineSpider(Spider):
	name = 'fb-page'

	login_url = 'https://mbasic.facebook.com/login.php'
	target_url = 'https://mbasic.facebook.com/KTXDHQGConfessions?v=timeline'
	#'https://mbasic.facebook.com/tintucvtv24?v=timeline'

	email = 'mailchunghoclaptrinh@gmail.com' 
	password = 'HOCMAI1221!'
	
	crawled_comments = 0
	crawled_pages = 0
	max_crawled_comments = 50
	max_crawled_pages = 2

	start_url = 'https://mbasic.facebook.com/'
	def start_requests(self):
		yield scrapy.Request(url=self.login_url, callback=self.login)

	# login
	def login(self, response):
		print('-' * 30 + 'login' + '-' * 30)
		# Extract CSRF token and other necessary fields from the login form
		csrf_token = response.css('input[name="fb_dtsg"]::attr(value)').get()
		# Assuming 'email' and 'pass' are the input names for the username and password fields
		return FormRequest.from_response(
			response,
			formdata={
				'email': self.email,
				'pass': self.password,
				'fb_dtsg': csrf_token,
			},
			callback=self.after_login
		)

	def after_login(self, response):
		print('-' * 30 + 'after_login' + '-' * 30)
		time.sleep(10)
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
		print('-' * 30 + 'parse_content' + '-' * 30)

		if response.status == 200:
			print("Received a valid response from the URL.")
		# Now you can proceed with extracting data using XPath or other methods
		else:
			print("Failed to receive a valid response from the URL. Status code:", response.status)
		print("==============================")
		print(Selector(response).css("title"))
		content = Selector(response).xpath('//*[@id="structured_composer_async_container"]')
		print('content:', content)

		time.sleep(np.random.randint(2, 10))
		# filename = 'content.html'
		# with open(filename,'w',encoding='utf-8') as f:
		# 	f.write('\n'.join(content.getall()))
		# print("-done" * 10)
		
		print("*" * 100)
		
		post = content.xpath('./div[1]/div')
		print("=========================\n")
		
		i = 0
		for p in post:
			i += 1
			print("\n page = {}, post {} \n".format(self.crawled_pages, i))
			link_comment_one_post = self.start_url + p.xpath("./div[2]/div[2]/a[1]/@href").get()
			print("link commnet: ", link_comment_one_post)
			# neu muon gioi han max cmt cho tung post thi de lai dong duoi
			self.crawled_comments = 0
			time.sleep(np.random.randint(2,4))
			yield response.follow(link_comment_one_post, callback=self.parse_comment)

		# see more post
		print('-'*40 + 'see more page' + '-'*40)
		see_more_page = content.xpath('./div[2]/a/@href').get()

		print(see_more_page)
		link_new_page = self.start_url + see_more_page
		if (self.crawled_pages < self.max_crawled_pages):
			self.crawled_pages += 1
			time.sleep(np.random.randint(5, 10))
			yield response.follow(link_new_page, callback=self.parse_content)
		
		return
	
	# for the first page load
	def parse_comment(self, response):
		print('-' * 30 + 'parse_comment' + '-' * 30)

		# print(response.css("title::text").get())

		if response.status == 200:
			print("Received a valid response from the URL.")
		# Now you can proceed with extracting data using XPath or other methods
		else:
			print("Failed to receive a valid response from the URL. Status code:", response.status)

		content = Selector(response).xpath(
			'//*[@id[starts-with(., "ufi")]]/div'
		)

		first_generation_descendants = content.xpath('./*')
		# print(len(first_generation_descendants))

		# comment content section doesn't have id attribute
		comment_class = None
		for f in first_generation_descendants:

			_class = f.xpath('@class').get()
			_id = f.xpath('@id').get()

			if _id is None:
				comment_class = _class

		# print(comment_class)

		if comment_class is not None:
			comment_selector = content.xpath(f'div[@class="{comment_class}"]')

			# list of first-class children
			com = comment_selector.xpath('./*')

			# # extract links to the previous and the next comments page
			see_prev = comment_selector.xpath('.//div[starts-with(@id,"see_prev")]').get()
			see_next = comment_selector.xpath('.//div[starts-with(@id,"see_next")]')

			# handle comments sections
			for c in com:
				if self.crawled_comments < self.max_crawled_comments:
					self.crawled_comments += 1
					print("crawled_comments: ", self.crawled_comments)
					print("+" * 30)
					_comments = FbCommentsCrawlerItem()

					# _comments['Id'] = c.xpath('@id').get()
					comment_id = c.xpath('@id').get()
					if comment_id.startswith('see_prev'):
						continue
					if comment_id.startswith('see_next'):
						print("see_next")
						continue

					# print(c.xpath('div').get())
					_comments['name'] = c.xpath('div/h3/a/text()').get()
					_comments['cmt'] = c.xpath('div/div/text()').get()
					_comments['time'] = c.xpath('div/div[3]/abbr/text()').get()

					yield _comments
				else:
					return

			# Extracting the link for the "see next" page
			see_next_link = see_next.xpath('a/@href').get()

			print("=" * 30)
			# Inside parse_content method
			if see_next_link:
				time.sleep(np.random.randint(2, 10))
				# If the link exists, yield a request to parse the next page
				yield response.follow(see_next_link, self.parse_comment)

		print("done - " * 10)
		return