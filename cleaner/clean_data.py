# cleaner/clean_data.py
from bs4 import BeautifulSoup
from crawler.selectors import SELECTORS
import re,json

def extract_shipping(text: str):
    """提取运费金额，免运费返回 0"""
    if not text:
        return 0
    text = text.strip()
    if "free" in text.lower():
        return 0
    m = re.search(r"([\d\.,]+)", text)
    return m.group(1) if m else 0


# def parse_amazon_html(html):
#     soup = BeautifulSoup(html, 'lxml')

#     def safe_select_text(sel):
#         node = soup.select_one(sel)
#         return node.get_text(strip=True) if node else ''

#     def safe_select_multi(selectors):
#         """多选择器提取，按顺序尝试"""
#         for sel in selectors:
#             node = soup.select_one(sel)
#             if node and node.get_text(strip=True):
#                 return node.get_text(strip=True)
#         return ''

#     ######################################
#     #
#     #  通用基础数据
#     #
#     ######################################

#     # ===== 提取 ASIN =====
#     asin_match = re.search(r"/dp/([A-Z0-9]{10})", html)
#     asin = asin_match.group(1) if asin_match else ""

#     # ============ 价格 ============
#     price = safe_select_multi(SELECTORS['price'])

#     # ============ 标题、特征、描述、分类 ============
#     title = safe_select_text(SELECTORS['title'])
#     features = [li.get_text(strip=True) for li in soup.select(SELECTORS['features'])]
#     description = safe_select_text(SELECTORS['description'])
#     category = ''.join([li.get_text(strip=True) for li in soup.select(SELECTORS['category'])])

#     # ============ 评分 & 评论数 ============
#     ratings = safe_select_text(SELECTORS['ratings'])
#     reviews = safe_select_text(SELECTORS['reviews'])

#     # ============ 近一个月销量 ============
#     bought_in_past_month = safe_select_text(SELECTORS['bought_in_past_month'])

#     # ============ 品牌 ============
#     brand = safe_select_text(SELECTORS['brand'])

#     # ============ 尺寸 & 重量 ============
#     product_dimensions = safe_select_multi(SELECTORS['product_dimensions'])
#     item_weight = safe_select_multi(SELECTORS['item_weight'])

#     # ============ 运费 ============
#     shipping_text = safe_select_text(SELECTORS['shipping'])
#     shipping = extract_shipping(shipping_text)

#     # ========== BSR 排名 & 上架时间 ====
#     BSR = safe_select_text(SELECTORS['BSR'])
#     Date_First_Available = safe_select_text(SELECTORS['Date_First_Available'])

#     # ===== 图片：区分主图与附图 =====
#     main_image = ""
#     other_images = []

#     main_node = soup.select_one("#imgTagWrapperId img")
#     if main_node:
#         main_image = main_node.get("data-old-hires") or main_node.get("src")

#     hires_matches = re.findall(r'"hiRes"\s*:\s*"([^"]+)"', html)
#     for img in hires_matches:
#         if img and img.lower().startswith("http") and img not in other_images and img != main_image:
#             other_images.append(img)

#     # ===== 运费 =====
#     shipping_text = safe_select_text(SELECTORS["shipping"])
#     shipping = 0
#     if "free" in shipping_text.lower():
#         shipping = 0
#     else:
#         m = re.search(r"\$([\d\.,]+)", shipping_text)
#         if m:
#             shipping = m.group(1)

#     #################################################
#     #
#     # 变体信息
#     #
#     #################################################
#     variants = []
#     variant_attributes = set()

#     try:
#         # 抓取变体结构 JSON
#         json_match = re.search(
#             r'<script type="application/json" id="twister-plus-inline-twister-data-init">(.+?)</script>',
#             html,
#             re.DOTALL,
#         )
#         if not json_match:
#             json_match = re.search(
#                 r'<script type="application/json" id="twister-js-init">(.+?)</script>',
#                 html,
#                 re.DOTALL,
#             )

#         if json_match:
#             tw_data = json.loads(json_match.group(1))
#             twister = tw_data.get("twisterData", {})

#             # 优先解析 colorImages (有时更全面)
#             color_images = twister.get("colorImages") or tw_data.get("colorImages")

#             for asin_key, v in twister.get("asin_variations", {}).items():
#                 variant = {"asin": asin_key, "attributes": {}, "price": "", "main_image": "", "images": []}

#                 # 属性
#                 dims = v.get("dimensionsDisplay", {})
#                 for k, val in dims.items():
#                     variant["attributes"][k.lower()] = val
#                     variant_attributes.add(k.lower())

#                 # 价格
#                 if "price" in v:
#                     variant["price"] = v["price"]

#                 # 变体主图（优先 colorImages）
#                 if color_images and asin_key in color_images:
#                     imgs = color_images[asin_key]
#                     if imgs:
#                         variant["main_image"] = imgs[0].get("hiRes") or imgs[0].get("large")
#                         for img in imgs[1:]:
#                             url = img.get("hiRes") or img.get("large")
#                             if url:
#                                 variant["images"].append(url)
#                 else:
#                     # 备用来源
#                     img = v.get("image", "")
#                     if isinstance(img, str) and img.startswith("http"):
#                         variant["main_image"] = img

#                 variants.append(variant)

#     except Exception as e:
#         print(f"[WARN] Failed to parse variant JSON: {e}")

#     # ===== Fallback: DOM 提取（部分站点）=====
#     if not variants:
#         color_nodes = soup.select("#variation_color_name li img")
#         for node in color_nodes:
#             color = node.get("alt") or node.get("title") or ""
#             img = node.get("src") or node.get("data-old-hires") or ""
#             if color:
#                 variants.append({
#                     "asin": asin,
#                     "attributes": {"color": color},
#                     "main_image": img,
#                     "images": [],
#                 })
#                 variant_attributes.add("color")

#         size_nodes = soup.select("#variation_size_name li")
#         for node in size_nodes:
#             size = node.get_text(strip=True)
#             if size:
#                 variants.append({
#                     "asin": asin,
#                     "attributes": {"size": size},
#                     "main_image": "",
#                     "images": [],
#                 })
#                 variant_attributes.add("size")


#     return {
#         'asin': asin,
#         'title': title,
#         'price': price,
#         'features': features,
#         'description': description,
#         'main_image': main_image,
#         'other_images': other_images,
#         'category': category,
#         'shipping': shipping,
#         'product_dimensions': product_dimensions,
#         'item_weight': item_weight,
#         'ratings': ratings,
#         'reviews': reviews,
#         'bought_in_past_month': bought_in_past_month,
#         'brand': brand,
#         'BSR': BSR,
#         'Date_First_Available': Date_First_Available,
#         'variants': variants,
#         'variant_attributes': list(variant_attributes),
#     }


# # small utility to normalize text
# def normalize_text(s):
#     if not s:
#         return ''
#     return ' '.join(s.split())

def parse_amazon_html(html):
    soup = BeautifulSoup(html, 'lxml')

    def safe_select_text(sel):
        node = soup.select_one(sel)
        return node.get_text(strip=True) if node else ''

    def safe_select_multi(selectors):
        for sel in selectors:
            node = soup.select_one(sel)
            if node and node.get_text(strip=True):
                return node.get_text(strip=True)
        return ''

    # ============ ASIN & Parent ASIN ============
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', html)
    asin = asin_match.group(1) if asin_match else ""

    parent_match = re.search(r'"parentAsin"\s*:\s*"([A-Z0-9]{10})"', html)
    parent_asin = parent_match.group(1) if parent_match else asin

    # ============ 基本字段 ============
    title = safe_select_text(SELECTORS['title'])
    price = safe_select_multi(SELECTORS['price'])
    features = [li.get_text(strip=True) for li in soup.select(SELECTORS['features'])]
    description = safe_select_text(SELECTORS['description'])
    category = ''.join([li.get_text(strip=True) for li in soup.select(SELECTORS['category'])])
    brand = safe_select_text(SELECTORS['brand'])
    ratings = safe_select_text(SELECTORS['ratings'])
    reviews = safe_select_text(SELECTORS['reviews'])
    product_dimensions = safe_select_multi(SELECTORS['product_dimensions'])
    item_weight = safe_select_multi(SELECTORS['item_weight'])
    bought_in_past_month = safe_select_text(SELECTORS['bought_in_past_month'])
    BSR = safe_select_text(SELECTORS['BSR'])
    Date_First_Available = safe_select_text(SELECTORS['Date_First_Available'])
    OEM_Part_Number = safe_select_text(SELECTORS['OEM_Part_Number'])


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
    shipping_text = safe_select_text(SELECTORS['shipping'])
    shipping = extract_shipping(shipping_text)

    # ============ 变体结构 ============
    variants = []
    variant_attributes = set()

    try:
        # 1️⃣ 尝试新版 JSON 结构
        json_match = re.search(r'<script type="application/json" id="twister-js-init">(.+?)</script>', html, re.DOTALL)
        if not json_match:
            json_match = re.search(r'<script type="application/json" id="twister-plus-inline-twister-data-init">(.+?)</script>', html, re.DOTALL)

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

                # 2️⃣ 处理图片（主图 + 附图）
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

    # Fallback DOM 变体
    if not variants:
        for node in soup.select("#variation_color_name li img"):
            color = node.get("alt") or ""
            img = node.get("src") or ""
            if color:
                variants.append({
                    "asin": asin,
                    "attributes": {"color": color},
                    "main_image": img,
                    "images": [],
                })
                variant_attributes.add("color")

    return {
        "asin": asin,
        "parent_asin": parent_asin,
        "title": title,
        "brand": brand,
        "price": price,
        "features": features,
        "description": description,
        "main_image": main_image,
        "other_images": other_images,
        "category": category,
        "product_dimensions": product_dimensions,
        "item_weight": item_weight,
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
