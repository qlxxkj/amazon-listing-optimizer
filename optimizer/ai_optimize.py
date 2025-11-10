# optimizer/ai_optimize.py
import os, json, logging
from urllib.parse import urlparse
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

from datetime import datetime
from db.save_data import check_if_first_run, update_run_status
from .prompts import PROMPTS

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取环境变量配置openai的API参数
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')  # 提供默认值
BASE_URL = os.getenv('BASE_URL')

if not OPENAI_API_KEY:
    raise RuntimeError('OPENAI_API_KEY environment variable is not set')

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

# 域名到语言代码的映射字典 (确保与PROMPTS的键匹配)
DOMAIN_TO_LANG = {
    # 英语系列
    'amazon.com': 'en',        # 美国
    'amazon.co.uk': 'en',      # 英国
    'amazon.ca': 'en',         # 加拿大
    'amazon.com.au': 'en',     # 澳大利亚
    # 其他语言
    'amazon.co.jp': 'ja',      # 日本
    'amazon.de': 'de',         # 德国
    'amazon.fr': 'fr',         # 法国
    'amazon.it': 'it',         # 意大利
    'amazon.es': 'es',         # 西班牙
    'amazon.nl': 'nl',         # 荷兰
    'amazon.com.br': 'pt',     # 巴西
    'amazon.se': 'sv',         # 瑞典
    'amazon.pl': 'pl',         # 波兰
    # 可根据需要继续添加
}

# 检测域名语言，为匹配PROMPTS
def detect_lang_from_url(url: str) -> str:
    """
    根据 Amazon 域名判断站点语言。

    Args:
        url: 商品页面的完整URL字符串。

    Returns:
        str: 语言代码字符串 (en, ja, de, fr, it, es, 或 en 作为默认值)。
    """
    # 1. 检查输入有效性 - 添加更严格的检查
    if not url or not isinstance(url, str) or url.strip() == "":
        logger.warning(f"Invalid URL provided: '{url}', defaulting to 'en'")
        return 'en' # 默认英语

    url = url.strip() # 去除首尾空格

    # 2. 解析URL
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc.lower() # 获取主机名并转为小写

        # 3. 遍历映射字典，检查主机名是否包含已知的亚马逊域名后缀
        for domain_suffix, lang_code in DOMAIN_TO_LANG.items():
            if hostname.endswith(domain_suffix):
                logger.info(f"Detected language '{lang_code}' from URL: {url}")
                return lang_code

        # 4. 如果没有匹配到已知域名，尝试匹配更通用的模式
        if 'amazon.co.jp' in hostname:
            return 'ja'
        elif 'amazon.de' in hostname:
            return 'de'
        elif 'amazon.fr' in hostname:
            return 'fr'
        elif 'amazon.it' in hostname:
            return 'it'
        elif 'amazon.es' in hostname:
            return 'es'
        elif 'amazon.' in hostname: # 其他亚马逊站点默认英语
            logger.info(f"Recognized as Amazon domain but no specific language mapping for {hostname}, defaulting to 'en'")
            return 'en'
        else:
            logger.warning(f"Unrecognized domain: {hostname}, defaulting to 'en'")
            return 'en'

    except Exception as e:
        logger.error(f"Error parsing URL {url}: {e}")
        return 'en' # 解析出错时默认英语



##############################################################
#
#  optimize_listing_struct-V3.0
#
##############################################################
#
def optimize_listing_struct(cleaned, site="us", url=""):
    lang = site.lower()
    today = datetime.now().strftime("%Y-%m-%d")
    is_first_run = check_if_first_run(site=lang, date=today)

    # -------- 第一步：若首次调用，只发优化规则 Prompt --------
    if is_first_run:
        prompt_template = PROMPTS.get(lang, PROMPTS["en"])
        logger.info(f"🟩 第一次调用 {lang} 模型，仅发送优化规则 Prompt（无商品内容）")

        try:
            res1 = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt_template}],
                max_tokens=500,
                temperature=0.3,

            )
            logger.info("✅ 第一次调用成功，Prompt 模板已加载上下文")
        except Exception as e:
            logger.error(f"❌ 第一次调用失败: {e}")

        # 标记为已执行，以便后续直接发内容
        update_run_status(site=lang, date=today)

    # -------- 第二步：发要优化的字段 --------
    title = cleaned.get("title", "")
    desc = cleaned.get("description", "")
    features = cleaned.get("features", [])
    features_text = "\n".join(f"- {f}" for f in features)
    brand = cleaned.get("brand","")

    input_text = f"""
        Optimize this Amazon listing:
        Title: {title}
        Description: {desc}
        Features: {features_text}
        Output a JSON with:
        - optimized_title
        - optimized_features
        - optimized_description
        - search_keywords
        Please ensure the output is in the language of the input site ({lang}).
        No brand ({brand}) are allowed.
        """

    logger.info(f"🟦 第二次调用（含字段内容）: {len(input_text)} chars")

    try:
        res2 = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": input_text}],
            max_tokens=1500,
            temperature=0.6,
            response_format={"type": "json_object"}  # 明确要求JSON格式
        )

        text = res2.choices[0].message.content

        # 尝试解析JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON对象
            import re
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    logger.error("⚠️ JSON解析失败，返回原始文本")
                    return {"raw_output": text}
            return {"raw_output": text}

    except Exception as e:
        # logger.error(f"Error calling OpenAI API: {e}")
        logger.error(f"❌ 第二次调用失败: {e}")
        return {"error": f"OpenAI API call failed: {str(e)}"}
