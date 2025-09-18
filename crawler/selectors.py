# crawler/selectors.py
# Centralize selectors for Amazon pages — update as Amazon HTML changes
SELECTORS = {
    'title': '#productTitle',
    'price': '.a-price .a-offscreen',
    'features': '#feature-bullets li',
    'description': '#productDescription',
    'images': '.a-unordered-list .imgTagWrapper img',
    'category': '#wayfinding-breadcrumbs_feature_div li',
    'product_dimensions': '#productDetails_techSpec_section_1 > tbody > tr:nth-child(3) > td',
    'item_weight': '#productDetails_techSpec_section_1 > tbody > tr:nth-child(6) > td',
    'shipping': '#mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE > span'
}