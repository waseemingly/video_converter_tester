# Automated Video Conversion Test Suite

This project is an automated test suite for a video conversion website, [video-converter.com](https://video-converter.com/), utilizing Playwright for browser automation and OpenAI's API for generating descriptions of test results. The suite includes positive and negative test cases, with the option to export test results as a CSV file. The dashboard interface provides a simple way to initiate tests and monitor their statuses in real-time.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Running the Tests](#running-the-tests)
- [Exporting Results](#exporting-results)
- [Considerations and Priorities](#considerations-and-priorities)
- [Potential Improvements](#potential-improvements)

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
2. **Playwright** (Python package)
3. **OpenAI API Key** (needed for generating test descriptions using OpenAI's API)
4. **Environment Variables**: `.env` file for storing your OpenAI API key

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

## Considerations and Priorities

Initially, I approached element identification using CSS selectors to streamline interactions within the test cases. However, this approach proved ineffective due to the dynamic nature of the elements and the limitations of strict selectors. I then referred to the implementation of WebVoyager on LangGraph to enhance robustness in navigating the test site. This allowed for bounding box annotations and LLM-driven actions that could better adapt to changing or unpredictable UI components. This approach provided an advantage by reducing dependency on specific CSS selectors while using the `mark_page.js` for annotating elements.

To improve annotation precision, I had to refine bounding boxes to ensure smaller areas were accurately captured, particularly for interactive elements that were not initially recognized. This adjustment significantly improved accuracy in capturing and interacting with essential UI components across the tests.

For automation, I focused on using Playwright to manage web navigation across all test cases. For the positive test case, I was able to automate file upload for an MP4 less than 4GB, select AVI format, and choose the lowest HD setting (720p). However, the test encountered an obstacle with the "Convert" button, as the button either did not appear interactable immediately after processing or required an additional delay. To address this, I implemented scrolling and retry attempts to ensure the button was clicked, but I was unable to resolve it.

Similarly, for Negative Test Case 2 (uploading a file exceeding 4GB), I automated the upload, but the test failed to detect the expected error message. Adjustments to handle this error state may involve additional wait times or checks after file uploads complete.

For Negative Test Case 1, which involved uploading a YouTube URL, I faced challenges in handling the pop-up dialog box. The dialog box was not consistently captured by the bounding box approach, which made it difficult to programmatically enter the URL into the input field. I believe further fine-tuning with Playwright’s dialog handling features could support such interactions. With more time, I would focus on exploring Playwright's handling of dynamic elements and external dialogs within LangGraph to enhance test robustness and accuracy.

In light of these technical challenges, I prioritised the following areas for completion:

1.  **Use of OpenAI API for Result Descriptions**: I utilised OpenAI’s API to generate concise, descriptive summaries of each test result. The `generate_test_description` function uses error messages directly for failed steps and sends a prompt to OpenAI for an AI-generated description. This minimizes additional API calls for the failed steps, tying the generated summary closely to the actual error message.
    
2.  **CSV Export Implementation**: The CSV export function worked as intended, capturing the test case name, status (Success/Fail), failed steps, and AI-generated description of the result. This allowed for efficient reporting with columns as specified.
    
3.  **Dashboard Simplicity and Usability**: Given time constraints, I focused on creating a clean, simple dashboard interface with essential functionality, prioritizing backend processing and ensuring automated actions were thoroughly implemented.

With additional time, I would focus on refining error handling within Playwright and expanding the interactions with pop-up dialogs to enhance automation reliability for dynamic UIs.

---

## Potential Improvements

- **Enhance Error Handling**: Refine error detection for more robust and specific handling of test failures.
- **UI Enhancements**: Improve the dashboard interface with real-time updates and animations for better user experience.
- **Parallel Execution**: Modify the test runner to support parallel execution of test cases to save time.
- **Result Storage**: Implement a database to log historical test results, enabling trend analysis and test reporting over time.

---
