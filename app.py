import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data (you can replace this with your actual data)
study_years = ["Freshman", "Sophomore", "Junior", "Senior"]
mental_health_stages = ["Low", "Moderate", "High"]

# Define attributes and corresponding questions
attributes = {
    "Attitude": [1, 6],
    "Solitude/Loneliness": [7, 8],
    "Stress or Depression": [2, 3],
    "Participation in Extracurricular Activities": [9, 10],
}

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


def process_mcq_responses(mcq_answers, mcq_questions):
    attribute_scores = {}
    for attribute, questions in attributes.items():
        total_score = 0
        for question_num in questions:
            question = mcq_questions[question_num]["question"]
            answer = mcq_answers.get(question, None)
            # Assuming binary answers (Yes/No)
            if answer == "Yes":
                total_score += 1
        # Normalize score to percentage
        attribute_scores[attribute] = total_score / len(questions) * 100
    return attribute_scores


def process_attribute(attribute, score):
    # Placeholder logic: Assume random scores for demonstration
    ml_model_score = score * 0.75
    counselor_score = score * 0.65
    return ml_model_score, counselor_score


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

    button_label = "Next Question"
    if st.session_state.question_num == len(mcq_questions):
        button_label = "Analyze"

    if st.button(button_label):
        if st.session_state.question_num == len(mcq_questions):
            # All questions answered, process responses
            attribute_scores = process_mcq_responses(mcq_answers, mcq_questions)

            # Compare ML model accuracy with career counselor's assessment
            ml_model_scores = {}
            counselor_scores = {}
            for attribute, score in attribute_scores.items():
                ml_model_score, counselor_score = process_attribute(attribute, score)
                ml_model_scores[attribute] = ml_model_score
                counselor_scores[attribute] = counselor_score

            # Create DataFrames for ML model and counselor scores
            df_ml_model = pd.DataFrame({
                "Attribute": list(ml_model_scores.keys()),
                "Score": list(ml_model_scores.values())
            })
            df_counselor = pd.DataFrame({
                "Attribute": list(counselor_scores.keys()),
                "Score": list(counselor_scores.values())
            })

            # Sort by scores
            df_ml_model = df_ml_model.sort_values(by="Score", ascending=False).head(4)
            df_counselor = df_counselor.sort_values(by="Score", ascending=False).head(4)

            # Plot pie charts for ML model and career counselor
            fig_ml_model = px.pie(df_ml_model, names="Attribute", values="Score", hole=0.5, title="ML Model Analysis")
            fig_counselor = px.pie(df_counselor, names="Attribute", values="Score", hole=0.5, title="Career Counselor Analysis")

            # Display pie charts side by side using column layout
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_ml_model, use_container_width=True)
            with col2:
                st.plotly_chart(fig_counselor, use_container_width=True)

            # Calculate depression risk
            avg_score = (sum(df_ml_model["Score"]) + sum(df_counselor["Score"])) / 8
            if avg_score <= 33:
                risk_color = "green"
                risk_level = "Low Risk"
            elif avg_score <= 66:
                risk_color = "yellow"
                risk_level = "Moderate Risk"
            else:
                risk_color = "red"
                risk_level = "High Risk"

            # Display depression risk line chart
            st.subheader("Depression Risk")
            st.write(f"Average Score: {avg_score:.2f}%")
            st.write(f"Risk Level: {risk_level}")
            st.plotly_chart(px.line(x=[0, 100], y=[avg_score, avg_score], title="Depression Risk", labels={"x": "Percentage", "y": "Risk Level"}, line_shape="spline", color_discrete_sequence=[risk_color]))

        else:
            # Move to the next question
            st.session_state.question_num += 1


if __name__ == "__main__":
    main()
