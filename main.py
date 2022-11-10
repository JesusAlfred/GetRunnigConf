import paramiko
import pandas as pd

class Device:
  def __init__(self, ip, user, password):
    self.ip = ip
    self.user = user
    self.password = password

def getDevices():
  df = pd.read_csv('devices.csv')
  df = df.reset_index()
  return df

if __name__ == "__main__":
  devices = []
  for index, d in getDevices().iterrows():
    devices.append(Device(d['ip'], d['user'], d['password']))
  for i in devices:
    print(i.ip, i.user, i.password)
    router_ip = i.ip
    router_username = i.user
    router_password = i.password


    ssh = paramiko.SSHClient()

    # Load SSH host keys.
    ssh.load_system_host_keys()
    # Add SSH host key automatically if needed.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to router using username/password authentication.
    ssh.connect(router_ip, 
                username=router_username, 
                password=router_password,
                look_for_keys=False )

    # Run command.
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("show running config")

    output = ssh_stdout.readlines()

    for line in output:
      if ">" in line:
        hostname = line.split('>')[0]
    # Close connection.
    ssh.close()
    f = open(hostname + ".txt", "w")
    f.write(output)
    f.close()

