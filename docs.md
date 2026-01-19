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





