


# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data (you can replace this with your actual data)
study_years = ["Freshman", "Sophomore", "Junior", "Senior"]
mental_health_stages = ["Low", "Moderate", "High"]

# Function to process MCQ responses (replace with your logic)
def process_mcq_responses(mcq_answers):
    # Placeholder logic: Assume random scores for demonstration
    ml_model_score = 0.75
    counselor_score = 0.65
    return ml_model_score, counselor_score
# Sample questions and options
def get_sample_questions():
    questions = {
        1: {
            "question": "What type of area do you come from?",
            "options": ["Rural", "Urban"]
        },
        2: {
            "question": "How many income members are there in your family?",
            "options": ["Less than 3", "3-5", "More than 5"]
        },
        3: {
            "question": "Did you or your family take any loans for your graduation?",
            "options": ["Yes", "No"]
        },
        4: {
            "question": "What is the highest level of education attained by your parents?",
            "options": ["High school", "Bachelor's degree", "Master's degree or higher"]
        },
        5: {
            "question": "What is the primary source of financial support for your education?",
            "options": ["Scholarships", "Family income", "Part-time job"]
        },
        6: {
            "question": "How has your living situation influenced your college experience?",
            "options": ["Positively", "Neutral", "Negatively"]
        },
        7: {
            "question": "Are there any cultural or societal expectations impacting your education choices?",
            "options": ["Yes", "No"]
        },
        8: {
            "question": "Have you faced any challenges related to your background that affected your academic performance?",
            "options": ["Yes", "No"]
        },
        9: {
            "question": "How far is your hometown from your college or university?",
            "options": ["Less than 50 miles", "50-100 miles", "More than 100 miles"]
        },
        10: {
            "question": "Did you receive any financial aid or grants for your education?",
            "options": ["Yes", "No"]
        }
    }
    return questions


def main():
    st.title("Mental Health Assessment Tool")

    # Dropdown menu for study years
    study_year = st.selectbox("Select Study Year", study_years)

    # Sample MCQs
    mcq_questions = get_sample_questions()

    # Initialize session state for question number
    if "question_num" not in st.session_state:
        st.session_state.question_num = 1

    # Display current question and collect answer
    current_question = mcq_questions[st.session_state.question_num]
    mcq_answers = {}
    mcq_answers[current_question["question"]] = st.radio(current_question["question"], current_question["options"])

    if st.button("Next Question"):
        # Move to the next question
        st.session_state.question_num += 1

    if st.session_state.question_num > len(mcq_questions):
        # All questions answered, process responses
        ml_score, counselor_score = process_mcq_responses(mcq_answers)

        # Display results (same as before)
        st.subheader("Results:")
        st.write(f"Machine Learning Model Score: {ml_score:.2f}")
        st.write(f"Career Counselor Score: {counselor_score:.2f}")

        # Create pie charts
        df = pd.DataFrame({
            "Method": ["ML Model", "Career Counselor"],
            "Score": [ml_score, counselor_score]
        })
        fig = px.pie(df, names="Method", values="Score", hole=0.5)
        st.plotly_chart(fig)

        # Display mental health stage
        mental_health_stage = mental_health_stages[int((ml_score + counselor_score) / 2 * 2)]
        st.write(f"Mental Health Stage: {mental_health_stage}")

if __name__ == "__main__":
    main()
