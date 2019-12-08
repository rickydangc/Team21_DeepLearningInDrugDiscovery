from pyspark import SparkConf, SparkContext
import os
import cPickle as pickle
import argparse
from subprocess import PIPE, Popen

from fast_jtnn import *

train_path = ""
# spark_master = "local[*]"

def tensorize(smiles, assm=False):
    mol_tree = MolTree(smiles)
    mol_tree.recover()
    if assm:
        mol_tree.assemble()
        for node in mol_tree.nodes:
            if node.label not in node.cands:
                node.cands.append(node.label)

    del mol_tree.mol
    for node in mol_tree.nodes:
        del node.mol
        del node.clique

    return mol_tree


def tensorize_pair(line):
    smiles_pair = line.strip().split()
    mol_tree0 = tensorize(smiles_pair[0], assm=False)
    mol_tree1 = tensorize(smiles_pair[1], assm=True)
    return (mol_tree0, mol_tree1)


def debug():
    args= type('', (), {})()
    args.train = train_path
    args.mode = "pair"
    return args


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', type=str, default='')
    parser.add_argument('--pkl', type=str, default='') # "wasbs:///jing/resultbd4h/logp06"
    # parser.add_argument('--mode', type=str, default='pair')
    parser.add_argument('--trainpkl', type=str, default='')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    conf = SparkConf()#.setAppName('bd4h') # .setMaster(spark_master)
    sc = SparkContext(conf=conf)

    args = argument_parser()

    """
    TODO - by default, only 60000 out of 75xxx data pair is used. Can use more (if not more because batch size may need 
    to be fixed) and expect better performance. For example, the batch size is 20. So we can use data up to any integer
    multiple of 20.
    """
    size_split = 10000
    if args.train:
        print "Starting to generate MolTree and save RDD to hdfs..."
        data = sc.textFile(args.train)
        print "Total pairs: {}".format(data.count())
        all_data = data.map(tensorize_pair).map(lambda x: pickle.dumps(x, pickle.HIGHEST_PROTOCOL)).map(lambda x: x.encode('string-escape')) # .collect()
        print "After pickle, total is {}".format(all_data.count())
        print all_data.take(1)
        parent_folder, _ = os.path.split(args.train)
        out_path = "wasbs:///jing/resultbd4h/{}/".format(os.path.split(parent_folder)[-1])
        all_data.saveAsTextFile(out_path)
        print "Success."
    elif args.pkl:
        src = args.pkl # "wasbs:///jing/resultbd4h/logp06"
        data = sc.textFile(src).collect()
        output = []
        for obj in data:
            c = obj.encode().decode('string_escape')
            output.append(pickle.loads(c))
        _, datafile = os.path.split(src)
        pkl_file = 'tensors-{}.pkl'.format(datafile)
        with open(pkl_file, 'wb') as f:
            pickle.dump(output, f, pickle.HIGHEST_PROTOCOL)
        print "Pickle dump is successfully saved to {}".format(os.path.join(os.getcwd(), pkl_file))
        hdfs_file = "/jing/{}".format(pkl_file)
        put = Popen(
            ["hdfs", "dfs", "-copyFromLocal", pkl_file, hdfs_file], stdin = PIPE, bufsize = -1)
        put.communicate()
        print "Pickle obj ({}) is successfully saved to hdfs ({})".format(pkl_file, hdfs_file)
    elif args.trainpkl:
        _, datafile = os.path.split(args.trainpkl)
        print "{}::Starting to generate MolTree and save pickle obj to hdfs...".format(datafile)
        data = sc.textFile(args.trainpkl)
        print "Total pairs: {}".format(data.count())
        all_data = data.map(tensorize_pair).map(lambda x: pickle.dumps(x, pickle.HIGHEST_PROTOCOL)).map(
            lambda x: x.encode('string-escape')).collect()
        output = []
        for obj in all_data:
            c = obj.decode('string_escape')
            output.append(pickle.loads(c))
        _, datafile = os.path.split(args.trainpkl)
        pkl_file = 'tensors-{}.pkl'.format(datafile)
        with open(pkl_file, 'wb') as f:
            pickle.dump(output, f, pickle.HIGHEST_PROTOCOL)
        print
        "Pickle dump is successfully saved to {}".format(os.path.join(os.getcwd(), pkl_file))
        hdfs_file = "/jing/{}".format(pkl_file)
        put = Popen(
            ["hdfs", "dfs", "-copyFromLocal", pkl_file, hdfs_file], stdin=PIPE, bufsize=-1)
        put.communicate()
        print
        "Pickle obj ({}) is successfully saved to hdfs ({})".format(pkl_file, hdfs_file)
    else:
        print "Nothing is run. Check command line arguments."
