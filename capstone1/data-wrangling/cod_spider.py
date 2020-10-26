# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 18:26:34 2020

@author: jenny
"""

import scrapy
from fundrazr.items import FundrazrItem
class Fundrazr(scrapy.Spider):
	name = "my_scraper"

	# First Start Url
	start_urls = ["http://codstats.net/leaderboards"]

	npages = 2

	# This mimics getting the pages using the next button. 
	for i in range(2, npages + 2):
		start_urls.append("http://codstats.net/leaderboards/&page="+str(i)+"")
	
	def parse(self, response):
		for href in start_urls:
			# add the scheme, eg http://
			url  =  href
 
			yield scrapy.Request(url, callback=self.parse_dir_contents)	
					
	def parse_dir_contents(self, response):
		item = FundrazrItem()

		# Getting Campaign Title
		item['leader'] = response.xpath("/a[contains(@class, 'white')]//@href").extract()

		yield item
