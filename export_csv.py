# export_csv.py
import os, csv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_, func
from db.db_config import engine
from db.save_data import listings_table

Session = sessionmaker(bind=engine)

def export_to_csv(output_path="out/result.csv", start_date=None, end_date=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    session = Session()

    query = select(listings_table)
    if start_date and end_date:
        query = query.where(
            and_(
                listings_table.c.created_at >= start_date,
                listings_table.c.created_at < end_date + " 23:59:59"
            )
        )
    elif start_date:
        query = query.where(listings_table.c.created_at >= start_date)
    elif end_date:
        query = query.where(listings_table.c.created_at < end_date + " 23:59:59")

    rows = session.execute(query).all()
    if not rows:
        print("[EXPORT] 没有符合条件的数据")
        return

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # 创建Excel导出模板
        writer.writerow([
            "url",
            "asin",
            "title_optimized",
            "description_optimized",
            "features_optimized",
            "title",
            "description",
            "features",
            "main_image",
            "other_images",
            "product_dimensions",
            "item_weight",
            "price",
            "shipping",
            "category",
            "ratings",
            "reviews",
            "bought_in_past_month",
            "brand",
            "BSR",
            "Date_First_Available",
            "variants",
            "variant_attributes"

        ])


        for row in rows:
            row = row._mapping
            opt = row.get("optimized") or {}
            cleaned = row.get("cleaned") or {}

            # 导出数据到Excel采集模板，要和模板字段顺序对应
            writer.writerow([
                row.get("url", ""),
                cleaned.get("asin"),
                opt.get("title_optimized", ""),
                opt.get("description_optimized", ""),
                "\n".join(opt.get("features_optimized", []) or []),
                cleaned.get("title", ""),
                cleaned.get("description", ""),
                "\n".join(cleaned.get("features", []) or []),
                cleaned.get("main_image",""),
                " ".join(cleaned.get("other_images") or []),
                cleaned.get("product_dimensions", ""),
                cleaned.get("item_weight", ""),
                cleaned.get("price", ""),
                cleaned.get("shipping", ""),
                cleaned.get("category", ""),
                cleaned.get("ratings",""),
                cleaned.get("reviews",""),
                cleaned.get("bought_in_past_month",""),
                cleaned.get("brand", ""),
                cleaned.get("BSR",""),
                cleaned.get("Date_First_Available",""),
            ])

    session.close()
    print(f"[EXPORT] 已生成 {output_path}，共 {len(rows)} 条数据")

# import csv
# import datetime
# import os
# import json
# import openpyxl

# from db.save_data import get_all_cleaned  # 你已有的函数：查询数据库cleaned结果

# def export_amazon_autopart_variations(xlsm_template_path: str, output_path: str):
#     """
#     将数据库中爬取 + 优化后的数据导出为适配亚马逊汽车零件模板的 XLSM。
#     保留宏，只在新 Sheet 中写入数据。
#     """
#     # 加载模板
#     wb = openpyxl.load_workbook(xlsm_template_path, keep_vba=True)
#     if "DataReady" in wb.sheetnames:
#         ws = wb["DataReady"]
#         wb.remove(ws)
#     ws = wb.create_sheet("DataReady")

#     # 写表头
#     headers = [
#         "parent-sku", "sku", "item-name", "brand-name", "standard-price",
#         "department-name", "product-description", "bullet_point1", "bullet_point2",
#         "bullet_point3", "bullet_point4", "bullet_point5",
#         "main-image-url", "other-image-url1", "other-image-url2", "other-image-url3",
#         "other-image-url4", "other-image-url5", "other-image-url6",
#         "other-image-url7", "other-image-url8", "other-image-url9", "other-image-url10",
#         "parentage", "relationship-type", "variation-theme",
#         "color-name", "size-name", "style-name",
#         "item-weight", "item-dimensions"
#     ]
#     ws.append(headers)

#     # 查询数据库数据
#     all_data = get_all_cleaned()
#     for row in all_data:
#         url = row["url"]
#         cleaned = row["cleaned"] or {}
#         title = cleaned.get("title", "")
#         brand = cleaned.get("brand", "")
#         description = cleaned.get("description", "")
#         price = cleaned.get("price", "").replace("$", "").strip()
#         category = cleaned.get("category", "")
#         features = cleaned.get("features", [])
#         weight = cleaned.get("item_weight", "")
#         dimensions = cleaned.get("product_dimensions", "")
#         main_image = cleaned.get("main_image", "")
#         other_images = cleaned.get("images", [])[1:11]

#         parent_asin = url.split("/dp/")[-1][:10]  # 用URL中ASIN作为父SKU

#         variants = cleaned.get("variants", [])
#         if not variants:
#             # 无变体商品
#             ws.append([
#                 parent_asin, parent_asin, title, brand, price,
#                 category, description,
#                 *features[:5],
#                 main_image, *other_images,
#                 "", "", "", "", "", "", "", "", "", "",
#                 "parent", "", "", "", "", "", weight, dimensions
#             ])
#         else:
#             # 写入父体
#             ws.append([
#                 parent_asin, parent_asin, title, brand, "", category, description,
#                 *features[:5],
#                 main_image, *other_images,
#                 "", "", "Size/Color", "", "", "", "", "", "", "",
#                 "parent", "", "Size/Color", "", "", "", weight, dimensions
#             ])

#             # 写入子体
#             for v in variants:
#                 asin = v.get("asin", "")
#                 v_price = v.get("price", price).replace("$", "").strip()
#                 v_main = v.get("main_image", "")
#                 v_imgs = v.get("images", [])[1:11]
#                 v_type = v.get("variant_type", "")
#                 v_value = v.get("variant_value", "")

#                 color = size = style = ""
#                 if "color" in v_type.lower():
#                     color = v_value
#                 elif "size" in v_type.lower():
#                     size = v_value
#                 else:
#                     style = v_value

#                 ws.append([
#                     parent_asin, asin, title, brand, v_price,
#                     category, description,
#                     *features[:5],
#                     v_main, *v_imgs,
#                     "", "child", "Size/Color",
#                     color, size, style,
#                     weight, dimensions
#                 ])

#     # 保存新文件
#     wb.save(output_path)
#     print(f"[EXPORT] ✅ 导出完成：{output_path}")
