import paramiko
import pandas as pd
import time

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
    try:
      ssh.connect(router_ip, 
                  username=router_username, 
                  password=router_password,
                  look_for_keys=True )
      remote_conn = ssh.invoke_shell()
    except Exeption as e:
      print(e)

    
    print(ssh)
    # Run command.
    
    print("enable")
    #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("enable")
    
    #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("admin")
    #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("show running-config")
    output = remote_conn.recv(65535)
    print(output)
    remote_conn.send("enable\n")
    time.sleep(.5)
    output = remote_conn.recv(65535)
    print(output)
    remote_conn.send("admin\n")
    time.sleep(.5)
    output = str(remote_conn.recv(65535), "utf-8")
    print(output)
    hostname = output.split('#')[0].replace("\r", "").replace("\n", "")
    remote_conn.send("terminal lengt 0\n")
    time.sleep(.5)
    output = str(remote_conn.recv(65535), "utf-8")
    print(output)
    remote_conn.send("show running-config\n")
    time.sleep(2)
    output = str(remote_conn.recv(65535), "utf-8")
    print(output)
    # Close connection.
    ssh.close()
    f = open("./Conf/" + hostname + ".txt", "w")
    f.write(output)
    f.close()

