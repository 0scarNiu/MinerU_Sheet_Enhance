#用于先MinerU一次产生了对应的相应json文件
#通过其middle.json文件取得其表格的边界信息

import fitz
import json
import os

#参数部分：
#存放mineru处理后的整体的文件夹
root_dir = ""
#输出重新截取表格图片的位置
img_output_dir = ""
#对图片的渲染600 800
dpi = 600

#路径处理
pdf_abs_path = os.path.abspath(root_dir)
#pdf_name, pdf_ext = os.path.splitext(pdf_abs_path)

#遍历
for root, dirs, files in os.walk(root_dir):
    origin_pdf_path = None
    middle_json_path = None

    for file in files:
        if "origin.pdf" in file: 
            origin_pdf_path = os.path.join(root, file)
        if "middle.json" in file:
            middle_json_path = os.path.join(root, file)

        if not origin_pdf_path or not middle_json_path:
            continue

        doc = fitz.open(origin_pdf_path)

        #没找到content就下一个
        print("获得middle.json用于寻找bbox",middle_json_path)

        parent_name = os.path.basename(os.path.dirname(root))
        current_output_dir = os.path.join(img_output_dir, parent_name)
        os.makedirs(current_output_dir, exist_ok=True)

        #读取json文件
        with open(middle_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        table_idx = 0

        for page_idx, page_data in enumerate(data["pdf_info"]):
            
            page = doc[page_idx]    #拿页码的具体页，准备缩放裁剪
            mineru_w, mineru_h = page_data["page_size"]
                
            zoom = dpi/72
            mat = fitz.Matrix(zoom, zoom)

            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = pix.pil_image()
            render_w, render_h = img.size

            scale_x = render_w / mineru_w
            scale_y = render_h / mineru_h

            # blocks
            blocks = page_data["para_blocks"]

            for block in blocks:
                if block["type"] != "table":
                    continue

                x0, y0, x1, y1 = block["bbox"]

                # remap
                crop_x0 = int(x0 * scale_x)
                crop_y0 = int(y0 * scale_y)
                crop_x1 = int(x1 * scale_x)
                crop_y1 = int(y1 * scale_y)

                # padding边界值 提升可靠性
                pad = 20

                crop_x0 = max(crop_x0 - pad, 0)
                crop_y0 = max(crop_y0 - pad, 0)
                crop_x1 = min(crop_x1 + pad, render_w)
                crop_y1 = min(crop_y1 + pad, render_h)

                table_img = img.crop(
                    (crop_x0, crop_y0, crop_x1, crop_y1)
                )

                gray = table_img.convert("L")

                threshold = 254
                binary = gray.point(lambda x: 255 if x > threshold else 0,mode='1')
                table_img = binary
                pdf_stem = os.path.splitext(os.path.basename(origin_pdf_path))[0]
                #out_path = os.path.join(img_output_dir,f"page_{page_idx+1}_table_{table_idx}.png")
                out_path = os.path.join(current_output_dir,f"{pdf_stem}_page_{page_idx+1}_table_{table_idx}.png")

                table_img.save(out_path)
                print("保存：",out_path)
                table_idx += 1



