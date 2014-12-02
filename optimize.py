import json


def split_to_entries(calendar, split):
    """
    Turns the split JSON into a list of entries (as in entries.json).
    WARNING: The object will be modified, assigned hours will be substracted.
    :param calendar: Hours available each date. As in dt.json.
    :param split: List of items, as in split.json.
    :type split: dict
    :return:
    """
    entries = []


    # Iterator over each item in the items list.
    items_iterator = iter(split["items"])
    item = next(items_iterator, None)
    if item is None:
        return

    total_hours_assigned = 0

    for date, dayhours in calendar.iteritems():

        # Somewhat messy to have this check in two places.
        if item is None:
            print "[DONE WITH ALL ITEMS. STOPPING.]"
            break

        while dayhours > 0:
            remaining_hours_in_item = item["hours"]
            hours_to_assign = min(dayhours, remaining_hours_in_item)

            # Remove the hours from the item.
            item["hours"] -= hours_to_assign

            # Remove the hours from the day
            dayhours -= hours_to_assign

            # Create the new entry
            new_entry = {
                "project": item["project"],
                "unit": item["unit"],
                "concept": item["concept"],
                "date": date,
                "hours": hours_to_assign
            }

            entries.append(new_entry)

            total_hours_assigned += hours_to_assign

            print "[%s] Assigned %d hours (%s: %s)" % (new_entry["date"], new_entry["hours"], new_entry["concept"], new_entry["project"])

            # If we are done with the current item (ex: Y-PROJECT), go to the next one.
            if item["hours"] == 0:
                item = next(items_iterator, None)
                if item == None:
                    break

    print "ASSIGNED TOTAL HOURS: %d" % total_hours_assigned


if __name__ == "__main__":
    calendar = json.loads(open("dt.json").read())
    split = json.loads(open("split.json").read())

    print split_to_entries(calendar, split)

