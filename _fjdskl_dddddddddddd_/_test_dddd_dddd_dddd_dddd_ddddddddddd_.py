
































































#!/usr/bin/env python3
# coding: utf-8
"""
Kards session helper
· 每 24 小时最多登陆一次
· JWT 持久化到磁盘
· 失效时自动刷新
"""

import base64, json, os, time, pathlib, requests
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning
import urllib3; urllib3.disable_warnings(InsecureRequestWarning)

# --------------------------------------------------------------
BASE_URL   = "https://kards.live.1939api.com"
LOGIN_URL  = urljoin(BASE_URL, "/session")
TOKEN_FILE = pathlib.Path("kards_token.json")     # 也可以改成 .txt
MAX_AGE    = 24 * 3600                            # 最多一天登一次
TIMEOUT    = 10
PROXIES    = {"http": None, "https": None}





import os, sys

## 目标脚本绝对路径
file_path = r"..\_test_5_x_ddddd_.py"#r"Y:\_fjklsdjl_dddddddddddddd_\_test_5_x_ddddd_.py"#r"Y:\_fjklsdjl_dddddddddddddd_\_def_get_ddddddd_.py"#"./"#r"C:\_jfdkls_ddddddd_fjdskl_dddddddddd_fdsjklsdf_ddddddddddddddddddddd_\_fwk_kai_kal_test_fx_ddddddddddddddddddddddddddd_.py"########@_test_fwk_kal_kah_ddddddddddddd_.py"
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


##########################################################################################from _def_get_ddddddd_ import test_grd_










# ============== 1. 你的登陆实现 (保持原来的三步调用) =================
def _real_login() -> str:
    """
    真正去服务器换 JWT。  
    直接搬你的原逻辑：dl_() → login_ss_()，并返回 str(token)
    """
    from _test_5_x_ddddd_ import dl_, login_ss_#your_origin_module import dl_, login_ss_     # <<< 保持原接口
    dl_()
    return login_ss_(None, None)
# ===================================================================


# ---------------------- 工具函数 ----------------------------
def _decode_payload(jwt_: str) -> dict:
    """
    解析 JWT 第二段 payload，判断 exp。失败返回 {}。
    """
    try:
        payload_b64 = jwt_.split('.')[1]
        # jwt 使用 urlsafe_b64，需要补 '='
        payload_b64 += '=' * (-len(payload_b64) % 4)
        payload = base64.urlsafe_b64decode(payload_b64.encode())
        return json.loads(payload)
    except Exception:
        return {}

def _jwt_expired(jwt_: str) -> bool:
    info = _decode_payload(jwt_)
    exp  = info.get('exp')            # Unix epoch
    if not exp:
        return False
    # 提前 60 秒视为过期，避免并发调用边界
    return exp < time.time() + 60


def _load_cached() -> dict | None:
    if not TOKEN_FILE.exists():
        return None
    try:
        return json.loads(TOKEN_FILE.read_text('utf-8'))
    except Exception:
        return None


def _save_cache(jwt_: str):
    TOKEN_FILE.write_text(
        json.dumps({"token": jwt_, "ts": int(time.time())}, indent=2),
        encoding="utf-8"
    )


# ------------------- 对外主入口 -----------------------------
def get_jwt(force: bool = False,jwt_=None) -> str:#,jwt_) -> str:
    """
    返回可用 JWT。  
    force=True 或 token 失效 / 超龄 时会重新登陆。
    """
    cached = _load_cached()

    if not force and cached:
        ok_age  = (time.time() - cached.get("ts", 0)) < MAX_AGE
        ok_jwt  = not _jwt_expired(cached["token"])
        if ok_age and ok_jwt:
            return cached["token"]




################################################################



###############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################   print("grd_dddddd_")

    print("grd_ddddddddddddddd_fjsdkljsdfkl jsdklfjsdklj ksdjkl fjsdklj fkljsdklj fkldsjkl fjsdklj fklsdjf sdklfkld sdklj klfsdjkl fjkldjkl jdls_")


    # 重新登陆
    jwt_ = _real_login()
    if not jwt_:
        raise RuntimeError("登陆失败，未拿到 JWT")
    _save_cache(jwt_)
    return jwt_


# ---------------- 带自动续约的请求包装 ----------------------
def _build_headers(jwt_: str, extra: dict | None = None) -> dict:
    h = {
        "Accept": "application/json",
        "Authorization": f"JWT {jwt_}",
        "User-Agent": "kards-extractor/0.1",
    }
    if extra:
        h.update(extra)
    return h


def kards_request(method: str,
                  path: str,
                  *,
                  json_body=None,
                  params=None,
                  headers=None,
                  retry=True):
    """
    对 requests 的简单包裹：  
    - 自动带上 JWT  
    - 收到 401/403 时再刷新一次（仅重试一回）  
    """
    jwt_ = get_jwt()
    url  = urljoin(BASE_URL, path.lstrip("/"))
    hdrs = _build_headers(jwt_, headers)

    resp = requests.request(method.upper(), url,
                            json=json_body, params=params,
                            headers=hdrs, timeout=TIMEOUT,
                            verify=False, proxies=PROXIES)
    if resp.status_code in (401, 403) and retry:
        # 可能 token 过期 → 强刷一次
        jwt_ = get_jwt(force=True)
        hdrs = _build_headers(jwt_, headers)
        resp = requests.request(method.upper(), url,
                                json=json_body, params=params,
                                headers=hdrs, timeout=TIMEOUT,
                                verify=False, proxies=PROXIES)
    resp.raise_for_status()
    return resp



