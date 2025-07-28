"""

#!/usr/bin/env python3
"" "



Kards Match Extractor v2.1
功能：
  1. 从 `matches/v2/` 接口获取 match_id 列表。
  2. 对每个 match_id：
     - 获取比赛基础信息（含 player_id_left/right 与 deck_left/right）。
     - 提取双方初始牌组中的卡牌 ID 列表。
     - 获取完整对局 action 日志并提取使用卡牌。
  3. 加载本地 nfile（参考卡牌列表），比较日志和参考文件差异。
  4. 支持命令行参数：
     --nfile      本地参考列表文件路径。
     --dataset    本地卡牌数据集路径（JSON/CSV）。
     --detail     是否输出交互式详情（True/False）。

更新：
  - 打印时将 ID 映射为名称（来自数据集），格式：`[ID] Name`。

运行示例：
  python kards_match_extractor.py \
    --nfile nfile.txt --dataset cards.json --detail True
"" "




"" "

import argparse
import json
import time
import requests
import csv
from pathlib import Path
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)


"" "

############################################################################tokne


#################################################################################################################################################################try
  #########################################################################################################################################################################################################################################################################################################################################################################################################################  okn



"" "




token_test_dddddddddd_=""





# 全局配置
BASE_URL = "https://kards.live.1939api.com"
HEADERS = {
    'Accept': 'application/json',
    'X-Api-Key': '1939-kards-5dcda429f:Kards 1.38.22432.launcher',
    'Drift-Api-Key': '1939-kards-5dcda429f:Kards 1.38.22432.launcher',
    'Authorization': 'JWT <YOUR_JWT_TOKEN>',  # TODO: 设置真实 JWT
    'User-Agent': 'kards/Client'
}
PROXIES = {"http": None, "https": None}






"" "

BASE_URL = "https://kards.live.1939api.com"

#####################################################################################################################jwt_tk_fwk_kal_kah_d_dddd_dsl_srbd_ddddd_=""



jwt_tk_fwk_kal_kah_d_dddd_dsl_srbd_ddddd_=#"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX25hbWUiOiJsaW5rZXI6MzE0MTU5MjY1MzU4OTc5MzIzODQ2MjY0MzM4MzI3OTUwNDk3QHByb3Rvbi5tZSIsInVzZXJfaWQiOjEwNTc3NjE0NSwiaWRlbnRpdHlfaWQiOjIxMDgzMjk1NiwicHJvdmlkZXIiOiJkZXZpY2UiLCJleHRlcm5hbF9pZCI6IldpbmRvd3MtNjU2RkIzQ0U0NjhCNDBDMTFERDZERTlDRUI1NDRERDkiLCJwYXltZW50Ijoibm90YXZhaWxhYmxlIiwicm9sZXMiOltdLCJpYXQiOjE3NTM1NTQ5MzIsImV4cCI6MTc1MzY0MTMzMiwianRpIjoiVVpNejJJWExPbm84bjJMcFkza0QiLCJpc3MiOiJrYXJkcy1iYWNrZW5kIiwidGllciI6IkxJVkUiLCJsYW5ndWFnZSI6InpoLUhhbnMiLCJjbGllbnRfaWQiOjMwMDM3NzM4MiwicGxheWVyX2lkIjo1NzQ2NDY4fQ.aK6yAxi7Q7kn66df_MGdteY5Z8SA2nZ620reL3a2DkAGfm-1yxKBV_nNxSoxwFrjc0BOOnj0okx29dIzfG01ipOkxhdF-J6baiXsQifOotm3eRx4C-MHablegD99mCtL3jlLaRT18n_Zro3GGaqdx_beUy32NGQvtjDoc8pmWsU6WNjKczrVRykqac7Rb_3amPNTBhkZC5ejwgyLjsbA8NWFUJkrCEnkAls2Hexebu4JKFjUacXYvWPyb7xF5WZiA7AyDwSMSN5gUFmFzwj5IoUFm8ayu0tuLV0jeHoqSN2QSry81Wgg6EBViiqiFuztCWO54O3zpHx9oV5lENm0fg"



#############################################################################################"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX25hbWUiOiJsaW5rZXI6MzE0MTU5MjY1MzU4OTc5MzIzODQ2MjY0MzM4MzI3OTUwNDk3QHByb3Rvbi5tZSIsInVzZXJfaWQiOjEwNTc3NjE0NSwiaWRlbnRpdHlfaWQiOjIxMDgzMjk1NiwicHJvdmlkZXIiOiJkZXZpY2UiLCJleHRlcm5hbF9pZCI6IldpbmRvd3MtNjU2RkIzQ0U0NjhCNDBDMTFERDZERTlDRUI1NDRERDkiLCJwYXltZW50Ijoibm90YXZhaWxhYmxlIiwicm9sZXMiOltdLCJpYXQiOjE3NTI4MDE1NDEsImV4cCI6MTc1Mjg4Nzk0MSwianRpIjoiN0c5ZWRpZ3RSbzVpTWphN1BoRTAiLCJpc3MiOiJrYXJkcy1iYWNrZW5kIiwidGllciI6IkxJVkUiLCJsYW5ndWFnZSI6InpoLUhhbnMiLCJjbGllbnRfaWQiOjI4OTYxODM0OCwicGxheWVyX2lkIjo1NzQ2NDY4fQ.l7JvOpKL7Xgayj9XuHMBokiU9rfFag5gM7JMK_nh2iepm-G_BpBR6OMEaA4_8bzsmBE1cszWr5Y63_Lj_se6dgIR8emen84pJx_D6YQd3u9kyX_Y2WOuh3PNjLGrkWolGXysxQ32hYX3DYhvZkQwa6obBtwga2jBzcUWi3nAifjJXgNYbT45U3Er717NqA6XS5H9Y-do_BqK4mgcfPJB-Kt8bb8z1PFLZpeIXHi0dfOSCbJgOsBuue7wBugSmCwNfCjjAkH_KncEv_NdET_VFM9VVMhjXTC5dv8so_ZveGm4_f2PYIstH6fDlkoW_olQEN5MTKJ86vSc0T9-s1GNxw"###########################""########################################### ""##################################################################################################################################################"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX25hbWUiOiJsaW5rZXI6MzE0MTU5MjY1MzU4OTc5MzIzODQ2MjY0MzM4MzI3OTUwNDk3QHByb3Rvbi5tZSIsInVzZXJfaWQiOjEwNTc3NjE0NSwiaWRlbnRpdHlfaWQiOjIxMDgzMjk1NiwicHJvdmlkZXIiOiJkZXZpY2UiLCJleHRlcm5hbF9pZCI6IldpbmRvd3MtNjU2RkIzQ0U0NjhCNDBDMTFERDZERTlDRUI1NDRERDkiLCJwYXltZW50Ijoibm90YXZhaWxhYmxlIiwicm9sZXMiOltdLCJpYXQiOjE3NTI2Njg5NDQsImV4cCI6MTc1Mjc1NTM0NCwianRpIjoiNFY0QXlOaU1xRzZpWG5FbTlLWkoiLCJpc3MiOiJrYXJkcy1iYWNrZW5kIiwidGllciI6IkxJVkUiLCJsYW5ndWFnZSI6InpoLUhhbnMiLCJjbGllbnRfaWQiOjI4Nzk5NDQzOCwicGxheWVyX2lkIjo1NzQ2NDY4fQ.TXBPwyDdQqydf4V_XrnzZGo3OQdLRbGlg7iZiNsMS927JLjyqNKKmKWAREU9JevswqYz_RMMHuN_xnh0iC3KJj0RiZ_nFDwXwyYWg41EOMzwL_MbmiayTFP2Cyszs19o3MJeYxvItXZpdTwR8Tvlc0KbVvKmibdjIP1hjbU9F5rrtyLf1DdFsj7BwzeOgNbKVRegGw9n9ttJDGfxNG8B-e7KSGwsQd7KdVJReuPcWImyudY55PugTdtfrIqezOS6NtZePmzjLFQwxhCyoqv1DJO8ASahlfqx_pKdi6cGsCngt5oAJp8bqyyrgScT5OcF5EP1GRLyPAwW99yshzePEA"

# —— 【2】 从 Fiddler 里看到的“X-Api-Key” 与“Drift-Api-Key”，版本号必须一致
api_key_value = "1939-kards-5dcda429f:Kards 1.38.22432.launcher"#"1939-kards-5dcba429f:Kards 1.34.21831.launcher"  # 示例，务必与抓包时相同
drift_key_value = "1939-kards-5dcda429f:Kards 1.38.22432.launcher"###############################################################################################"1939-kards-5dcba429f:Kards 1.34.21831.launcher"

########### —— 【3】 从 Payload 解码或从 JWT 中提取的 纯数字 player_id
#fjkldjklfjsdkljfkl sldjf klsdjklfj sdjkl sdklj klsdjkl fjklsdj klfjsdkl lsdjklsdjfd kl

player_id="5746468"

# 构造完整的 Headers
headers = {
    # ① 身份验证必须：完整复制“Authorization”一行
    "Authorization": jwt_tk_fwk_kal_kah_d_dddd_dsl_srbd_ddddd_,

    # ② 这两个 Key 都要加上，否则后端不会允许你访问
    "X-Api-Key": api_key_value,
    "Drift-Api-Key": drift_key_value,

    # ③ 告诉服务器你要 JSON 格式返回
    "Accept": "application/json",

    # ④ “User-Agent” 必须与官方客户端或抓包时看到的一致，否则也会被拒绝
    "User-Agent": "kards/++UE5+Release-5.5-CL-40574608 (http-eventloop) Windows/10.0.19045.1.256.64bit"


#"kards/++UE5+Release-5.5-CL-40574608 (http-eventloop) Windows/10.0.19045.1.256.64bit"


}

# —— 【4】 确认请求走“直连”模式，不通过本地代理
proxies = {"http": None, "https": None}


###################################################################################################################################################################################################################################################################################################################PROXIES = {"http": None, "https": None}


PROXIES=proxies



HEADERS=headers



"" "

import sys



sys.exit()



"" "


"""




import argparse
import json
import time
import requests
import csv
from pathlib import Path
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)


"""
import os, sys

## 目标脚本绝对路径
file_path = "./"#r"C:\_jfdkls_ddddddd_fjdskl_dddddddddd_fdsjklsdf_ddddddddddddddddddddd_\_fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_.py"########@_test_fwk_kal_kah_ddddddddddddd_.py"
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
from _fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_ import aaa_ddd_


"""



def test_grd_(jwt_):


    



    BASE_URL = "https://kards.live.1939api.com"

#####################################################################################################################jwt_tk_fwk_kal_kah_d_dddd_dsl_srbd_ddddd_=""



    jwt_tk_fwk_kal_kah_d_dddd_dsl_srbd_ddddd_=jwt_#"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX25hbWUiOiJsaW5rZXI6MzE0MTU5MjY1MzU4OTc5MzIzODQ2MjY0MzM4MzI3OTUwNDk3QHByb3Rvbi5tZSIsInVzZXJfaWQiOjEwNTc3NjE0NSwiaWRlbnRpdHlfaWQiOjIxMDgzMjk1NiwicHJvdmlkZXIiOiJkZXZpY2UiLCJleHRlcm5hbF9pZCI6IldpbmRvd3MtNjU2RkIzQ0U0NjhCNDBDMTFERDZERTlDRUI1NDRERDkiLCJwYXltZW50Ijoibm90YXZhaWxhYmxlIiwicm9sZXMiOltdLCJpYXQiOjE3NTM1NTQ5MzIsImV4cCI6MTc1MzY0MTMzMiwianRpIjoiVVpNejJJWExPbm84bjJMcFkza0QiLCJpc3MiOiJrYXJkcy1iYWNrZW5kIiwidGllciI6IkxJVkUiLCJsYW5ndWFnZSI6InpoLUhhbnMiLCJjbGllbnRfaWQiOjMwMDM3NzM4MiwicGxheWVyX2lkIjo1NzQ2NDY4fQ.aK6yAxi7Q7kn66df_MGdteY5Z8SA2nZ620reL3a2DkAGfm-1yxKBV_nNxSoxwFrjc0BOOnj0okx29dIzfG01ipOkxhdF-J6baiXsQifOotm3eRx4C-MHablegD99mCtL3jlLaRT18n_Zro3GGaqdx_beUy32NGQvtjDoc8pmWsU6WNjKczrVRykqac7Rb_3amPNTBhkZC5ejwgyLjsbA8NWFUJkrCEnkAls2Hexebu4JKFjUacXYvWPyb7xF5WZiA7AyDwSMSN5gUFmFzwj5IoUFm8ayu0tuLV0jeHoqSN2QSry81Wgg6EBViiqiFuztCWO54O3zpHx9oV5lENm0fg"


  #  y y b d l d,(),

 #   ,(),



#############################################################################################"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX25hbWUiOiJsaW5rZXI6MzE0MTU5MjY1MzU4OTc5MzIzODQ2MjY0MzM4MzI3OTUwNDk3QHByb3Rvbi5tZSIsInVzZXJfaWQiOjEwNTc3NjE0NSwiaWRlbnRpdHlfaWQiOjIxMDgzMjk1NiwicHJvdmlkZXIiOiJkZXZpY2UiLCJleHRlcm5hbF9pZCI6IldpbmRvd3MtNjU2RkIzQ0U0NjhCNDBDMTFERDZERTlDRUI1NDRERDkiLCJwYXltZW50Ijoibm90YXZhaWxhYmxlIiwicm9sZXMiOltdLCJpYXQiOjE3NTI4MDE1NDEsImV4cCI6MTc1Mjg4Nzk0MSwianRpIjoiN0c5ZWRpZ3RSbzVpTWphN1BoRTAiLCJpc3MiOiJrYXJkcy1iYWNrZW5kIiwidGllciI6IkxJVkUiLCJsYW5ndWFnZSI6InpoLUhhbnMiLCJjbGllbnRfaWQiOjI4OTYxODM0OCwicGxheWVyX2lkIjo1NzQ2NDY4fQ.l7JvOpKL7Xgayj9XuHMBokiU9rfFag5gM7JMK_nh2iepm-G_BpBR6OMEaA4_8bzsmBE1cszWr5Y63_Lj_se6dgIR8emen84pJx_D6YQd3u9kyX_Y2WOuh3PNjLGrkWolGXysxQ32hYX3DYhvZkQwa6obBtwga2jBzcUWi3nAifjJXgNYbT45U3Er717NqA6XS5H9Y-do_BqK4mgcfPJB-Kt8bb8z1PFLZpeIXHi0dfOSCbJgOsBuue7wBugSmCwNfCjjAkH_KncEv_NdET_VFM9VVMhjXTC5dv8so_ZveGm4_f2PYIstH6fDlkoW_olQEN5MTKJ86vSc0T9-s1GNxw"###########################""########################################### ""##################################################################################################################################################"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX25hbWUiOiJsaW5rZXI6MzE0MTU5MjY1MzU4OTc5MzIzODQ2MjY0MzM4MzI3OTUwNDk3QHByb3Rvbi5tZSIsInVzZXJfaWQiOjEwNTc3NjE0NSwiaWRlbnRpdHlfaWQiOjIxMDgzMjk1NiwicHJvdmlkZXIiOiJkZXZpY2UiLCJleHRlcm5hbF9pZCI6IldpbmRvd3MtNjU2RkIzQ0U0NjhCNDBDMTFERDZERTlDRUI1NDRERDkiLCJwYXltZW50Ijoibm90YXZhaWxhYmxlIiwicm9sZXMiOltdLCJpYXQiOjE3NTI2Njg5NDQsImV4cCI6MTc1Mjc1NTM0NCwianRpIjoiNFY0QXlOaU1xRzZpWG5FbTlLWkoiLCJpc3MiOiJrYXJkcy1iYWNrZW5kIiwidGllciI6IkxJVkUiLCJsYW5ndWFnZSI6InpoLUhhbnMiLCJjbGllbnRfaWQiOjI4Nzk5NDQzOCwicGxheWVyX2lkIjo1NzQ2NDY4fQ.TXBPwyDdQqydf4V_XrnzZGo3OQdLRbGlg7iZiNsMS927JLjyqNKKmKWAREU9JevswqYz_RMMHuN_xnh0iC3KJj0RiZ_nFDwXwyYWg41EOMzwL_MbmiayTFP2Cyszs19o3MJeYxvItXZpdTwR8Tvlc0KbVvKmibdjIP1hjbU9F5rrtyLf1DdFsj7BwzeOgNbKVRegGw9n9ttJDGfxNG8B-e7KSGwsQd7KdVJReuPcWImyudY55PugTdtfrIqezOS6NtZePmzjLFQwxhCyoqv1DJO8ASahlfqx_pKdi6cGsCngt5oAJp8bqyyrgScT5OcF5EP1GRLyPAwW99yshzePEA"

# —— 【2】 从 Fiddler 里看到的“X-Api-Key” 与“Drift-Api-Key”，版本号必须一致
    api_key_value = "1939-kards-5dcda429f:Kards 1.38.22432.launcher"#"1939-kards-5dcba429f:Kards 1.34.21831.launcher"  # 示例，务必与抓包时相同
    drift_key_value = "1939-kards-5dcda429f:Kards 1.38.22432.launcher"###############################################################################################"1939-kards-5dcba429f:Kards 1.34.21831.launcher"

########### —— 【3】 从 Payload 解码或从 JWT 中提取的 纯数字 player_id
#fjkldjklfjsdkljfkl sldjf klsdjklfj sdjkl sdklj klsdjkl fjklsdj klfjsdkl lsdjklsdjfd kl

    player_id="5746468"

# 构造完整的 Headers
    headers = {
    # ① 身份验证必须：完整复制“Authorization”一行
        "Authorization": jwt_tk_fwk_kal_kah_d_dddd_dsl_srbd_ddddd_,

    # ② 这两个 Key 都要加上，否则后端不会允许你访问
        "X-Api-Key": api_key_value,
        "Drift-Api-Key": drift_key_value,

    # ③ 告诉服务器你要 JSON 格式返回
        "Accept": "application/json",

    # ④ “User-Agent” 必须与官方客户端或抓包时看到的一致，否则也会被拒绝
        "User-Agent": "kards/++UE5+Release-5.5-CL-40574608 (http-eventloop) Windows/10.0.19045.1.256.64bit"


#"kards/++UE5+Release-5.5-CL-40574608 (http-eventloop) Windows/10.0.19045.1.256.64bit"


    }

# —— 【4】 确认请求走“直连”模式，不通过本地代理
    proxies = {"http": None, "https": None}


###################################################################################################################################################################################################################################################################################################################PROXIES = {"http": None, "https": None}


    PROXIES=proxies



    HEADERS=headers

    return HEADERS,PROXIES,player_id



