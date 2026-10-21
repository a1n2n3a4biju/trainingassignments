with open("unstructured_data.txt") as f:
    text=f.read()
# print(text)
# words=text.split()
# print(len(words))
# lines=text.splitlines()
# print(len(lines))
# if "maintenance" in text.lower():
#     print("Yes its mentioned")
# print(text.lower().count("conveyor"))

# for line in text.splitlines():
#     if "team" in line.lower():
#         print(line)


# for line in text.splitlines():
#     if "incident" in line.lower():
#         print(line)

# for line in text.splitlines():
#     if "damaged" in line.lower():
#         print(line)

# txt=text.lower()
# with open("lowercase_report.txt","w") as f:
#     f.write(txt)

keywords=["maintenance","injuries","inspection","replacement","operations"]
for keyword in keywords:
    if keyword in text:
        print(keyword,":Found")
    else:
        print(keyword,":Not Found")



