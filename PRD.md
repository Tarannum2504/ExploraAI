# Project Requirements Document (PRD): ExploraAI

## 1. Project Overview
**ExploraAI** is an interactive, educational web application built with Streamlit. It serves as a comprehensive "Exploratory Data Analysis (EDA) Simulation & Learning Platform" designed to help students and data science beginners intuitively understand the mechanics and importance of data cleaning, statistical analysis, and visualization.

**Author**: Tarannum Khan (B.Tech AI/ML)  
**Version**: 2.0_CYBER

## 2. Target Audience
- Data science beginners and university students.
- Educators looking for visual, interactive tools to teach EDA concepts.
- Self-taught learners needing hands-on confirmation of data manipulation techniques.

## 3. Core Features & Requirements

### 3.1. Data Playground (Interactive Simulation)
- **Objective**: Allow users to manipulate a messy dataset and observe the real-time impact on statistics and distributions.
- **Requirements**:
  - Provide a sample dataset with intentional flaws (missing values, duplicates, outliers).
  - Include controls for missing value handling (Mean, Median, Drop).
  - Include a slider for Outlier Threshold via Z-score clipping.
  - Include a toggle for duplicate removal.
  - Present side-by-side previews of the "Raw" dataset and the "Cleaned" dataset.
  - Render real-time visualizations (Histogram and Boxplot) that update dynamically based on cleaning operations.

### 3.2. Data Insights (Automated Analytics)
- **Objective**: Automatically generate statistical insights from the user-processed data.
- **Requirements**:
  - Calculate and visualize a Correlation Heatmap for all numeric features.
  - Identify the maximum correlation pair and automatically classify relationship strength.
  - Automatically detect and highlight remaining outliers using the IQR method.
  - Evaluate and display the distribution skewness of primary variables.

### 3.3. How It Works (Interactive Tutorial)
- **Objective**: Break down the standard EDA code workflow into a guided, step-by-step interactive tutorial.
- **Requirements**:
  - Display Python code snippets inside a simulated "Terminal View".
  - Provide clear, beginner-friendly explanations for each specific operation.
  - Support forward/backward UI navigation through the tutorial steps.

### 3.4. Easy Explanation (Bilingual Analogies)
- **Objective**: Lower the barrier to entry by explaining complex data concepts using everyday analogies.
- **Requirements**:
  - Support toggleable languages: English and Hinglish.
  - Use a relatable "room cleaning" analogy to explain the phases of Data Exploration.

### 3.5. Quiz Arena (Gamified Testing)
- **Objective**: Test user knowledge with a built-in gamified assessment.
- **Requirements**:
  - Minimum 10 questions covering core EDA concepts (Histograms, Z-scores, Missing Values, Pandas commands).
  - Real-time accuracy scoring and "Hot Streak" tracking.
  - Post-answer explanations and difficulty tier indicators.
  - Final scoring summary dashboard with a "Retake Quiz" option.

## 4. Technical Architecture
- **Framework**: Streamlit
- **Data Manipulation**: Pandas, NumPy
- **Visualization**: Altair
- **Styling**: Custom CSS and JS injection, `augmented-ui` framework for cyber-punk aesthetics, Google Fonts integration.

## 5. Design System Specifications
- **Theme**: "Cyber-Minimalist"
- **Background**: `#05050A` with a subtle grid overlay.
- **Primary Accents**: Volt Green (`#ADFF2F`), Purple (`#9D4EDD`), Magenta (`#FF007A`).
- **Typography**: `Orbitron` for headers, `Share Tech Mono` for metrics/code, `Rajdhani` for standard readable text.
- **UI Components**: Angled, clipped corners using `augmented-ui`, custom glowing interactive buttons.
