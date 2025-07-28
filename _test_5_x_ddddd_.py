








#!/usr/bin/env python3
"""
Kards Match Extractor 核心模块汇总 (v0.0.1)

包含以下函数定义：
  - `get_field(obj, path)`
  - `login_session()`
  - `get_match_ids()`
  - `fetch_match_info(match_id)`
  - `do_mulligan(match_id, side)`
  - `poll_actions(match_id, min_id, opponent_id)`
  - `extract_used_cards(raw_actions)`
  - `load_dataset(path)`
  - `load_nfile(path)`
  - `compare_sets(extracted, reference)`
  - `extract_name(raw_name)`
  - `format_cards(ids, dataset)`

今后扩展仅需修改 `main()`，记得调用上述所有函数。

"""
# --- 以下为函数定义区（略） ---
# def get_field(...): ...
                                       # def login_session(): ...
# def get_match_ids(): ...
# def fetch_match_info(match_id): ...
# def do_mulligan(match_id, side): ...
# def poll_actions(match_id, min_id, opponent_id): ...
# def extract_used_cards(raw_actions): ...
# def load_dataset(path): ...
# def load_nfile(path): ...
# def compare_sets(extracted, reference): ...
# def extract_name(raw_name): ...
# def format_cards(ids, dataset): ...





import argparse, json, time, requests, csv
from pathlib import Path
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)




# 全局配置
BASE_URL = "https://kards.live.1939api.com"

"""


HEADERS = { 'Accept': 'application/json', 'Authorization': 'JWT <YOUR_JWT>' }
PROXIES = {"http": None, "https": None}
POLL_INTERVAL = 1.0



"""


Jwt_fdsjfklds_=""

Jwt_fdsjfklds_="JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX25hbWUiOiJsaW5rZXI6MzE0MTU5MjY1MzU4OTc5MzIzODQ2MjY0MzM4MzI3OTUwNDk3QHByb3Rvbi5tZSIsInVzZXJfaWQiOjEwNTc3NjE0NSwiaWRlbnRpdHlfaWQiOjIxMDgzMjk1NiwicHJvdmlkZXIiOiJkZXZpY2UiLCJleHRlcm5hbF9pZCI6IldpbmRvd3MtNjU2RkIzQ0U0NjhCNDBDMTFERDZERTlDRUI1NDRERDkiLCJwYXltZW50Ijoibm90YXZhaWxhYmxlIiwicm9sZXMiOltdLCJpYXQiOjE3NTM2ODkzOTEsImV4cCI6MTc1Mzc3NTc5MSwianRpIjoieUhvNlduODFzWGJSVFliRXFxekciLCJpc3MiOiJrYXJkcy1iYWNrZW5kIiwidGllciI6IkxJVkUiLCJsYW5ndWFnZSI6InpoLUhhbnMiLCJjbGllbnRfaWQiOjMwMjEzNzYwMiwicGxheWVyX2lkIjo1NzQ2NDY4fQ.B5uzpVXnOpFKC9wIYylUZoFJXrvclydODgVCnHluF9sbnbpDa6Ho_PWSNH4PzJ_Ei6mus2V3bIqq6hpBWzcM--Uo9KHWbwqR6fj9tklrDxtN5tkuQrI-3h6Mrrtue4p2hg_J0UZrWWIMMdmsedxR969WVLrkbk7elg5GId42T0uLFIoUEmAnnBBV5Gv1XIehN9zsskskgJElCV37oJDeLMq6RAFqBHBHnn_YmtGnw2_nTLk96wHuK1IJLyuyDwZyacJ1dWSuadQ1Fg87lTtYf91jLUBFIPjCVHgsAJZ8Eoqqk-CJAfxO0sE1sjL_-Kv253oZoEU5D5UiIp8qmPj89A"#"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX25hbWUiOiJsaW5rZXI6MzE0MTU5MjY1MzU4OTc5MzIzODQ2MjY0MzM4MzI3OTUwNDk3QHByb3Rvbi5tZSIsInVzZXJfaWQiOjEwNTc3NjE0NSwiaWRlbnRpdHlfaWQiOjIxMDgzMjk1NiwicHJvdmlkZXIiOiJkZXZpY2UiLCJleHRlcm5hbF9pZCI6IldpbmRvd3MtNjU2RkIzQ0U0NjhCNDBDMTFERDZERTlDRUI1NDRERDkiLCJwYXltZW50Ijoibm90YXZhaWxhYmxlIiwicm9sZXMiOltdLCJpYXQiOjE3NTM1ODkyMDIsImV4cCI6MTc1MzY3NTYwMiwianRpIjoiMk5hUVlGMjg0WXBIZHlKWGt6elIiLCJpc3MiOiJrYXJkcy1iYWNrZW5kIiwidGllciI6IkxJVkUiLCJsYW5ndWFnZSI6InpoLUhhbnMiLCJjbGllbnRfaWQiOjMwMDcwMzcxMCwicGxheWVyX2lkIjo1NzQ2NDY4fQ.Z4ZkuTyHeEwq0rEAaVz2mSbrnSrrCoGfAxZhMDBBpE6yOFy9EDYFR6judlyWTvJnWTeozKmdFP0ZpnMe9rj69WI1fqZCJzpiVzlruiyk4bpMUutzbZOBhl0K0j-0CzUkVBdtwwhIzIl1A8P4Zvj2ultVzUvb0gI548lkprRnzo1UHnGZJSXK50C6QAfluEAFTUyzcK2zW4_68Otm7LQLnr199Vkf8z-yZxIFuPX1tlbY3g_iHFiEGOCo_AUbum_nTEuJb2OZkiqTVSuxaQau-HgjfVQmsv-LsCIHk_Lx1jgmX1PGthZI3ST-rwe7X6-nbwgIScfa85LU1RVQ6oq3kw"



reponse2=0


def dl_():


    global response2


    import requests
    import base64

    headers = {
     'Accept':'*/*',
     'Accept-Encoding':'deflate, gzip',
     'User-Agent':'kards/++UE5+Release-5.5-CL-40574608 (http-eventloop) Windows/10.0.19045.1.256.64bit',
     'Content-Length':'0'}
    payload=None

    response0 = requests.request("GET", "https://kards.live.1939api.com/config", headers=headers, data=payload)
    

    headers = {
     'Accept-Encoding':'deflate, gzip',
     'Accept':'application/json',
     'X-Api-Key':'1939-kards-5dcda429f:Kards 1.38.22432.launcher',
     'Drift-Api-Key':'1939-kards-5dcda429f:Kards 1.38.22432.launcher',
     'User-Agent':'kards/++UE5+Release-5.5-CL-40574608 (http-eventloop) Windows/10.0.19045.1.256.64bit',
     'Content-Length':'0'}
    payload=None

    response1 = requests.request("GET", "https://kards.live.1939api.com/", headers=headers, data=payload)


    headers = {
     'Accept-Encoding':'deflate, gzip',
     'Accept':'application/json',
     'X-Api-Key':'1939-kards-5dcda429f:Kards 1.38.22432.launcher',
     'Drift-Api-Key':'1939-kards-5dcda429f:Kards 1.38.22432.launcher',
     'Content-Type':'application/json',
     'User-Agent':'kards/++UE5+Release-5.5-CL-40574608 (http-eventloop) Windows/10.0.19045.1.256.64bit',
     'Content-Length':'953'}
    payload=base64.b64decode("ew0KCSJwcm92aWRlciI6ICJkZXZpY2VfaWQiLA0KCSJwcm92aWRlcl9kZXRhaWxzIjoNCgl7DQoJCSJwYXltZW50X3Byb3ZpZGVyIjogIlhTT0xMQSINCgl9LA0KCSJjbGllbnRfdHlwZSI6ICJVRTUiLA0KCSJidWlsZCI6ICJLYXJkcyAxLjM4LjIyNDMyLmxhdW5jaGVyIiwNCgkicGxhdGZvcm1fdHlwZSI6ICJXaW5kb3dzIiwNCgkiYXBwX2d1aWQiOiAiS2FyZHMiLA0KCSJ2ZXJzaW9uIjogIkthcmRzIDEuMzguMjI0MzIubGF1bmNoZXIiLA0KCSJwbGF0Zm9ybV9pbmZvIjogIntcclxuXHRcImRldmljZV9wcm9maWxlXCI6IFwiV2luZG93c1wiLFxyXG5cdFwiY3B1X3ZlbmRvclwiOiBcIkdlbnVpbmVJbnRlbFwiLFxyXG5cdFwiY3B1X2JyYW5kXCI6IFwiSW50ZWwoUikgQ29yZShUTSkgaTMtNDE2MCBDUFUgQCAzLjYwR0h6XCIsXHJcblx0XCJncHVfYnJhbmRcIjogXCJNaWNyb3NvZnQgUmVtb3RlIERpc3BsYXkgQWRhcHRlclwiLFxyXG5cdFwibnVtX2NvcmVzX3BoeXNpY2FsXCI6IDIsXHJcblx0XCJudW1fY29yZXNfbG9naWNhbFwiOiA0LFxyXG5cdFwicGh5c2ljYWxfbWVtb3J5X2diXCI6IDgsXHJcblx0XCJoYXNoXCI6IFwiNDE4ZDQ0MjAyOTk1MmM5ZDk4ZjRjYzQ1ZTM3MmIxM2UyYzYzMTczYTkxYmJlMzNmZjFmZTQyM2NmNzkxNjk0N1wiLFxyXG5cdFwibG9jYWxlXCI6IFwiemgtQ05cIlxyXG59IiwNCgkicGxhdGZvcm1fdmVyc2lvbiI6ICJXaW5kb3dzIDEwICgyMkgyKSBbMTAuMC4xOTA0NS40NTI5XSAiLA0KCSJhY2NvdW50X2xpbmtpbmciOiAiIiwNCgkibGFuZ3VhZ2UiOiAiemgtSGFucyIsDQoJImF1dG9tYXRpY19hY2NvdW50X2NyZWF0aW9uIjogdHJ1ZSwNCgkidXNlcm5hbWUiOiAiZGV2aWNlOldpbmRvd3MtNjU2RkIzQ0U0NjhCNDBDMTFERDZERTlDRUI1NDRERDkiLA0KCSJwYXNzd29yZCI6ICIwMDNDMTg0ODRBRjY4NDIxQ0UyRTE3ODg5RTAzMTVGRCINCn0=")

    response2 = requests.request("POST", "https://kards.live.1939api.com/session", headers=headers, data=payload)

    """
"" "

POST https://kards.live.1939api.com/session HTTP/1.1
Host: kards.live.1939api.com
Accept-Encoding: deflate, gzip
Accept: application/json
X-Api-Key: 1939-kards-5dcda429f:Kards 1.38.22432.launcher
Drift-Api-Key: 1939-kards-5dcda429f:Kards 1.38.22432.launcher
Content-Type: application/json
User-Agent: kards/++UE5+Release-5.5-CL-40574608 (http-eventloop) Windows/10.0.19045.1.256.64bit
Content-Length: 953

{
	"provider": "device_id",
	"provider_details":
	{
		"payment_provider": "XSOLLA"
	},
	"client_type": "UE5",
	"build": "Kards 1.38.22432.launcher",
	"platform_type": "Windows",
	"app_guid": "Kards",
	"version": "Kards 1.38.22432.launcher",
	"platform_info": "{\r\n\t\"device_profile\": \"Windows\",\r\n\t\"cpu_vendor\": \"GenuineIntel\",\r\n\t\"cpu_brand\": \"Intel(R) Core(TM) i3-4160 CPU @ 3.60GHz\",\r\n\t\"gpu_brand\": \"Microsoft Remote Display Adapter\",\r\n\t\"num_cores_physical\": 2,\r\n\t\"num_cores_logical\": 4,\r\n\t\"physical_memory_gb\": 8,\r\n\t\"hash\": \"418d442029952c9d98f4cc45e372b13e2c63173a91bbe33ff1fe423cf7916947\",\r\n\t\"locale\": \"zh-CN\"\r\n}",
	"platform_version": "Windows 10 (22H2) [10.0.19045.4529] ",
	"account_linking": "",
	"language": "zh-Hans",
	"automatic_account_creation": true,
	"username": "device:Windows-656FB3CE468B40C11DD6DE9CEB544DD9",
	"password": "003C18484AF68421CE2E17889E0315FD"
}


"" "

    """

    print(response2)

###############################print(response2)





def login_ss_(u,p):


    #设定


    dl_()


    global response2


    #无所谓了，这个是为了严谨

    resp=response2



    resp.raise_for_status()
    data = resp.json()
    return data.get('jwt') or data.get('token')












import os, sys

## 目标脚本绝对路径
file_path = r".\_def_get_ddddddd_.py"#"./"#r"C:\_jfdkls_ddddddd_fjdskl_dddddddddd_fdsjklsdf_ddddddddddddddddddddd_\_fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_.py"########@_test_fwk_kal_kah_ddddddddddddd_.py"
folder = os.path.dirname(file_path)
#
## 1) 把脚本目录加到模块搜索路径
if folder not in sys.path:
    sys.path.insert(0, folder)
#
print("fsdjlkfjdklsjklfjsdklj_")
#
## 2) 正常 import
##############@@@@@@@@@@@@@import _test_fwk_kal_kah_ddddddddddddd_
#
#
# 
# 
# #######"" "



# ── 引入你的处理函数 ──
#from _fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_ import aaa_ddd_


from _def_get_ddddddd_ import test_grd_







"""







import os, sys

## 目标脚本绝对路径
file_path = r"Y:\_fjklsdjl_dddddddddddddd_\_def_get_ddddddd_.py"#"./"#r"C:\_jfdkls_ddddddd_fjdskl_dddddddddd_fdsjklsdf_ddddddddddddddddddddd_\_fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_.py"########@_test_fwk_kal_kah_ddddddddddddd_.py"
folder = os.path.dirname(file_path)
#
## 1) 把脚本目录加到模块搜索路径
if folder not in sys.path:
    sys.path.insert(0, folder)
#
print("fsdjlkfjdklsjklfjsdklj_")
#
## 2) 正常 import
##############@@@@@@@@@@@@@import _test_fwk_kal_kah_ddddddddddddd_
#
#
# 
# 
# #######"" "



# ── 引入你的处理函数 ──
#from _fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_ import aaa_ddd_


from _def_get_ddddddd_ import test_grd_












































































































































































































"""




























import os, sys

## 目标脚本绝对路径
file_path_ = r".\_fjdskl_dddddddddddd_\_test_dddd_dddd_dddd_dddd_ddddddddddd_.py"#r"Y:\_fjklsdjl_dddddddddddddd_\_def_get_ddddddd_.py"#"./"#r"C:\_jfdkls_ddddddd_fjdskl_dddddddddd_fdsjklsdf_ddddddddddddddddddddd_\_fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_.py" ########@_test_fwk_kal_kah_ddddddddddddd_.py" #r"Y:\_jdfkl_fjdskl_fjdskl_fjdskl_fjdkldfskl_ddddd_d_d_d_ddddddddddd_\_test_dddd_dddd_dddd_dddd_ddddddddddd_.py"#r"Y:\_fjklsdjl_dddddddddddddd_\_def_get_ddddddd_.py"#"./"#r"C:\_jfdkls_ddddddd_fjdskl_dddddddddd_fdsjklsdf_ddddddddddddddddddddd_\_fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_.py"########@_test_fwk_kal_kah_ddddddddddddd_.py"
folder = os.path.dirname(file_path)
#
## 1) 把脚本目录加到模块搜索路径
if folder not in sys.path:
    sys.path.insert(0, folder)
#
print("fsdjlkfjdklsjklfjsdklj_2_")
#
## 2) 正常 import
##############@@@@@@@@@@@@@import _test_fwk_kal_kah_ddddddddddddd_
#
#
# 
# 
# #######"" "



# ── 引入你的处理函数 ──
#from _fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_ import aaa_ddd_


#from _def_get_ddddddd_ import test_grd_



#from _test_dddd_dddd_dddd_dddd_ddddddddddd_.py


################################################################################################################################################################################################################################from _test_dddd_dddd_dddd_dddd_ddddddddddd_ import 


#################################################################import _test_dddd_dddd_dddd_dddd_ddddddddddd_ as sm#_test_dddd_dddd_dddd_dddd_ddddddddddd_ as sm

"""

import _test_dddd_dddd_dddd_dddd_ddddddddddd_ as sm#_test_dddd_dddd_dddd_dddd_ddddddddddd_ as sm





##############################################################_test_dddd_dddd_dddd_dddd_ddddddddddd_


#################################################################################from _test_dddd_dddd_dddd_dddd_ddddddddddd_ import get_jwt, kards_request#session_mgr import get_jwt, kards_request








from _test_dddd_dddd_dddd_dddd_ddddddddddd_ import get_jwt, kards_request#session_mgr import get_jwt, kards_request



"""
#


"""


aaa_=sm.get_jwt()
aaa_2+


aaa_2+


2

aaa_2_=sm.get_jwt



















































"""



########################################################################################new import

#"" "


import os
import importlib.util

###############################_


# 绝对路径
file_path = file_path_#r"Y:\…\_test_dddd_dddd_dddd_dddd_ddddddddddd_.py"

# 模块名：取文件名（去掉 .py）
module_name = os.path.splitext(os.path.basename(file_path))[0]

# 1) 生成 spec
spec = importlib.util.spec_from_file_location(module_name, file_path)
# 2) 创建模块对象
module = importlib.util.module_from_spec(spec)

sm=module

# 3) 执行加载
spec.loader.exec_module(sm)

# 模块里的函数／变量，都在 module 下
#jwt = module.get_jwt(...)
#resp = module.kards_request(...)





# 假设你想要导入的函数叫 `foo`：
#foo = getattr(sm,"get_jwt") #"foo")     # foo 现在就是原模块里的函数对象

# 直接调用
#result = foo(arg1, arg2)



####################################################################################fds_=getattr(sm,"get_jwt")




get_jwt=getattr(sm,"get_jwt")


kards_request=getattr(sm,"kards_request")










#"" "






#def xxx_(xxx_):

  ##  /xxx_

  #  return resp






"""



from session_mgr import get_jwt, kards_request

# ======= 初始化 =======
jwt_token = get_jwt()          # 确保本地有一个可用 JWT
HEADERS = {"Authorization": f"JWT {jwt_token}", "Accept": "application/json"}

# 如果只想写原来的 requests：
resp = kards_request("GET", "/matches/v2/")
data = resp.json()

# 如果仍要手工调用 requests 也行，只是过期时不会自动续约：
# import requests
# resp = requests.get(BASE_URL + "/matches/v2/", headers=HEADERS, verify=False)

# =============================================================
# 例如重写你原来的 get_match_ids：
def get_match_ids():
    resp = kards_request("GET", "/matches/v2/")
    return [m["match_id"] for m in resp.json().get("matches", [])]















    







"""



def do_mulligan_(id_,dz_):

    fwk_=f"https://kards.live.1939api.com"

    #grd_="{fwk_}/{}"


    grd_=f"{fwk_}/match/v2/{id_}"#/"#mu"

    tmd_=f"{grd_}/mulligan/{dz_}"


    #fjsdkljfkls_=""{fwk_}/match/v2/{id_}/""


    fjdsklfjklsdjfjsdl_=f"{fwk_}/match/v2/{id_}/mulligan/{dz_}"
 #   fjsdkljfklsdjklfjklsd

 #   fjdklsfjkls

  #  fsdjlkfsd

  #  fdsjlfkjdskl

  #  fjdsklfjklsdjklfjsdlf


  #  fjdsklfjklsdjklfjsd_fjsdljflsd_fjkdsl_fjdsklfjlsd_fjdsflsdj_=f"{fwk_}/match/v2/{id_}/mulligan/{dz_}"


   ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################## ############# resp_2_=resp





























































    resp_2_ = requests.get(fjdsklfjklsdjfjsdl_,headers=HEADERS, verify=False, proxies=PROXIES)#f"{BASE_URL}/matches/v2/", headers=HEADERS, verify=False, proxies=PROXIES)


    #t z m y n l g z d,          z s n g z h z q g


                              ###################################################### t z m y m  y l l g z d d d d d                 t z m y l l g z d d d d d d d d d d ,(),            ,(),





  #  print(resp_2_)

    print(resp_2_.text)


    aaa_test_data_dfds_=resp_2_.json()


    return aaa_test_data_dfds_




























#################HEADERS,PROXIES=0


HEADERS, PROXIES = {}, {}


#=""





#####################################################################################################HEADERS,PROXIES=test_grd_(token_)








def get_field_(obj, path):
    """通用字段提取：path 格式 'a.b[0].c' 支持列表索引"""
    cur = obj
    for part in path.split('.'):
        if '[' in part and ']' in part:
            key, idx = part[:-1].split('[')
            cur = cur.get(key, [])
            cur = cur[int(idx)] if len(cur) > int(idx) else None
        else:
            cur = cur.get(part) if isinstance(cur, dict) else None
        if cur is None: break
    return cur



############################################



"""


data_=""

data_2_=""""""


data_=""




























"""





import time
import msvcrt

def input_with_timeout_win(prompt: str, timeout: int, default: str) -> str:
    """
    Windows 下带超时的输入：
      - 每 0.1s 检测一次键盘输入
      - 超时后返回 default
    """
    print(prompt, end='', flush=True)
    buf = ''
    start = time.time()
    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getwch()  # 读取宽字符
            if ch in ('\r', '\n'):
                # 回车，结束输入
                print() 
                return buf
            elif ch == '\b':
                # 处理退格
                buf = buf[:-1]
                print('\b \b', end='', flush=True)
            else:
                buf += ch
                print(ch, end='', flush=True)
        # 超时判断
        if time.time() - start > timeout:
            print(f"\n[超时 {timeout}s] 自动返回默认值: '{default}'")
            return default
        time.sleep(0.1)  # 降低 CPU 占用

#if __name__ == "__main__":
 #   while True:
  #      s = input_with_timeout_win("请输入指令（30s 内）：", 30, "or")
   #     print(f"接收到：{s}")
    #    if s == "or":
     #       print("检测到 'or'，退出程序。")
      #      break
       # # 其他逻辑继续……












data_=""



data_2_=""













def get_match_ids():

#要改变， 不得不tian

#3####前面那个

###########已关闭

#####################y g b     b d b t         

#############################################(0fdsjfkdjsdfl
 ##################################################################)


#h m z g z x 


#fjklsdjklfj



#y g b      b d b try
    

   # fjsdklfsdkl



  #   h m z g z s        d d d d dd d d d d d d         d d d d d dd  d d ,(),
    

  #  ,(),

    resp = requests.get(f"{BASE_URL}/matches/v2/", headers=HEADERS, verify=False, proxies=PROXIES)
    data = resp.json()
    # 示例：提取 token（若在响应中）
    #pirnt()


    def aaa_200():
    
        print("fsdjj_")#fsdh#fwk_)


   ######################################################################################################################### print(str(str(resp.status_code)"()"))


    print(str(str(resp.status_code)+"()"))


   ####################################################################################################################################################################################################################################################################################################### print(str(("aaa_"+str(resp.status_code))()))

    print(str(("aaa_"+str(resp.status_code))+"()"))

    print(resp.status_code)


    #####################################print()




    print(resp.text)


    data_=data



######################\

    print("data_:")

    print(data_)

 #   global token_

   # token = get_field_(data, 'token')
  #  print(f"[core] token: {token_}")



   # return [get_field_(m, 'match_id') for m in data_.get('matches', [])]


   #r



##################################2 


################################################fsdfdsfs

    aaa_=[]

    fjdskl_={}


   # global data_

    global data_2_#\
    


    data_2_=data_


    ######狗日的，没安检测循环

    if data_==None:

        ######is None

        return None

    """

2

sdfsdfsdfs


fdsfsd=2


2=fdsfsd


fsdfsd=data_


2=fdsfdsf


    """


















    """





fjklsd=data_


fdsfsdf=2


2=data_\



2=data_


fklsd;=data_


jfkldsjfkljsdkljfkljsdklfklsd=2


    """

    aaa_.append(data_['match_and_starting_data']['match']['match_id'])


  #################################################################################  return #match_data['match_and_starting_data']['match']['match_id']



    return data_['match_and_starting_data']['match']['match_id']#############,data_

#狗日的

#grd

#shit shti shtisthisthishithsihtithishi

###############################################################################################################################################################

    return [get_field_(m, 'match_id') for m in data_.get('match', [])]


  #########################################################################################################  return get_field_(m, 'match_id')




token_=""


token_=Jwt_fdsjfklds_





def fetch_match_info(mid):
    resp = requests.get(f"{BASE_URL}/matches/v2/{mid}", headers=HEADERS, verify=False, proxies=PROXIES)
    data = resp.json()
    # 提取状态示例
    status = get_field_(data, 'match_and_starting_data.match.status')
    print(f"[core] match_id: {mid}, status: {status}")
    return data


#def generic_post(path, payload=None):
 #   resp = requests.post(f"{BASE_URL}{path}", headers=HEADERS, json=payload,
  #                       verify=False, proxies=PROXIES)#XIESPRO)
   # data = resp.json()
   # # 提取可能的卡组字段
   # deck = get_field(data, 'starting_hands')
   # print(f"[core] POST {path} returned starting_hands: {deck}")
   # return data


def poll_actions(mid, min_id, opp_id):
    all_raw = []
    while True:
        params = {'min_action_id': min_id, 'opponent_id': opp_id, 'time_since_opponent_ping': 0}
        resp = requests.get(f"{BASE_URL}/matches/v2/{mid}/actions", headers=HEADERS,
                            params=params, verify=False, proxies=PROXIES)
        
      #  put


        data = resp.json()
        status = get_field_(data, 'match.status') or get_field_(data, 'match_and_starting_data.match.status')
        print(f"[core] polling status: {status}")
        acts = data.get('actions', [])
        if not acts and status != 'running': break
        all_raw += acts
        min_id = (int(acts[-1][1:7]) + 1) if acts else min_id
        time.sleep(POLL_INTERVAL)
    return all_raw
#
  #  """

 #   def fetch_match_info(mid):
  #     resp = requests.get(f"{BASE_URL}/matches/v2/{mid}", headers=HEADERS, verify=False, proxies=PROXIES)
  #  data = resp.json()
 #   # 提取状态示例
 #   status = get_field(data, 'match_and_starting_data.match.status')
 #   print(f"[core] match_id: {mid}, status: {status}")
 #   return data

    
 #   """

    return

    resp = requests.get(f"{BASE_URL}/matches/v2/{mid}", headers=HEADERS, verify=False, proxies=PROXIES)
    data = resp.json()
    # 提取状态示例
    status = get_field(data, 'match_and_starting_data.match.status')
    print(f"[core] match_id: {mid}, status: {status}")
    return data





    status = get_field(data, 'match_and_starting_data.match.status')
    print(f"[core] match_id: {mid}, status: {status}")
    return data





    resp = requests.get(f"{BASE_URL}/matches/v2/{mid}", headers=HEADERS, verify=False, proxies=PROXIES)
    data = resp.json()
    # 提取状态示例


    status = get_field(data, "")

  #  running loading fin
    

"""

################################################################# #################################################################################

def get_match_ids():
    "" "获取所有 match_id 列表"" "
    resp = requests.get(f"{BASE_URL}/matches/v2/", headers=HEADERS, verify=False, proxies=PROXIES)
    resp.raise_for_status()
    data = resp.json()
    return [m['match_id'] for m in data.get('matches', [])]



###########################################################match v2


def fetch_match_info(match_id):
    "" "
    获取比赛基础信息及初始牌组：
      - player_id_left/right
      - deck_left/right 列表 of card dicts
    返回 tuple(player_ids: list[int], decks: list[list[int]])
    "" "
    resp = requests.get(f"{BASE_URL}/matches/v2/{match_id}", headers=HEADERS,
                        verify=False, proxies=PROXIES)
    resp.raise_for_status()
    info = resp.json().get('match_and_starting_data', {})
    m = info.get('match', {})
    sd = info.get('starting_data', {})
    pids = [m.get('player_id_left'), m.get('player_id_right')]
    decks = []
    for side in ('deck_left', 'deck_right'):
        raw = sd.get(side, [])
        decks.append([card.get('card_id') for card in raw if 'card_id' in card])
    return pids, decks






def fetch_match_info_2_(match_id):
    "" "
    获取比赛基础信息及初始牌组：
      - player_id_left/right
      - deck_left/right 列表 of card dicts
    返回 tuple(player_ids: list[int], decks: list[list[int]])
    "" "
    resp = requests.get(f"{BASE_URL}/matches/v2/", headers=HEADERS,
                        verify=False, proxies=PROXIES)
    resp.raise_for_status()
    info = resp.json().get('match_and_starting_data', {})
    m = info.get('match', {})
    sd = info.get('starting_data', {})
    pids = [m.get('player_id_left'), m.get('player_id_right')]
    decks = []
    for side in ('deck_left', 'deck_right'):
        raw = sd.get(side, [])
        decks.append([card.get('card_id') for card in raw if 'card_id' in card])
    return pids, decks









def fetch_match_actions(match_id):
    ""                                         "获取完整对局 action 日志（JSON 列表）""                            ########################## "
    resp = requests.get(f"{BASE_URL}/matches/v2/{match_id}/actions", headers=HEADERS,
                        verify=False, proxies=PROXIES)
    resp.raise_for_status()
    return resp.json()






def extract_actions_cards(actions):
    "" "从 actions 中提取所有使用过的 card_id 列表"" "
    cards = set()
    for act in actions:
        payload = act.get('payload', {}) or {}
        cid = payload.get('card_id') or payload.get('cardIndex')
        if cid is not None:
            cards.add(int(cid))
    return cards





"""




# kill     shit     ,(),        ,(),as


def load_dataset(path):
    """加载本地卡牌元数据（JSON/CSV），映射 id->dict，id 保持原始字符串格式"""
    data = {}
    p = Path(path)
    if p.suffix == '.json':
        raw = json.loads(p.read_text(encoding='utf-8'))
        for item in raw:
            raw_id = item.get('id') or item.get('card_index') or ''
            if not raw_id:
                # 没有 id，则跳过
                continue
            # 直接以字符串 id 作为 key
            data[str(raw_id)] = item

    else:
        with p.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_id = row.get('id') or row.get('card_index') or ''
                if not raw_id:
                    continue
                data[str(raw_id)] = row

    return data





#def load_nfile(path):
 #   """读取参考卡牌列表，一行一个 id"""
  #  return set(int(line.strip()) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip())


"""


from pathlib import Path

def load_nfile(path):
    "" "
    读取参考卡牌列表，一行一个 id（整数），返回 set[int]。
    - path=None、'' 或 'None' → 返回空集
    - 文件不存在       → 抛 FileNotFoundError
    - 非整数行         → 跳过（并打印警告）
    "" "
    # 1) 处理 None、空字符串或字面 "None"
    if not path or str(path).strip().lower() == "none":
        return set()

    p = Path(path)
    # 2) 文件存在性检查
    if not p.is_file():
        raise FileNotFoundError(f"参考列表文件不存在：{path}")

    ids = set()
    # 3) 逐行读取并尝试转 int
    for line in p.read_text(encoding='utf-8').splitlines():
        raw = line.strip()
        if not raw:
            continue  # 跳过空行
        try:
            ids.add(int(raw))
        except ValueError:
            # 警告并跳过非纯数字行
            print(f"WARNING: 跳过无效行（非整数）：{raw!r}")
    return ids


"""

def compare_sets(extracted, reference):
    """比较两个集合，返回差异列表"""
    ext = set(extracted)
    return sorted(ext - reference), sorted(reference - ext)


from pathlib import Path

def load_nfile(path):
    """
    读取参考卡牌列表，一行一个 id（整数），返回 set[int]。
    - path=None、'' 或 'None' → 返回空集
    - 文件不存在       → 抛 FileNotFoundError
    - 非整数行         → 跳过（并打印警告）
    """
    # 1) 处理 None、空字符串或字面 "None"
    if not path or str(path).strip().lower() == "none":
        return set()

    p = Path(path)
    # 2) 文件存在性检查
    if not p.is_file():
        raise FileNotFoundError(f"参考列表文件不存在：{path}")

    ids = set()
    # 3) 逐行读取并尝试转 int
    for line in p.read_text(encoding='utf-8').splitlines():
        raw = line.strip()
        if not raw:
            continue  # 跳过空行
        try:
            ids.add(int(raw))
        except ValueError:
            # 警告并跳过非纯数字行
            print(f"WARNING: 跳过无效行（非整数）：{raw!r}")
    return ids






def format_cards(card_list, dataset):
    """将 ID 列表映射为字符串列表 '[ID] Name'"""
    formatted = []
    for cid in card_list:
        info = dataset.get(cid, {})
        name = info.get('title', {}).get('en-EN') or info.get('name') or info.get('cardId') or 'N/A'
        formatted.append(f"[{cid}] {name}")
    return formatted

"""
def main():
    parser = argparse.ArgumentParser(description="Kards Match Extractor v2.1 with Name Mapping")
    parser.add_argument('--nfile', required=True, help='参考卡牌列表文件')
    parser.add_argument('--dataset', required=True, help='卡牌元数据 JSON/CSV')
    parser.add_argument('--detail', action='store_true', help='输出差异卡牌详细信息')
    args = parser.parse_args()

    # 加载本地数据
    dataset = load_dataset(args.dataset)
    ref_set = load_nfile(args.nfile)

    # 获取 match 列表
    match_ids = get_match_ids()
    print(f"共获取到 {len(match_ids)} 场比赛 (match_id)。")

    all_actions_cards = set()
    all_starting_decks = []
    all_player_ids = []

    for mid in match_ids:
        pids, decks = fetch_match_info(mid)
        all_player_ids.extend(pids)
        all_starting_decks.extend(decks)

        acts = fetch_match_actions(mid)
        cards = extract_actions_cards(acts)
        all_actions_cards |= cards
        time.sleep(0.1)

    # 去重
    player_ids = sorted(set(all_player_ids))
    starting_cards = sorted(set(sum(all_starting_decks, [])))

    # 输出玩家 ID
    print("玩家 ID:", ", ".join(str(pid) for pid in player_ids))

    # 输出初始牌组卡牌及名称
    print("初始牌组包含卡牌:")
    for line in format_cards(starting_cards, dataset):
        print(" ", line)

    # 比较
    only_in_actions, only_in_ref = compare_sets(all_actions_cards, ref_set)

    # 输出差异并映射名称
    print("\n日志使用但参考文件无：")
    for line in format_cards(only_in_actions, dataset):
        print(" ", line)

    print("\n参考文件有但日志未用：")
    for line in format_cards(only_in_ref, dataset):
        print(" ", line)

    # 详情
    if args.detail:
        print("\n-- 显示详细元数据 --")
        for cid in only_in_actions + only_in_ref:
            info = dataset.get(cid, {})
            print(f"\n>> 卡牌 {cid} 详情:")
            for k, v in info.items():
                print(f"   {k}: {v}")

if __name__ == '__main__':
    main()
"""






#################







##########################################











"""




























































































































































































































































































































































































"""










def format_starting_deck(deck, dataset):
    """格式化起始手牌（deck_left）信息"""
    lines = []
    for entry in deck:
        cid = entry.get('card_id')
        raw_name = entry.get('name', '')
        name_key = raw_name.split('_', 2)[-1]  # 取第二个下划线之后部分







        matched = None




        for k, v in dataset.items():
            if (
                k == cid or
                v.get('id') == cid or
                v.get('name') == name_key or


                v.get('id')==name_key or



                v.get('title', {}).get('zh-Hans', '') == name_key
            ):
                matched = v
                break
        if matched:
            name = matched.get('name') or matched.get('title', {}).get('zh-Hans', str(cid))
            desc = matched.get('desc') or matched.get('text', {}).get('zh-Hans', '')
        else:

          ##############################################################################################################################################  raw_name

            raw_name_=raw_name


             #################n d d x c d d b        z t q d d d d d d dd d d  d d d d d 
            name = name_key
            desc = ''
        lines.append(f"初始卡牌ID {cid}: {name} 说明: {desc}     {raw_name_}")
    return lines


























def main():
    # 1. 登录并获取 JWT

    global token_


 #S   不导入pisi d m y         ,(),


#                                                                                                                                                                         ,(),

  #  token = login_ss_(None,None)#login_session()

    

  ##################################################  dl_()

   ####################### fiel
    """

    parser.add_argument('--force-login', action='store_true')


   
################################w
   # jwt = sm.get_jwt(force=True)   # 不管三七二十一重登


    jwt_ = get_jwt(force=args.force_login)

   ########################################################### token_ = login_ss_(None,None)#login_session()

    """



  #  print(f"登录成功，JWT: {token_}")




    



   ######################################################################################################### token_=login_ss_(None,None)





    print(f"，JWT: {token_}")




############一天登一次，不要频繁登,(),

##########################################,90,







    # 2. 加载本地数据集与参考列表
    dataset = load_dataset(args.dataset)



    reference = load_nfile(args.nfile)






    





    
################## # 后续逻辑可以放心地用 reference，无需额外判断
  ############################################################################################################## #################################################################  if some_card_id in reference:
       #################################################################################################################################################################################################################################################### ...




  #  parser.add_argument('--force-login', action='store_true')


   ######################################### import parser


  #  import argparse
  #  parser_ = argparse.ArgumentParser()


  #  parser_.add_argument('--force-login', action='store_true')


   # args_ = parser_.parse_args()
 
    args_=args

#...

    if args_.force_login:

        jwt_ = get_jwt(force=args.force_login)

        token_=jwt_

        print("grd_dddddddd_")

   # jwt = get_jwt(force=args.force_login)


    global HEADERS,PROXIES

    HEADERS,PROXIES,player_id_=test_grd_(token_)






    # 3. 获取所有 match_id
  #  match_ids,data_2_ = get_match_ids()
   # print(f"共获取到 {len(match_ids)} 个 match_id")


   #print

 #  if match_ids = get_match_ids() is not None:


    """



    if match_ids is not None:
        
        run #= get_match_ids() is not None:

        break

    is NOne :

            break
            

    """


    match_ids = get_match_ids()



  ################ if match_ids = get_match_ids() is not None:

    if match_ids is not None:
        
        print("run")###########_run #= get_match_ids() is not None:

       # break

    #is NOne :


    if match_ids is None:

         #   break


        return



    match_ids = get_match_ids()







  #   match_ids,data_2_ = get_match_ids()



   














  #   match_ids,data_2_ = get_match_ids()






















    print(f"狗日的.{match_ids},kill all human,")


  #####################################################################################################################################  print("狗日的.{match_ids},kill all human,")

    print(match_ids)


    ########sys.

   ####### do_mulligan()


    import sys

   # sys.exit()



##############################################################


    ###########y l 

    # 4. 遍历每个 match:
    used_cards = set()
  
    aaa_22222_=[]

    aaa_22222_.append(match_ids)
#a
    for mid in aaa_22222_:##match_ids:
        # 4.1 获取比赛信息
      ###########################################  match_data = fetch_match_info(mid)

        match_data=data_2_


        #日你妈                         提结果                                                                也有,(),


                                                          #,(),


                                                          #######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################bianshuyueduo       y r y c g z         x d x h x h d j l y d         b s y d        x dc y r y c g z         x d x  hx h d j l y d    ddddddddddddd<(),    ,(),

        # 4.2 初始化洗牌阶段
      #  do_mulligan(mid, 'left')
      #  do_mulligan(mid, 'right')

        # 4.3 轮询获取动作日志
     #   raw_actions = poll_actions(mid, min_id=1, opponent_id=match_data['match_and_starting_data']['match']['player_id_right'])

##################




        #满级ai

        ##########################################################################################################################################哪个是自己 另一个就是bier



        






       # return [get_field_(m, 'match_id') for m in data_.get('match', [])]


        if match_data['match_and_starting_data']['match']['player_id_right']==player_id_:
    

            print("left_")
  
       # else:


        

        elif match_data['match_and_starting_data']['match']['player_id_right']!=player_id_:

            print("right")

        elif match_data['match_and_starting_data']['match']['player_id_left']==player_id_:


            #########################



            print("right_")






#match_data['match_and_starting_data']['match']['player_id_left']##;ef']==player_id_


        elif match_data['match_and_starting_data']['match']['player_id_left']!=player_id_:#l']==player_id_


            print("right_2_")

            print("right_")

            print("left_")

        # 4.4 提取使用过的卡牌
      #  used_cards |= extract_used_cards(raw_actions)












    # 5. 对比参考列表






    only_used, only_ref = compare_sets(used_cards, reference)


############狗日的     老子当时整了lsit

#g rd             lz d s z l list
#
 #       grd                             l z d s z l        list,(),
#
#
#
                                                                            #,(),



    
  #  used_cards = set()
    # 4. 遍历每场比赛
    for mid in aaa_22222_:#match_ids:
        #match_data = fetch_match_info(mid)











        """
























































































































































































































































































































































        """


















































#######################################################################################################################################"" "































































































































































##

























































































































































##############"" " 




































































############ "" "                 "" "




























########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################## ##################

        aaa_=["left","right"]


       # aaa_[x_]

       ############### y=x_^1























        #"" "   





     






      #  for i in fjlsd_(a,b):

       #     print()



      # ##########  print(f"\n比赛 {mid} 初始牌组信息：")
      # ########  for line in format_starting_deck(deck_n_, dataset):
       ############### #######################     print(line)


































        








 




 #match_data = fetch_match_info(mid)






        match_info=match_ids





# match_data = fetch_match_info(mid)

        match_info=match_data#\
        




     #    match_data = fetch_match_info(mid)

        match_info=data_2_


 #match_data = fetch_match_info(mid)






































        # 判断我方位置与对手 ID
        m = match_info.get('match', {})
        left_id = m.get('player_id_left')
        right_id = m.get('player_id_right')
        if player_id_ == left_id:
            opponent_id = right_id

            infi_o_="right_"


            infi_o_2_="right"








            info_dddd_2_=infi_o_2_


            x_=1

            print("1")










        else:
            opponent_id = left_id

            info_dddd_2_="left"


            x_=0

            print("0")





















































































































































        """


        print("0就 right is 自己       1就left is zj")














































                    y 0                                                                                                                                                                                                                                                                            z 1
        










































































































































































































































































































































































































































































































































































































































































































y 0 z 1








































































fksdl;fsdj















                                                                                                                                                                                                                                                                                                                                                           y 0 z 1,(),

,(),






sdfsdfsdfsdfsdf





























































































































































































































































































































































































fjlksdjklfjsdl

























    y0 z 1,(),

,(),










                                                                                                                                                         y 0 z 1,(),

,(),



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  y0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      y 0 z 1 d d d d d                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
























































































                                                                                                                                                                   y 0 z 1 d d d d d                                                                                                                                                                                                                                                                                                                                                               d d d d d,(),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               ,(),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       ,(),


































    "" "


      ########################################################################################################################################################################################  "" "


    """

      #######################################  info_dddd_2_=infi_o_2_



##########当时wangshan l


###################################################################

################################################################################################################\





########################################################################################################################################################################################################################################

################################################################################################################################################################################################################################################################################################################################################################################ d sf ds fsd kfl;sd fjsdkl fklsd jfdsj l ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################\\\


#######################################"" " "" "#########\\






        


        n_fdsfsd_=aaa_[x_]

        y=x_^1


# t c q,       w z c h l d d d d d d


                 ############################################################################################################################################################################################################################################################ ######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################## ######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################## ######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################## ############################################################################################################################################################################################################################################################ ############################################################################################################################################################################################################################################################ ######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################## ######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################## ######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################## ############################################################################################################################################################################################################################################################################################################                              t c q              w 
        


        # t c q                                                                                                                                                                                                                                                                                      t c q        w z c h l d,

     #   fjkldjklsf t c q     w z x h l d,(),

       # ,(),



        match_data_2_=data_2_


        match_data=match_data_2_




        ############## kjdksjfsdl jkldj klsdjfkl sdkl jksdj klfjsdkl jsdklj klsdjl sdkl lsdflsdf jkl_fdjkl jsdklj ksdj fjssdfksdf klsdfkl_


        match_info = match_data.get('match_and_starting_data', {})
        # 输出起始牌组 deck_left
        deck_n_fsdfds_ = match_info.get('starting_data', {}).get(f'deck_{info_dddd_2_}', [])

##############################################################fdsfjsdklfjsdlk_=[]



        deck_n_ = match_info.get('starting_data', {}).get(f'deck_{aaa_[y]}', [])#info_dddd_2_}', [])


        deck_n_2_ = match_info.get('starting_data', {}).get(f'deck_{aaa_[x_]}',[])   #info_dddd_2_}', [])




        y_dfs_=do_mulligan_(match_ids,aaa_[y])

        x_fdsfsd_=do_mulligan_(match_ids,aaa_[x_])


        #y_dfs_.get("aaa_",{}).get(f"fwk_{grd_}",{}),[]




#成品暂时不写

      #半成品



                              ############################################################################################################################################################################# get x d c b d d d d d d       d d d d d        






                        #      get("fds_",{}).get("fsdfsd_",[])
        





########## dsjfkljsdkl jklsdjfk jsd_


                                     #fdjsklfjklsdjklfjsdkljfskl——












       ##### aaa_[y]

####################################################################aaa_[x_]























































































































































































































































































        aaa_=["left","right"]






       #     先处理对手

           #        先处理自己


           



      #  "" "




#########################################################$$$$$$$$$$$$$$$$$$$$




#########################################################################################get list     f y d d d d ,(),



#################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### #################################################################################### ,(),






        """





        x

        aaa_[x_]

        |x_-1|


        if aaa_[x_]==0:
     
     x=0

           aaa_

                    | x-1|






                    



        """














#否者反之


#######djsfklsdklfjklsdjklfjsdkl jklfjkl sdj fklsdjkl fjsdkljfkl sdklj fklsdj 


         ########         c d,              c def




 ##########  f;sdkfkdl;skfkl;sdjklfjkldsjklfjdklsjfkljsdkljfkljdskljfkldjslfsdkljklfsdklflsdjklfsdfjkl




       #############
       # 
       # 
       # 
       # 
       # 
       #                                                                                        c d                                                        c d,(),                                                                                                                                                                                                                                                                                                   ,(),



        aaa_[x_]

#######################################################################################################################################################################################|x_-1|


##############################################################################################################################################################################################################################################################################^2 ^0.5


##################################################1-x


       ############################################################ y=x^1


        y=x_^1


                      

#下面往上，上面往下

                         #######################                                                                                                                                                                                                                                    人          jb


    



   #     aaa_[x_]

       #     aaa_[y]


       #    aaa_[y]




        """

                                 aaa_[x_]



                                                 x_

                                                       y



y


                  x_





                                                                                                                                                                                                                 aaa_[x_]









    aaa_[y]
























            """




















                                                                             #################################################                                                                                                                                                                                                                    aaa_[x_]

    






        """

aaa_[y]



aaa_[y]



aaa_[x_]






aaa_[x_]

aaa_[y]

aaa_[y]

aaa_[x_]




        """






      #  for i in fjlsd_(a,b):

       #     print()



        print(f"\n比赛 {mid} 初始牌组信息：")



        for line in format_starting_deck(deck_n_, dataset):
            print(line)
           ########################################################################################################################## \\


        print("fkdsl;fksdjl_ jdklfjlsdk_fjdklsjfsdkl_fjdskljfklsd_fjdklsjfklsd_fjdskljfsdjkl_")



        for line_ in format_starting_deck(deck_n_2_, dataset):
            print(line_)


        #，at



        #match_id



      ################################################### @ time.sleep(30)





        y_dfs_=do_mulligan_(match_ids,aaa_[y])

        x_fdsfsd_=do_mulligan_(match_ids,aaa_[x_])


      #  wli


        while True:

            a_=input("0 1")


            a_=input_with_timeout_win("请输入指令（30s 内）：", 30, 0)

            if a_==0:

               # break

               continue


        """


import time
import msvcrt

def input_with_timeout_win(prompt: str, timeout: int, default: str) -> str:
    "" "
   # Windows 下带超时的输入：
   #   - 每 0.1s 检测一次键盘输入
  #    - 超时后返回 default
    "" "
    print(prompt, end='', flush=True)
    buf = ''
    start = time.time()
    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getwch()  # 读取宽字符
            if ch in ('\r', '\n'):
                # 回车，结束输入
                print() 
                return buf
            elif ch == '\b':
                # 处理退格
                buf = buf[:-1]
                print('\b \b', end='', flush=True)
            else:
                buf += ch
                print(ch, end='', flush=True)
        # 超时判断
        if time.time() - start > timeout:
            print(f"\n[超时 {timeout}s] 自动返回默认值: '{default}'")
            return default
        time.sleep(0.1)  # 降低 CPU 占用

if __name__ == "__main__":
    while True:
        s = input_with_timeout_win("请输入指令（30s 内）：", 30, "or")
        print(f"接收到：{s}")
        if s == "or":
            print("检测到 'or'，退出程序。")
            break
        # 其他逻辑继续……






        












        








        """










######################狗日的，上次有超时，这次不搞了,(),

################################################################,(),

            elif a_==1:


                y_dfs_=do_mulligan_(match_ids,aaa_[y])

                x_fdsfsd_=do_mulligan_(match_ids,aaa_[x_])

                break
    

            elif a_==2:
                y_dfs_=do_mulligan_(match_ids,aaa_[y])

                x_fdsfsd_=do_mulligan_(match_ids,aaa_[x_])




            elif a_=="break":

                break








        print(y_dfs_)

       ############################################################################# print(x_fds_fsd_)

       ############################################################################################################################################################### #################################################################################################### -

        print(x_fdsfsd_)




























































 




 #match_data = fetch_match_info(mid)






        match_info=match_ids





# match_data = fetch_match_info(mid)

        match_info=match_data#\
        




     #    match_data = fetch_match_info(mid)

        match_info=data_2_


 #match_data = fetch_match_info(mid)















        # 判断我方位置与对手 ID
        m = match_info.get('match', {})
        left_id = m.get('player_id_left')
        right_id = m.get('player_id_right')
        if player_id_ == left_id:
            opponent_id = right_id

            infi_o_="right_"


            infi_o_2_="right"








            info_dddd_2_=infi_o_2_


            x_=1







            """

                   0
            

                                 1


                                         """











        else:
            opponent_id = left_id

            info_dddd_2_="left"


            x_=0



            """



                                                  0



                                                  """


       ################################################################ info_dddd_2_=infi_o_2_
####################\


        """####         不想了，头发少了


        本来相对先那个xdct, ()<

                                    ,(), x d c d d,(),

                                           ,(),


                                           概念renzhe l


        if info_dddd_2_=="left":
    
    0

             1


                 x_=1


                     right_id



             right_id



                          1
elif info_fdsfdsjl_=="right":



                         = 0

                                       jfklsdkl


                                                         x_=0



                               =    1

                                             jfsdkljfklsd


        """
                       


       ############################################################################################################### ################################################################################################  ############################################################################################################################################################################################################################################################################################################################################# f"deck_{info_dddd_2_}"



        ###########################################################z j n y y p d a, z g y s m z p d d ,(),
    
    ####################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################,90,

        # 获取并提取已使用卡牌
     # @  raw_actions = poll_actions(mid, min_id=1, opponent_id=opponent_id)
       # used_cards |= extract_used_cards(raw_actions)








































































































































































































































































###########################################################################################################################################################################



































































































    


    # 6. 输出结果
    print("日志使用但参考无：")
    for line in format_cards(only_used, dataset): print(line)

    print("参考有但日志无：")
    for line in format_cards(only_ref, dataset): print(line)


  #  break

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--nfile', required=True)
    parser.add_argument('--dataset', required=True)

    parser.add_argument('--force-login', action='store_true')

    args = parser.parse_args()
    main()
