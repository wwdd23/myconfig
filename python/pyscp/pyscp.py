#!/usr/bin/env python

import MySQLdb
import os
import pexpect

def conn_to_mysql():
       """Make a Connection to the mysql server"""
       db_host = 'localhost'
       db_user = 'root'
       db_pass = 'william'
       db_name = 'backup'
       conn = MySQLdb.connect(host=db_host,user=db_user,passwd=db_pass,db=db_name)
       return conn

def check_path(path):
    """Check if a path exist,and create if it`s not"""
    if not os.patch.exists(patch):
        mkdir_cmd = "mkdir -p" +patch
        pexpect.run(mkdir_cmd)


def do_rotate(file,rotate):
    """Rotate files for $rotate times"""
    list = []
    for i in range(int(rotate)):
        list.insert(0,i)

    for i in list:
        if i == 0:
            src = backup_path + file
        else:
            src = backup_path + file + "." + str(i)
     
     dst = backup_path + file + "." + str(i+1)

     if os.path.exist(src):
         move_cmd = "mv" + src + " " +dst
         pexpect.run(move_cmd)
def get_new(instance_id, compute_node, file):
    """Get the new backup $file from $host"""
    src = "william@" + compute_node + ":/var/lib/openstack/" + instance_id + "/" + file
    dst = "/ver/lib/openstack-backup/" + instance_id + "/"
    copy_cmd = "scp" + src + " " + dst 
    
    ssh_newkey = "Are you sure you want to continue connecting"
    p = pexpect.spawn(copy_cmd)
    i = p.expect([ssh_newkey,'password:',pexpect.EOF])
    if i == 0:
        print "i say yes"
        p.sendline('yes')
        i = p.expect([ssh_newkey,'password:',pexpect.EOF])
    if i == 1:
        # print "i give password"
        p.sendline("william")
        p.expect(pexpect.EOF)
    elif i == 2:
        print "I either got key or connection timesout"
        pass
    #print p.before
   
def do_backup(instance_id, compute_node, rotate, files):
    for file in files:
        do_rotate(file, rotate)
        get_new(instance_id, complete_node, file)
if __name__ == "__main__"
    db=conn_to_mysql()
    cursor = db.cursor()
    cursor.execute('select * from schedule')

    for result in cursors.fetchal():
        instance_id = result[0]
        count = int(result[5])
        interval = int(result[2])
        compute_node = result[1]
        rotate = result[3]
        files = result[4].split(",")

        backup_path ="/vars/lib/openstack-backup/" + instance_id +"/"
        check_path(backup_path)

        if count == 0:
            do_backup(instance_id, compute_node, rotate, files)
            count += 1
        elif count == interval:
            count = 0

        else:
            count += 1

    #Update database
    update_cmd ="update backup.schedule set count=" + str(count) + "where instance_id=" + str(instance_id) + ""
    cursor.execute(update_cmd)
  
  db.close()
                        
