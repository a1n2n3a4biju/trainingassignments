with open('wildlife_report.txt') as file:
    text=file.read()
print(text)

words=text.split()
print("Total words:" , len(words))

if "elephant" in text.lower():
    print("It was mentioned")

print(text.lower().count("elephant"))


for line in text.splitlines():
    if "trail" in line.lower():
        print(line)
for line in text.splitlines():
    if "elephant" in line.lower():
        print(line)