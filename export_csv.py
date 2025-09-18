# export_csv.py
import csv
import os

def export_to_csv(products, filename="out/result.csv"):
    """
    products: 本次批次抓取和优化后的数据列表，每项为 dict：
        {
            'url': str,
            'title': str,
            'optimized': dict,   # 优化结果
            'images': list,       # 图片列表
            'product_dimensions': str,
            'item_weight': str,
            'price': str,
            'shipping': str,
            'category': str
        }
    """
    if not products:
        print("[EXPORT] 没有数据可导出")
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "title", "description", "bullet_points", "images","product_dimensions","item_weight","price","shipping","category"])

        for p in products:
            opt = p.get("optimized") or {}
            bullets = opt.get("bullets") or []
            images = p.get("images") or []

            writer.writerow([
                p.get("url", ""),
                opt.get("title", ""),
                opt.get("description", ""),
                "\n".join([b for b in bullets if b]),
                " | ".join([img for img in images if img]),
                opt.get("product_dimensions",""),
                opt.get("item_weight",""),
                opt.get("price",""),
                opt.get("shipping",""),
                opt.get("category")
            ])
    print(f"[EXPORT] 已生成 {filename}，共 {len(products)} 条数据")
