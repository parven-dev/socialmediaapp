
import random

otp = "".join([str(random.randint(0, 9)) for _ in range(6)])

email = ["user@gmail.com"]
sender_mail = email[0]
print(sender_mail)
