---
dataset_info:
  features:
  - name: conversations
    list:
    - name: from
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: train
    num_bytes: 39012345.30742474
    num_examples: 83946
  - name: validation
    num_bytes: 9753318.692575263
    num_examples: 20987
  download_size: 24407884
  dataset_size: 48765664.0
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: validation
    path: data/validation-*
---
