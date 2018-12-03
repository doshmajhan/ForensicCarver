#!/usr/bin/env python

import os
import subprocess

# first find where USB is mounted
# use the following line for Kristen's USB 
output = subprocess.check_output(['mount| grep KRISTEN'], shell=True)
# use the following line for other USBs 
#output = subprocess.check_output(['lsblk | grep media'], shell=True)
output = output.decode('utf-8')
mount = output[:output.find('on')] 
print('USB is mounted at ' + mount)

# then run dd command
cmd = 'sudo dd if=' + mount.rstrip() + ' of=/home/sansforensics/Desktop/kristen.dd'
print('Running dd command: ' + cmd)
exit_code = os.system(cmd)
if exit_code==0:
	print('dd command complete')
else:
	print('dd command failed')

print('Generating and comparing hashes...')
# MD5 first
output_md5 = subprocess.check_output(['md5sum kristen.dd'], shell=True)
output_md5 = output_md5.decode('utf-8')
output_md5 = output_md5.split(' ') 
print('MD5 Hash of kristen.dd: ' + output_md5[0])
cmd = 'sudo md5sum ' + mount
mount_md5 = subprocess.check_output([cmd], shell=True)
mount_md5 = mount_md5.decode('utf-8')
mount_md5 = mount_md5.split(' ')
print('MD5 Hash of mounted USB: ' + mount_md5[0])
if output_md5[0] == mount_md5[0]:
	print('MD5 hashes match!')
else:
	print('MD5 hashes do not match.')


# then SHA1
output_sha1 = subprocess.check_output(['sha1sum kristen.dd'], shell=True)
output_sha1 = output_sha1.decode('utf-8')
output_sha1 = output_sha1.split(' ')
print('SHA1 Hash of kristen.dd: ' + output_sha1[0])
cmd = 'sudo sha1sum ' + mount
mount_sha1 = subprocess.check_output([cmd], shell=True)
mount_sha1 = mount_sha1.decode('utf-8')
mount_sha1 = mount_sha1.split(' ')
print('SHA1 Hash of mounted USB: ' + mount_sha1[0])
if output_sha1[0] == mount_sha1[0]:
        print('SHA1 hashes match!')
else:
        print('SHA1 hashes do not match.')

