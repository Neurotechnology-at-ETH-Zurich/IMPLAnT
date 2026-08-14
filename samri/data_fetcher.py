import sys
import os
import glob
from scp import SCPClient
import paramiko


#Data fetcher from Bruker Host PC
#Collects the bruker scan files given the subject id

def main(server, password, local_path, animal_id,local_fodler):
    # server = ""
    port = 22
    # password = ""
    user = "mri"
    # animal_id = ""
    client = createSSHClient(server, port, user, password)
    print(client)
    files=find_data(client, animal_id)
    if not files:
        client.close()
        raise FileNotFoundError(f"No data found on the server for Animal ID '{animal_id}'")
    scp = scpClient(client)
    # local_path = "./fetcher_test/"
    #Set below the directory where the scan data is originally stored
    remote_path = "/opt/PV6.0.1/data/mri/"
    local_files=get_local_data_list(animal_id,local_fodler)
    get_data(client, files, local_path, remote_path,local_files)

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def find_data(client, animal_id):
    stdin, stdout, stderr = client.exec_command("ls -l /opt/PV6.0.1/data/mri/ | grep " + animal_id)
                                                # "| grep /opt/PV6.0.1/data/mri/" + animal_id)
    print(stdout)
    files = []
    for line in stdout:
        files.append(line.split(" ")[-1].split("\n")[0])
    print(files)
    return files

def scpClient(client):
    scp = SCPClient(client.get_transport(), progress=progress)
    return scp

def get_data(client, files, local_path, remote_path, local_files):
    scp = SCPClient(client.get_transport(),  progress=progress)
    for file in files:
        if file not in local_files:
            print("Fetching " + file)
            scp.get(remote_path + file, local_path=local_path, recursive=True)
            print("complete")
        else:
            # Session exists locally — check for scan subdirs missing on disk
            stdin, stdout, stderr = client.exec_command(
                "ls " + remote_path + file + "/ | grep -E '^[0-9]+$'"
            )
            remote_scans = [l.strip() for l in stdout if l.strip()]
            local_session_path = os.path.join(local_path, file)
            local_scans = [d for d in os.listdir(local_session_path) if d.isdigit()]
            missing = [s for s in remote_scans if s not in local_scans]
            if missing:
                print(f"Session {file} already exists — fetching {len(missing)} missing scan(s): {missing}")
                for scan in missing:
                    scp.get(remote_path + file + "/" + scan,
                            local_path=local_session_path, recursive=True)
                print("complete")
    scp.close()

def get_local_data_list(animal_id,local_fodler):
    file_list=glob.glob(local_fodler + animal_id +"/*") #"./samri_bindata/"
    files = []
    for file in file_list:
        files.append(file.split("/")[-1])

    return(files)



def progress(filename, size, sent):
    sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

if __name__ == '__main__':
    main()

