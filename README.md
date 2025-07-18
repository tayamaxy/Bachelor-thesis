# Generating latin squares and orthogonality – Bachelor Thesis

This repository accompanies my bachelor’s thesis **“Generating latin squares and orthogonality.”**  
It contains a pure-Python implementation of two heuristic algorithms that, given a Latin square \(L\) of order \(n\), try to construct an orthogonal mate \(L'\)′, also satisfying the Latin square properties.

## 💡 Motivation

Not every Latin square has an orthogonal mate. Euler conjectured in the 18th century that there are no two orthogonal Latin squares of order 6 — a result later confirmed by Gaston Tarry in 1900.

This makes the search for orthogonal mates highly nontrivial, especially for squares with very few compatible partners. Moreover, even when a mate exists, the time required to find it can vary dramatically depending on the structure of the square and the randomness in the search path.

This project implements two heuristics to address this challenge:
- A simple local-search algorithm based on neighbor exploration.
- A genetic algorithm that reduces average search time using population-based optimization and parallel evaluation.


> 📝 The full thesis (Czech) is included in `report/`.

## ✨ Key ideas

| Topic | Where in code / thesis |
|-------|------------------------|
| **Improper Latin squares** extend the classical definition by allowing temporary “three-symbol” cells, enlarging the search space while preserving connectivity. | §1.1, `Latin_square.py` |
| **Local switch (Jacobson & Matthews random walk)** replaces a \(2 × 2\) subsquare and always stays inside the (improper) Latin-square space. | §1.5, Algorithm 1.5.1, `Latin_square.py` |
| **Hill-climbing heuristic (`find_ort`)** explores *n* random neighbours per step and keeps the best. |§2.2, Algorithm 2.2.2, `OrtMate_algorithm.py` |
| **Genetic heuristic (`find_ort_gen`)** maintains a population, evaluates in parallel, and applies roulette-wheel selection plus random immigrants. |§2.3, Algorithm 2.3.2, `OrtMateGen_algorithm.py` |

## 🚀 Installation

```bash
git clone https://github.com/<your-username>/orthogonal-latin-squares.git
cd orthogonal-latin-squares
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # installs numpy only
```

## 🧠 Features

- Pure-Python implementation with no external dependencies (only NumPy required)
- Two heuristic strategies for constructing orthogonal Latin squares:
  - Local search via hill-climbing (based on neighbor quality)
  - Genetic search with population selection, mutation, and parallel evaluation
- Extensible LatinSquare class:
  - Supports improper squares, random walk (Jacobson–Matthews), neighbor generation, and validation
- Scoring function for measuring how close a square is to orthogonality
- Easily modifiable search parameters (iterations, neighbors per step, etc.)
- Basic CLI / script support for reproducible experiments

## 🛠️ Technologies

- Language: Python 3.8+
- Core library: NumPy
- Style: Functional + Object-Oriented design
- Main class: LatinSquare (core data structure & operators)
- Heuristic modules:
  - OrtMate_algorithm.py (hill-climbing)
  - OrtMateGen_algorithm.py (genetic variant using multiprocessing)


## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.


## 🖇️ Citation

If you use this code in academic work, please cite the associated thesis:

@bachelorthesis{Starchenko2024,
  author  = {Taisiia Starchenko},
  title   = {Generating latin squares and orthogonality},
  school  = {Charles University},
  year    = {2024}
  type    = {Bachelor's thesis},
  supervisor = {prof. RNDr. Aleš Drápal, CSc., DSc.}
  url     = {https://dspace.cuni.cz/handle/20.500.11956/193704}
}

## 👤 Author

Name: Taisiia Starchenko
[LinkedIn](https://www.linkedin.com/in/tayamaxy)