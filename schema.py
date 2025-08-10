from pydantic import BaseModel, Field   
from typing import List

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

