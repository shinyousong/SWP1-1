from cgi import parse_qs
from template import html

def application(environ, start_response):
	d=parse_qs(environ['QUERY_STRING'])
	num1=d.get('num1',[''])[0]
	num2=d.get('num2',[''])[0]
	sum=0
	mul=0
	flag="the error has not occured"
	try:
		if '' not in [num1, num2]:
			num1=int(num1)
			num2=int(num2)
			sum=num1+num2
			mul=num1*num2
		elif num1=='' and num2=='':
			sum=-1
			mul=-1
		else:
			raise Error
	except:
		flag="the error has occured"
		sum=-1
		mul=-1
	response_body=html % {'sum': sum, 'mul':mul, 'flag':flag}
	start_response('200 OK',
	[('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))])
	return [response_body]


