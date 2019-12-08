#!/bin/bash

# logp06
echo "logp06 task:"
spark-submit --name "bd4h_logp06" --master yarn --deploy-mode client --conf spark.yarn.maxAppAttempts=1 --py-files dependencies.zip preprocessing_azure.py --trainpkl wasbs:///jing/data/logp06/train_pairs.txt
# logp04
echo "logp04 task:"
spark-submit --name "bd4h_logp04" --master yarn --deploy-mode client --conf spark.yarn.maxAppAttempts=1 --py-files dependencies.zip preprocessing_azure.py --trainpkl wasbs:///jing/data/logp04/train_pairs.txt
# QED
echo "QED task:"
spark-submit --name "bd4h_QED" --master yarn --deploy-mode client --conf spark.yarn.maxAppAttempts=1 --py-files dependencies.zip preprocessing_azure.py --trainpkl wasbs:///jing/data/qed/train_pairs.txt
# DRD2
echo "DRD2 task:"
spark-submit --name "bd4h_DRD2" --master yarn --deploy-mode client --conf spark.yarn.maxAppAttempts=1 --py-files dependencies.zip preprocessing_azure.py --trainpkl wasbs:///jing/data/drd2/train_pairs.txt