# Automated Video Conversion Test Suite

This project is an automated test suite for a video conversion website, [video-converter.com](https://video-converter.com/), utilizing Playwright for browser automation and OpenAI's API for generating descriptions of test results. The suite includes positive and negative test cases, with the option to export test results as a CSV file. The dashboard interface provides a simple way to initiate tests and monitor their statuses in real-time.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Running the Tests](#running-the-tests)
- [Exporting Results](#exporting-results)
- [Project Structure](#project-structure)
- [Evaluation Criteria](#evaluation-criteria)

---

## Project Overview

This test suite is designed to automate video conversion tests on [video-converter.com](https://video-converter.com/). The suite includes:
1. **Positive Test**: Converts an MP4 file to AVI format with HD 720p resolution.
2. **Negative Test 1**: Attempts to upload a YouTube link, expecting a failure.
3. **Negative Test 2**: Attempts to upload a large video file, expecting a failure due to file size restrictions.

OpenAI's API is integrated to provide AI-generated descriptions of test results, enhancing the readability and interpretability of outcomes.

---

## Features

- **Automated Browser Testing**: Uses Playwright to interact with and test the web interface of the video converter site.
- **AI-Powered Result Descriptions**: Leverages OpenAI's API to generate detailed descriptions for test results.
- **CSV Export**: Allows exporting of test results with descriptions to a CSV file for easy review and documentation.
- **Dashboard Interface**: Provides a simple frontend to run individual test cases and view real-time results.
- **WebVoyager Implementation**: Implements the [WebVoyager](https://github.com/langgraph/WebVoyager) approach on LangGraph for LLM-driven web navigation, allowing the use of AI to handle complex user interactions and navigate web elements efficiently.

## How WebVoyager is Used

This project leverages WebVoyager to perform LLM-assisted web navigation. WebVoyager is an implementation by LangGraph designed to streamline interactions on the web using Large Language Models (LLMs). It allows the system to interpret webpage elements dynamically, which reduces the dependency on strict CSS selectors or XPath for every interaction. By using WebVoyager, this project can navigate the test site more robustly, as it relies on bounding box annotations and LLM-generated actions to locate and interact with elements on the page.

---

## Setup Instructions

### Prerequisites

1. **Python 3.7+**
2. **Node.js** (required by Playwright for browser control)
3. **Playwright** (Python package)
4. **OpenAI API Key** (needed for generating test descriptions using OpenAI's API)
5. **Environment Variables**: `.env` file for storing your OpenAI API key

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a Virtual Environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install Playwright Browsers**

    Playwright requires its own browser binaries. Install them using:

    ```bash
    playwright install
    ```

5. **Set Up OpenAI API Key**

    Create a `.env` file in the project root and add your OpenAI API key:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    ```

6. **Install Frontend Dependencies**

    ```bash
    npm install
    ```

### Setting Up the Dashboard

To run the dashboard for managing tests, ensure that `app.py` and the `index.html` frontend file are set up in the project root.

---

## Running the Tests

1. **Start the Flask Server**

    ```bash
    flask run
    ```

    This will start the backend server and make the endpoints for each test case available.

2. **Access the Dashboard**

    Open `index.html` in a browser to view the dashboard, which contains buttons to initiate each test.

3. **Running Tests from the Dashboard**

    - **Positive Test**: Click the "Run Positive Test" button to test video conversion with an MP4 file.
    - **Negative Test 1**: Click the "Run Negative Test 1 - YouTube Link" button to check behavior with a YouTube URL.
    - **Negative Test 2**: Click the "Run Negative Test 2 - Large File" button to test behavior with a large file upload.

4. **Viewing Results**

    - Test statuses and descriptions are displayed on the dashboard in real-time.
    - The status can be "Success", "Fail", or "Running".
    - A detailed AI-generated description of the test results appears after each test completes.

---

## Exporting Results

To export test results as a CSV file:

1. Click the "Export CSV" button on the dashboard.
2. The exported CSV file will contain:
   - Test Case Name
   - Status (Success/Fail)
   - Steps that failed (if any)
   - AI-generated description of the result

---

## Potential Improvements

- **Enhance Error Handling**: Refine error detection for more robust and specific handling of test failures.
- **UI Enhancements**: Improve the dashboard interface with real-time updates and animations for better user experience.
- **Additional Test Cases**: Extend the suite to cover more edge cases or variations of file types and sizes.
- **Parallel Execution**: Modify the test runner to support parallel execution of test cases to save time.
- **Result Storage**: Implement a database to log historical test results, enabling trend analysis and test reporting over time.

---
