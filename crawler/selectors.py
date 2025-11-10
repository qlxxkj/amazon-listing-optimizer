# crawler/selectors.py

# ============ 通用基础选择器 ============
BASE_SELECTORS = {
    "title": "#title #productTitle",
    "features": "#feature-bullets ul li",
    "description": "#productDescription",
    "category": "#wayfinding-breadcrumbs_feature_div li",
    "shipping": "#mir-layout-DELIVERY_BLOCK slot",  # 可能需要补充
    "ratings": "#acrPopover span.a-declarative a span",
    "reviews": "#acrCustomerReviewText",
    "bought_in_past_month": "#social-proofing-faceout-title-tk_bought span.a-text-bold",
    "brand": "tr:has(th:-soup-contains('Brand')) td", #
    "BSR": "tr:has(th:-soup-contains('Best Sellers Rank')) td",
    "Date_First_Available": "tr:has(th:-soup-contains('Date First Available')) td",
    "OEM Part Number":"tr:has(th:-soup-contains('OEM Part Number')) td",
}

# ============ 多语言价格选择器 ============
PRICE_SELECTORS = [
    ".a-price .a-offscreen",  # 通用
    "#priceblock_ourprice",   # 普通售价（旧版）
    "#priceblock_dealprice",  # 折扣价
    "#corePriceDisplay_desktop_feature_div span.a-offscreen",  # 新版布局
    "span.offer-price",       # 部分地区
    "span.aok-offscreen",
    "span#price_inside_buybox",   # UK/DE 常见
    "span#priceblock_saleprice",  # 特殊促销价
    "span.a-price-whole",
    "#corePriceDisplay_desktop_feature_div div.a-section.a-spacing-none.aok-align-center.aok-relative span.aok-offscreen",
]

# ============ 多语言尺寸选择器 ============
PRODUCT_DIMENSIONS_SELECTORS = [
    # 英文
    "tr:has(th:-soup-contains('Dimensions')) td",
    "tr:has(th:-soup-contains('Product Dimensions')) td",
    "#detailBullets_feature_div li:-soup-contains('Dimensions') span.a-text-bold + span",
    "#prodDetails .a-keyvalue tr:-soup-contains('Product Dimensions') td",
    # 日语
    "tr:has(th:-soup-contains('商品の寸法')) td",
    "#detailBullets_feature_div li:-soup-contains('商品の寸法') span.a-text-bold + span",
    # 德语
    "tr:has(th:-soup-contains('Produktabmessungen')) td",
    "#detailBullets_feature_div li:-soup-contains('Produktabmessungen') span.a-text-bold + span",
    # 法语
    "tr:has(th:-soup-contains('Dimensions du produit')) td",
    "#detailBullets_feature_div li:-soup-contains('Dimensions du produit') span.a-text-bold + span",
    # 西班牙语
    "tr:has(th:-soup-contains('Dimensiones del producto')) td",
    "#detailBullets_feature_div li:-soup-contains('Dimensiones del producto') span.a-text-bold + span",
]

# ============ 多语言重量选择器 ============
ITEM_WEIGHT_SELECTORS = [
    # 英文
    "tr:has(th:-soup-contains('Item Weight')) td",
    "#detailBullets_feature_div li:-soup-contains('Item Weight') span.a-text-bold + span",
    "#prodDetails .a-keyvalue tr:-soup-contains('Item Weight') td",
    "#detailBullets_feature_div ul li:nth-child(1) span span:nth-child(2)",
    # 日语
    "tr:has(th:-soup-contains('商品の重量')) td",
    "#detailBullets_feature_div li:-soup-contains('商品の重量') span.a-text-bold + span",
    # 德语
    "tr:has(th:-soup-contains('Artikelgewicht')) td",
    "#detailBullets_feature_div li:-soup-contains('Artikelgewicht') span.a-text-bold + span",
    # 法语
    "tr:has(th:-soup-contains('Poids de l')) td",
    "#detailBullets_feature_div li:-soup-contains('Poids de l') span.a-text-bold + span",
    # 西班牙语
    "tr:has(th:-soup-contains('Peso del producto')) td",
    "#detailBullets_feature_div li:-soup-contains('Peso del producto') span.a-text-bold + span",
]

# ============ 对外统一接口 ============
SELECTORS = {
    "title": BASE_SELECTORS["title"],
    "features": BASE_SELECTORS["features"],
    "description": BASE_SELECTORS["description"],
    "category": BASE_SELECTORS["category"],
    "shipping": BASE_SELECTORS["shipping"],
    "ratings": BASE_SELECTORS["ratings"],
    "reviews": BASE_SELECTORS["reviews"],
    "bought_in_past_month": BASE_SELECTORS['bought_in_past_month'],
    "brand": BASE_SELECTORS['brand'],
    "BSR": BASE_SELECTORS['BSR'],
    "Date_First_Available": BASE_SELECTORS['Date_First_Available'],
    "OEM_Part_Number": BASE_SELECTORS['OEM Part Number'],

    "price": PRICE_SELECTORS,
    "product_dimensions": PRODUCT_DIMENSIONS_SELECTORS,
    "item_weight": ITEM_WEIGHT_SELECTORS,
}
