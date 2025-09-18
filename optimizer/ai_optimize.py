# optimizer/ai_optimize.py
import os
import textwrap
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = os.getenv('OPENAI_MODEL')
BASE_URL = os.getenv('BASE_URL')
if not OPENAI_API_KEY:
    raise RuntimeError('OPENAI_API_KEY not set')

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=BASE_URL
    )

PROMPT_TEMPLATE = textwrap.dedent('''
你是亚马逊Listing优化师。
输入：原始Listing结构（title, price, features, description, category, product_dimensions, item_weight, shipping）
输出：JSON 字段：{{"title":...,"price":..., "bullets": ["...", "..."], "description": ..., "notes": ..., "images": ["...", "..."],"product_dimensions":...,"item_weight":..., "shipping":..., "category":...}}

要求：
- 标题不超过200字符，自然植入高频关键词
- 生成 5 个卖点 bullet，简洁、可读、含购买理由（每点不超过500字符,每点开头要有个关键词，关键词后边跟着英文":",每点句尾不要标点符号）
- 商品描述不少于1000字符，不大于1500个字符
- 保留原有关键信息
- 输出为纯 JSON
- 不能有品牌名称
- 不能有极限词（比如高、提高、优质、完美等，可以改为近义词）
- 输出语言与输入语言保持一致

原始数据：
{input}
''')


def optimize_listing_struct(cleaned: dict):
    inp = {
        'title': cleaned.get('title'),
        'price': cleaned.get('price'),
        'features': cleaned.get('features'),
        'description': cleaned.get('description'),
        'category': cleaned.get('category'),
        'product_dimensions': cleaned.get('product_dimensions'),
        'item_weight': cleaned.get('item_weight'),
        'shipping': cleaned.get('shipping')
    }
    prompt = PROMPT_TEMPLATE.format(input=inp)

    # Call Chat Completions or chat.create depending on openai client version
    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.6
    )

    text = res.choices[0].message.content
    # Try to parse JSON from the assistant response robustly
    import json, re
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return {'raw_output': text}
    return {'raw_output': text}