

from actions import Action

print "Running HoursFillerCmd"


act = Action()

act.login()

d = dict(project="GO-LAB", unit="Unidad Internet", concept="I+D Desarrollo Proyecto", date="1/1/2014", hours="1")
act.add_entry(**d)
act.add_entry(**d)
act.add_entry(**d)