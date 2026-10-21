with open("airport_report_operations.txt") as f:
    text=f.read()

# words=text.split()
# print(len(words))
# lines=text.splitlines()
# print(len(lines))

# print(len(text))
# print(text.lower().count("flight"))
# print(text.lower().count("runway"))
# print(text.lower().count("operations"))
# print(text.lower().count("reported"))

# for line in text.splitlines():
#     if "runway" in line.lower():
#         print(line)

# for line in text.splitlines():
#     if "delay" or "" in line.lower():
#         print(line)
#
# for line in text.splitlines():
#     if "delay" in line.lower() or "delayed" in line.lower() or "delays" in line.lower():
#         print(line.strip())

# for line in text.splitlines():
#     if "reported" in line.lower():
#         print(line.strip())

# words=text.split()
# if "emergency" in words:
#     print("Yes emergency appears")
# if "inspection" in words:
#     print("Yes inspection appears")
# if "weather" in words:
#     print("Yes weather appears")
# if "passengers" in words:
#     print("Yes passengers appears")
# if "maintenance" in words:
#     print("Yes maintenance appears")

# airport={
#     "flight": text.count("flight"),
#     "runway":text.count("runway"),
#     "operations":text.count("operations")
# }
# print(airport)

# longest_line=max(text.splitlines(),key=len)
# print(longest_line)

for line in text.splitlines():
    if "delays" in text.lower() or "weather" in text.lower():
        filtered_text=line.strip()
        print(filtered_text)

with open("filtered_airports.txt","w") as f:
    f.write(filtered_text)
print("success")








