from pydantic import BaseModel, ValidationError, Field,EmailStr,field_validator

from typing import Literal
import logging
import json



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

class Registration(BaseModel):
    registration_id: str
    name: str
    email: EmailStr
    age: int = Field(gt=18)
    ticket_type:Literal["Standard", "Premium", "VIP"]
    amount: float=Field(gt=0)


with open("registrations.json") as file:
    data=json.load(file)




# for record in data:
#         try:
#             registration = Registration(**record)
#             logging.info("Registration  created successfully")
#
#         except ValidationError as e:
#             logging.error("Validation error")

# for record in data:
#         try:
#             registration = Registration(**record)
#             print(registration)
#         except ValidationError as e:
#             pass

# for record in data:
#     try:
#         registration = Registration(**record)
#     except ValidationError as e:
#         reg_id=record.get("registration_id","unknown")
#         for problem in e.errors():
#             field=".".join(str(p) for p in problem["loc"])
#             print(f"Field: {field}")
#             print(f"Message: {problem["msg"]}")


# for record in data:
#     try:
#         registration = Registration(**record)
#
#         registration_dict = registration.model_dump()
#         print(registration_dict)
#
#
#     except ValidationError as error:
#         pass



# for record in data:
#     try:
#         registration = Registration(**record)
#
#         registration_dict = registration.model_dump_json(indent=4)
#         print(registration_dict)
#
#
#     except ValidationError as error:
#         pass

validation_data=[]
# for record in data:
#     try:
#         registration = Registration(**record)
#
#         registration_dict = registration.model_dump(mode="json")
#         validation_data.append(registration_dict)
#
#
#     except ValidationError as error:
#         pass
#
#
with open("valid_registrations.json", "w") as file:
    json.dump(validation_data, file, indent=4)
print("Updated")


# for record in data:
#     if record["ticket_type"] == "VIP":
#         logging.warning(f"VIP ticket {record['registration_id']}")


# filename="registrations.log"
# print("File created successfully")

# try:
#     with open("registrations.json", "r") as file:
#         records = json.load(file)
#
# except FileNotFoundError:
#     logging.error("registrations.json was not found")
#
# except json.JSONDecodeError:
#     logging.error("registrations.json contains invalid JSON")

total_records=len(data)
invalid_records=0

for record in data:
    try:
        registration = Registration(**record)

        registration_dict = registration.model_dump(mode="json")
        validation_data.append(registration_dict)


    except ValidationError as error:
        invalid_records+=1


print("Total records:", total_records)
print("Valid records:", len("valid_registrations"))
print("Invalid records:", invalid_records)







