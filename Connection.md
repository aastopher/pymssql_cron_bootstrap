# How to change the connection configuration and encrypt the new configuration.

* Navigate to the project directory and copy the `conn_template.cfg` file and rename your copy to `conn.cfg`
* change all the variables in the template to your new configuration **NOTE: do not add any spaces or end of line characters**
* Open the `enc.py` script file and edit the **input_file** to equal `'./CFG/conn.cfg'`
* Then change **ouput_file** to equal `'./CFG/en_conn.cfg'` **WARNING: this will override the original config and the new key MUST copied from terminal and changed in the `key.txt` file.**
* Please navigate to the project directory in WSL terminal. Then run the following line
* `sudo python3 CFG/enc.py`
* copy the key from the terminal window **NOTE: do not close the terminal window or you will have to run again for a new key**
* From the `CFG` folder open `key.txt` change this to you new key and save **NOTE: do not add any spaces or end of line characters**
* Remove your `conn.cfg` file or save it in a different secure location for reference. **WARNING: DO NOT upload your `conn.cfg` file as it contains sensitive information!**
* Congratulations your new configuration is active!
