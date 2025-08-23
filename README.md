# lastfm-project

Analysis and exploration of the Last.fm dataset for the ITC6001 (Introduction to Big Data) final project. The code loads raw `.dat` files, explores the data, stores it in MySQL, performs outlier handling and temporal analysis, and computes user similarity and friend–listening correlations. Outputs (figures, CSV/TSV files, and neighbor lists) are written to `output/`.

## Contents
- Project overview
- Setup (Python + MySQL)
- How to run
- Tasks (Q1–Q5)
- Project structure
- Notes and assumptions
- License

---

## Project overview
The project answers the following questions using the Last.fm data:
- Q1: Read and explore the raw `.dat` files; visualize top artists and tags.
- Q2: Clean/outlier handling for artists and tags and export cleaned CSVs.
- Q3: Temporal exploration of user listening behavior.
- Q4: User–user similarity based on the user–artist matrix (cosine similarity) and export of nearest neighbors.
- Q5: Relationship between user friendship links and listening similarity.

---

## Setup

### Python
- Python 3.10+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  If you do not have a `requirements.txt`, install:
  ```bash
  pip install pandas numpy matplotlib seaborn mysql-connector-python
  ```

### MySQL (required for DB steps)
- A local MySQL server (8.x recommended).
- Create a user with permissions to create databases and tables.
- Configure credentials via environment variables (recommended) or edit `src/db_utils.py`:
  - `host`, `user`, `password`
- Database name used: `LastFM` (created by the code).

> Tip: replace hard‑coded credentials in `src/db_utils.py` with environment variables (read via `os.getenv`) before publishing.

---

## How to run

From the project root (`lastfm_project/`):

1) Create database schema and tables, then insert data:
```bash
python src/db_utils.py            # creates DB + tables
python src/insert_data.py         # loads .dat files and inserts to MySQL
```

2) Run individual analysis tasks:
```bash
python src/q1_read_explore.py
python src/q2_outlier_removal.py
python src/q3_temporal_exploration.py
python src/q4_user_similarity.py
python src/q5_user_friend_correlation.py
```

All outputs are saved in `output/`.

---

## Tasks

### Q1 — Read & Explore
- Load `.dat` files into pandas.
- Basic EDA and figures: `q1_top_10_artists.png`, `q1_top_10_tags.png`.

### Q2 — Outlier handling
- Identify and remove/clip problematic records.
- Export cleaned CSVs: `q2_cleaned_artists.csv`, `q2_cleaned_tags.csv`.

### Q3 — Temporal exploration
- Analyze listening patterns over time; export per‑question outputs to `output/`.

### Q4 — User similarity
- Build user–artist matrix and compute cosine similarity.
- Export similarity and nearest neighbors (e.g., `neighbors-k3-users.dat`, `neighbors-k10-users.dat`).

### Q5 — Friends vs similarity
- Examine correlation between friendship links and listening similarity.
- Produce summary statistics/plots in `output/`.

---

## Project structure
```
lastfm_project/
├─ data/                          # raw .dat files
├─ output/                        # generated figures/tables
├─ src/
│  ├─ db_utils.py                 # MySQL connection + schema creation
│  ├─ load_data.py                # file loading helpers
│  ├─ insert_data.py              # insert pandas DataFrames into MySQL
│  ├─ q1_read_explore.py
│  ├─ q2_outlier_removal.py
│  ├─ q3_temporal_exploration.py
│  ├─ q4_user_similarity.py
│  └─ q5_user_friend_correlation.py
└─ main.py                        # optional orchestration entrypoint
```

---