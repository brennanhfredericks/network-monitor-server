#!/bin/bash

COMMIT="FLUSH PRIVILEGES;"

function execute {
    local res=$(mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "$1")
    echo $res
}

# function to create database, arguments databename and commit
function create_database {
    # arg 1 - database name
    # arg 2 - commit
    local op="CREATE DATABASE IF NOT EXISTS $1;"
    execute "$op"
}

# function to create user. argumens user,host,password and commit
function create_user {
    # arg 1 - username
    # arg 2 - hostname
    # arg 3 - password
    # arg 4 - commit
    local op="CREATE USER IF NOT EXISTS '$1'@'$2' IDENTIFIED BY '$3';"
    echo {$op,$COMMIT}
}


# function to grant low privileges access to database, arguments database name, user, host
function grant_low_privileges_on_database {
    # arg 1 - database name
    # arg 2 - username
    # arg 3 - host
    local op="GRANT CREATE,DELETE,INSERT,SELECT,UPDATE,REFERENCES on $1.* TO '$2'@'$3';"
   
    
    echo {$op,$COMMIT}
}

# function to load /run/secrets *-user
function init_from_secrets {
    for f in /run/secrets/*-user 
    do
        while IFS='=' read -ra line 
        do
           local user=${line[0]}
           local host=${line[1]}
           local pass=${line[2]}
        done <<< $(cat $f)

        # execute mysql statement to create user
        execute "$(create_user $user $host $pass)"
        # execute mysql statement to grant appropriate priviliages
        execute "$(grant_low_privileges_on_database $DB_PACKETS $user $host)"
        #remove users configs
        #rm $f, root getting permission denied errors?
    done
}

# show databases
# echo $(execute "SHOW DATABASES")

#create packets table
create_database $DB_PACKETS

#init database users
init_from_secrets

# check users
echo $(execute "SELECT User FROM mysql.user")

# delete script
#rm ./init.sh
#exit 0
