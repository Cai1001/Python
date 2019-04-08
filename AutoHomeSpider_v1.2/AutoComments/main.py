from multiprocessing import Process
from scrapy import cmdline
import os
import time
from datetime import datetime
import sched
'''
AutoComments/async_proxy_pool/config.py 文件中配置端口
'''
schedule = sched.scheduler(time.time, time.sleep)


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
	cmdline.execute("scrapy crawl AutocommentsDetailSpider".split())


def loop_ip_service(inc=60):
	global schedule
	schedule.enter(0,0, run_pool_client, (inc, ))
	schedule.run()


def run_spider1():
	print('<<<<<<<<<<<<<<< start crawling data >>>>>>>>>>>>>')
	cmdline.execute("scrapy crawl AutoCommentSpider1".split())

if __name__ =="__main__":
	# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。


	run_spider1()
	# p1 = Process(target=loop_ip_service, args=(7200,))
	# print('Process 1 is starting')
	# p1.start()
	# p1 = Process(target=run_pool_client)
	# p1.start()
	# print("<<<<<<<<<<<<<<<代理服务启动中....请等待>>>>>>>>>>>>>>>>>>")
	# time.sleep(10)
	# p2 = Process(target=run_pool_server)
	# print('Process 2 is starting')
	# p2.start()
	# print("<<<<<<<<<<<<<<<flask服务启动中....请等待>>>>>>>>>>>>>>>>>>")
	# time.sleep(10)
	# run_spider()

	# p3 = Process(target=run_spider)
	# print('Process 3 is starting')
	# time.sleep(5)
	# p3.start()







