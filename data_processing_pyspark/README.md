# Pyspark Environment Setup

This is the Pyspark version of original [SMILE-to-Molecule preprocessing code](https://github.com/wengong-jin/iclr19-graph2graph/blob/master/scripts/preprocess.py).

## Spark Cluster Setup
* The Spark cluster is set up with Azure HDInsight service with 2 head nodes and 2 worker nodes. Each node is a “D12v2” instance with 4-core CPU and 28-GB RAM. 
* [Script action](azure/azure_spark_cluster_script_action.sh) is provided to install dependencies (e.g. Numpy, Pytorch etc) on all head and worker nodes. 
* [dependencies.zip](azure/dependencies.zip) contains custom python package (`fast_jtnn`) which will be sent from head node to all worker nodes.
* Azure blob storage is set up to save script action shell script, dependencies zipfile and results (RDD and pickle object)

## Quick Start
The main function is in [preprocessing_azure.py](azure/preprocessing_azure.py). Three command line options are available: 
1) “--train”: Path for train data. Generate molecule trees and save molecule tree RDD to HDFS (Azure Storage Blobs); 
2) “--pkl”: Path for molecule tree RDD in Azure blob storage. Collect molecule tree RDD from HDFS, convert to pickle object and save pickle object to HDFS; 
3) “--trainpkl”: Path for train data. Combines 1) and 2) operations into one.

For example, below command generates molecule trees, save molecule trees to pickle object and save pickle object to HDFS (Azure blob storage)  
```spark-submit --name "bd4h_logp06" --master yarn --deploy-mode client --conf spark.yarn.maxAppAttempts=1 --py-files dependencies.zip preprocessing_azure.py --trainpkl wasbs:///jing/data/logp06/train_pairs.txt```

Alternatively, [preprocessing_pyspark.sh](azure/preprocessing_pyspark.sh) can be used to preprocess SMILE strings for all four tasks (make sure to change output path):
* logp06
* logp04
* QED
* DRD2