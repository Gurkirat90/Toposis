# TOPSIS Implementation

**BY**: Gurkirat Singh  
**Roll Number**: 102303256  
**Group**: 3C21  

`topsis-gurkirat-102303256` is a Python library for solving **Multiple Criteria Decision Making (MCDM)** problems using the **Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)**.

---

##  Installation

Install the package from PyPI using pip:

```bash
pip install topsis-gurkirat-102303256
```

---

##  Usage

Run the package via the command line:

```bash
topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>
```

### Example

```bash
topsis topsis_dataset.csv "0.2,0.15,0.15,0.2,0.15,0.15" "-,+,+,+,+,+" result.csv
```

---

## 🧮 Steps Followed in TOPSIS

1. **Normalization**  
   Transform the data into a comparable scale.

2. **Weighting**  
   Apply user-defined weights to the normalized decision matrix.

3. **Ideal Solutions**  
   Determine the ideal best and ideal worst values for each criterion.

4. **Distance Calculation**  
   Compute the Euclidean distance of each alternative from the ideal best and ideal worst.

5. **Closeness Score**  
   Calculate the relative closeness of each alternative to the ideal solution.

6. **Ranking**  
   Rank the alternatives based on the TOPSIS score.

---

## 📊 Sample Dataset

| Alternative | Cost | Quality | Delivery Time | Durability | Service | Energy Efficiency |
|------------|------|---------|---------------|------------|---------|-------------------|
| A1 | 250 | 7 | 5 | 8 | 8 | 6 |
| A2 | 200 | 6 | 7 | 7 | 7 | 7 |
| A3 | 300 | 8 | 4 | 9 | 9 | 8 |
| A4 | 275 | 7 | 6 | 8 | 8 | 7 |
| A5 | 225 | 9 | 3 | 9 | 8 | 9 |
| A6 | 260 | 8 | 5 | 8 | 9 | 8 |

---

## 🖥️ Output (Printed in Terminal)

```text
--- TOPSIS RESULTS (Score & Rank) ---
   Topsis Score    Rank
       0.534277      3
       0.308368      5
       0.691632      1
       0.534737      2
       0.401046      4
       0.582190      3
-------------------------------------
```

---

## 📚 Description

This package helps users evaluate and rank alternatives based on multiple criteria by applying the TOPSIS methodology.  
It is suitable for academic assignments, research work, and real-world decision-making problems.

---

## 📝 License

This project is intended for academic and educational use.
