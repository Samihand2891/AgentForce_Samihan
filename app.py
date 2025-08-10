import streamlit as st
import torch
import json
from transformers import pipeline
from pydantic import BaseModel, Field, ValidationError
from typing import List
import os
from dotenv import load_dotenv

class SemesterPlan(BaseModel):
    semester_number: int = Field(description="The sequential number of the semester (e.g., 1, 2, 3)")
    courses: List[str] = Field(description="A list of 3-4 recommended university courses for this semester (e.g., 'Foundation of Machine Learning')")
    certifications: List[str] = Field(description="A list of 3-4 recommended certifications for this semester(e.g., 'Coursera , edx , Udemy ')")
    project_idea: List[str] = Field(description="A detailed hands on project ideas to improve the resume and applies semester (e.g., 'Building a AI assistant')")

class GithubRepoPlan(BaseModel):
    readme_content: str = Field(description="A complete well-formatted markdown template for a README.md file,It should include a title, description, features, and tech stack sections")
    starter_issues: List[str] = Field(description="A list of 3-5 starter GitHub issues titles for the repo,(e.g., 'Setup project structure', 'Implement core algorithm')")
    project_plan: str = Field(description="A detailed project plan for the repo")
    project_structure: str = Field(description="A detailed project structure for the repo")
    project_roadmap: str = Field(description="A detailed project roadmap for the repo")
    project_milestones: List[str] = Field(description="A list of 3-5 project milestones for the repo")
    project_tasks: List[str] = Field(description="A list of 3-5 project tasks for the repo")
    project_files: List[str] = Field(description="A list of 3-5 project files for the repo")
    project_tests: List[str] = Field(description="A list of 3-5 project tests for the repo")
    project_docs: List[str] = Field(description="A list of 3-5 project docs for the repo")

class AcademicPlan(BaseModel):
    full_plan: List[SemesterPlan] = Field(description="A list of semester plans, typically for 4 to 8 semesters")
    github_plan: GithubRepoPlan = Field(description="A plan for initial Github project")

@st.cache_resource
def load_planner_pipeline():
    try:
        planner_pipeline = pipeline(
            "text-generation",
            model="google/gemma-2b-it",
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
            token=st.secrets["HF_TOKEN"]
        )
        return planner_pipeline
    except Exception as e:
        st.error(f"Failed to load the AI Model. Please ensure you have a Hugging Face token set. Error: {e}")
        return None

def generate_academic_plan(user_goal: str, pipeline_instance):
    if pipeline_instance is None:
        return None
    
    json_schema = AcademicPlan.model_json_schema()
    prompt = f"""<start_of_turn>user
You are an expert academic and career advisor for university students in tech. A student has the following goal: "{user_goal}".
Generate a detailed, semester-by-semester academic plan to help them achieve this goal.
The output MUST be a JSON object that strictly conforms to the following JSON Schema. Do not include any text, explanations, or markdown formatting outside of the JSON object itself.

JSON Schema:
{json.dumps(json_schema, indent=2)}<end_of_turn>
<start_of_turn>model
"""
    
    try:
        outputs = pipeline_instance(
            prompt,
            max_new_tokens=3072,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )
        response_text = outputs["generated_text"]
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON object found in model's response")
        
        json_string = response_text[json_start:json_end]
        parsed_output = AcademicPlan.model_validate_json(json_string)
        return parsed_output
    except (json.JSONDecodeError, ValidationError, ValueError) as e:
        st.error(f"Error parsing the AI's response. Details: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during AI generation: {e}")
        return None

# Streamlit app code
st.set_page_config(layout="wide", page_title="Academic Planner AI")
planner_pipeline = load_planner_pipeline()

if 'plan' not in st.session_state:
    st.session_state.plan = None

st.title("🎓 Academic Planner AI")
st.markdown("Enter your goals and let AI craft your personalized learning journey!")
st.sidebar.header("Your Profile")
career_goal = st.sidebar.text_area(
    "What is your ultimate career goal?",
    "Example: Become a top-tier Machine Learning Engineer at a FAANG company specializing in Natural Language Processing.",
    height=150
)
current_year = st.sidebar.selectbox(
    "What is your current age?",
    ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
)
interests = st.sidebar.multiselect(
    "What are your technical interests?",
    ["AI/ML", "Embedded Systems", "Cloud Computing", "Cybersecurity", "IoT", "Web Development"],
    default=["AI/ML", "IoT"]
)

if st.button("😊Generate your career plan", type="primary", use_container_width=True):
    if career_goal and planner_pipeline:
        full_goal_description = f"As a {current_year} with interests in {','.join(interests)}, my goal is to {career_goal}."
        with st.spinner("🤖 AI is crafting your plan... This may take a moment."):
            st.session_state.plan = generate_academic_plan(full_goal_description, planner_pipeline)
    else:
        if not career_goal:
            st.error("Please enter your career goal first.")
        if not planner_pipeline:
            st.error("The AI model is not available. Please check the configuration.")

if st.session_state.plan is not None:
    st.success("Your personalized academic plan is ready!")
    plan_data = st.session_state.plan
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Your Semester Roadmap")
        for semester in plan_data.full_plan:
            with st.expander(f"Semester {semester.semester_number}"):
                st.subheader("📚 Recommended Courses")
                for course in semester.courses:
                    st.markdown(f"- {course}")
                st.subheader("📜 Recommended Certifications")
                for cert in semester.certifications:
                    st.markdown(f"- {cert}")
                st.subheader("💡 Project Ideas")
                for project in semester.project_idea:
                    st.markdown(f"- {project}")
    
    with col2:
        st.header("Github Starter Kit")
        st.subheader("📄 README.md Template")
        st.code(plan_data.github_plan.readme_content, language="markdown")
        st.subheader("✅ Starter Issues")
        for issue in plan_data.github_plan.starter_issues:
            st.markdown(f"- [ ] {issue}") 
            