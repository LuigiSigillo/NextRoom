v3 = [2, 0, 0, 0]
visits = {"v1": [10, 20, 2, 30], "v2": [0, 5, 23, 1]}
lst = []
score = [0,0,0,0] #indice 0 = visita 0

for i in range(len(v3)):
    if v3[i] != 0:
       lst.append(i)


for visit in visits:
    score[int(visit[1])] = 0
    for r in lst:
        score[int(visit[1])] += abs(v3[r] - visits[visit][r])

print("score ", score)

""" def on_new_message(msgs):
    for msg in msgs:
        for dev in msg['list_devices']:
 """

print("il minimo è ", min(score))

# do all utente la lista ordinata dal piu grande al piu piccolo della visita del min(score)
# EX "v1": [10, 20, 2, 30] ---> "v1": [4, 2, 1, 3] (stanze)

