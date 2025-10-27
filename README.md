# LastFM Analysis

Last.fm dataset analysis: data exploration, outlier removal, temporal analysis, user similarity, and friend correlations.

---

## Setup

### MySQL
```bash
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql -p
```

```sql
CREATE USER 'lastfm'@'localhost' IDENTIFIED BY 'lastfm123';
GRANT ALL PRIVILEGES ON *.* TO 'lastfm'@'localhost';
EXIT;
```

Update `src/db_utils.py`:
```python
DB_CONFIG = {'host': 'localhost', 'user': 'lastfm', 'password': 'lastfm123'}
```

### Python
```bash
python3 -m venv lastfm.venv
source lastfm.venv/bin/activate
pip install -r requirements.txt
```

### Data
Place `.dat` files in `data/` directory.

---

## Run

```bash
python main.py
```

Outputs saved to `output/` directory.

---

### Data
Download dataset: [Last.fm Hetrec 2011](http://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip)

Extract and place `.dat` files in `data/` directory.

---

## Structure

```
├── data/          # .dat files
├── src/           # analysis scripts
├── main.py        # run pipeline
└── output/        # results
```
