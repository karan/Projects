maxi = 0
answ = 0
perc = 0
visited = [False] * 1000000
for b in range(len(visited)):
    if not visited[b]:
        times = 0
        a = b
        if float(b)/len(visited) > perc * .05:
            perc += 1
	    print "Completed: ["+(perc*"=")+((20-perc)*" ")+"] "+str(perc*5)+"%"
        while not a <= 1:
            a = a/2 if a % 2 == 0 else 3*a + 1
            times += 1
            if a < len(visited):
                visited[a] = True
#           print a
        if times > maxi:
            answ = b
            maxi = times
print answ
