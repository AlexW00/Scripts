import os
import datetime
import json

# config options (in ~/.config/work_tracker.json)
# time_entries_dir: directory where the time entries are stored
# off_days: list of days that are not work days (e.g. ['Saturday', 'Sunday'])
# hours_per_week: number of hours you want to work per week

CONFIG_FILE = os.path.expanduser("~/.config/work_tracker.json")
STANDARD_OFF_DAYS = ['Saturday', 'Sunday']

# config

def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as file:
            return json.load(file)
    else:
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def get_off_days():
    config = get_config()
    return config.get('off_days', STANDARD_OFF_DAYS)

def get_work_days():
    config = get_config()
    off_days = get_off_days()
    return [day for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] if day not in off_days]

def get_hours_per_week():
    config = get_config()
    return config.get('hours_per_week', 40)

def get_average_hours_per_day():
    return get_hours_per_week() / len(get_work_days())

# hours

def get_hours(day):
    config = get_config()
    time_entries_dir = config.get('time_entries_dir', '~/work_time_entries')
    time_entries_dir = os.path.expanduser(time_entries_dir)

    if not os.path.exists(time_entries_dir):
        os.makedirs(time_entries_dir)

    day_file = os.path.join(time_entries_dir, day)

    if not os.path.exists(day_file):
        return 0

    with open(day_file, 'r') as file:
        return float(file.readline().strip())

def set_hours(day, hours):
    config = get_config()
    time_entries_dir = config.get('time_entries_dir', '~/work_time_entries')
    time_entries_dir = os.path.expanduser(time_entries_dir)

    if not os.path.exists(time_entries_dir):
        os.makedirs(time_entries_dir)

    day_file = os.path.join(time_entries_dir, day)

    with open(day_file, 'w') as file:
        file.write(str(hours))

def add_hours_to_today(hours, do_add=True):
    today = get_today_day()
    current_hours = get_hours(today)
    new_hours = current_hours + hours if do_add else current_hours - hours
    set_hours(today, new_hours)

    

# date

def get_today_day():
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")

def get_day(day, month, year):
    return datetime.date(year, month, day).strftime("%Y-%m-%d")

def get_workdays_of_current_week():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    return [monday + datetime.timedelta(days=i) for i in range(5)]

def get_ramaining_workdays_of_current_week():
    return [day for day in get_workdays_of_current_week() if day >= datetime.date.today()]

# calculations

def get_hours_worked_this_week():
    return sum([get_hours(day.strftime("%Y-%m-%d")) for day in get_workdays_of_current_week()])

def get_hours_remaining_this_week():
    return get_hours_per_week() - get_hours_worked_this_week()

def get_average_hours_to_work_per_day():
    return get_hours_remaining_this_week() / len(get_ramaining_workdays_of_current_week())

def get_hours_worked_today():
    return get_hours(get_today_day())

def get_hours_remaining_today():
    return get_average_hours_per_day() - get_hours_worked_today()

# commands

def start_work():
    start_time = datetime.datetime.now()
    try:
        input("Press enter to stop the timer.")
    except KeyboardInterrupt:
        pass
    end_time = datetime.datetime.now()

    hours = (end_time - start_time).total_seconds() / 3600
    print(f"You worked for {hours:.2f} hours.")
    add_hours_to_today(hours)

def adjust_today(hours):
    if len(hours) < 2:
        print("Invalid adjustment, must be of the form +2 or -1.")
        return

    if hours[0] == '+':
        add_hours_to_today(float(hours[1:]))
    elif hours[0] == '-':
        add_hours_to_today(float(hours[1:]), do_add=False)
    else:
        print("Invalid adjustment, must be of the form +2 or -1.")

def today_summary():
    # PRETTY PRINT!
    print(f"=== Summary: Today ===")
    print(f"Today: {get_hours_worked_today():.2f}h")
    print(f"Remaining: {get_hours_remaining_today():.2f}h")

def week_summary():
    print(f"=== Summary: Week ===")
    print(f"Worked: {get_hours_worked_this_week():.2f}h")
    print(f"Remaining: {get_hours_remaining_this_week():.2f}h ({get_average_hours_to_work_per_day():.2f}h/day, {len(get_ramaining_workdays_of_current_week())} days left)")

def week_overview():
    print(f"=== Overview: Week ===")
    for day in get_workdays_of_current_week():
        print(f"{day.strftime('%A')}: {get_hours(day.strftime('%Y-%m-%d')):.2f}h ({get_hours(day.strftime('%Y-%m-%d')) - get_average_hours_per_day():+.2f}h)")

def main():
    argument = os.sys.argv[1] if len(os.sys.argv) > 1 else None
    if argument is None or argument == 'start':
        start_work()
    elif argument == 'today':
        today_summary()
    elif argument == 'week':
        week_overview()
        print()
        week_summary()
    elif argument == 'overview':
        week_overview()
        print()
        week_summary()
        print()
        today_summary()
    elif argument == 'adjust':
        adjust_today(os.sys.argv[2])
    else:
        print(f"Invalid argument: {argument}")

if __name__ == "__main__":
    main()
