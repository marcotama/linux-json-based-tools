import re

print(re.match(r'([a-zA-Z0-9-_]+)', 'is-directory'))
print(re.match(r'(==|>=|>|<=|<|!=|=~)', '=='))
print(re.match(r'\d+(?:(?:[KMGTPE])?i?)|\d+\.\d+(?:(?:[KMGTPE])?i?)|\d+\.\d+e\d+|"[^"]+"|True|False', '1'))
