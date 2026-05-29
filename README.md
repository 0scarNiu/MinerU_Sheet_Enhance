# MinerU_Sheet_Enhance
Mineru在处理较大尺寸的工程图像时会渲染DPI，可能会导致该页面的其余表格的分辨率很低，从而影响识别精度，但是能通过json文件获取其bbox重新进行高DPI截取，再通过mineru即可实现表格的高精度识别  

图一乐吧，至少对我挺方便的  QAQ

OCR目录情况
--DIR
  --a.pdf
  --b.pdf
  --...

OCR后格式为
--DIR_OCR
  --a
    --hybrid_auto
      --具体内容
  --b
    --hybrid_auto
      --具体内容
  --...

文件夹格式sheet_enhance的root文件夹，即为刚才的DIR_OCR
--root_dir  
  --a
    --hybrid_auto
      --具体内容
  --b
    --hybrid_auto
      --具体内容
  --...

  处理完会生成对应的png
