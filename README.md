# CAME Integration - Versione Personalizzata
![Esempio di Immagine](Came.png)

***
⚠️ **Questa è una versione modificata e ottimizzata dell'integrazione CAME originale**

Basata sul lavoro di [Den901/ha_came](https://github.com/Den901/ha_came) - grazie Danny! 🙏

Questa versione include modifiche specifiche per il mio impianto CAME, con ottimizzazioni e correzioni di bug.
***

## 🔧 Modifiche Rispetto all'Originale

- ✅ Risolto problema dispositivi duplicati quando rinominati in CAME
- ✅ Ottimizzata velocità e ridotta lentezza
- ✅ Semplificati i nomi delle entità
- ✅ Migliorata gestione del riavvio di Home Assistant
- ✅ Corretta procedura di disinstallazione
- ✅ Rimossa dipendenza dal token (utilizza solo username e password)
- ✅ Configurazione solo tramite UI (più semplice e moderna)

## 📦 Installazione

### Tramite HACS (Consigliato)

1. Apri **HACS** in Home Assistant
2. Vai in **Integrazioni**
3. Clicca sui tre puntini in alto a destra
4. Seleziona **Repository personalizzati**
5. Aggiungi l'URL: `https://github.com/StefanoPaoletti/ha_came_personale`
6. Categoria: **Integrazione**
7. Cerca "CAME (Stefano)" e clicca **Scarica**
8. Riavvia Home Assistant

### Installazione Manuale

1. Scarica la [ultima release][releases-latest]
2. Estrai il contenuto nella cartella `custom_components/came` di Home Assistant
3. Riavvia Home Assistant

## ⚙️ Configurazione

1. Vai in **Impostazioni** → **Dispositivi e Servizi**
2. Clicca il pulsante **"+ Aggiungi integrazione"**
3. Cerca **"CAME"**
4. Inserisci i dati richiesti:
   - **Host**: Indirizzo IP del tuo dispositivo CAME ETI/Domo (es. `192.168.1.100`)
   - **Username**: Nome utente (default: `admin`)
   - **Password**: Password (default: `admin`)
5. Clicca **Invia**

Fatto! I tuoi dispositivi CAME verranno automaticamente rilevati e aggiunti a Home Assistant. 🎉

## 🛠️ Servizi Disponibili

- `came.force_update` - Forza l'aggiornamento di tutti i dispositivi
- `came.pull_devices` - Rileva nuovi dispositivi
- `came.refresh_scenarios` - Aggiorna l'elenco degli scenari

## 🐛 Debug

Per abilitare i log di debug, aggiungi al tuo `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.came: debug
    custom_components.came.pycame: debug
```

Poi riavvia Home Assistant.

## ⚠️ Nota Importante

Questa è una versione **personalizzata** ottimizzata per il mio specifico impianto. Potrebbe non funzionare perfettamente con altre configurazioni.

**Per il progetto originale e supporto ufficiale**, visita: [Repository originale di Den901](https://github.com/Den901/ha_came)

## 📄 Licenza

MIT License - Vedi file [LICENSE](LICENSE) per il testo completo.

## 🙏 Crediti

- **Autore Originale**: [Danny Mauro (Den901)](https://github.com/Den901)
- **Modifiche**: Stefano Paoletti

***
[releases-latest]: https://github.com/StefanoPaoletti/ha_came_personale/releases/latest
