from cryptography.fernet import Fernet

key = Fernet.generate_key()
input_file = './CFG/conn_template.cfg' # change this to your connn.cfg with a specific configuration
ouput_file = './CFG/en_conn_test.cfg' # remove '_test' to create a new official configuration

with open (input_file,'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.encrypt(data)

with open(ouput_file,'wb') as f:
    f.write(encrypted)

print(key)

# Most recent Key: 
