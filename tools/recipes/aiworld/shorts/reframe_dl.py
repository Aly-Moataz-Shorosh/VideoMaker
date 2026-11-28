"""python dl.py <job_id>=<url> ... : download finished reframes into out/<clip name> (names from jobs.json), record in urls.json"""
import json, os, sys, subprocess
J = {v: k for k, v in json.load(open('jobs.json')).items()}
U = json.load(open('urls.json')) if os.path.exists('urls.json') else {}
for a in sys.argv[1:]:
    j, u = a.split('=', 1); n = J[j]; U[n] = u
    if not os.path.exists('out/' + n): subprocess.run(['curl', '-s', '-o', 'out/' + n, u], check=True)
json.dump(U, open('urls.json', 'w'), indent=1)
print(len(U), 'of 28 downloaded')
