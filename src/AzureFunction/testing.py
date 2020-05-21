# do all utente la lista ordinata dal piu grande al piu piccolo della visita del min(score)
# EX "v1": [10, 20, 2, 30] ---> "v1": [4, 2, 1, 3] (stanze)

current_visit = {'room1': 2, 'room4': 20}

last_visits = {"v1": {
                    'room1': 10, 
                    'room2': 20,
                    'room3': 2, 
                    'room4': 30
                    }, 
                "v2": {
                    'room1': 0, 
                    'room2': 5,
                    'room3': 23, 
                    'room4': 1
                    }
}

score = {}

for visit_id, visit in last_visits.items():
    score[visit_id] = 0
    for room, minutes in current_visit.items():
        score[visit_id] += abs(current_visit[room] - visit[room])

min_score = min(score.keys(), key=score.get)

best_visit = last_visits[min_score]

suggested_visit = {}

for room, minutes in best_visit.items():
    try:
        current_visit[room]
    except:
        suggested_visit[room] = minutes

suggestions = sorted(suggested_visit.keys(), key=suggested_visit.get, reverse=True)

print(suggestions)