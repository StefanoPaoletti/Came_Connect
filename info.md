# CAME Integration - Versione Personalizzata di Stefano

⚠️ **Basata sul progetto originale di [Den901](https://github.com/Den901/ha_came)**

Questa è una versione ottimizzata per il mio specifico impianto CAME.

***

## 🔧 Modifiche e Miglioramenti

- ✅ Risolto problema dispositivi duplicati
- ✅ Ottimizzata velocità
- ✅ Nomi entità semplificati
- ✅ Migliorata gestione riavvio HA
- ✅ Corretta disinstallazione
- ✅ Rimossa dipendenza dal token
- ✅ Configurazione solo tramite UI

***

## Piattaforme Supportate

Piattaforma | Descrizione
-- | --
`binary_sensor` | Sensori di stato (ingressi digitali)
`climate` | Zone termiche (termostati e fan coil)
`light` | Luci, dimmer e RGB
`cover` | Tapparelle e coperture
`sensor` | Sensori analogici e contatori energia
`switch` | Relè generici
`scene` | Scenari CAME

![came-logo][came-logo]

## Funzionalità:

- Controllo luci, dimmer, RGB
- Gestione sensori analogici (temperatura, umidità, pressione)
- Gestione entità climatiche (termostati e fan coil)
- Gestione aperture (tapparelle, porte, cancelli)
- Monitoraggio energia (consumo e produzione)
- Attivazione scenari CAME
- Controllo relè generici
- Sensori di stato (ingressi digitali)

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

1. Scarica `came.zip` dalla [sezione releases][releases-latest]
2. Estrai tutti i file nella cartella `custom_components/came`
3. Riavvia Home Assistant

## ⚙️ Configurazione

1. Vai in **Impostazioni** → **Dispositivi e Servizi**
2. Clicca **"+ Aggiungi integrazione"**
3. Cerca **"CAME"**
4. Compila il form:
   - **Host**: `192.168.1.100` (il tuo IP)
   - **Username**: `admin` (default)
   - **Password**: `admin` (default)

## 🐛 Debug

Aggiungi al `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.came: debug
```

## ⚠️ Importante

Versione personalizzata - potrebbe non funzionare con altre configurazioni CAME.

**Per supporto ufficiale**: [Repository Originale Den901](https://github.com/Den901/ha_came)

## 📄 Licenza

MIT License - Basato sul lavoro originale di Danny Mauro (Den901)

***
[came-logo]: came-logo.png
[releases-latest]: https://github.com/StefanoPaoletti/ha_came_personale/releases/latest
