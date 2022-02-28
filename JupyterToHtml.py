# JupyterToHtml.py
import json
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from markdown import markdown
import os

# 样式配置
style_config = {
	# 页面
	'page_with' : '90%', 							# 页面宽度 1%~100%

	# 代码块
	'code_base_style': 'xcode', 				# pygments代码高亮预设: xcode、monokai、trac、rainbow_dash、perldoc、vim、rrt、autumn、lovelace
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
	'table_align' : 'left',						# 表格在页面中的水平位置：center、left

	# 图片
	'img_align' : 'left',							# 表格在页面中的水平位置：center、left

	# markdown
	'markdown_font_family' : 'Microsoft YaHei'		# markdown字体名称
}

# 将输出内容转化为html标签
def decode_output(outputs):
	out = []

	# 以下依次是图片、表格、纯文本的处理函数
	out_format = {
		'image/png' : lambda x: out.append('<div class = "image"><img src="data:image/png;base64,{}"></div>'.format(x)),
		'text/html' : lambda x: out.append('<div class = "tebleContainer">{}</div>'.format(''.join(x))),
		'text/plain' : lambda x: out.append('<pre class = "plaintext">{}</pre>'.format(''.join(x)))
	}

	# 遍历输出内容列表
	for o in outputs:
		if 'text' in o.keys(): # 优先处理print的暑促内容
			out.append('<pre class = "plaintext">{}</pre>'.format(''.join(o['text']))) 
		if  'data' not in o.keys():
			continue
		keys_1 = o['data'].keys()  # 实际输出的key
		keys_2 = out_format.keys() # 需要的输出key
		keys = set(keys_1) & set(keys_2) # 求交集

		# 当存在表格或图片时，默认不输出纯文本内容
		if ('image/png' in keys or 'text/html' in keys) and 'text/plain' in keys:
			keys.remove('text/plain')

		# 遍历输出内容并转换为html
		for k in keys:
			out_format[k](o['data'][k])
	
	return '\n'.join(out) # 返回html代码

# 生成CSS代码
def css_generate(config):
	# 页面CSS
	page_style = 'body {-webkit-print-color-adjust: exact;' + 'width: {};'.format(config['page_with']) + '}\n'

	# 代码CSS
	code_style = '.highlight {'+'font-size:{fs}; padding-left: 10px; margin: 10px;border: {bw} solid #000;border-radius: {br};'.format(
					fs = config['code_font_size'], 
					bw = config['code_borer_with'], 
					br = config['code_borer_radius']) +'}\n'\
			   + 'pre {'+'font-family: {ff}; margin:5px; display:block;line-height: {lh};'.format(
			   		ff = config['code_font-family'],
			   		lh = config['code_line-height'])+'}\n'

	# 纯文本CSS
	output_style = '.plaintext {'+'font-size:{fs}; font-family:{ff}; padding-left:20px;color:{fc};'.format(
					fs = config['output_font_size'],
					ff = config['output_font_family'],
					fc = config['output_color'])+'}\n'

	# 表格CSS
	table_style ='table {'+'margin-left:10px; border:{}; border-collapse:collapse;'.format(config['table_border'])+'}\n' \
				+ 'table tr {'+'background-color:{bc}; font-size:{fs}; color: {fc}; font-family:{ff};'.format(
					bc = config['table_background_color_odd'],
					fs = config['table_font_size'],
					fc = config['table_color'],
					ff = config['table_font_family'])+'}\n'\
				+ 'table tr:nth-child(even) {'+'background-color:{};'.format(config['table_background_color_even'])+'}\n' \
				+ 'table tr th {'+'font-weight:bold;padding:5px 15px 5px 15px; border:{};'.format(config['table_border'])+'}\n'\
				+ 'table tr td {'+'padding:5px 15px 5px 15px;text-align: right; border:{};'.format(config['table_border'])+'}\n' \
				+ '.tebleContainer {' \
				+ ('width:fit-content; margin:auto;' if  config['table_align'] == 'center' else '') \
				+ '}\n'

	# 图片CSS
	img_style = '.image {'+ ('margin-left:20px;text-align:{};'.format(config['img_align']) if config['img_align'] != 'center' else 'text-align:center') +'}\n'

	# markdown CSS
	markdown_style =  '.markdown{'+ 'font-family:\"{}\"'.format(config['markdown_font_family']) + '}\n'

	css = HtmlFormatter(style = config['code_base_style']).get_style_defs('.highlight') + '\n' \
		+ page_style \
		+ code_style \
		+ table_style \
		+ output_style \
		+ img_style \
		+ markdown_style
	return css

def main(file, target, config):
	source = ''
	with open(file, 'rb') as f:
		source = f.read()
	
	HTML = ''
	# 获取并遍历单元格
	cells = json.loads(source)['cells'] # 
	for c in cells:
		# 代码单元格
		if c['cell_type'] == 'code':
			# 获取python源代码
			code = ''.join(c['source'])
			code = '<div>{}</div>'.format(highlight(code, PythonLexer(), HtmlFormatter()))
			HTML += code
			
			# 获取输出内容
			output = c['outputs'] 
			HTML += decode_output(output)

		# markdown单元格
		elif c['cell_type'] == 'markdown':
			md = ''.join(c['source'])
			md = markdown(md) # 将markdown转化为html
			HTML += '<div class = "markdown">{}<div>'.format(md) 

	# html文件模板
	html_template = '''
					<!DOCTYPE html>
					<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
					<head><style type="text/css">{}</style></head>
					<body style="margin: 0px auto;">{}</body>'''
	
	
	CSS = css_generate(config) # 获取CSS
	# 保存文件(默认保存在桌面)
	target = os.path.join(os.path.expanduser("~"), 'Desktop') + '/{}.html'.format(target)
	with open(target, 'w', encoding='utf-8') as f:
		f.write(html_template.format(CSS, HTML))

if __name__ == '__main__':
	main(file = "F:/JupyterNotebooks/客户聚类分析.ipynb", 	# 源文件
		 target= 'test', 				# 生成的html文件名（不带后缀，默认保存在桌面）
		 config = style_config) 				 # 配置
