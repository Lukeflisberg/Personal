def add_time(start, duration, day=None):
    # Format day
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    do_days = day
    day_index = list(map(lambda x: x.upper(), days)).index(day.upper()) if day else None

    # Format start time
    s_time = start.replace("AM", "").replace("PM", "").strip()
    s_hours, s_minutes = map(int, s_time.split(":"))
    s_hours += 12 if 'PM' in start and s_hours != 12 else 0

    # Format duration time
    d_hours, d_minutes = map(int, duration.split(":"))

    # Calculate new time
    n_hours = s_hours + d_hours
    n_minutes = s_minutes + d_minutes

    # Account for overflow
    n_hours += n_minutes // 60
    n_minutes = n_minutes % 60

    days_passed = n_hours // 24
    day_index = (day_index + days_passed) % 7 if do_days else None
    n_hours = n_hours % 24

    suffix = "PM" if n_hours >= 12 else "AM"
    
    if n_hours > 12:
        n_hours -= 12
    if n_hours == 0:
        n_hours = 12

    n_hours = n_hours % 12 if n_hours > 12 else n_hours
    n_hours = 12 if n_hours == 12 else n_hours 

    return f"{n_hours}:{'0' if n_minutes < 10 else ''}{n_minutes} {suffix}" + (f", {days[day_index]}" if do_days else '') + (" (next day)" if days_passed == 1 else '') + (f" ({days_passed} days later)" if days_passed > 1 else '')

print(add_time('3:30 PM', '2:12'))