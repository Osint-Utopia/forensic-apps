---
dataset_info:
  features:
  - name: instruction
    dtype: string
  - name: input
    dtype: string
  - name: output
    dtype: string
  splits:
  - name: train
    num_bytes: 36241
    num_examples: 104
  download_size: 20085
  dataset_size: 36241
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
