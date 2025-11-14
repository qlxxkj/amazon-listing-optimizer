# export_csv.py
import os, csv
from db.save_data import get_all_data



def export_to_csv(output_path="out/result.csv", start_date=None, end_date=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rows = get_all_data(start_date=start_date,end_date=end_date)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # 创建Excel导出模板
        writer.writerow([
            "url",
            "asin",
            "title_optimized",
            "description_optimized",
            "features_optimized",
            "search_keywords",
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
            "variant_attributes",
            "OEM_Part_Number",

        ])


        for row in rows:
            row = row._mapping
            opt = row.get("optimized") or {}
            cleaned = row.get("cleaned") or {}

            # 导出数据到Excel采集模板，要和模板字段顺序对应
            writer.writerow([
                row.get("url", ""),
                cleaned.get("asin"),
                opt.get("optimized_title", ""),
                opt.get("optimized_description", ""),
                "\n".join(opt.get("optimized_features", []) or []),
                opt.get("search_keywords",""),
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
                cleaned.get("variants", ""),
                cleaned.get("variant_attributes", ""),
                cleaned.get("OEM_Part_Number",""),

            ])

    print(f"[EXPORT] 已生成 {output_path}，共 {len(rows)} 条数据")