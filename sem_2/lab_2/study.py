l1 = [2,4,3]
l2 = [5,6,4]
l3 = [] 
l4 = [] 
l5 = []
for l in range(0,len(l1)):
    l3.insert(0,l1[l])
    l += 1

for l in range(0,len(l2)):
    l4.insert(0,l2[l])
    l += 1

res1 = int(''.join(map(str, l3))) 

res2 = int(''.join(map(str, l4))) 

col = res1 + res2

while col > 0:
    l5.append(col%10)
    col//=10

#l5.reverse()
print(l5)