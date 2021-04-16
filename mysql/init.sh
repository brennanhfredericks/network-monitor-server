#!/bin/bash

DB_PACKETS="packets"

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


function privileges_type {
    # arg 1 - priviliage type
    # arg 2 - database name
    # arg 3 - username
    # arg 4 - host

    echo "GRANT $1 ON $2.* TO '$3'@'$4';"
}

# function to grant low privileges access to database, arguments database name, user, host
function grant_low_privileges_on_database {
    # arg 1 - database name
    # arg 2 - username
    # arg 3 - host
    
    local op_create=$(privileges_type "CREATE" $1 $2 $3)
    local op_delete=$(privileges_type "DELETE" $1 $2 $3)
    local op_insert=$(privileges_type "INSERT" $1 $2 $3)
    local op_select=$(privileges_type "SELECT" $1 $2 $3)
    local op_update=$(privileges_type "UPDATE" $1 $2 $3)
    
    echo {$op_create,$op_delete,$op_insert,$op_select,$op_update,$COMMIT}
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
    done
}

echo $(execute "SHOW DATABASES")

#create packets table
create_database $DB_PACKETS

echo $(execute "SHOW DATABASES")

echo $(execute "SELECT User FROM mysql.user")

#init database users
init_from_secrets

# check users
echo $(execute "SELECT User FROM mysql.user")


