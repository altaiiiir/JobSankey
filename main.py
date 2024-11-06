import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# Set the page layout to wide
st.set_page_config(layout="wide")

# Constants
CSV_FILE = "job_applications.csv"
DEFAULT_STAGES = ["Applied", "Ghosted", "Phone Screen", "Tech Screen", "Final Round", "Offer", "Rejected", "Withdrawn"]


class JobApplication:
    def __init__(self, row, stages):
        self.row = row  # Contains both index and row data
        self.stages = stages

    def render(self):
        # Extract row index and data
        index, row_data = self.row

        # Create an expander for each job application
        with st.expander(row_data["Name"], expanded=False):  # Keeps each expander collapsed by default
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

            # Display application name as a hyperlink if URL is provided
            if row_data["Application URL"]:
                name_link = f"[{row_data['Name']}]({row_data['Application URL']})"
            else:
                name_link = row_data["Name"]
            col1.markdown(name_link, unsafe_allow_html=True)

            # Display date (non-editable)
            col2.write(row_data["Date"])

            new_stage = col3.selectbox(
                "Stage",  # Accessible label for screen readers
                self.stages,
                index=self.stages.index(row_data["Stage"]),
                key=f"stage_{index}",
                label_visibility="collapsed"  # Hides the label visually
            )

            # Update the stage and history if it has changed
            if new_stage != row_data["Stage"]:
                st.session_state["app_data"].at[index, "Stage"] = new_stage

                # Ensure stage history is a list and update it with a new entry
                stage_history = row_data.get("Stage History", [])
                if not isinstance(stage_history, list):
                    stage_history = []
                stage_history.append({"stage": new_stage, "date": datetime.today().strftime("%Y-%m-%d")})
                st.session_state["app_data"].at[index, "Stage History"] = stage_history

                JobApplicationTracker.save_data(st.session_state["app_data"])  # Save changes to CSV

            # Remove button
            if col4.button("X", key=f"remove_{index}"):
                st.session_state["app_data"].drop(index=index, inplace=True)  # Remove row
                st.session_state["app_data"].reset_index(drop=True, inplace=True)  # Reset index after deletion
                JobApplicationTracker.save_data(st.session_state["app_data"])

            # Display stage history in timeline format
            stage_history = row_data.get("Stage History", [])
            timeline_text = " → ".join([f"{record['stage']} ({record['date']})" for record in stage_history])
            st.write(timeline_text)


class SankeyDiagram:
    def __init__(self, data, stages):
        self.data = data
        self.stages = stages

    def render(self):
        if not self.data.empty:
            # Define source-target mappings
            stage_index = {name: i for i, name in enumerate(self.stages)}
            sources, targets, values = [], [], []

            # Count stage transitions based on each application's stage history
            transition_counts = {}
            for _, row in self.data.iterrows():
                stage_history = row.get("Stage History", [])

                # Iterate over stage transitions in the history
                for i in range(len(stage_history) - 1):
                    current_stage = stage_history[i]["stage"]
                    next_stage = stage_history[i + 1]["stage"]

                    # Create a transition key and count occurrences
                    if current_stage in stage_index and next_stage in stage_index:
                        transition_key = (stage_index[current_stage], stage_index[next_stage])
                        transition_counts[transition_key] = transition_counts.get(transition_key, 0) + 1

            # Populate sources, targets, and values based on transition counts
            sources, targets, values = [], [], []
            for (source, target), count in transition_counts.items():
                sources.append(source)
                targets.append(target)
                values.append(count)

            # Render the Sankey diagram with full lifecycle data
            fig = go.Figure(go.Sankey(
                node=dict(
                    pad=20,
                    thickness=30,
                    line=dict(color="black", width=0.5),
                    label=self.stages
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values
                )
            ))

            fig.update_layout(font_size=28, width=1000, height=900)
            st.plotly_chart(fig, use_container_width=True)


class JobApplicationTracker:
    @staticmethod
    def load_data():
        # Load existing data or create a new DataFrame
        if os.path.exists(CSV_FILE):
            data = pd.read_csv(CSV_FILE)
            # Convert Stage History column from string to list if it's not empty
            data['Stage History'] = data['Stage History'].apply(
                lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else [])
        else:
            data = pd.DataFrame(columns=["Name", "Application URL", "Date", "Stage", "Stage History"])
        return data

    @staticmethod
    def save_data(df):
        # Save data to CSV
        df.to_csv(CSV_FILE, index=False)

    def __init__(self):
        # Initialize data and session state
        self.data = self.load_data()
        if "app_data" not in st.session_state:
            st.session_state["app_data"] = self.data.copy()

    def add_application(self, name, application_url, date, stage):
        # Add a new job application
        new_entry = pd.DataFrame({
            "Name": [name],
            "Application URL": [application_url if application_url else ""],
            "Date": [date.strftime("%Y-%m-%d")],
            "Stage": [stage],
            "Stage History": [[{"stage": stage, "date": date.strftime("%Y-%m-%d")}]]
        })
        self.data = pd.concat([self.data, new_entry], ignore_index=True)
        self.save_data(self.data)
        st.session_state["app_data"] = self.data.copy()

    def render(self):
        st.title("Job Application Tracker with Sankey Diagram")

        # Arrange the input fields and button in a single row with multiple columns
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])

        with col1:
            name = st.text_input("Application Name", placeholder="Application Name", label_visibility="collapsed")

        with col2:
            application_url = st.text_input("Application URL (optional)", placeholder="Application URL (optional)",
                                            label_visibility="collapsed")

        with col3:
            date = st.date_input("Date", value=datetime.today(), label_visibility="collapsed")

        with col4:
            stage = st.selectbox("Current Stage", DEFAULT_STAGES, index=0, label_visibility="collapsed")

        with col5:
            if st.button("Add Application"):
                if name.strip():
                    self.add_application(name, application_url, date, stage)
                    st.success("Application added!")
                else:
                    st.error("Please enter a name for the application.")

        # Display tracked job applications if any entries exist
        if not st.session_state["app_data"].empty:
            st.subheader("Tracked Job Applications")
            updated_data = st.session_state["app_data"]

            # Display job applications in rows of 4
            rows = [updated_data.iloc[i:i + 4] for i in range(0, len(updated_data), 4)]
            for row_group in rows:
                cols = st.columns(4)  # Create 4 columns per row
                for i, row in enumerate(row_group.iterrows()):
                    with cols[i]:  # Place each job application in a separate column
                        job_application = JobApplication(row, DEFAULT_STAGES)
                        job_application.render()

            # Render the Sankey diagram if there are entries
            #st.subheader("Application Flow Diagram (Sankey)")
            sankey_diagram = SankeyDiagram(updated_data, DEFAULT_STAGES)
            sankey_diagram.render()


# Main execution
if __name__ == "__main__":
    tracker = JobApplicationTracker()
    tracker.render()
