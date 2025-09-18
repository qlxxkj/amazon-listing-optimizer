from bs4 import BeautifulSoup
from crawler.selectors import SELECTORS
import re
import json


def extract_shipping(text: str):
    """提取运费金额，免运费返回 0"""
    if not text:
        return 0
    text = text.strip()
    if "free" in text.lower():
        return 0
    m = re.search(r"\$([\d\.,]+)", text)
    return m.group(1) if m else 0


def parse_amazon_html(html):
    soup = BeautifulSoup(html, 'lxml')

    def safe_select_text(sel):
        node = soup.select_one(sel)
        return node.get_text(strip=True) if node else ''

    title = safe_select_text(SELECTORS['title'])
    price = safe_select_text(SELECTORS['price'])
    features = [li.get_text(strip=True) for li in soup.select(SELECTORS['features'])]
    description = safe_select_text(SELECTORS['description'])
    category = '/'.join([li.get_text(strip=True) for li in soup.select(SELECTORS['category'])])
    # product_dimensions = safe_select_text(SELECTORS['product_dimensions'])
    # item_weight = safe_select_text(SELECTORS['item_weight'])

    # ====== 尺寸 & 重量 ======
    product_dimensions = ''
    item_weight = ''

    # 方法1: 从 table 里提取
    rows = soup.select("table tr")
    for row in rows:
        header = row.find("th")
        value = row.find("td")
        if not header or not value:
            continue
        key = header.get_text(strip=True).lower()
        val = value.get_text(strip=True)
        if "dimensions" in key:
            product_dimensions = val
        elif "item weight" in key:
            item_weight = val

    # 方法2: 从 detailBullets_feature_div 提取
    if not product_dimensions or not item_weight:
        bullets = soup.select("#detailBullets_feature_div li span")
        for i in range(len(bullets)-1):
            key = bullets[i].get_text(strip=True).lower()
            val = bullets[i+1].get_text(strip=True)
            if "dimensions" in key and not product_dimensions:
                product_dimensions = val
            elif "item weight" in key and not item_weight:
                item_weight = val
    # ===========================

   # ======== 运费提取 ========
    shipping_text = safe_select_text(SELECTORS['shipping'])
    shipping = extract_shipping(shipping_text)
    # ==========================

    images = []

    # ===== 1. 从内嵌 JSON 中提取 hiRes 大图 =====
    try:
        # 匹配所有 "hiRes": "https://..." 形式的 URL
        hires_matches = re.findall(r'"hiRes"\s*:\s*"([^"]+)"', html)
        for url in hires_matches:
            if url and url.lower().startswith("http") and url not in images:
                images.append(url)
    except Exception as e:
        print(f"[WARN] JSON hiRes parse error: {e}")

    # ===== 2. 抓主图（备用）=====
    main_img = soup.select_one('#imgTagWrapperId img')
    if main_img:
        url = main_img.get('data-old-hires') or main_img.get('src')
        if url and url not in images:
            images.append(url)

    # ===== 3. 抓 data-old-hires 附图（备用）=====
    ul = soup.find("ul", class_="a-unordered-list")
    if ul:
        for li in ul.find_all("li", class_="image item"):
            wrapper = li.find("div", class_="imgTagWrapper")
            if wrapper:
                img = wrapper.find("img")
                if img:
                    url = img.get("data-old-hires") or img.get("src")
                    if url and url not in images:
                        images.append(url)

    return {
        'title': title,
        'price': price,
        'features': features,
        'description': description,
        'images': images,
        'category': category,
        # 'size': size,
        # 'weight': weight,
        'shipping': shipping,
        'product_dimensions': product_dimensions,
        'item_weight': item_weight
    }

# small utility to normalize text
def normalize_text(s):
    if not s:
        return ''
    return ' '.join(s.split())
