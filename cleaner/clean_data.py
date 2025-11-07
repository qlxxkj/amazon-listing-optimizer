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


def parse_amazon_html(html):
    soup = BeautifulSoup(html, 'lxml')

    def safe_select_text(sel):
        node = soup.select_one(sel)
        return node.get_text(strip=True) if node else ''

    def safe_select_multi(selectors):
        """多选择器提取，按顺序尝试"""
        for sel in selectors:
            node = soup.select_one(sel)
            if node and node.get_text(strip=True):
                return node.get_text(strip=True)
        return ''

    ######################################
    #
    #  通用基础数据
    #
    ######################################

    # ===== 提取 ASIN =====
    asin_match = re.search(r"/dp/([A-Z0-9]{10})", html)
    asin = asin_match.group(1) if asin_match else ""

    # ============ 价格 ============
    price = safe_select_multi(SELECTORS['price'])

    # ============ 标题、特征、描述、分类 ============
    title = safe_select_text(SELECTORS['title'])
    features = [li.get_text(strip=True) for li in soup.select(SELECTORS['features'])]
    description = safe_select_text(SELECTORS['description'])
    category = ''.join([li.get_text(strip=True) for li in soup.select(SELECTORS['category'])])

    # ============ 评分 & 评论数 ============
    ratings = safe_select_text(SELECTORS['ratings'])
    reviews = safe_select_text(SELECTORS['reviews'])

    # ============ 近一个月销量 ============
    bought_in_past_month = safe_select_text(SELECTORS['bought_in_past_month'])

    # ============ 品牌 ============
    brand = safe_select_text(SELECTORS['brand'])

    # ============ 尺寸 & 重量 ============
    product_dimensions = safe_select_multi(SELECTORS['product_dimensions'])
    item_weight = safe_select_multi(SELECTORS['item_weight'])

    # ============ 运费 ============
    shipping_text = safe_select_text(SELECTORS['shipping'])
    shipping = extract_shipping(shipping_text)

    # ========== BSR 排名 & 上架时间 ====
    BSR = safe_select_text(SELECTORS['BSR'])
    Date_First_Available = safe_select_text(SELECTORS['Date_First_Available'])

    # ===== 图片：区分主图与附图 =====
    main_image = ""
    other_images = []

    main_node = soup.select_one("#imgTagWrapperId img")
    if main_node:
        main_image = main_node.get("data-old-hires") or main_node.get("src")

    hires_matches = re.findall(r'"hiRes"\s*:\s*"([^"]+)"', html)
    for img in hires_matches:
        if img and img.lower().startswith("http") and img not in other_images and img != main_image:
            other_images.append(img)

    # ===== 运费 =====
    shipping_text = safe_select_text(SELECTORS["shipping"])
    shipping = 0
    if "free" in shipping_text.lower():
        shipping = 0
    else:
        m = re.search(r"\$([\d\.,]+)", shipping_text)
        if m:
            shipping = m.group(1)

    #################################################
    #
    # 变体信息
    #
    #################################################
    variants = []
    variant_attributes = set()

    try:
        # 抓取变体结构 JSON
        json_match = re.search(
            r'<script type="application/json" id="twister-plus-inline-twister-data-init">(.+?)</script>',
            html,
            re.DOTALL,
        )
        if not json_match:
            json_match = re.search(
                r'<script type="application/json" id="twister-js-init">(.+?)</script>',
                html,
                re.DOTALL,
            )

        if json_match:
            tw_data = json.loads(json_match.group(1))
            twister = tw_data.get("twisterData", {})

            # 优先解析 colorImages (有时更全面)
            color_images = twister.get("colorImages") or tw_data.get("colorImages")

            for asin_key, v in twister.get("asin_variations", {}).items():
                variant = {"asin": asin_key, "attributes": {}, "price": "", "main_image": "", "images": []}

                # 属性
                dims = v.get("dimensionsDisplay", {})
                for k, val in dims.items():
                    variant["attributes"][k.lower()] = val
                    variant_attributes.add(k.lower())

                # 价格
                if "price" in v:
                    variant["price"] = v["price"]

                # 变体主图（优先 colorImages）
                if color_images and asin_key in color_images:
                    imgs = color_images[asin_key]
                    if imgs:
                        variant["main_image"] = imgs[0].get("hiRes") or imgs[0].get("large")
                        for img in imgs[1:]:
                            url = img.get("hiRes") or img.get("large")
                            if url:
                                variant["images"].append(url)
                else:
                    # 备用来源
                    img = v.get("image", "")
                    if isinstance(img, str) and img.startswith("http"):
                        variant["main_image"] = img

                variants.append(variant)

    except Exception as e:
        print(f"[WARN] Failed to parse variant JSON: {e}")

    # ===== Fallback: DOM 提取（部分站点）=====
    if not variants:
        color_nodes = soup.select("#variation_color_name li img")
        for node in color_nodes:
            color = node.get("alt") or node.get("title") or ""
            img = node.get("src") or node.get("data-old-hires") or ""
            if color:
                variants.append({
                    "asin": asin,
                    "attributes": {"color": color},
                    "main_image": img,
                    "images": [],
                })
                variant_attributes.add("color")

        size_nodes = soup.select("#variation_size_name li")
        for node in size_nodes:
            size = node.get_text(strip=True)
            if size:
                variants.append({
                    "asin": asin,
                    "attributes": {"size": size},
                    "main_image": "",
                    "images": [],
                })
                variant_attributes.add("size")


    return {
        'asin': asin,
        'title': title,
        'price': price,
        'features': features,
        'description': description,
        'main_image': main_image,
        'other_images': other_images,
        'category': category,
        'shipping': shipping,
        'product_dimensions': product_dimensions,
        'item_weight': item_weight,
        'ratings': ratings,
        'reviews': reviews,
        'bought_in_past_month': bought_in_past_month,
        'brand': brand,
        'BSR': BSR,
        'Date_First_Available': Date_First_Available,
        'variants': variants,
        'variant_attributes': list(variant_attributes),
    }


# small utility to normalize text
def normalize_text(s):
    if not s:
        return ''
    return ' '.join(s.split())

# import re
# import json
# from bs4 import BeautifulSoup

# def parse_amazon_html(html: str):
#     """
#     从亚马逊商品页HTML中提取基础信息 + 变体信息
#     """
#     soup = BeautifulSoup(html, "html.parser")

#     def get_text(sel_list):
#         for sel in sel_list:
#             el = soup.select_one(sel)
#             if el and el.get_text(strip=True):
#                 return el.get_text(strip=True)
#         return ""

#     def get_all(sel_list):
#         results = []
#         for sel in sel_list:
#             for el in soup.select(sel):
#                 txt = el.get_text(strip=True)
#                 if txt:
#                     results.append(txt)
#         return results

#     def get_attr(sel_list, attr):
#         for sel in sel_list:
#             el = soup.select_one(sel)
#             if el and el.has_attr(attr):
#                 return el[attr]
#         return ""

#     # ========== 基础信息 ==========
#     title = get_text(["#productTitle", "span#title", "h1.a-size-large"])
#     price = get_text([
#         ".a-price .a-offscreen",
#         "#priceblock_ourprice",
#         "#priceblock_dealprice",
#         "#corePriceDisplay_desktop_feature_div span.a-offscreen",
#         "span.offer-price",
#         "span.aok-offscreen"
#     ])
#     description = get_text([
#         "#productDescription p",
#         "#feature-bullets ul",
#         "#aplus",
#         "#bookDescription_feature_div"
#     ])
#     bullets = get_all(["#feature-bullets li span.a-list-item"])
#     brand = get_text(["#bylineInfo", "tr.po-brand td.a-span9 span"])
#     dimensions = get_text(["tr.po-item_dimensions td.a-span9", "#productDetails_techSpec_section_1 td"])
#     weight = get_text(["tr.po-item_weight td.a-span9", "#detailBullets_feature_div li span.a-text-bold:-soup-contains('Item Weight') + span"])
#     category = " > ".join([el.get_text(strip=True) for el in soup.select("#wayfinding-breadcrumbs_container a")])
#     images = [img["src"] for img in soup.select("#altImages img") if "src" in img.attrs]

#     # 主图：优先高清图
#     main_image = ""
#     for meta in soup.select('meta[property="og:image"]'):
#         main_image = meta.get("content", "")
#         break
#     if not main_image and images:
#         main_image = images[0]

#     # ========== 变体提取（核心部分） ==========
#     variants = []
#     try:
#         # 从 script 中提取 “twister” 数据或 “dimensionValuesDisplayData”
#         script_tags = soup.find_all("script", text=re.compile("dimensionValuesDisplayData|twister-js-init-dpx-data"))
#         for script in script_tags:
#             text = script.get_text()
#             if "dimensionValuesDisplayData" in text:
#                 json_str = re.search(r'dimensionValuesDisplayData\s*=\s*({.*?});', text)
#                 if json_str:
#                     data = json.loads(json_str.group(1))
#                     for asin, attrs in data.items():
#                         variant_info = {"asin": asin}
#                         for key, val in attrs.items():
#                             variant_info["variant_type"] = key
#                             variant_info["variant_value"] = val
#                         variants.append(variant_info)
#             elif "twister-js-init-dpx-data" in text:
#                 json_str = re.search(r"twister-js-init-dpx-data\s*=\s*({.*?})\s*;", text)
#                 if json_str:
#                     data = json.loads(json_str.group(1))
#                     child_asins = data.get("childAsins", [])
#                     variation_display = data.get("variationDisplayLabels", {})
#                     for asin in child_asins:
#                         variant_info = {"asin": asin}
#                         for k, v in variation_display.items():
#                             variant_info["variant_type"] = k
#                             variant_info["variant_value"] = v
#                         variants.append(variant_info)
#     except Exception as e:
#         print(f"[WARN] Failed to parse variants: {e}")

#     # ========== 补充变体图片与价格 ==========
#     try:
#         # 有些变体图片信息在 data-a-dynamic-image 中
#         img_blocks = soup.select("img[data-a-dynamic-image]")
#         for vb in img_blocks:
#             asin_guess = vb.get("data-asin") or vb.get("alt") or ""
#             imgs = list(json.loads(vb["data-a-dynamic-image"]).keys())
#             if not imgs:
#                 continue
#             found = next((v for v in variants if asin_guess and asin_guess in v.get("asin", "")), None)
#             if found:
#                 found["images"] = imgs
#                 found["main_image"] = imgs[0]
#     except Exception:
#         pass

#     # 如果无变体图片，也补空字段
#     for v in variants:
#         v.setdefault("images", [])
#         v.setdefault("main_image", "")
#         v.setdefault("price", price)
#         v.setdefault("product_dimensions", dimensions)
#         v.setdefault("item_weight", weight)

#     # ========== 汇总 ==========
#     cleaned = {
#         "title": title,
#         "price": price,
#         "description": description,
#         "features": bullets,
#         "brand": brand,
#         "category": category,
#         "item_weight": weight,
#         "product_dimensions": dimensions,
#         "main_image": main_image,
#         "images": images,
#         "variants": variants,
#     }

#     return cleaned
