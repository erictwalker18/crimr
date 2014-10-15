
'''
    CRIMR
    
    webapp.py (phase_3)
    
    Charlie Imhoff,
    Graham Earley,
    Eric Walker
'''

class CrimrHTMLBuilder:
	'''
		CrimrHTMLBuilder allows a quick, easy way to get reusable, flexible
		blocks of HTML via a cleaner interface than directly printing in Phython
		main methods.
		
		Allows us to have the wonders of both a code interface and a template file,
		without the downsides of managing a bunch of flat .HTML files
	'''
	
	def getStartingSequence():
		'''
			Returns the sequence that Python must first print before
			the print stream is read as HTML
		'''
		return '''Content-type: text/html\r\n\r\n''',
	
	def getTopOfHTML(title):
		''' 
			Returns an HTML string which starts the HTML tag 
			and fills in all the header info,
			setting param title as the title
		'''
		
		template = '''<!DOCTYPE HTML> <html> <head>[[TITLE]]</head>'''
		html = template.replace('[[TITLE]]',title)
		return html
		
	def getTopOfBody(subpageHeader):
		'''
			Returns an HTML string which starts the Body tag
			and fills in the first two headers (first one is CRIMR,
			second one is from parameter)
		'''
		
		template = '''<body>
		<h1>CRIMR</h1>
		<h2>[[SUBPAGE_HEADER]]</h2>
		'''
		html = template.replace('[[SUBPAGE_HEADER]]',subpageHeader)
		return html
	
	def getClosingHTML():
		'''
			Returns an HTML string which closes the Body & HTML tags
		'''
		
		return '''</body></html>'''
	
