print("Solución del programa")

a =[1,9,5,0,20,-4,12,16,7,20,-8,32,10,3,6,8,14,-1,-2,-10]
b=12

parejas=[]

for i in range(len(a)):
    for j in range(len(a)):
        if i!=j:
            if a [i] +a[j] == b:
                pareja = sorted ([a[i] ,a[j]]) 
                if pareja not in parejas:
                    parejas.append(pareja)
print (parejas)