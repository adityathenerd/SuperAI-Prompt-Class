from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# gets API Key from environment variable OPENAI_API_KEY
openrouter_client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPEN_ROUTER_KEY")
)

def openrouter_completion(model_name, user_query, system_message=None):
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": user_query})
    completion = openrouter_client.chat.completions.create(
        model=model_name,
        messages=messages
    )
    return completion.choices[0].message.content


def router(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": """You are a helpful router designed to output JSON. You decide which route user input belongs to based on the type of the user query.
            Return your response as follows:
            {
            "route": "route_name", which can be one of the following:
            - "chatbot-ai/converse-pro" for Chatbots and Virtual Assistants, Conversation
            - "mentalcare-ai/empathetic-companion" for Mental health
            - "image-ai/picasso-gen" for Image Generation
            - "video-ai/motion-maestro" for Video Generation
            - "audio-ai/melody-maker" for Music Creation, Speech Generation
            - "content-ai/podcast-genius" for Podcast Content Creation, Podcasts
            - "writing-ai/wordsmith-pro" for Blog Writing, Storytelling and Narrative Creation, Social Media Posts
            - "seo-ai/rankbooster" for SEO Optimization
            - "analysis-ai/market-insight" for Market Analysis
            - "translate-ai/polyglot-pro" for Translation
            - "code-ai/dev-assistant" for Coding and Programming Assistance, API Integration
            - "data-ai/insight-extractor" for Data Analysis
            - "finance-ai/report-wizard" for Financial Report Generation
            - "edu-ai/knowledge-crafter" for Educational Content Creation, Language Learning Assistance
            - "present-ai/slide-master" for Presentation Creation
            - "comm-ai/email-composer" for Email Generation
            - "legal-ai/document-drafter" for Legal Document Drafting, Contract Generation
            - "culinary-ai/recipe-innovator" for Recipe Generation
            - "health-ai/wellness-planner" for Fitness and Health Plans Recommendations
            - "study-ai/homework-helper" for Homework Solutions
            - "detect-ai/authenticity-checker" for AI content detection
            - "design-ai/brand-architect" for Branding and Logo Design
            - "travel-ai/journey-planner" for Travel Itinerary Creation
            - "event-ai/occasion-orchestrator" for Event Planning
            - "product-ai/description-craft" for Product Descriptions
            - "recommend-ai/personal-curator" for Personalized Recommendations
            - "career-ai/resume-crafter" for Resume and Cover Letter Writing, Job Description Creation
            - "research-ai/paper-assistant" for Research Paper Data
            - "summary-ai/concise-pro" for Summarisations, Content Summarization
            - "news-ai/article-generator" for News Article Generation
            - "generic-ai/multi-purpose" for Others or tasks that don't fit the above categories
            }"""},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

while True:
    user_input = input("Please enter your question (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    model = router(user_input)
    model = json.loads(model)
    model = model["route"]
    print(f"routing to {model}")
