---
license: apache-2.0
configs:  # Optional. This can be used to pass additional parameters to the dataset loader, such as `data_files`, `data_dir`, and any builder-specific parameters  
- config_name: default  # Name of the dataset subset, if applicable. Example: default
  data_files:
  - split: train  # Example: train
    path: psycology_data.json
---