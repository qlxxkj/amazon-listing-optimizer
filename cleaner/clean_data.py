# # cleaner/clean_data.py
from bs4 import BeautifulSoup
from crawler.selectors import SELECTORS
import re, json


# ============ 工具函数 ============

def extract_shipping(text: str):
    """提取运费金额，免运费返回 0"""
    if not text:
        return 0
    text = text.strip()
    if "free" in text.lower():
        return 0
    m = re.search(r"([\d\.,]+)", text)
    return m.group(1) if m else 0

def clean_text(s):
    """去除Amazon中常见的隐藏字符"""
    if not s:
        return ""
    return (
        str(s)
        .replace("‎", "")
        .replace("\xa0", " ")
        .replace("\u200b", "")
        .replace("\u200e", "")
        .replace("×", "x")
        .strip()
    )

def parse_price(price):
    """去除货币符号，保留数字（float）"""
    if not price:
        return 0.0
    price = clean_text(price)
    m = re.search(r"([\d\.,]+)", price)
    if m:
        return float(m.group(1).replace(",", ""))
    return 0.0

def parse_dimensions(dim_text):
    """解析尺寸字符串，示例: '10.07 x 6.73 x 2.56 inches'"""
    if not dim_text:
        return 0.0, 0.0, 0.0, ""
    dim_text = clean_text(dim_text)
    match = re.match(
        r"([\d\.]+)\s*[xX]\s*([\d\.]+)\s*[xX]\s*([\d\.]+)\s*([a-zA-Z]+)?", dim_text
    )
    if match:
        return (
            float(match.group(1)),
            float(match.group(2)),
            float(match.group(3)),
            (match.group(4) or "").strip(),
        )
    return 0.0, 0.0, 0.0, ""

def parse_weight(weight_text):
    """解析重量字符串，示例: '2.89 pounds'"""
    if not weight_text:
        return 0.0, ""
    weight_text = clean_text(weight_text)
    match = re.match(r"([\d\.]+)\s*([a-zA-Z]+)", weight_text)
    if match:
        return float(match.group(1)), match.group(2)
    return 0.0, ""


# ============ 主清洗逻辑 ============
def parse_amazon_html(html):
    soup = BeautifulSoup(html, "lxml")

    def safe_select_text(sel):
        node = soup.select_one(sel)
        return node.get_text(strip=True) if node else ""

    def safe_select_multi(selectors):
        for sel in selectors:
            node = soup.select_one(sel)
            if node and node.get_text(strip=True):
                return node.get_text(strip=True)
        return ""

    # ============ ASIN & Parent ASIN ============
    asin_match = re.search(r"/dp/([A-Z0-9]{10})", html)
    asin = asin_match.group(1) if asin_match else ""

    parent_match = re.search(r'"parentAsin"\s*:\s*"([A-Z0-9]{10})"', html)
    parent_asin = parent_match.group(1) if parent_match else asin

    # ============ 基本字段 ============
    title = safe_select_text(SELECTORS["title"])
    price = safe_select_multi(SELECTORS["price"])
    features = [li.get_text(strip=True) for li in soup.select(SELECTORS["features"])]
    description = safe_select_text(SELECTORS["description"])
    category = "".join([li.get_text(strip=True) for li in soup.select(SELECTORS["category"])])
    brand = safe_select_text(SELECTORS["brand"])
    ratings = safe_select_text(SELECTORS["ratings"])
    reviews = safe_select_text(SELECTORS["reviews"])
    product_dimensions = safe_select_multi(SELECTORS["product_dimensions"])
    item_weight = safe_select_multi(SELECTORS["item_weight"])
    bought_in_past_month = safe_select_text(SELECTORS["bought_in_past_month"])
    BSR = safe_select_text(SELECTORS["BSR"])
    Date_First_Available = safe_select_text(SELECTORS["Date_First_Available"])
    OEM_Part_Number = safe_select_text(SELECTORS["OEM_Part_Number"])

    # ============ 派生字段 ============
    price_value = parse_price(price)
    item_length, item_width, item_height, item_size_unit = parse_dimensions(product_dimensions)
    item_weight_value, item_weight_unit = parse_weight(item_weight)

    # ============ 主图 & 附图 ============
    main_image = ""
    other_images = []
    main_node = soup.select_one("#imgTagWrapperId img")
    if main_node:
        main_image = main_node.get("data-old-hires") or main_node.get("src")

    hires_matches = re.findall(r'"hiRes"\s*:\s*"([^"]+)"', html)
    for img in hires_matches:
        if img and img not in other_images and img != main_image:
            other_images.append(img)

    # ============ 运费 ============
    shipping_text = safe_select_text(SELECTORS["shipping"])
    shipping = extract_shipping(shipping_text)

    # ============ 变体结构 ============
    variants = []
    variant_attributes = set()

    try:
        json_match = re.search(
            r'<script type="application/json" id="twister-js-init">(.+?)</script>',
            html,
            re.DOTALL,
        )
        if not json_match:
            json_match = re.search(
                r'<script type="application/json" id="twister-plus-inline-twister-data-init">(.+?)</script>',
                html,
                re.DOTALL,
            )

        if json_match:
            tw_data = json.loads(json_match.group(1))
            twister = tw_data.get("twisterData", {})

            color_images = twister.get("colorImages") or tw_data.get("colorImages", {})
            asin_variations = twister.get("asin_variations", {})
            dimension_labels = tw_data.get("variation_display_labels", {})

            for asin_key, v in asin_variations.items():
                variant = {
                    "asin": asin_key,
                    "attributes": {},
                    "price": v.get("price", price),
                    "main_image": "",
                    "images": [],
                }

                dims = v.get("dimensionsDisplay", {})
                for k, val in dims.items():
                    variant["attributes"][k.lower()] = val
                    variant_attributes.add(k.lower())

                # 图片
                if color_images.get(asin_key):
                    imgs = color_images[asin_key]
                    if imgs:
                        variant["main_image"] = imgs[0].get("hiRes") or imgs[0].get("large")
                        for img in imgs[1:]:
                            url = img.get("hiRes") or img.get("large")
                            if url:
                                variant["images"].append(url)

                variants.append(variant)

    except Exception as e:
        print(f"[WARN] Variant parse failed: {e}")

    # fallback DOM 变体
    if not variants:
        for node in soup.select("#variation_color_name li img"):
            color = node.get("alt") or ""
            img = node.get("src") or ""
            if color:
                variants.append(
                    {"asin": asin, "attributes": {"color": color}, "main_image": img, "images": []}
                )
                variant_attributes.add("color")


    # ============ 返回清洗结果 ============
    return {
        "asin": asin,
        "parent_asin": parent_asin,
        "title": title,
        "brand": brand,
        "price": price,  # 含货币符号
        "price_value": price_value,  # 纯数字
        "features": features,
        "description": description,
        "main_image": main_image,
        "other_images": other_images,
        "category": category,
        "product_dimensions": product_dimensions,
        "item_length": item_length,
        "item_width": item_width,
        "item_height": item_height,
        "item_size_unit": item_size_unit,
        "item_weight": item_weight,
        "item_weight_value": item_weight_value,
        "item_weight_unit": item_weight_unit,
        "ratings": ratings,
        "reviews": reviews,
        "shipping": shipping,
        "variants": variants,
        "variant_attributes": list(variant_attributes),
        "bought_in_past_month": bought_in_past_month,
        "BSR": BSR,
        "Date_First_Available": Date_First_Available,
        "OEM_Part_Number": OEM_Part_Number,
    }
