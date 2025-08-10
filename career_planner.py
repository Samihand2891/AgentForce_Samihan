import streamlit as st
st.set_page_config(layout="wide")
st.title("🎓 Academic Planner AI " )
st.markdown("Enter your goals and let AI decide your journey!")
st.sidebar.header("Your profile")
career_goal= st.sidebar.text_area ("What is your intended career goal ?"                                                           
"EX:A Scientist , physicists or even a data scienist"
)
current_year=st.sidebar.selectbox("What is your current year of study?")
interests = st.sidebar.multiselect(
    "What are your key technical interests?",
    ["AI/ML", "Embedded Systems", "Cloud Computing", "Cybersecurity", "IoT", "Web Development"],
    default=["AI/ML", "IoT"]  # optional defaults
)
if st.button("😊Generate your career plan"):
    with st.spinner("🤖Evaluating your career path... This may take a moment"):
        pass 
else: 
    st.error("Please enter your career goal first")

if 'plan' in st.session_state and st.session_state.plan is not None:
    st.success("Your personalized academic plan is ready!")
    plan_data = st.session_state.plan
    st.header("Your semester to semester roadmap")
    for semester in plan_data.full_plan:
        with st.expander(f"### Semester {semester.semester_number}: {semester.theme}"):
            st.subheader("📚Your semester courses")
            for course in semester.courses:
                st.markdown(f"- {course}")
            st.subheader("Certifications you should do📃")
            for cert in semester.certifications:
                st.markdown(f"- {cert}")
            st.subheader("💡Project Idea")
            st.markdown(semester.project_idea)

    st.header("Your Project: Github starter kit")
    st.subheader("📃ReadMe.md Templates")
    st.code(plan_data.github_plan.readme_content, language="markdown") 
    st.subheader("✅Starter issues")
    for issue in plan_data.github_plan.starter_issues:
        st.markdown(f"- [ ] {issue}")






