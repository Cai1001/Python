from multiprocessing import Process
from scrapy import cmdline
import os
import time
'''
AutoComments/async_proxy_pool/config.py 文件中配置端口
'''
def run_pool_client():
	print('<<<<<<<<<<<<<<< start pool client, wait for a moment >>>>>>>>>>>>>')
	os.system("python ./startpool/client.py -o ip.txt")
	time.sleep(5)

def run_pool_server():
	print('<<<<<<<<<<<<<<< start pool server >>>>>>>>>>>>>')
	os.system("python ./startpool/server_flask.py")
	time.sleep(5)
def run_spider():
	print('<<<<<<<<<<<<<<< start crawling data >>>>>>>>>>>>>')
	cmdline.execute("scrapy crawl autohome_spider".split())


if __name__ =="__main__":
	p1 = Process(target=run_pool_client)
	print('Process 1 is starting')
	p1.start()
	time.sleep(5)
	p2 = Process(target=run_pool_server)
	print('Process 2 is starting')
	p2.start()
	time.sleep(5)
	run_spider()

# p3 = Process(target=run_spider)
	# print('Process 3 is starting')
	# time.sleep(5)
	# p3.start()







