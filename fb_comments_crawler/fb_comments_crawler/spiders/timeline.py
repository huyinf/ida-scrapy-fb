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
    name = 'timeline'
    visit_count = 0
    login_url = 'https://mbasic.facebook.com/login.php'
    target_url = 'https://mbasic.facebook.com/tintucvtv24?v=timeline'

    email = 'phamthaihuy94.yersin@gmail.com'
    password = '123Vnu##'
    
    max_comment = 0

    start_url = 'https://mbasic.facebook.com/'
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

        time.sleep(np.random.randint(2, 5))
        # filename = 'content.html'

        # with open(filename,'w',encoding='utf-8') as f:
        #     f.write('\n'.join(content.getall()))
        # print("-done" * 10)
        
        print("*" * 100)
        
        if self.visit_count == 0:
            post = content.xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[3]/div[2]/div/div[1]')
        else:
            post = content.xpath('/html/body/div[1]/div/div[1]/div/table/tbody/tr/td/div/div[1]')

        # # print(post)
        # # /html/body/div[1]/div/div[1]/div/table/tbody/tr/td/div/div[1]/div[1]/div[2]/div[2]/a[1]
        # print("*" * 100)

        if self.visit_count == 0:
            print("-"*100)
            print("\n page = {} \n".format(self.visit_count))
   
            print(self.start_url + post.xpath('./div/div[2]/div[2]/a[1]/@href').get())
            link_comment_one_post = self.start_url + post.xpath('./div/div[2]/div[2]/a[1]/@href').get()
            yield Request(url=link_comment_one_post, callback=self.parse_comment)
            next_page = self.start_url + content.xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/a/@href').get()
        else:
            for p in post.xpath('./*'):
                print("\n page = {} \n".format(self.visit_count))
                print(self.start_url + p.xpath('./div[1]/div[2]/div[2]/a[1]/@href').get())
                time.sleep(np.random.randint(2, 5))
                print("\n")
                link_comment_one_post = self.start_url + p.xpath('./div[1]/div[2]/div[2]/a[1]/@href').get()
                
                yield Request(url=link_comment_one_post, callback=self.parse_comment)

            
            # Bam vao nut see more stories
            next_page = self.start_url + content.xpath('/html/body/div[1]/div/div[1]/div/table/tbody/tr/td/div/div[2]/a/@href').get()
        
        time.sleep(np.random.randint(2, 5))
        # so lan bam nut view more stories
        if self.visit_count < 5:
            self.visit_count += 1
            yield response.follow(next_page, callback=self.parse_content)
        return

    
    
    # for the first page load
    def parse_comment(self, response):

        print(response.css("title::text").get())

        print("=" * 100)

        print("parse_content+" * 10)

        if response.status == 200:
            print("Received a valid response from the URL.")
        # Now you can proceed with extracting data using XPath or other methods
        else:
            print("Failed to receive a valid response from the URL. Status code:", response.status)

        content = Selector(response).xpath(
            '//*[@id[starts-with(., "ufi")]]/div'
        )

        first_generation_descendants = content.xpath('./*')
        print(len(first_generation_descendants))

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

            # count the numbers of its children (first-class)
            # print(len(comment_selector.xpath('./*')))

            # print(comment_selector.getall())

            # list of first-class children
            com = comment_selector.xpath('./*')
            # print("\n",com,"\n")

            # # extract links to the previous and the next comments page
            see_prev = comment_selector.xpath('.//div[starts-with(@id,"see_prev")]').get()
            see_next = comment_selector.xpath('.//div[starts-with(@id,"see_next")]')


            # print("see_prev: ", see_prev) 
            # print("see_next: ", see_next)

            # handle comments sections
            for c in com:
                if self.max_comment < 20:
                    self.max_comment += 1
                    print("max comment: ", self.max_comment)
                    print("+" * 30)
                    _comments = FbCommentsCrawlerItem()

                    _comments['Id'] = c.xpath('@id').get()
                    if _comments['Id'].startswith('see_prev'):
                        continue
                    if _comments['Id'].startswith('see_next'):
                        print("see_next")
                        continue

                    # print(c.xpath('div').get())
                    _comments['name'] = c.xpath('div/h3/a/text()').get()
                    _comments['cmt'] = c.xpath('div/div/text()').get()
                    _comments['time'] = c.xpath('div/div[3]/abbr/text()').get()

                    yield _comments
                else:
                    return
    

            '''
            task:
            navigate to the next page and get its content
            '''

            # Extracting the link for the "see next" page
            see_next_link = see_next.xpath('a/@href').get()
            #
            # if see_next_link:
            #   print(see_next_link)
            #   # If the link exists, yield a request to parse the next page
            #   next_url = response.urljoin(see_next_link)
            #   print("="*30)
            #   print(next_url)
            # #
            #   yield Request(url=next_url, callback=self.parse_content)

            print("=" * 30)
            # Inside parse_content method
            if see_next_link:
                print(see_next_link)
                time.sleep(np.random.randint(2, 10))
                # If the link exists, yield a request to parse the next page
                # yield Request(url=response.urljoin(see_next_link), callback=self.parse_next)
                print("-++" * 10)
    
                yield response.follow(see_next_link, self.parse_comment)
        print("-done" * 10)

        return