#!/bin/bash
# Run using ./run.sh [name of test file]

REPOSITORY_PATH=/home/clarence/teamx-codejam

java -jar $REPOSITORY_PATH/SPEC/msExchange.jar -p 3000 -t 3001 -d $1
python $REPOSITORY_PATH/CODE/client/web.py &
python $REPOSITORY_PATH/CODE/client/sock.py &
python $REPOSITORY_PATH/CODE/client/newblue.py &
