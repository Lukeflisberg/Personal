# Program allowing for an extensive time table management system
#
# The program will consist of multiple panels: 
# 1st: The timetable panel
# 2nd: The info editor/creator panel
# 3rd: The statistics panel(graph e.g. pie chart)
# 
# The timetable will have 2 axis, the x axis is T representing Time period; the y axis is G representing Group
# The user will have the ability to add and remove groups
# 
# Most importantly, the user is able to create and move around time blocks what will be very extensive:
# 1: You will be able to assign the blocks unique headers; colors
# 2: The blocks size will be determined by the duration
# 3: You will be able to add 'checks', these will consist of:
# 3.1: The block must be after or before a certain time period
# 3.2: The block must be after or before a certain other block
# e.g. I want to slot a timeblock called "create summary" that will be blue for group 1, but this timeblock can only occure after timeblock "perform research" from group 2 has elapsed
#
# Example of the format of the data:
# "Time Period Start", "Group", "Duration", "Header", "Description", "Color", "Before T Period", "After T Period", "Before Event", "After Event"
# This format is subject to change
#
# Most importantly, the user will be able to export and import this data in the form of a .csv file








# Evnetualy:
# Possible auto color code hte blocks by selecting a category