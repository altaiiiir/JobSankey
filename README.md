# Job Application Tracker with Sankey Diagram

A web application built with Streamlit for tracking job applications and visualizing the progression of each application through different stages. This app features a Sankey diagram to illustrate the flow of applications across various stages, helping users analyze the outcomes and bottlenecks in their job search process.

![image](https://github.com/user-attachments/assets/a11b9fb1-aa67-4793-80d7-6e6420b4ba5d)

*Screenshot of the Job Application Tracker*

## Features

- **Add New Job Applications**: Quickly add a new job application with details like company name, application URL, date, and current stage.
- **Track Progression**: Monitor each application's movement through stages such as "Applied," "Phone Screen," "Tech Screen," and more.
- **Sankey Diagram Visualization**: View a Sankey diagram that dynamically adjusts based on your application data, showing the flow between stages and highlighting the most common transitions.
- **Responsive Layout**: The interface is responsive, displaying job applications in rows of four and adjusting the input form for a cleaner, compact look.

## Technologies Used

- **Python**
- **Streamlit** for the web interface
- **Pandas** for data manipulation
- **Plotly** for generating the Sankey diagram visualization

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/job-application-tracker.git
   cd job-application-tracker
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
3. Run the Streamlit app using the provided batch script:
   ```bash
   run_streamlit.bat

## Usage
- Open the app in your browser (default: http://localhost:8501).
- Enter job application details in the form at the top.
- Click "Add Application" to save it to the tracker.
- View each application's stage history by expanding its section.
- Analyze the Sankey diagram at the bottom to see the flow of applications between stages.
