# Full script.
from actions import Action

if __name__ == "__main__":

    # Load the calendar.
    import json
    import optimize

    calendar = json.loads(open("dt.json").read())
    split = json.loads(open("my.split.json").read())
    entries = optimize.split_to_entries(calendar, split)


    act = Action()
    act.login()
    act.add_entries_safe(entries, "my.progress.json")


