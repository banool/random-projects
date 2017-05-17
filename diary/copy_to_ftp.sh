#!/usr/bin/env bash

# Generating html from all the .md files
./generate_html.sh $1

# You need lftp for this

HOST="members.iinet.net.au"
USER=$FTPUSER
PASS=$FTPPASS
FTPURL="ftp://$USER:$PASS@$HOST"
LCD="generated_html"
RCD="entries"
DELETE="--delete"  # Comment this out to not delete files that
                   # aren't present locally from the remote directory.
lftp -c "set ftp:list-options -a;
open '$FTPURL';
lcd $LCD;
cd $RCD;
mirror --reverse \
       $DELETE \
       --verbose \
       --exclude-glob a-dir-to-exclude/ \
       --exclude-glob a-file-to-exclude \
       --exclude-glob a-file-group-to-exclude* \
       --exclude-glob other-files-to-exclude"

LCD="images"
RCD="images"

lftp -c "set ftp:list-options -a;
open '$FTPURL';
lcd $LCD;
cd $RCD;
mirror --reverse \
       $DELETE \
       --verbose \
       --exclude-glob a-dir-to-exclude/ \
       --exclude-glob a-file-to-exclude \
       --exclude-glob a-file-group-to-exclude* \
       --exclude-glob other-files-to-exclude"
