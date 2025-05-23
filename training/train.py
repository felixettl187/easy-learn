import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score
from preprocessing import load_and_prepare_data
from model import ImportanceClassifier


csv_dir = "training_data"
X_train, X_val, y_train, y_val = load_and_prepare_data(csv_dir)


X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
y_val_tensor = torch.tensor(y_val, dtype=torch.float32)


input_dim = X_train.shape[1]
output_dim = 1
model = ImportanceClassifier(input_dim, output_dim)

criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


epochs = 20
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()

    outputs = model(X_train_tensor).squeeze()
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()


    model.eval()
    with torch.no_grad():
        val_outputs = model(X_val_tensor).squeeze()
        preds = (val_outputs >= 0.5).float()
        acc = accuracy_score(y_val_tensor, preds)

    print(f"Epoche {epoch + 1}/{epochs} - Loss: {loss.item():.4f} - Val Accuracy: {acc:.4f}")


torch.save(model.state_dict(), "models/importance_model.pth")
print("Modell gespeichert unter models/importance_model.pth")