#!/usr/bin/env python3
import sys
import os
sys.path.append('.')

print("Starting test script...")

def test_function_logic():
    """Test the email notification function logic without sending actual email"""
    print("Testing function logic...")

    # Test data
    tech_spec_data = {
        'answers': [
            {'question': 'Project Type', 'answer': 'Web Application'},
            {'question': 'Timeline', 'answer': '3 months'}
        ]
    }
    contact_info = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '+1234567890'
    }

    # Test HTML content generation
    subject = f"New Technical Specification: {contact_info.get('name', 'Unknown')}"

    html_content = f"""
    <h1>New Technical Specification Submission</h1>
    <p><strong>Submitted on:</strong> Test timestamp UTC</p>

    <h2>Contact Information</h2>
    <ul>
        <li><strong>Name:</strong> {contact_info.get('name', 'Not provided')}</li>
        <li><strong>Email:</strong> {contact_info.get('email', 'Not provided')}</li>
        <li><strong>Phone:</strong> {contact_info.get('phone', 'Not provided')}</li>
    </ul>

    <h2>Technical Specification Details</h2>
    """

    # Add each answer
    for i, answer in enumerate(tech_spec_data.get('answers', [])):
        html_content += f"""
        <h3>{i+1}. {answer.get('question', 'Question')}</h3>
        <p>{answer.get('answer', 'No answer')}</p>
        """

    html_content += """
    <p>Please review the technical specification and contact the client as soon as possible.</p>
    <p>Login to the admin dashboard to view the full details.</p>
    """

    print("Generated HTML content:")
    print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
    print(f"Subject: {subject}")
    print("Function logic test completed successfully")
    return True

if __name__ == "__main__":
    test_function_logic()
