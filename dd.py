#!/usr/bin/env python

import os
import subprocess

# first find where USB is mounted
output = subprocess.check_output(['mount | grep KRISTEN'], shell=True)
#output = subprocess.check_output(['lsblk | grep media'], shell=True)
output = output.decode('utf-8')
mount = output[:output.find('on')] 
print('USB is mounted at ' + mount)

# then run dd command
cmd = 'dd if=' + mount.rstrip() + ' of=/home/sansforensics/Desktop/kristen.dd'
print('Running dd command: ' + cmd)
exit_code = os.system(cmd)
if exit_code==0:
	print('dd command complete')
else:
	print('dd command failed')
