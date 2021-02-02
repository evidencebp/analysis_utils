"""

    Utilites to convert time and size to a readable representation

"""

def convert_minutes_to_text(minutes):
    DAYS_IN_YEAR = 365
    DAYS_IN_WEEK = 7
    MINUTES_IN_HOUR = 60
    MINUTES_PER_DAY = 24*MINUTES_IN_HOUR

    # import pdb; pdb.set_trace()
    cur_minutes = minutes

    years = cur_minutes//(DAYS_IN_YEAR*MINUTES_PER_DAY)
    cur_minutes = cur_minutes - (years*DAYS_IN_YEAR*MINUTES_PER_DAY)

    weeks = cur_minutes//(DAYS_IN_WEEK*MINUTES_PER_DAY)
    cur_minutes = cur_minutes - (weeks*DAYS_IN_WEEK*MINUTES_PER_DAY)

    days = cur_minutes//(MINUTES_PER_DAY)
    cur_minutes = cur_minutes - (days*MINUTES_PER_DAY)

    hours = cur_minutes//(MINUTES_IN_HOUR)
    minutes = cur_minutes - (hours*MINUTES_IN_HOUR)


    time_parts = []
    if years > 1:
        time_parts.append(" {years} years".format(years=years))
    if years == 1:
        time_parts.append(" {years} year".format(years=years))

    if weeks > 1:
        time_parts.append(" {weeks} weeks".format(weeks=weeks))
    if weeks == 1:
        time_parts.append(" {weeks} week".format(weeks=weeks))

    if days > 1:
        time_parts.append(" {days} days".format(days=days))
    if days == 1:
        time_parts.append(" {days} day".format(days=days))

    if hours > 1:
        time_parts.append(" {hours} hours".format(hours=hours))
    if hours == 1:
        time_parts.append(" {hours} hour".format(hours=hours))

    if minutes > 1:
        time_parts.append(" {minutes} minutes".format(minutes=minutes))
    if minutes == 1:
        time_parts.append(" {minutes} minute".format(minutes=minutes))

    return ",".join(time_parts)

def convert_char_to_size(chars):
    KILO = 1024
    if chars >= KILO*KILO:
        res = "{:.1f} MB".format(chars/KILO/KILO)
    elif chars >= KILO:
        res = "{:.1f} KB".format(chars/KILO)
    else:
        res = str(chars) + " b"

    return res

