import os
import pandas as pd

def extract_features_from_pslist(text):
    lines = text.strip().split('\n')
    processes = [line for line in lines if line.strip() and not line.startswith("Offset")]
    process_count = len(processes)
    svchost_count = sum(1 for line in processes if 'svchost.exe' in line.lower())
    return {
        'pslist_total_processes': process_count,
        'pslist_svchost_count': svchost_count
    }

def extract_features_from_dlllist(text):
    dll_count = text.lower().count('.dll')
    suspicious_dlls = sum(1 for line in text.splitlines() if 'temp' in line.lower() or 'appdata' in line.lower())
    return {
        'dlllist_total_dlls': dll_count,
        'dlllist_suspicious_dlls': suspicious_dlls
    }

PLUGIN_PARSERS = {
    'pslist': extract_features_from_pslist,
    'dlllist': extract_features_from_dlllist
}

def extract_features_from_dump(dump_path):
    features = {}
    for file in os.listdir(dump_path):
        plugin = file.split('.')[0]
        if plugin in PLUGIN_PARSERS:
            with open(os.path.join(dump_path, file), 'r', errors='ignore') as f:
                content = f.read()
                plugin_features = PLUGIN_PARSERS[plugin](content)
                features.update(plugin_features)
    return features

def build_dataset(base_path='data'):
    data = []
    for label_dir in ['malware', 'benign']:
        label = 1 if label_dir == 'malware' else 0
        label_path = os.path.join(base_path, label_dir)
        for dump_folder in os.listdir(label_path):
            dump_path = os.path.join(label_path, dump_folder)
            if os.path.isdir(dump_path):
                features = extract_features_from_dump(dump_path)
                features['label'] = label
                features['sample_id'] = f"{label_dir}_{dump_folder}"
                data.append(features)
    df = pd.DataFrame(data).fillna(0)
    return df
