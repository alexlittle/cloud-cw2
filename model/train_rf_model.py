import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import joblib


df = pd.read_csv('synth_traffic_data.csv')

X = df[["entropy", "packet_count", "pkt_size", "targetA_load", "targetB_load"]].copy()
y = df["action"].astype(int).values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    class_weight="balanced_subsample",
    random_state=42
)

rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
f1_macro = f1_score(y_test, y_pred, average="macro")

print(f"Accuracy: {acc:.3f}")
print(f"Macro-F1: {f1_macro:.3f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, digits=3))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=np.sort(np.unique(y))))


joblib.dump(rf, "../trafficrouter/rf_model.pkl")
