#coding = utf-8
from Crypto.Cipher import AES
import base64
import requests
import json
import time
import codecs
import sys   
reload(sys)
sys.setdefaultencoding('utf-8')


headers = {
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive',
	'Referer':'https://music.163.com/song?id=115502',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

MAX = 100


def AES_encrypt(text,key,iv):
	padding = 16 - len(text) % 16
	text = text + padding * chr(padding)
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	encrypt_text = encryptor.encrypt(text)
	encrypt_text = base64.b64encode(encrypt_text)
	return encrypt_text

def get_params(offset, limit):
	first_param = "{rid:\"\", offset:\"%s\", total:\"true\", limit:\"%s\", csrf_token:\"\"}" %(offset, limit)
	second_param = "010001"
	third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
	forth_param = "0CoJUm6Qyw8W8jud"
	iv = "0102030405060708"
	first_key = forth_param
	second_key = 16 * 'F'   
	enctryText = AES_encrypt(first_param, first_key, iv)
	enctryText = AES_encrypt(enctryText, second_key, iv)
	return enctryText

def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey

def get_json(url, params, encSecKey):
	data = {
		"params": params,
		"encSecKey": encSecKey
	}
	response = requests.post(url, headers = headers, data =data)
	return response.content

def get_total():
	params = get_params(0,0)
	encSecKey = get_encSecKey()
	json_text = get_json(url, params, encSecKey)
	json_dict = json.loads(json_text)
	total = int(json_dict['total'])
	return total

def save_to_file(list,filename):
	with codecs.open(filename,'a',encoding='utf-8') as f:
		f.writelines(list)
        print("write success!")


if __name__ == "__main__":
	start_time = time.time()     # start time
	filename = u"hongri.txt"
	url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_115502?csrf_token="
	total = get_total()
	target = total / MAX + 1    # max is 100
	for i in range(target):
		all_comments_list = [] # save all comment
		params = get_params(i*100, MAX)
		encSecKey = get_encSecKey()
		json_text = get_json(url, params, encSecKey)
		json_dict = json.loads(json_text)
		for item in json_dict['comments']:
			comment = item['content'].encode('utf-8', 'ignore')
			likedCount = item['likedCount']
			comment_time = item['time']
			userID = item['user']['userId']
			nickname = item['user']['nickname'].encode('utf-8', 'ignore')
			comment_info = nickname + "#" + str(comment_time) + "#" + str(likedCount) + "#" + comment + u"\n"
			all_comments_list.append(comment_info)
		save_to_file(all_comments_list,filename)
	end_time = time.time() 
	print("The program takes %f s." % (end_time - start_time))
