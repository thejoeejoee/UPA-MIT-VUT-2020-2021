from sys import stderr

from mongoengine import connect

conn = connect('upa', host='mongo')

print('It works!', conn, file=stderr)