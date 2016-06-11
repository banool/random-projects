import os

mountLocation = "/Users/daniel/Desktop/tempMount"
username = "daniel"
password = "stratakis5991"
remoteServerName = "SERVER"
remoteDirName = "Music"

print("Mounting %s/%s via smb to %s" % (remoteServerName, remoteDirName, mountLocation))

if not os.path.exists(mountLocation):
    print("hey")
    os.makedirs(mountLocation)
mountCommand = "mount_smbfs //%s:%s@%s/%s %s" % (username, password, remoteServerName, remoteDirName, mountLocation)

print(mountCommand)
os.system(mountCommand)
