import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import cv2
import os
import pickle
import joblib

from .preprocessing import ImagePreprocessor
from .signature_analysis import SignatureAnalyzer


class SignatureFeatureExtractor:
    """
    Classe per estrarre caratteristiche dalle firme da utilizzare nei modelli di machine learning.
    """
    
    def __init__(self):
        """Inizializza l'estrattore di caratteristiche."""
        self.preprocessor = ImagePreprocessor()
        self.analyzer = SignatureAnalyzer()
    
    def extract_features(self, image_path):
        """
        Estrae un vettore di caratteristiche da un'immagine di firma.
        
        Args:
            image_path (str): Percorso dell'immagine della firma
            
        Returns:
            dict: Dizionario di caratteristiche
        """
        # Pre-elabora la firma
        processed = self.preprocessor.preprocess_signature(image_path)
        
        # Estrai metriche grafometriche
        metrics = self.analyzer.extract_signature_metrics(processed['binary'])
        
        # Estrai caratteristiche ORB
        keypoints, descriptors = self.analyzer.extract_features_orb(processed['binary'])
        
        # Se non ci sono descrittori, restituisci un vettore di zeri
        if descriptors is None:
            orb_features = np.zeros(32)
        else:
            # Calcola la media dei descrittori per ottenere un vettore di caratteristiche fisso
            orb_features = np.mean(descriptors, axis=0) if descriptors.shape[0] > 0 else np.zeros(32)
        
        # Calcola caratteristiche aggiuntive dall'immagine binaria
        binary = processed['binary']
        
        # Calcola il numero di componenti connessi (tratti separati)
        num_labels, labels = cv2.connectedComponents(binary)
        
        # Calcola il rapporto tra pixel bianchi e neri
        white_pixels = cv2.countNonZero(binary)
        total_pixels = binary.shape[0] * binary.shape[1]
        black_pixels = total_pixels - white_pixels
        white_black_ratio = white_pixels / black_pixels if black_pixels > 0 else 0
        
        # Calcola la densità dei pixel (percentuale di pixel bianchi)
        density = white_pixels / total_pixels
        
        # Calcola il centro di massa
        y_indices, x_indices = np.where(binary > 0)
        if len(x_indices) > 0 and len(y_indices) > 0:
            center_x = np.mean(x_indices)
            center_y = np.mean(y_indices)
        else:
            center_x = 0
            center_y = 0
        
        # Normalizza il centro di massa rispetto alle dimensioni dell'immagine
        norm_center_x = center_x / binary.shape[1] if binary.shape[1] > 0 else 0
        norm_center_y = center_y / binary.shape[0] if binary.shape[0] > 0 else 0
        
        # Calcola momenti di Hu (invarianti alla rotazione, scala e traslazione)
        moments = cv2.moments(binary)
        hu_moments = cv2.HuMoments(moments).flatten()
        
        # Logaritmo dei momenti di Hu per gestire meglio i valori molto piccoli
        hu_moments = -np.sign(hu_moments) * np.log10(np.abs(hu_moments) + 1e-10)
        
        # Combina tutte le caratteristiche in un dizionario
        features = {
            # Metriche grafometriche
            'area': metrics['area'],
            'perimeter': metrics['perimeter'],
            'width': metrics['width'],
            'height': metrics['height'],
            'aspect_ratio': metrics['aspect_ratio'],
            'density': metrics['density'],
            'slant_angle': metrics['slant_angle'],
            
            # Caratteristiche aggiuntive
            'num_components': num_labels - 1,  # -1 perché lo sfondo è contato come componente
            'white_black_ratio': white_black_ratio,
            'pixel_density': density,
            'center_x_norm': norm_center_x,
            'center_y_norm': norm_center_y,
            
            # Momenti di Hu
            'hu1': hu_moments[0],
            'hu2': hu_moments[1],
            'hu3': hu_moments[2],
            'hu4': hu_moments[3],
            'hu5': hu_moments[4],
            'hu6': hu_moments[5],
            'hu7': hu_moments[6],
        }
        
        # Aggiungi le caratteristiche ORB
        for i, val in enumerate(orb_features):
            features[f'orb_{i}'] = float(val)
        
        return features
    
    def extract_features_batch(self, image_paths):
        """
        Estrae caratteristiche da un batch di immagini di firme.
        
        Args:
            image_paths (list): Lista di percorsi delle immagini
            
        Returns:
            pandas.DataFrame: DataFrame con le caratteristiche estratte
        """
        features_list = []
        
        for path in image_paths:
            try:
                features = self.extract_features(path)
                features['image_path'] = path
                features_list.append(features)
            except Exception as e:
                print(f"Errore nell'estrazione delle caratteristiche da {path}: {e}")
        
        return pd.DataFrame(features_list)


class AnomalyDetector:
    """
    Classe per il rilevamento di anomalie nelle firme utilizzando Isolation Forest.
    """
    
    def __init__(self, contamination=0.1, random_state=42):
        """
        Inizializza il rilevatore di anomalie.
        
        Args:
            contamination (float): Percentuale attesa di outlier nei dati
            random_state (int): Seed per la riproducibilità
        """
        self.model = IsolationForest(contamination=contamination, random_state=random_state)
        self.scaler = StandardScaler()
        self.feature_extractor = SignatureFeatureExtractor()
        self.is_fitted = False
    
    def fit(self, signatures_df=None, signatures_paths=None):
        """
        Addestra il modello di rilevamento anomalie.
        
        Args:
            signatures_df (pandas.DataFrame, optional): DataFrame con le caratteristiche estratte
            signatures_paths (list, optional): Lista di percorsi delle immagini di firme autentiche
            
        Returns:
            self: Istanza addestrata
        """
        if signatures_df is None and signatures_paths is None:
            raise ValueError("È necessario fornire o un DataFrame di caratteristiche o una lista di percorsi di immagini")
        
        if signatures_df is None:
            # Estrai caratteristiche dalle immagini
            signatures_df = self.feature_extractor.extract_features_batch(signatures_paths)
        
        # Rimuovi colonne non numeriche
        features_df = signatures_df.select_dtypes(include=['number'])
        
        # Normalizza le caratteristiche
        X = self.scaler.fit_transform(features_df)
        
        # Addestra il modello
        self.model.fit(X)
        self.is_fitted = True
        
        # Salva le colonne utilizzate
        self.feature_columns = features_df.columns.tolist()
        
        return self
    
    def predict(self, signature_path=None, features=None):
        """
        Predice se una firma è anomala.
        
        Args:
            signature_path (str, optional): Percorso dell'immagine della firma
            features (dict, optional): Caratteristiche già estratte
            
        Returns:
            dict: Risultato della predizione
        """
        if not self.is_fitted:
            raise ValueError("Il modello deve essere addestrato prima di fare predizioni")
        
        if signature_path is None and features is None:
            raise ValueError("È necessario fornire o un percorso di immagine o le caratteristiche estratte")
        
        if features is None:
            # Estrai caratteristiche dall'immagine
            features = self.feature_extractor.extract_features(signature_path)
        
        # Crea un DataFrame con le caratteristiche
        features_df = pd.DataFrame([features])
        
        # Seleziona solo le colonne utilizzate durante l'addestramento
        features_df = features_df[self.feature_columns]
        
        # Normalizza le caratteristiche
        X = self.scaler.transform(features_df)
        
        # Predici l'anomalia
        # -1 per outlier (anomalia), 1 per inlier (normale)
        prediction = self.model.predict(X)[0]
        
        # Calcola il punteggio di anomalia
        # Più negativo è il punteggio, più anomala è la firma
        score = self.model.decision_function(X)[0]
        
        # Converti il punteggio in un valore percentuale
        # 0% = molto anomalo, 100% = normale
        normalized_score = (score + 0.5) / 1.0  # Adatta in base ai tuoi dati
        normalized_score = max(0, min(1, normalized_score)) * 100
        
        return {
            'is_anomaly': prediction == -1,
            'anomaly_score': score,
            'confidence': normalized_score,
            'prediction': 'anomaly' if prediction == -1 else 'normal'
        }
    
    def save_model(self, model_path, scaler_path=None):
        """
        Salva il modello addestrato.
        
        Args:
            model_path (str): Percorso dove salvare il modello
            scaler_path (str, optional): Percorso dove salvare lo scaler
        """
        if not self.is_fitted:
            raise ValueError("Il modello deve essere addestrato prima di essere salvato")
        
        # Salva il modello
        joblib.dump(self.model, model_path)
        
        # Salva lo scaler se specificato
        if scaler_path:
            joblib.dump(self.scaler, scaler_path)
        
        # Salva anche le colonne delle caratteristiche
        metadata = {
            'feature_columns': self.feature_columns
        }
        
        # Salva i metadati
        metadata_path = os.path.splitext(model_path)[0] + '_metadata.pkl'
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
    
    def load_model(self, model_path, scaler_path=None):
        """
        Carica un modello addestrato.
        
        Args:
            model_path (str): Percorso del modello salvato
            scaler_path (str, optional): Percorso dello scaler salvato
        """
        # Carica il modello
        self.model = joblib.load(model_path)
        
        # Carica lo scaler se specificato
        if scaler_path:
            self.scaler = joblib.load(scaler_path)
        
        # Carica i metadati
        metadata_path = os.path.splitext(model_path)[0] + '_metadata.pkl'
        if os.path.exists(metadata_path):
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
            self.feature_columns = metadata['feature_columns']
        
        self.is_fitted = True


class SignatureDataset(Dataset):
    """
    Dataset PyTorch per le immagini di firme.
    """
    
    def __init__(self, image_paths, labels=None, transform=None, target_size=(128, 128)):
        """
        Inizializza il dataset.
        
        Args:
            image_paths (list): Lista di percorsi delle immagini
            labels (list, optional): Lista di etichette (1 per autentico, 0 per falso)
            transform (callable, optional): Trasformazioni da applicare alle immagini
            target_size (tuple): Dimensione target per le immagini
        """
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        self.target_size = target_size
        self.preprocessor = ImagePreprocessor()
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        # Carica l'immagine
        image = self.preprocessor.load_image(self.image_paths[idx])
        
        # Pre-elabora l'immagine
        image = self.preprocessor.convert_to_grayscale(image)
        image = self.preprocessor.normalize_image(image)
        
        # Ridimensiona l'immagine
        image = cv2.resize(image, self.target_size)
        
        # Normalizza i valori dei pixel nell'intervallo [0, 1]
        image = image.astype(np.float32) / 255.0
        
        # Aggiungi una dimensione per il canale (1 canale per immagini in scala di grigi)
        image = np.expand_dims(image, axis=0)
        
        # Converti in tensore PyTorch
        image = torch.from_numpy(image)
        
        # Applica trasformazioni se specificate
        if self.transform:
            image = self.transform(image)
        
        # Restituisci l'immagine e l'etichetta se disponibile
        if self.labels is not None:
            label = self.labels[idx]
            return image, torch.tensor(label, dtype=torch.float32)
        else:
            return image


class SiameseNetwork(nn.Module):
    """
    Rete siamese per la verifica delle firme.
    """
    
    def __init__(self):
        """Inizializza la rete siamese."""
        super(SiameseNetwork, self).__init__()
        
        # CNN per l'estrazione delle caratteristiche
        self.cnn = nn.Sequential(
            # Prima convoluzione
            nn.Conv2d(1, 64, kernel_size=10, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            # Seconda convoluzione
            nn.Conv2d(64, 128, kernel_size=7, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            # Terza convoluzione
            nn.Conv2d(128, 128, kernel_size=4, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            # Quarta convoluzione
            nn.Conv2d(128, 256, kernel_size=4, stride=1),
            nn.ReLU(inplace=True)
        )
        
        # Fully connected per la classificazione
        self.fc = nn.Sequential(
            nn.Linear(256 * 9 * 9, 4096),
            nn.Sigmoid()
        )
        
        # Layer di output
        self.output = nn.Sequential(
            nn.Linear(4096, 1),
            nn.Sigmoid()
        )
    
    def forward_one(self, x):
        """
        Forward pass per una singola immagine.
        
        Args:
            x (torch.Tensor): Immagine di input
            
        Returns:
            torch.Tensor: Embedding dell'immagine
        """
        x = self.cnn(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
    
    def forward(self, input1, input2):
        """
        Forward pass per una coppia di immagini.
        
        Args:
            input1 (torch.Tensor): Prima immagine
            input2 (torch.Tensor): Seconda immagine
            
        Returns:
            torch.Tensor: Probabilità che le firme siano della stessa persona
        """
        # Ottieni gli embedding per entrambe le immagini
        output1 = self.forward_one(input1)
        output2 = self.forward_one(input2)
        
        # Calcola la distanza euclidea
        distance = torch.abs(output1 - output2)
        
        # Calcola la probabilità
        prob = self.output(distance)
        
        return prob


class SignatureVerifier:
    """
    Classe per la verifica delle firme utilizzando una rete siamese.
    """
    
    def __init__(self, model_path=None):
        """
        Inizializza il verificatore di firme.
        
        Args:
            model_path (str, optional): Percorso del modello pre-addestrato
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = SiameseNetwork().to(self.device)
        self.preprocessor = ImagePreprocessor()
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def train(self, genuine_paths, forged_paths, epochs=20, batch_size=32, learning_rate=0.0001):
        """
        Addestra la rete siamese.
        
        Args:
            genuine_paths (list): Lista di percorsi delle firme autentiche
            forged_paths (list): Lista di percorsi delle firme false
            epochs (int): Numero di epoche di addestramento
            batch_size (int): Dimensione del batch
            learning_rate (float): Tasso di apprendimento
            
        Returns:
            dict: Metriche di addestramento
        """
        # Crea coppie di immagini e etichette
        pairs = []
        labels = []
        
        # Coppie genuine (stessa persona)
        for i in range(len(genuine_paths)):
            for j in range(i + 1, len(genuine_paths)):
                pairs.append((genuine_paths[i], genuine_paths[j]))
                labels.append(1)  # 1 = stessa persona
        
        # Coppie false (persone diverse)
        for genuine_path in genuine_paths:
            for forged_path in forged_paths:
                pairs.append((genuine_path, forged_path))
                labels.append(0)  # 0 = persone diverse
        
        # Dividi in training e validation
        train_pairs, val_pairs, train_labels, val_labels = train_test_split(
            pairs, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Crea i dataset
        train_dataset = PairDataset(train_pairs, train_labels)
        val_dataset = PairDataset(val_pairs, val_labels)
        
        # Crea i dataloader
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size)
        
        # Definisci l'ottimizzatore e la funzione di perdita
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        criterion = nn.BCELoss()
        
        # Addestra il modello
        train_losses = []
        val_losses = []
        val_accuracies = []
        
        for epoch in range(epochs):
            # Training
            self.model.train()
            train_loss = 0
            
            for batch_idx, (img1, img2, target) in enumerate(train_loader):
                img1, img2, target = img1.to(self.device), img2.to(self.device), target.to(self.device)
                
                # Forward pass
                output = self.model(img1, img2)
                loss = criterion(output, target.view(-1, 1))
                
                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            train_loss /= len(train_loader)
            train_losses.append(train_loss)
            
            # Validation
            self.model.eval()
            val_loss = 0
            correct = 0
            
            with torch.no_grad():
                for img1, img2, target in val_loader:
                    img1, img2, target = img1.to(self.device), img2.to(self.device), target.to(self.device)
                    
                    # Forward pass
                    output = self.model(img1, img2)
                    val_loss += criterion(output, target.view(-1, 1)).item()
                    
                    # Calcola l'accuratezza
                    pred = (output > 0.5).float()
                    correct += pred.eq(target.view(-1, 1)).sum().item()
            
            val_loss /= len(val_loader)
            val_losses.append(val_loss)
            
            val_accuracy = 100. * correct / len(val_dataset)
            val_accuracies.append(val_accuracy)
            
            print(f'Epoch: {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.2f}%')
        
        return {
            'train_losses': train_losses,
            'val_losses': val_losses,
            'val_accuracies': val_accuracies
        }
    
    def verify(self, image_path1, image_path2):
        """
        Verifica se due firme sono della stessa persona.
        
        Args:
            image_path1 (str): Percorso della prima immagine
            image_path2 (str): Percorso della seconda immagine
            
        Returns:
            dict: Risultato della verifica
        """
        self.model.eval()
        
        # Carica e pre-elabora le immagini
        img1 = self._preprocess_image(image_path1)
        img2 = self._preprocess_image(image_path2)
        
        # Converti in tensori PyTorch
        img1 = torch.from_numpy(img1).unsqueeze(0).to(self.device)
        img2 = torch.from_numpy(img2).unsqueeze(0).to(self.device)
        
        # Forward pass
        with torch.no_grad():
            output = self.model(img1, img2)
        
        # Calcola la probabilità
        probability = output.item()
        
        return {
            'is_same_person': probability > 0.5,
            'probability': probability,
            'confidence': probability * 100 if probability > 0.5 else (1 - probability) * 100
        }
    
    def _preprocess_image(self, image_path, target_size=(128, 128)):
        """
        Pre-elabora un'immagine per la rete siamese.
        
        Args:
            image_path (str): Percorso dell'immagine
            target_size (tuple): Dimensione target
            
        Returns:
            numpy.ndarray: Immagine pre-elaborata
        """
        # Carica l'immagine
        image = self.preprocessor.load_image(image_path)
        
        # Pre-elabora l'immagine
        image = self.preprocessor.convert_to_grayscale(image)
        image = self.preprocessor.normalize_image(image)
        
        # Ridimensiona l'immagine
        image = cv2.resize(image, target_size)
        
        # Normalizza i valori dei pixel nell'intervallo [0, 1]
        image = image.astype(np.float32) / 255.0
        
        # Aggiungi una dimensione per il canale (1 canale per immagini in scala di grigi)
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def save_model(self, model_path):
        """
        Salva il modello addestrato.
        
        Args:
            model_path (str): Percorso dove salvare il modello
        """
        torch.save(self.model.state_dict(), model_path)
    
    def load_model(self, model_path):
        """
        Carica un modello pre-addestrato.
        
        Args:
            model_path (str): Percorso del modello salvato
        """
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()


class PairDataset(Dataset):
    """
    Dataset PyTorch per coppie di immagini di firme.
    """
    
    def __init__(self, pairs, labels, target_size=(128, 128)):
        """
        Inizializza il dataset.
        
        Args:
            pairs (list): Lista di coppie di percorsi di immagini
            labels (list): Lista di etichette (1 per stessa persona, 0 per persone diverse)
            target_size (tuple): Dimensione target per le immagini
        """
        self.pairs = pairs
        self.labels = labels
        self.target_size = target_size
        self.preprocessor = ImagePreprocessor()
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, idx):
        # Carica la prima immagine
        img1_path, img2_path = self.pairs[idx]
        
        # Pre-elabora le immagini
        img1 = self._preprocess_image(img1_path)
        img2 = self._preprocess_image(img2_path)
        
        # Converti in tensori PyTorch
        img1 = torch.from_numpy(img1)
        img2 = torch.from_numpy(img2)
        
        # Restituisci le immagini e l'etichetta
        return img1, img2, self.labels[idx]
    
    def _preprocess_image(self, image_path):
        """
        Pre-elabora un'immagine.
        
        Args:
            image_path (str): Percorso dell'immagine
            
        Returns:
            numpy.ndarray: Immagine pre-elaborata
        """
        # Carica l'immagine
        image = self.preprocessor.load_image(image_path)
        
        # Pre-elabora l'immagine
        image = self.preprocessor.convert_to_grayscale(image)
        image = self.preprocessor.normalize_image(image)
        
        # Ridimensiona l'immagine
        image = cv2.resize(image, self.target_size)
        
        # Normalizza i valori dei pixel nell'intervallo [0, 1]
        image = image.astype(np.float32) / 255.0
        
        # Aggiungi una dimensione per il canale (1 canale per immagini in scala di grigi)
        image = np.expand_dims(image, axis=0)
        
        return image
