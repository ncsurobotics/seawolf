import hub

conn = hub.connect('NewClient')

print(conn.set_var('hello', 'there'))

print(conn.get_var('hello'))
print(conn.get_vars())
