# Rezultate Statistice - Disertație de Master

**Facultatea de Sociologie, UBB Cluj-Napoca**  
**Master: Analiza Datelor Complexe**  
**Masterand: Răzvan-Andrei Enache**  

**Data generare:** 2026-06-08 05:59  

---

## Tabel 1: Distribuție Sentiment

| Sentiment   |   Count |   Percentage |
|:------------|--------:|-------------:|
| Positive    |    4906 |      33.5797 |
| Negative    |    9704 |      66.4203 |
| Total       |   14610 |     100      |

---

## Tabel 2: Sentiment pe Candidați

| Candidat      |   Positive % |   Negative % |    N |
|:--------------|-------------:|-------------:|-----:|
| Nicușor Dan   |      32.8767 |      67.1233 | 1825 |
| George Simion |      32.6653 |      67.3347 | 3343 |

---

## Tabel 3: Teste Statistice RQ1-RQ2

| Test                | Statistic   |    p-value | Effect Size      |
|:--------------------|:------------|-----------:|:-----------------|
| Mann-Whitney U      | U=3197868   |   0.004041 | r=-0.0483        |
| Chi-square          | χ²=0.02     |   0.901471 | V=0.0017         |
| Bootstrap CI Dan    | Mean=0.7438 | nan        | [0.7376, 0.7504] |
| Bootstrap CI Simion | Mean=0.7319 | nan        | [0.7274, 0.7366] |

---

## Tabel 5: Corelații Spearman RQ3

| Predictor                     |   Spearman ρ |     p-value | Significant   |
|:------------------------------|-------------:|------------:|:--------------|
| Caps Ratio                    |  -0.00875851 | 0.289788    | ❌            |
| Aggressive Punctuation        |   0.05104    | 6.70945e-10 | ✅            |
| Has Caps (Binary)             |  -0.00554684 | 0.5026      | ❌            |
| Has Aggressive Punct (Binary) |   0.0498093  | 1.70405e-09 | ✅            |
| Has Emoji (Binary)            |   0.0416511  | 4.74873e-07 | ✅            |
| Text Length                   |   0.0454825  | 3.79941e-08 | ✅            |

---

## Tabel 6: Teste Chi-Pătrat RQ3

| Test                             |    Chi2 |    p-value |   Cramér's V | Significant   |
|:---------------------------------|--------:|-----------:|-------------:|:--------------|
| Sentiment × Has Caps             | 2.96214 | 0.0852351  |    0.0140921 | No            |
| Sentiment × Has Aggressive Punct | 8.69712 | 0.00318714 |    0.0241469 | Yes           |

---

