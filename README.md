# Smartphone Interaction Profiling: Mindful vs. Mindless

This project aims to classify the cognitive state and focus level of smartphone users into two distinct profiles: `Mindful` and `Mindless`. The classification is achieved by applying Machine Learning algorithms to user interaction data, specifically Touch Logs (screen swipe behaviors) and Sensor Logs (device physical motion/orientation).

## Directory Structure

```text
data-processing/
│
├── data/               # Raw datasets mapped per participant (P-001 to P-020).
├── docs/               # Project documentation and participant metadata.
├── master/             # Aggregated master datasets ready for modeling.
│   ├── Master_SensorLog_All.csv
│   └── Master_TouchLog_All.csv
│
├── main.ipynb          # Main Jupyter Notebook encompassing EDA, Preprocessing, and Modeling.
├── preprocess.py       # Python script for ETL operations: converts raw data into master data.
├── requirements.txt    # List of Python dependencies.
└── README.md           # Project documentation (this file).
```

## System Requirements & Installation

We recommend using a Python virtual environment to avoid dependency conflicts. Install the required packages via `requirements.txt`:

```bash
pip install -r requirements.txt
```

Key libraries used in this project:
- **Data Manipulation**: `pandas`, `numpy`
- **Data Visualization**: `matplotlib`, `seaborn`
- **Machine Learning**: `scikit-learn`, `xgboost`

## Project Workflow & Features

The end-to-end pipeline is mostly encapsulated within the `main.ipynb` notebook. The workflow is divided into several core stages:

### 1. Data Alignment (Merge AsOf)
Since Touch Logs and Sensor Logs are recorded asynchronously, we align them using Pandas' `merge_asof` function. This algorithm matches every touch/swipe interaction with the nearest device sensor reading based on the timestamp, using a maximum tolerance of 1000 milliseconds (1 second).

### 2. Exploratory Data Analysis (EDA)
We conduct visual explorations using Boxplots and Violin plots to analyze the differences in user behavior between `Mindful` and `Mindless` states. Key aspects analyzed include:
- **Scroll Velocity**: Visualized on a logarithmic scale to highlight rapid flicking anomalies commonly found in the *Mindless* state.
- **Inter-swipe Duration (Time Delta)**: Highlights the rest periods between swipes.
- **Device Motion Magnitude**: Assesses the physical steadiness of the device during usage.

### 3. Data Preprocessing
- **Handling Missing Values**: Rows with infinite or null values in critical feature columns are isolated and removed.
- **Label Encoding**: Target string labels (`Mindful`, `Mindless`) are converted into binary numerical formats (`0` and `1`).
- **Group Shuffle Split**: To prevent **Data Leakage**, the train-test split is grouped by `Participant_ID`. This strictly ensures that the model is never tested on data from participants it has already seen during the training phase.
- **Feature Scaling**: Features are normalized using `StandardScaler` to optimize model convergence.

### 4. Extracted Features
The selected features for building the Machine Learning model include:
- `Time_Delta_Sec`: Time passed since the last interaction.
- `Swipe_Distance`: Pixel distance covered by a drag/swipe.
- `Scroll_Velocity`: Speed of the swipe interaction (pixels per second).
- `Magnitude`: Overall acceleration force applied to the device.
- `Pitch` & `Roll`: Device orientation angles.

## Modeling & Evaluation

The project establishes a baseline using three supervised learning algorithms:
1. **Random Forest** (ensemble, tree-based)
2. **XGBoost** (gradient boosting framework)
3. **Support Vector Machine (SVM)** (using RBF kernel)

### Metrics
We comprehensively evaluate the models using:
- **Accuracy**: The ratio of correctly predicted observations to the total observations.
- **F1-Score**: The harmonic mean of Precision and Recall, which is crucial for handling class imbalances and assessing actual model robustness. mindfulness.
