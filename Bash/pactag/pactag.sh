#!/bin/sh

sync_flag=''
sync_val=''

remove_flag=''
remove_val=''

tag_flag=''
tag_val=''

print_usage() {
  printf "Usage: ..."
}

while getopts S:R:T: flag
do
    case "${flag}" in
        S)  sync_flag=1
            sync_val="$OPTARG";;
        R)  remove_flag=1 
            remove_val="$OPTARG";;
        T)  tag_flag=1
            tag_val="$OPTARG";;
        *)  print_usage
            exit 1 ;;
    esac
done

if [ -n "$sync_flag" ]; then
    ./pactag_sync.sh "$sync_val" "$tag_val"
fi

if [ -n "$remove_flag" ]; then
    ./pactag_remove.sh "$remove_val" "$tag_val"
fi