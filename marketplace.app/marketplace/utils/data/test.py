file = open('producer-description.txt', 'r')
description = file.read()
file.close()
print(len(description))