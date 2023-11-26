# s3632442-COSC2639-a3

# Automotive Image Verification Web App

This application aims to conduct pre-approval checks for submitted images to ensure that users do not upload previously used images for verification. It's designed to streamline the approval process and prevent duplicate image submissions, facilitating efficient verification for automotive club permits.

### Live Link
[Automotive Image Verification Web App](http://ec2-18-188-86-156.us-east-2.compute.amazonaws.com)

### Source Code
[GitHub Repository](git@github.com:s3632442/s3632442-COSC2639-a3.git)

## Summary

As the president of an automotive club, ensuring the authenticity and uniqueness of submitted vehicle images for annual approval is crucial. This web app mitigates the submission of duplicate images by conducting pre-verification checks, saving time, and ensuring that valid, recent images are provided for permit renewals.

## Introduction

The application aims to address the challenges faced in verifying members' vehicles remotely. It prevents the resubmission of old images, reducing the risk of permit lapses due to insufficient evidence.

## Motivation

The primary motivation behind this app is to streamline the verification process, preventing delays caused by last-minute image submissions or reusing previous images. It ensures timely approval and reduces the manual effort required for verification.

## High-Level View

As the president and sole signatory of the automotive club, the app aims to prevent users from re-submitting images for subsequent approvals. By ensuring uniqueness in image submissions, it expedites the approval process.

## Beneficiaries

This app benefits both club administrators and members by reducing time wasted on incorrect submissions and ensuring timely and accurate approval processes.

## Requirements

- **Security:** Ensures data privacy and security through SHA256-based authentication.
- **Simplicity:** Provides a user-friendly interface to prevent user confusion.
- **Centralization:** Avoids third-party dependencies to maintain data privacy.
- **Organization:** Categorizes and organizes data for association with specific years during submissions.

## Related Work

This project aims to address specific needs not met by existing platforms. While leveraging various AWS services, it provides customizability and full control for further development.

## Architecture

### EC2

- Hosts the web application using Flask on an Ubuntu 20.04 instance via Nginx.
- Implements an initialization sequence for resource checks and data population.
- Authentication: SHA256 algorithm with hashed passwords and salts.

### S3

- Stores images in separate folders for approved and pending images.
- Enables a simple maintenance strategy and avoids accidental image deletion.
  
### CloudFront

- Caches high-definition images stored in S3 for faster rendering.
- Eliminates delays caused by cross-region hosting and transmission.

### DynamoDB

- Stores authentication info, image data, and vehicle information.
- Segregates vehicle and vehicle image data for better organization and management.

### AWS API Gateway

- Configured to accept JSON payloads for image comparison trigger.

### AWS Lambda

- Hosts functions for image comparison and verification.
- Currently utilizes a basic hashing algorithm; future plans include improved likeness evaluation.

## Usage

### Prerequisites

#### Linux Environment:

- [Python](https://www.python.org/) installed (version 3.6 or higher).
- [Git](https://git-scm.com/) for cloning the repository.
- Terminal or command-line interface.

#### Windows Environment:

- [Python](https://www.python.org/) installed (version 3.6 or higher).
  - During installation, ensure that you check the option to add Python to your system PATH.
- [Git](https://git-scm.com/) for cloning the repository.
- Command Prompt or PowerShell.

### Steps

1. **Clone the GitHub Repository:**

    ```bash
    git clone git@github.com:s3632442/s3632442-COSC2639-a3.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd s3632442-COSC2639-a3/retroideal
    ```

3. **Create and Activate a Python Environment:**

    For Linux:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    For Windows:

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Application:**

    ```bash
    python3 application.py
    ```

6. **Access the Web Application:**

    Open your web browser and visit [http://localhost:5000](http://localhost:5000) to access the web application.

These steps provide a general guide for running the application on both Linux and Windows environments. Make sure to follow the appropriate commands based on your operating system. Additionally, if there are any specific configurations or settings needed, you can include them in this section.

## Project Status and Planned Improvements

### Current Stage

The project is currently in the phase of implementing crucial features for filtering approved images and facilitating image uploads by vehicle registration (reg) through the side panel. CloudFront has been integrated as a proof of concept, establishing the groundwork for interfacing with members' glamshots or chosen display images.

### Ongoing Development

1. **Filtering Approved Images by Reg:**
   - Implementing functionality to filter approved images based on vehicle registration numbers.
   - Enabling seamless categorization and display of approved images specific to each vehicle.

2. **Enhanced Image Uploads by Reg:**
   - Enabling users to upload vehicle images while associating them directly with vehicle registration for verification.

3. **CloudFront Integration for Member Display Images:**
   - Finalizing integration with CloudFront to handle members' display images or glamshots efficiently.

### Planned Future Improvements

Beyond the current phase, several high-priority improvements and new features are on the roadmap:

1. **User Registration:**
   - Implementation of user registration functionality to manage member accounts securely.

2. **Enhanced Image Comparison Algorithm:**
   - Refinement of the image comparison algorithm based on a percentage of likeness rather than relying solely on an identical match.
   - Ensuring greater flexibility in image matching for slightly modified or similar images.

3. **Improved Styling and UI/UX:**
   - Enhancing the application's appearance and user experience with better styling and intuitive design.

4. **Request for Assessment Feature:**
   - Introduction of a feature enabling users to request assessments, streamlining the permit renewal process.

5. **AWS Glacier Archiving:**
   - Implementation of AWS Glacier for data backup, ensuring data durability and long-term storage.

6. **Email Reminders for Evidence Updates:**
   - Introducing automated email reminders to inform members about upcoming evidence updates for permit renewal.

7. **Admin Assessment Reminders:**
   - Implementing email reminders for administrators to conduct assessments, ensuring timely permit renewals.

### Roadmap and Priorities

The highest priority currently lies in implementing user registration, refining the image comparison algorithm, and improving the overall user experience. Future iterations will focus on additional functionalities and enhancements to streamline the approval process and ensure data integrity and user convenience.
