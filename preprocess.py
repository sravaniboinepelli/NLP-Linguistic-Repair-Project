ip = open("test_replace.txt", "r")
op = open("test_replaced.txt", "w")
diction = {"very very": "V", "w i": "W"}

if ip.mode == 'r': 
    contents =ip.read()
    contents = contents.rstrip()
    for f_key, f_value in diction.items():
        if f_key in contents:
            contents = contents.replace(f_key, f_value)
    op.write(contents)

op.close()
ip.close()