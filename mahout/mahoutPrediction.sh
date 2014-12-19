#!/bin/bash
#
# Downloads the dataset from Yahoo Finance, trains and tests a classifier.
#
# Deal with cvx file as following before running
# Select predictors and target values:
# predictors： open, highest, lowest and close prices
# target values: create the target values by Excel using a simple formula:
# =IF(E2>=B3, ‘Lower’, ‘Higher’)
# where E2 is current day’s close and B3 is next day’s open.
#
# To run:  change into the mahout directory and type:
# bin/mahoutPrediction.sh



if [ "$1" = "--help" ] || [ "$1" = "--?" ]; then
  echo "This script runs SGD classifier and tests the model you built over the stock data."
  exit
fi

SCRIPT_PATH=${0%/*}
if [ "$0" != "$SCRIPT_PATH" ] && [ "$SCRIPT_PATH" != "" ]; then
  cd $SCRIPT_PATH
fi
START_PATH=`pwd`

if [ "$HADOOP_HOME" != "" ] && [ "$MAHOUT_LOCAL" !== "" ] ; then
  HADOOP="$HADOOP_HOME/bin/hadoop"
  if [ ! -e $HADOOP ]; then
    echo "Can't find hadoop in $HADOOP, exiting"
    exit 1
  fi
fi

WORK_DIR=/tmp/mahout-work-${USER}
algorithm=( sgd clean)
if [ -n "$1" ]; then
  choice=$1
else
  echo "Please select a number to choose the corresponding task to run"
  echo "1. ${algorithm[0]}"
  echo "2. ${algorithm[1]} -- cleans up the work area in $Workdir"
  read -p "Enter your choice : " choice
fi

echo "ok. You chose $choice and we'll use ${algorithm[$choice-1]}"
alg=${algorithm[$choice-1]}

#echo $START_PATH
cd $START_PATH
cd ../..

set -e

if [ "x$alg" == "xsgd" ]; then

  echo "Split the preprocessed dataset and create a 90% percent of training set and a 10% percent of testing set"
  ./bin/mahout splitDataset \
    -i ${Workdir}/table.csv \
    -o ${Workdir}/table_train \
    --trainingPercentage 0.9 \
    --probePercentage 0.1

  echo "Convert dataset of training set to sequence file"
  ./bin/mahout seqdirectory \
    -i ${Workdir}/table_train/trainingSet \
    -o ${Workdir}/sequence/train \
    -c UTF-8 \
    -chunk 64 \
    -xm sequential

  echo "Convert sequence file of training set to csv file"
  ./bin/mahout seqdumper \
    -i ${Workdir}/sequence/train \
    -o ${Workdir}/table_train.csv

  echo "Convert dataset of test set to sequence file"
  ./bin/mahout seqdirectory \
  -i ${Workdir}/table_train/probeSet \
  -o ${Workdir}/sequence/test \
  -c UTF-8 \
  -chunk 64 \
  -xm sequential

  echo "Convert sequence file of test set to csv file"
  ./bin/mahout seqdumper \
  -i ${Workdir}/sequence/test \
  -o ${Workdir}/table_test.csv

# User has to revise table_train.csv and table_test.csv mannually before running the following commands.

  echo "Train the model"
  ./bin/mahout org.apache.mahout.classifier.sgd.TrainLogistic \
  --passes 100 \
  --rate 1 \
  --lambda 0.0001 \
  -i ${Workdir}/table_train.csv \
  --features 21 \
  -o ${Workdir}/stock.model \
  --target nextday_price_dir \
  --categories 2 \
  --predictors Open High Low Close \
  --types n n

  echo "Test the model"
  ./bin/mahout org.apache.mahout.classifier.sgd.RunLogistic \
  -i ${Workdir}/table_test.csv \
  --model /tmp/stock.model \
  --auc \
  --scores \
  --confusion

elif [ "x$alg" == "xclean" ]; then
  rm -rf ${Workdir}
  rm -rf /tmp/stock.model
fi
# Remove the work directory
#
