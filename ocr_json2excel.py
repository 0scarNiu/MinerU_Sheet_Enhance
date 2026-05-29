#再将刚才的png重新经过mineru ocr之后效果基本上没问题了
#故只需要将content.json中的table提取出对应内容即可保存成excel
#批量处理 json -> excel

import os
import json
import pandas as pd

#输入路径
root_dir = ""
output_dir = ""

os.makedirs(output_dir, exist_ok=True)

table_count = 0

for root, dirs, files in os.walk(root_dir):

    for file in files:

        # 找 content_list.json
        if "content_list.json" not in file:
            continue

        json_path = os.path.join(root, file)

        print("processing:", json_path)

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # list
            if isinstance(data, list):
                items = data

            # dict
            elif "content_list" in data:
                items = data["content_list"]

            else:
                print("unknown json structure")
                continue

            # 遍历 table
            for item in items:

                if item.get("type") != "table":
                    continue

                # html字段兼容
                html = (
                    item.get("html")
                    or item.get("table_body")
                    or ""
                )

                if not html:
                    continue
                
                #对于工程图经常会有固定表格，可以通过寻找其共同html内容跳过他们
                wrong_html = ""

                if wrong_html in html:
                    continue

                try:
                    dfs = pd.read_html(html)

                    if len(dfs) == 0:
                        continue

                    df = dfs[0]

                    # 父目录名
                    parent_name = os.path.basename(
                        os.path.dirname(root)
                    )

                    # excel名字
                    excel_name = (
                        f"{parent_name}_{table_count}.xlsx"
                    )

                    out_path = os.path.join(
                        output_dir,
                        excel_name
                    )

                    df.to_excel(
                        out_path,
                        index=False
                    )

                    print("saved:", out_path)

                    table_count += 1

                except Exception as e:
                    print("table parse failed:", e)

        except Exception as e:
            print("json read failed:", e)
