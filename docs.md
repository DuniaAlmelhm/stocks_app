## Ansible 
I am following the official documentation of ansible

### Installation
Ansible will result in this error on Windows 
#### AttributeError: module 'os' has no attribute 'get_blocking'
According to this issue on Stack Overflow https://stackoverflow.com/questions/74701206/install-ansible-windows-machine, installing ansible on Windows with WSL is not supported. 
Thus, I am installing it on Ubuntu-22.04. 
```commandline
pip install ansible 
ansible --version 
```



### Start
```commandline
mkdir ansible
cd ansible
touch inventory.ini
ansible-inventory -i inventory.ini --list
touch playbook.yaml
```
In the inventory.ini file, I added my Hetzner server IPv4

### Ping
To verify there is a connection between ansible and my server and there is a python interpreter, I have to ping the host using the command  

```commandline
ansible myhosts -m ping -i inventory.ini
```
ansible: tool I am using to execute the command 

myhosts: list of all IP addresses defined in the file inventory

-m ping: specifically calling module ping. The module communicates with the listed hosts under myhosts. If a successful connection is established, it will return **pong** for the host is reachable

-i inventory.ini: it specifies the file to be used as a source for hosts 

This command resulted in this error 
<img src="images/ping_error.png" >

This command has two issues: 
1. the username needs to be specified since it is different between the managed node (Hetzner server) and the control node (local system), so I added the flag -u
    ```commandline
    ansible myhosts -m ping -i inventory.ini -u root
    ```
2. Permission is denied: I am adding a flag --ask-pass, so I am prompted to enter ssh password 
    ```commandline
    ansible myhosts -m ping -i inventory.ini -u root --ask-pass
    ```
   This resulted in the following error 
    ##### "msg": "to use the 'ssh' connection type with passwords or pkcs11_provider, you must install the sshpass program"
    I ran the following to install sshpass on Ubuntu https://www.firsttiger.com/blogs/install-sshpass-program-on-macos/
    ```commandline
    sudo apt install sshpass
    ```

re-running this command 
```commandline
ansible myhosts -m ping -i inventory.ini -u root --ask-pass
```
and passing the ssh password, resulted in **SUCCESS and the path to python interpreter as well as PONG** In other words, the inventory has been successfully created 

P.S. inventory is a list of hosts to be managed by ansible 

### Setup SSH
Running the ansible playbook requires the two tags -u and --ask-pass 
```commandline
ansible-playbook -i inventory.ini playbook.yaml -u root --ask-pass
```
To avoid specifying these two tags everytime, 
I added **remote_user: root** in the playbook which will eliminates the use of flag -u

To avoid --ask-pass, I tried the following
1. according to their documentation https://docs.ansible.com/projects/ansible/latest/inventory_guide/connection_details.html, I started the agent and then added my private rsa key to the agent
```commandline
ssh-agent bash
ssh-add ~/.ssh/id_ed25519
```
However, I got this warning
<img src="images/rsa_warning.png" >
To fix this warning, I needed to change the permission of my private key so that only the owner (me) can write and read the file (no other users can do any action). I ran the following commands:
```commandline
chmod 600 ~/.ssh/id_ed25519
ssh-add ~/.ssh/id_ed25519
ansible-playbook -i inventory.ini playbook.yaml
```
I got this error now
<img src="images/unreachable_server_error.png" >
Which means I need to copy my public key to the server according to this https://www.ssh.com/academy/ssh/copy-id, so I can avoid accessing the server with a password 
```commandline
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@46.62.220.105
```
This command basically connect to the server through the IPv4 address and copies the public rsa key to it. It prompts me to enter the password for the server, so it can finish adding the rsa key. To check if the key is actually added, I connected to the server which prompted me to enter the passphrase to my rsa key. I then moved to the directory in which I have the file containing the rsa public key
```commandline
ssh root@46.62.220.105
ls -all
cd .ssh
ls
cat authorized_keys
```
Now I can finally run the playbook without the need to enter the authentication everytime
```commandline
ansible-playbook -i inventory.ini playbook.yaml
```


## clean up 
https://alexhernandez.info/articles/infrastructure/how-to-install-docker-using-ansible/

https://community.hetzner.com/tutorials/howto-docker-install

installing these libraries is important since apt doesn't communicate with https protocol (it only makes request to http protocol)

GPG is like rsa key 



