import os
import datetime
import json
import time

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
    return config.get('hours_per_week', 38)

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

def add_hours_to_day(day, hours, do_add=True):
    current_hours = get_hours(day)
    new_hours = current_hours + hours if do_add else current_hours - hours
    set_hours(day, new_hours)
    print(f"Adjusted {day}'s hours by {hours:.2f}h to {new_hours:.2f}h.")

def add_hours_to_today(hours, do_add=True):
    add_hours_to_day(get_today_day(), hours, do_add)

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
    return get_hours_remaining_this_week() / (len(get_ramaining_workdays_of_current_week()))

def get_hours_worked_today():
    return get_hours(get_today_day())

def get_hours_remaining_today():
    return get_average_hours_to_work_per_day() - get_hours_worked_today()

# commands

def start_work():
    start_time = datetime.datetime.now()
    try:
        interval_no = 0
        while True:
            interval_no += 1
            # clear terminal
            os.system('clear')
            current_time = datetime.datetime.now()
            hours = (current_time - start_time).total_seconds() / 3600
            today_summary()
            print(f"\rSession: {hours:.2f}h", end="")

            if interval_no % 60 == 0:
                # update the day file every 60 seconds
                hours_worked_so_far = get_hours_worked_today()
                set_hours(get_today_day(), hours_worked_so_far + 1/60)
            time.sleep(1)
    except KeyboardInterrupt:  # stop the timer when Ctrl+C is pressed
        pass
    finally:
        end_time = datetime.datetime.now()
        hours = (end_time - start_time).total_seconds() / 3600
        print(f"\nWorked {hours:.2f}h in this session.")

def adjust_today(hours):
    if hours.startswith('+'):
        add_hours_to_today(float(hours[1:]))
    elif hours.startswith('-'):
        add_hours_to_today(float(hours[1:]), do_add=False)
    else:
        add_hours_to_today(float(hours))

def adjust_day(day, hours):
    if hours.startswith('+'):
        add_hours_to_day(day, float(hours[1:]))
    elif hours.startswith('-'):
        add_hours_to_day(day, float(hours[1:]), do_add=False)
    else:
        add_hours_to_day(day, float(hours))

def today_summary():
    # PRETTY PRINT!
    print(f"=== Summary: Today ===")
    print(f"Today: {get_hours_worked_today():.2f}h")
    print(f"Remaining: {get_hours_remaining_today():.2f}h ({get_average_hours_to_work_per_day():.2f}h/day)")

def week_summary():
    print(f"=== Summary: Week ===")
    print(f"Worked: {get_hours_worked_this_week():.2f}h")
    print(f"Remaining: {get_hours_remaining_this_week():.2f}h ({get_average_hours_to_work_per_day():.2f}h/day, {len(get_ramaining_workdays_of_current_week())} days left)")

def week_overview():
    print(f"=== Overview: Week ===")
    for day in get_workdays_of_current_week():
        print(f"{day.strftime('%A')}: {get_hours(day.strftime('%Y-%m-%d')):.2f}h ({get_hours(day.strftime('%Y-%m-%d')) - get_average_hours_per_day():+.2f}h)")

def is_valid_adjustment(hours):
    return hours.startswith('+') or hours.startswith('-') or hours.isdigit()

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
        today = get_today_day()
        input_day = input(f"Which day do you want to adjust? [default: {today}] ")
        if input_day == '':
            input_day = today

        input_hours = input("How many hours do you want to add/subtract? ")
        if is_valid_adjustment(input_hours):
            adjust_today(input_hours)
        else:
            print(f"Invalid argument: {input_hours}")
    else:
        print(f"Invalid argument: {argument}")

if __name__ == "__main__":
    main()
