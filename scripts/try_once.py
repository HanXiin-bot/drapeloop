"""用 1 张人物照 + 1 张上衣图，调用一次 AI 试衣服务，把结果图存到本地。

只用 Python 自带的库，不用另外安装。

用法：
    export DASHSCOPE_API_KEY=...   # 阿里云百炼
    export FASHN_API_KEY=...       # FASHN
    python3 scripts/try_once.py aliyun 人物照.jpg 上衣.jpg
    python3 scripts/try_once.py fashn  人物照.jpg 上衣.jpg      # tryon-v1.6
    python3 scripts/try_once.py fashn-max 人物照.jpg 上衣.jpg  # Try-On Max

结果图保存在 trial-output/ 里（不会提交到 Git）。
"""

import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "trial-output"
POLL_SECONDS = 3
TIMEOUT_SECONDS = 180

ALIYUN_BASE = "https://dashscope.aliyuncs.com/api/v1"
ALIYUN_MODEL = "aitryon-plus"
FASHN_BASE = "https://api.fashn.ai/v1"


class TryOnError(Exception):
    pass


def http(method, url, headers=None, body=None):
    """发一个 HTTP 请求，返回 (状态码, 响应内容)。"""
    # FASHN 的图片 CDN 会拒绝 Python 默认的 User-Agent（HTTP 403），所以统一带一个
    headers = {"User-Agent": "Mozilla/5.0 (DrapeLoop trial script)", **(headers or {})}
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def http_json(method, url, headers, payload=None):
    body = json.dumps(payload).encode() if payload is not None else None
    headers = {**headers, "Content-Type": "application/json"}
    status, raw = http(method, url, headers, body)
    try:
        data = json.loads(raw or b"{}")
    except json.JSONDecodeError:
        raise TryOnError(f"服务返回的不是 JSON（HTTP {status}）：{raw[:200]!r}")
    if status >= 400:
        raise TryOnError(f"HTTP {status}：{data}")
    return data


def require_key(name):
    key = os.environ.get(name)
    if not key:
        raise TryOnError(f"没找到 {name}。先在终端运行：export {name}=你的API Key")
    return key


def check_image(path):
    p = Path(path)
    if not p.is_file():
        raise TryOnError(f"找不到图片：{path}")
    if p.stat().st_size > 5 * 1024 * 1024:
        raise TryOnError(f"图片超过 5MB，请先压缩：{path}")
    return p


def wait_for(poll, label):
    """每隔几秒查一次结果，直到成功、失败或超时。"""
    start = time.time()
    while time.time() - start < TIMEOUT_SECONDS:
        done, result = poll()
        if done:
            return result
        print(f"  {label}：生成中…（已等 {time.time() - start:.0f} 秒）")
        time.sleep(POLL_SECONDS)
    raise TryOnError(f"等了 {TIMEOUT_SECONDS} 秒还没出结果，先停下")


# ---------- 阿里云百炼 AI试衣 Plus ----------

def aliyun_upload(key, path):
    """把本地图片传到百炼的临时存储，得到 oss:// 地址（48 小时后自动删除）。"""
    auth = {"Authorization": f"Bearer {key}"}
    policy = http_json(
        "GET", f"{ALIYUN_BASE}/uploads?action=getPolicy&model={ALIYUN_MODEL}", auth
    )["data"]
    object_key = f"{policy['upload_dir']}/{uuid.uuid4().hex}{path.suffix.lower()}"
    fields = {
        "OSSAccessKeyId": policy["oss_access_key_id"],
        "Signature": policy["signature"],
        "policy": policy["policy"],
        "x-oss-object-acl": policy["x_oss_object_acl"],
        "x-oss-forbid-overwrite": policy["x_oss_forbid_overwrite"],
        "key": object_key,
        "success_action_status": "200",
    }
    body, content_type = multipart(fields, "file", path)
    status, raw = http("POST", policy["upload_host"], {"Content-Type": content_type}, body)
    if status != 200:
        raise TryOnError(f"上传图片失败（HTTP {status}）：{raw[:300]!r}")
    return f"oss://{object_key}"


def multipart(fields, file_field, path):
    """拼一个 multipart/form-data 请求体，文件字段必须放在最后。"""
    boundary = uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()
        )
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; '
        f'filename="{path.name}"\r\nContent-Type: {mime}\r\n\r\n'.encode()
        + path.read_bytes()
        + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def run_aliyun(person, garment):
    key = require_key("DASHSCOPE_API_KEY")
    print("  上传图片到百炼临时存储…")
    person_url = aliyun_upload(key, person)
    garment_url = aliyun_upload(key, garment)

    headers = {
        "Authorization": f"Bearer {key}",
        "X-DashScope-Async": "enable",
        "X-DashScope-OssResourceResolve": "enable",
    }
    task = http_json(
        "POST",
        f"{ALIYUN_BASE}/services/aigc/image2image/image-synthesis",
        headers,
        {
            "model": ALIYUN_MODEL,
            "input": {"person_image_url": person_url, "top_garment_url": garment_url},
            "parameters": {"resolution": -1, "restore_face": True},
        },
    )
    task_id = task["output"]["task_id"]

    def poll():
        out = http_json("GET", f"{ALIYUN_BASE}/tasks/{task_id}", headers)["output"]
        status = out.get("task_status")
        if status == "SUCCEEDED":
            return True, out["image_url"]
        if status in ("FAILED", "CANCELED", "UNKNOWN"):
            raise TryOnError(f"生成失败：{out.get('code')} {out.get('message')}")
        return False, None

    return wait_for(poll, "阿里云")


# ---------- FASHN ----------

def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


# M1 固定提示词的英文版（Try-On Max 才收提示词），见 docs/evaluation/m1-test-set.md
FASHN_MAX_PROMPT = (
    "Replace only the top. Keep the person's face, hairstyle, skin tone, body proportions, "
    "pose, bottoms, shoes, accessories and background exactly the same. No beautification, "
    "no slimming. The top's color, fit, length, pattern and text must exactly match the "
    "garment image. Do not bring over the model, necklace, hat, text labels or UI elements "
    "from the garment image. The result should look like a real photo taken with a phone."
)


def run_fashn(person, garment):
    """旧模型 tryon-v1.6：每张 1 个额度，不收提示词。"""
    return fashn_job({
        "model_name": "tryon-v1.6",
        "inputs": {
            "model_image": data_uri(person),
            "garment_image": data_uri(garment),
            "category": "tops",
            "garment_photo_type": "auto",
        },
    })


def run_fashn_max(person, garment):
    """新模型 Try-On Max：2k · balanced 每张 3 个额度，收提示词。"""
    return fashn_job({
        "model_name": "tryon-max",
        "inputs": {
            "model_image": data_uri(person),
            "product_image": data_uri(garment),
            "prompt": FASHN_MAX_PROMPT,
            "resolution": "2k",
            "generation_mode": "balanced",
            "num_images": 1,
        },
    })


def fashn_job(payload):
    key = require_key("FASHN_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    job = http_json("POST", f"{FASHN_BASE}/run", headers, payload)
    if job.get("error"):
        raise TryOnError(f"提交失败：{job['error']}")
    job_id = job["id"]

    def poll():
        out = http_json("GET", f"{FASHN_BASE}/status/{job_id}", headers)
        status = out.get("status")
        if status == "completed":
            return True, out["output"][0]
        if status == "failed":
            raise TryOnError(f"生成失败：{out.get('error')}")
        return False, None

    return wait_for(poll, "FASHN")


# ---------- 主流程 ----------

PROVIDERS = {"aliyun": run_aliyun, "fashn": run_fashn, "fashn-max": run_fashn_max}


def main(argv):
    if len(argv) != 4 or argv[1] not in PROVIDERS:
        print(__doc__)
        return 2
    provider = argv[1]
    try:
        person, garment = check_image(argv[2]), check_image(argv[3])
        print(f"开始：{provider}｜人物 {person.name}｜上衣 {garment.name}")
        start = time.time()
        result_url = PROVIDERS[provider](person, garment)
        elapsed = time.time() - start

        status, image = http("GET", result_url)
        if status != 200:
            raise TryOnError(f"结果图下载失败（HTTP {status}），链接：{result_url}")
        OUTPUT_DIR.mkdir(exist_ok=True)
        out = OUTPUT_DIR / f"{time.strftime('%Y%m%d-%H%M%S')}-{provider}-{person.stem}.png"
        out.write_bytes(image)
    except TryOnError as e:
        print(f"❌ {e}")
        return 1
    print(f"✅ 完成，用时 {elapsed:.0f} 秒（填进打分表的“等待秒数”）")
    print(f"   结果图：{out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
