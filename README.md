# JupyterToHtml
将jupyter notebook的文件转换为html文件
偶尔需要将jupyter notebook的文件转换为hml或pdf，但觉得jupyter自带的转换功能又有点丑，于是自己写了一个脚本。

jupyter notebook的打印预览长这样

![image-20220222171024116](F:\typora imgs\image-20220222171024116.png)

自己脚本转换出来html的长下面这样

![image-20220222171141347](F:\typora imgs\image-20220222171141347.png)

或者长这样

![image-20220222171615469](F:\typora imgs\image-20220222171615469.png)

你可以在脚本中更改配置得到自己需要的效果

```python
# 样式配置
style_config = {
	# 页面
	'page_with' : '90%', 							# 页面宽度 1%~100%

	# 代码块
	'code_base_style': 'monokai', 					# pygments代码高亮预设: xcode、monokai、trac、rainbow_dash、perldoc、vim、rrt、autumn、lovelace
	'code_font_size' : '12pt',						# 字体大小
	'code_font-family' : 'monaco',					# 字体名称
	'code_borer_radius' : '2px',					# 边框圆角半径
	'code_borer_with' : '1px',						# 边框宽度
	'code_line-height' : '1.5',						# 行高
	
	# 文本输出
	'output_color' : '#424242',						# 字体颜色
	'output_font_size' : '12pt',					# 字体大小
	'output_font_family' : 'monaco',				# 字体名称

	# 表格
	'table_font_size' : '10pt', 					# 字体大小
	'table_font_family' : 'arial', 					# 字体名称
	'table_color' : '#000', 						# 字体颜色
	'table_border' : 'none', 						# 边框，默认无边框：1px solid #000
	'table_background_color_odd' : '#fff', 			# 奇数行背景颜色
	'table_background_color_even' : '#eee', 		# 偶数行背景颜色
	'table_align' : 'center',						# 表格在页面中的水平位置：center、left

	# 图片
	'img_align' : 'center',							# 表格在页面中的水平位置：center、left

	# markdown
	'markdown_font_family' : 'Microsoft YaHei'		# markdown字体名称
}
```

现在暂不支持latex公式

注：运行此脚本需要两个包

```shell
pip install pygments # 代码高亮
pip install markdown # 将markdown转化为html
```

