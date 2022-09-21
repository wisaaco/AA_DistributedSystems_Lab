# Configuring a NTP server and client
----
## Activity for Distributed System subject 
## Unity 3. Logical Clocks 
----


### Step 1. VM preparation with multipass

Launch two VM and open them in inddepent terminals
```bash
multipass launch --name master --cpus 8 --mem 10G --disk 12G
multipass launch --name worker1 --cpus 4 --mem 6G --disk 10G

multipass shell master
multipass shell worker1

```

In the host terminal:
```bash
% multipass list
Name                    State             IPv4             Image
master                  Running           192.168.64.8     Ubuntu 20.04 LTS
                                          10.1.219.64
worker1                 Running           192.168.64.9     Ubuntu 20.04 LTS
                                          10.1.235.128

```


## Step 2. In the Master VM

Run and understand the next commands:
```bash
sudo apt install chrony

cat /etc/chrony/chrony.conf

ip a

sudo vi /etc/chrony/chrony.conf

  allow  192.168.64.0/24
  local stratum 10 


sudo service chrony restart

sudo service chrony status

chronyc sources -v

chronyc sourcestats -v

sudo apt install firewalld
sudo firewall-cmd --permanent --add-service=ntp
sudo firewall-cmd --reload

```

## Step 3. In the Worker1 VM

We include our NTP server as the only NTP server in our machine.

Run and understand the next commands:
```bash
sudo apt install chrony

sudo vi /etc/chrony/chrony.conf

    #pool ntp.ubuntu.com        iburst maxsources 4
    #pool 0.ubuntu.pool.ntp.org iburst maxsources 1
    #pool 1.ubuntu.pool.ntp.org iburst maxsources 1
    #pool 2.ubuntu.pool.ntp.org iburst maxsources 2
    pool 192.168.64.8 iburst maxsources 4

sudo service chrony restart

chronyc activity

chronyc sources -v

chronyc sourcestats -v
```


## Step 4. In the Master VM
Lets disconnect  all NTP servers from our NTP server.
We will change the timezone and the date. In the next step, our second VM will update with those values.

Run and understand the next commands:
```bash
sudo vi /etc/chrony/chrony.conf

    #pool ntp.ubuntu.com        iburst maxsources 4
    #pool 0.ubuntu.pool.ntp.org iburst maxsources 1
    #pool 1.ubuntu.pool.ntp.org iburst maxsources 1
    #pool 2.ubuntu.pool.ntp.org iburst maxsources 2

    manual
    allow 192.168.64.0/24
    local stratum 10 

sudo service chrony restart

cat /etc/localtime

timedatectl list-timezones | grep -i tokyo

sudo unlink /etc/localtime
sudo ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

cat /etc/localtime

sudo date --set="1980-10-12 10:05:59.990"

date
```

## Step 5. In the Master VM
We will call  our NTP server to update the date.

```bash
sudo chronyd -q 'server 192.168.64.8 iburst'
```

```bash
ubuntu@worker1:~$ sudo chronyd -q 'server 192.168.64.8 iburst'
2022-06-07T09:04:07Z chronyd version 3.5 starting (+CMDMON +NTP +REFCLOCK +RTC +PRIVDROP +SCFILTER +SIGND +ASYNCDNS +SECHASH +IPV6 -DEBUG)
2022-06-07T09:04:07Z Initial frequency 2.880 ppm
2022-06-07T09:04:12Z System clock wrong by -1314431506.654610 seconds (step)
1980-10-12T01:12:25Z chronyd exiting
````



## Step 6. Clean the VM
```bash
multipass stop -all
multipass delete --all
multipass purge
```

Restart the date server
```
# fix the zoneinfo 
sudo ln -s /usr/share/zoneinfo/Europe/Madrid /etc/localtime

chronyd -q 'server 0.europe.pool.ntp.org iburst'
```
