d = open("d.txt", "r", encoding="utf8")
q = open("q.txt", "w")

s = d.read()
for i in s.replace(" ", "").split(","):
    q.write(i + "\n")
q.close()
d.close()


import json
ar = s.replace(" ", "").split(",")
with open('cenz.json', 'w', encoding = "utf-8") as e:
    json.dump(ar,e)
    
