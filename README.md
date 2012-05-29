python27-on-openshift
=====================

Use python 2.7.3 on http://openshift.redhat.com.

It will get a complied package of python 2.7.3 form dropbox, it includes easy_install and pip in this package.
There is a sample site with tornado in this repository.

Create your own gear
=========================
1.Create an account at http://openshift.redhat.com/ , and install the client tools.

2.Create a diy-0.1 application :

    rhc app create -a py27 -t diy-0.1 -l email

3.Add this upstream py27 repo

    cd py27
    git remote add upstream -m master git://github.com/bjjay/python27-on-openshift.git
    git pull -s recursive -X theirs upstream master
    
4.Then push the repo upstream

    git push

5.That's it, you can now checkout your application at:

    http://py27-$yournamespace.rhcloud.com


NOTES:
=====

Generate ssh public key for existed openshift account:

        #create keys
        $ ssh-keygen -t rsa -f ~/.ssh/libra_id_rsa -C email  
        #add public key
        $ rhc sshkey add -i public_key_name -k ~/.ssh/libra_id_rsa.pub  -l email
        #edit your ssh config   
        $ cat ~/.ssh/config
        Host *.rhcloud.com
          IdentityFile ~/.ssh/libra_id_rsa
          VerifyHostKeyDNS yes
          StrictHostKeyChecking no
          UserKnownHostsFile ~/.ssh/libra_known_hosts
