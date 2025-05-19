# a2.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Katherine Wei
# yininw17@uci.edu
# 14645993

join_msg = '{"authenticate": {"username": "mike_zimmermann","password": "password123"}}'

send = client.makefile('w')
recv = client.makefile('r')

send.write(join_msg + '\r\n')
send.flush()

resp = recv.readline()
print(resp)
# >>> b{"response": {"type": "ok", "message": "Welcome back, ohhimark", "token": "07da3ddc-6b9a-4734-b3ca-f0aa7ff22360"}}
