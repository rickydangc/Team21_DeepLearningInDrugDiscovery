# Team21_DeepLearningInDrugDiscovery
This repository basically reproduce the result of Learning Multimodal Graph-to-Graph Translation for Molecular Optimization (ICLR 2019)

Original Repository: https://github.com/wengong-jin/iclr19-graph2graph

The current method utilizes basic dot-product attention, and we tried the scaled dot-product because the scaling factor would promote more efficient learning since dot-product grows large when input is large, thus leading vanishing gradients in the softmax function which normalizes the attention score.

## Quick Start

A quick summary of different folders:
* `data/` contains the training, validation and test set of logP, QED and DRD2 tasks described in the paper.
* `data_processing_pyspark/` contains the implementation of pyspark to process raw data ([README](./data_processing_pyspark)).
* `fast_jtnn/` contains the implementation of junction tree encoder-decoder.
* `diff_vae/` includes the training and decoding script of variational junction tree encoder-decoder ([README](./diff_vae)).
* `diff_vae_gan/` includes the training and decoding script of adversarial training module ([README](./diff_vae_gan)).
* `props/` is the property evaluation module, including penalized logP, QED and DRD2 property calculation.
* `scripts/` provides evaluation and data preprocessing scripts.

## Team Member
Muyang Sun, Chong Dang, Fangxiang Wang, Jingliang Zhang














