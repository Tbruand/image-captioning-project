from tqdm import tqdm
import os
import json
import torch
from datetime import datetime
import matplotlib.pyplot as plt
from torch.optim.lr_scheduler import ReduceLROnPlateau
from src.train.metrics import compute_bleu, compute_rouge


def train_model(decoder, train_loader, val_loader, tokenizer, criterion, optimizer, num_epochs=10, patience=3):
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    decoder.to(device)

    # 📁 Dossier de sortie daté
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = f"outputs/{timestamp}"
    os.makedirs(save_dir, exist_ok=True)
    best_model_path = os.path.join(save_dir, "decoder.pt")
    checkpoint_path = os.path.join(save_dir, "checkpoint.pt")
    metrics_path = os.path.join(save_dir, "metrics.json")

    # 🔢 Historique
    train_losses, val_losses = [], []
    val_bleus_1, val_bleus_2, val_bleus_3, val_bleus_4 = [], [], [], []
    val_rouges = []
    all_metrics = []

    best_bleu = 0
    patience_counter = 0
    scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=1)

    print(f"🚀 Training started on {device}")
    epoch_bar = tqdm(range(num_epochs), desc="📆 Epochs")

    for epoch in epoch_bar:
        decoder.train()
        total_loss = 0.0

        batch_bar = tqdm(train_loader, desc=f"🧠 Training Epoch {epoch+1}", leave=True, position=1)
        for features, captions, lengths in batch_bar:
            features, captions = features.to(device), captions.to(device)
            optimizer.zero_grad()

            outputs = decoder(features, captions, lengths)
            targets = captions[:, 1:]
            outputs = outputs.view(-1, outputs.shape[-1])
            targets = targets.reshape(-1)

            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            batch_bar.set_postfix(loss=loss.item())

        avg_loss = total_loss / len(train_loader)
        train_losses.append(avg_loss)

        # 🔍 Évaluation
        decoder.eval()
        all_preds, all_refs = [], []
        val_loss_total = 0.0  # ← On initialise le cumul de val loss

        val_bar = tqdm(val_loader, desc=f"🔍 Evaluating Epoch {epoch+1}", leave=True, position=2)
        with torch.no_grad():
            for features, captions, lengths in val_bar:
                features, captions = features.to(device), captions.to(device)
                outputs = decoder(features, captions, lengths)

                # 🎯 Calcul de la loss sur la validation
                targets = captions[:, 1:]
                output_flat = outputs.view(-1, outputs.shape[-1])
                target_flat = targets.reshape(-1)
                val_loss = criterion(output_flat, target_flat)
                val_loss_total += val_loss.item()

                # 🔡 Captions pour BLEU/ROUGE
                preds = outputs.argmax(-1).detach().cpu().tolist()
                refs = captions[:, 1:].detach().cpu().tolist()

                decoded_preds = [tokenizer.decode(p) for p in preds]
                decoded_refs = [tokenizer.decode(r) for r in refs]
                all_preds.extend(decoded_preds)
                all_refs.extend(decoded_refs)

        avg_val_loss = val_loss_total / len(val_loader)
        val_losses.append(avg_val_loss)

        # 📏 Calcul des métriques
        bleu_1 = compute_bleu(all_refs, all_preds, n=1)
        bleu_2 = compute_bleu(all_refs, all_preds, n=2)
        bleu_3 = compute_bleu(all_refs, all_preds, n=3)
        bleu_4 = compute_bleu(all_refs, all_preds, n=4)
        rouge_l = compute_rouge(all_refs, all_preds)

        val_bleus_1.append(bleu_1)
        val_bleus_2.append(bleu_2)
        val_bleus_3.append(bleu_3)
        val_bleus_4.append(bleu_4)
        val_rouges.append(rouge_l)
        scheduler.step(bleu_3)

        print(f"\n📊 Epoch {epoch+1}/{num_epochs} — Loss: {avg_loss:.4f}")
        print(f"   ➤ BLEU-1: {bleu_1:.4f} | BLEU-2: {bleu_2:.4f} | BLEU-3: {bleu_3:.4f} | BLEU-4: {bleu_4:.4f} | ROUGE-L: {rouge_l:.4f}\n")

        # 💾 Sauvegarde du meilleur modèle
        if bleu_3 > best_bleu:
            best_bleu = bleu_3
            patience_counter = 0
            torch.save(decoder.state_dict(), best_model_path)
            torch.save({
                "epoch": epoch,
                "decoder_state_dict": decoder.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "train_losses": train_losses,
                "val_bleu_3": val_bleus_3,
                "val_rouge_l": val_rouges,
                "tokenizer": tokenizer.word2idx
            }, checkpoint_path)
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print("⛔ Early stopping triggered.")
                break

        # 💾 Sauvegarde metrics.json à chaque epoch
        epoch_metrics = {
            "epoch": epoch + 1,
            "train_loss": avg_loss,
            "val_loss": avg_val_loss,
            "bleu_1": bleu_1,
            "bleu_2": bleu_2,
            "bleu_3": bleu_3,
            "bleu_4": bleu_4,
            "rouge_l": rouge_l
        }
        all_metrics.append(epoch_metrics)

        with open(metrics_path, "w") as f:
            json.dump(all_metrics, f, indent=4)

        # 📊 Graphe 1 : train_loss vs val_loss
        plt.figure(figsize=(8, 5))
        plt.plot(train_losses, label="Train Loss")
        plt.plot(val_losses, label="Val Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title("Train vs Val Loss")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(save_dir, "losses_plot.png"))
        plt.close()

        # 📊 Graphes BLEU-1 à BLEU-4 + ROUGE-L
        metric_plots = {
            "bleu_1_plot.png": val_bleus_1,
            "bleu_2_plot.png": val_bleus_2,
            "bleu_3_plot.png": val_bleus_3,
            "bleu_4_plot.png": val_bleus_4,
            "rouge_l_plot.png": val_rouges
        }

        for filename, values in metric_plots.items():
            plt.figure(figsize=(8, 5))
            plt.plot(values, label=filename.replace("_plot.png", "").upper())
            plt.xlabel("Epoch")
            plt.ylabel("Score")
            plt.title(filename.replace("_plot.png", "").upper())
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(save_dir, filename))
            plt.close()

    return train_losses, val_bleus_3, val_rouges
