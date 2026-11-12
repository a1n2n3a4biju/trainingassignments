
with open('para.txt') as file:
    text=file.read()
print(text)

words=text.split()
print("Total words:" , len(words))

if "vibration" in text.lower():
    print("It was mentioned")

print(text.lower().count("vibration"))