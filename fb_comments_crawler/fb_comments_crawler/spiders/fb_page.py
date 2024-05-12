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
	name = 'fb-page' #Tên của spider

	start_url = 'https://mbasic.facebook.com/' #Đăng nhập giao diện mbasic của FB

	login_url = start_url + 'login.php'   #Trang login của FB
	target_url = start_url + 'KTXDHQGConfessions?v=timeline'  #Link Fanpage muốn crawl
	#'https://mbasic.facebook.com/tintucvtv24?v=timeline'

	email = 'mailchunghoclaptrinh@gmail.com'	#TK để đăng nhập vào FB
	password = 'HOCMAI1221!'					#Mật khẩu
	
	crawled_comments = 0
	crawled_pages = 0
	max_crawled_comments = 50   #Số cmt muốn crawl trong 1 bài đăng (post)
	max_crawled_pages = 2       #Số lượng trang muốn crawl (trong 1 page (trang) có nhiều bài đăng (post))


	def start_requests(self): #Gửi yêu cầu truy cập trang web
		yield scrapy.Request(url=self.login_url, callback=self.login)

	# Đăng nhập
	def login(self, response):  #Gửi yêu cầu đăng nhập
		
		#print('-' * 30 + 'login' + '-' * 30)
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

	def after_login(self, response): # Lấy trạng thái sau khi đăng nhập => Thành công/Thất bại
		
		#print('-' * 30 + 'after_login' + '-' * 30)
		time.sleep(10)
		# Check login success before scraping
		if "login_error" in response.url:
			self.log("Login failed", level=scrapy.logging.ERROR)
		else:
			self.log("Login succeeded")
		# Proceed with scraping after successful login
		# For example, navigate to the target page
		yield Request(url=self.target_url, callback=self.parse_page)

		return

	
	#Crawl dữ liệu
	def parse_page(self, response): #Duyệt mỗi bài đăng trong một trang
		#print('-' * 30 + 'parse_page' + '-' * 30)

		if response.status == 200:
			print("Received a valid response from the URL.")
		# Now you can proceed with extracting data using XPath or other methods
		else:
			print("Failed to receive a valid response from the URL. Status code:", response.status)
		#print("==============================")
		#print(Selector(response).css("title"))


		#Lấy danh sách các thẻ chứa bài đăng và link dẫn tới trang tiếp theo và các mốc tgian trong fanpage
		content = Selector(response).xpath('//*[@id="structured_composer_async_container"]') 
		#print('content:', content)

		time.sleep(np.random.randint(2, 10))
		# filename = 'content.html'
		# with open(filename,'w',encoding='utf-8') as f:
		# 	f.write('\n'.join(content.getall()))
		# print("-done" * 10)
		
		#print("*" * 100)
		
		post = content.xpath('./div[1]/div')  #Lấy danh sách các bài post ở thẻ div đầu tiên

		"""
		- Thẻ div đầu tiên: Danh sách các bài đăng 
		- Thẻ div thứ hai: Link kiết dẫn tới các bài đăng ở trang tiếp  theo
		- Các thẻ  div còn lại: Các mốc thời gian của fanpage
		"""
		#print("=========================\n")
		
		i = 0
		for p in post: #Duyệt qua các bài post
			i += 1
			print("\n page = {}, post {} \n".format(self.crawled_pages, i))
			link_comment_one_post = self.start_url + p.xpath("./div[2]/div[2]/a[1]/@href").get() #Lấy ra liên kết dẫn tới trang bình luận của bài đăng
			#print("link commnet: ", link_comment_one_post)

			# giới hạn số lượng bình luận trong 1 bài đăng 
			self.crawled_comments = 0
			time.sleep(np.random.randint(2,4))
			yield response.follow(link_comment_one_post, callback=self.parse_comment) #Truy xuất trang chứa comment của mỗi post
	

		# see more post
		#print('-'*40 + 'see more page' + '-'*40)

		#Xem trang tiếp theo (truy cập vào thẻ thứ 2)
		see_more_page = content.xpath('./div[2]/a/@href').get()

		#print(see_more_page)


		#Liên kết dẫn tới trang tiếp theo
		link_new_page = self.start_url + see_more_page
		if (self.crawled_pages < self.max_crawled_pages):  #Kiểm tra điều kiện về số trang tối đa muốn crawl
			self.crawled_pages += 1
			time.sleep(np.random.randint(5, 10))
			yield response.follow(link_new_page, callback=self.parse_page) #Dẫn tới trang tiếp  theo
		
		return
	
	# for the first page load

	#Lấy từng comment trong 1 bài đăng
	def parse_comment(self, response):
		#print('-' * 30 + 'parse_comment' + '-' * 30)

		# print(response.css("title::text").get())

		if response.status == 200:
			print("Received a valid response from the URL.")
		# Now you can proceed with extracting data using XPath or other methods
		else:
			print("Failed to receive a valid response from the URL. Status code:", response.status)

		#Lấy ra nội dung comment
		content = Selector(response).xpath(
			'//*[@id[starts-with(., "ufi")]]/div' #Đi từ gốc tới thẻ id bắt đầu bằng tù khóa "ufi", tức là thẻ chứa thông tin tương tác của bài đăng
		)

		#

		first_generation_descendants = content.xpath('./*') #Tất cả thẻ con trong content
		# print(len(first_generation_descendants))

		# comment content section doesn't have id attribute
		comment_class = None

		for f in first_generation_descendants: #Tìm thẻ chứa danh sách các comments

			_class = f.xpath('@class').get()
			_id = f.xpath('@id').get()

			if _id is None:
				comment_class = _class

		# print(comment_class)

		if comment_class is not None:
			
			comment_selector = content.xpath(f'div[@class="{comment_class}"]') #Chứa các thẻ  thể hiện comments

		

			# # extract links to the previous and the next comments page
			see_prev = comment_selector.xpath('.//div[starts-with(@id,"see_prev")]').get() #Quay lại trang phía trước

			see_next = comment_selector.xpath('.//div[starts-with(@id,"see_next")]') #Qua trang tiếp theo để crawl tiếp

			# list of first-class children
			com = comment_selector.xpath('./*') #Lấy danh sách các thẻ con của comment_selector, tức là các thẻ thể hiện từng cmt
			# handle comments sections
			for c in com: #Duyệt qua từng thẻ con chứa comment
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
						#print("see_next")
						continue

					# print(c.xpath('div').get())
					_comments['name'] = c.xpath('div/h3/a/text()').get()
					_comments['cmt'] = c.xpath('div/div/text()').get()
					_comments['time'] = c.xpath('div/div[3]/abbr/text()').get()

					yield _comments #Xuất ra file output
				else:
					return

			#Lấy liên kết để đi tới trang tiếp theo để crawl comments
			see_next_link = see_next.xpath('a/@href').get()

			
			#Đi tới trang tiếp theo nếu có tồn tại
			if see_next_link:
				time.sleep(np.random.randint(2, 10))
				
				yield response.follow(see_next_link, self.parse_comment) #Gọi đệ quy để cứ đi tới trang tiếp theo

		return