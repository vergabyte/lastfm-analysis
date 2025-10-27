# LastFM Analysis - Minimal Version

Implementation of Last.fm dataset analysis.

---

## Project Overview

Analyzes Last.fm music listening data to answer:
- **1**: Data exploration and basic statistics
- **2**: Outlier detection and removal (z-score method)
- **3**: Temporal analysis of user activity
- **4**: User similarity via cosine similarity and k-NN
- **5**: Correlation between friendship and listening behavior

---

## Setup

### 1. Install MySQL

```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

### 2. Create Database User

```bash
sudo mysql -p
# Enter your MySQL password
```

In MySQL:
```sql
CREATE USER 'lastfm'@'localhost' IDENTIFIED BY 'lastfm123';
GRANT ALL PRIVILEGES ON *.* TO 'lastfm'@'localhost';
EXIT;
```

### 3. Configure Credentials

Edit `src/db_utils.py` line 3:
```python
DB_CONFIG = {'host': 'localhost', 'user': 'lastfm', 'password': 'lastfm123'}
```

### 4. Create Virtual Environment

```bash
python3 -m venv lastfm.venv
source lastfm.venv/bin/activate  # Linux/Mac
# OR
lastfm.venv\Scripts\activate     # Windows
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Add Data Files

Ensure your data files are in the `data/` directory:
```
lastfm-analysis/
├── data/
│   ├── artists.dat
│   ├── tags.dat
│   ├── user_artists.dat
│   ├── user_taggedartists.dat
│   └── user_friends.dat
├── src/
└── main.py
```

---

## Run

```bash
python main.py
```

This executes all analysis steps in sequence:
1. Creates MySQL database and tables
2. Loads data into MySQL
3. Explores data 
4. Removes outliers 
5. Temporal analysis 
6. Computes user similarity 
7. Analyzes friend correlations 

**Output:** Results saved to `output/` directory

---

## Individual Scripts

Run scripts separately if needed:

```bash
# Database setup
python src/db_utils.py           # Create tables
python src/data_loader.py        # Insert data

# Analysis
python src/q1_read_explore.py
python src/q2_outlier_removal.py
python src/q3_temporal_exploration.py
python src/q4_user_similarity.py
python src/q5_user_friend_correlation.py
```

---

## Project Structure

```
lastfm-analysis/
├── data/                      # Raw .dat files
├── output/                    # Generated results (auto-created)
├── src/
│   ├── db_utils.py           # MySQL connection + schema (25 lines)
│   ├── data_loader.py        # Data loading + insertion (31 lines)
│   ├── q1_read_explore.py    # Data exploration (11 lines)
│   ├── q2_outlier_removal.py # Outlier removal (34 lines)
│   ├── q3_temporal_exploration.py # Temporal analysis (32 lines)
│   ├── q4_user_similarity.py # Similarity + k-NN (46 lines)
│   └── q5_user_friend_correlation.py # Correlations (18 lines)
├── main.py                    # Pipeline orchestration (17 lines)
├── requirements.txt
└── lastfm.venv/              # Virtual environment (create locally)
```

---

## Output Files

**Q2 - Outlier Removal:**
- `output/q2_clean_artists.csv`
- `output/q2_clean_tags.csv`
- `output/q2_clean_users.csv`

**Q3 - Temporal Analysis:**
- `output/q3_monthly_counts.csv`
- `output/q3_top5_tags.csv`
- `output/q3_top5_artists.csv`

**Q4 - User Similarity:**
- `output/user-pairs-similarity.dat`
- `output/neighbors-k3-users.dat`
- `output/neighbors-k10-users.dat`

**Q5 - Correlations:**
- Console output showing correlation coefficients

---
