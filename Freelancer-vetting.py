import re
import PyPDF2
import requests
import io

def extract_text_from_pdf(file_path_or_url):
    text = ""
    if file_path_or_url.startswith('http'):
        response = requests.get(file_path_or_url)
        if response.status_code == 200:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))
        else:
            print(f"Failed to download PDF from {file_path_or_url}")
            return text
    else:
        with open(file_path_or_url, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
        
    return text

def analyze_non_dev_freelancer(text):
    skills = set()
    qualifications = set()
    total_experience_years = 0
    rating = 0
    feedback = []
    
    # Define skill sets for different roles
    writing_skills = ['Copywriting', 'SEO Writing', 'Technical Writing', 'Content Creation']
    design_skills = ['Graphic Design', 'UI/UX Design', 'Adobe Suite']
    marketing_skills = ['SEO', 'SEM', 'Social Media Marketing', 'Email Marketing']
    community_skills = ['Community Moderation', 'Community Management']
    
    # Qualifications
    qualifications_list = ['Bachelor', 'Master', 'PhD', 'Certified', 'Diploma']
    
    for skill in writing_skills + design_skills + marketing_skills + community_skills:
        if re.search(rf'\b{skill}\b', text, re.IGNORECASE):
            skills.add(skill)
            rating += 1
    
    for qual in qualifications_list:
        if re.search(rf'\b{qual}\b', text, re.IGNORECASE):
            qualifications.add(qual)
            rating += 1
            feedback.append(f"Has qualification: {qual}")
    
    # Extract years of experience
    experience_match = re.search(r'(\d+)[+~><]* year', text, re.IGNORECASE)
    if experience_match:
        experience_str = experience_match.group(1)
        if experience_str.isnumeric():
            total_experience_years = int(experience_str)
    
    if total_experience_years >= 5:
        rating += 2
    elif total_experience_years >= 2:
        rating += 1
    
    rating = min(10, rating)
    
    if len(skills) == 0 and total_experience_years < 2:
        recommendation = "Reject application"
        feedback.append("Insufficient skills or experience.")
    elif skills == {'Community Moderation', 'Community Management'}:
        recommendation = "Reject application"
        feedback.append("Community roles need to be backed up with other skills.")
    else:
        recommendation = "Accept into Everbuild talent pool"
    
    return list(skills), list(qualifications), total_experience_years, rating, recommendation, feedback

if __name__ == "__main__":
    file_path_or_url = "https://www.everbuild.pro/wp-content/uploads/wpforms/946-07b67c26f764cc6be3b22e721ea31a5c/Chime-Web3-Resume-59511122123b8cea2a3794914d5392a7.pdf"  # Replace with your PDF file path or URL
    text = extract_text_from_pdf(file_path_or_url)
    
    if text:
        skills, qualifications, total_experience_years, rating, recommendation, feedback = analyze_non_dev_freelancer(text)
        
        print(f"Skills: {skills}")
        print(f"Qualifications: {qualifications}")
        print(f"Total Years of Experience: {total_experience_years}")
        print(f"Rating: {rating}")
        print(f"Recommendation: {recommendation}")
        if feedback:
            print(f"Feedback: {', '.join(feedback)}")
    else:
        print("Failed to extract text from PDF.")
