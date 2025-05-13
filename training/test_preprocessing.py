from preprocessing import load_and_prepare_data


csv_path = "/Users/felixettl/Desktop/HTWG/Semester04SoSe25/IoX/easy-learn/training/training_data"


X_train, X_val, y_train, y_val = load_and_prepare_data(csv_path)


print("Trainingsdaten:", X_train.shape)
print("Validierungsdaten:", X_val.shape)
print("Trainingslabels:", y_train.shape)
print("Validierungslabels:", y_val.shape)
print("\nBeispiel-Datensatz (Text-Vektor):", X_train[0])
print("Beispiel-Label:", y_train[0].item())