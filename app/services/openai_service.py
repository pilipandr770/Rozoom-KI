import os
import openai
import logging
import requests
import time
from flask import current_app
from datetime import datetime
from typing import Tuple, Dict, List, Optional

# Настройка логирования
logger = logging.getLogger(__name__)

class OpenAIService:
    """
    Сервисный класс для работы с OpenAI API
    """
    
    def __init__(self, api_key=None):
        """
        Инициализация сервиса с API ключом
        """
        self.api_key = api_key or current_app.config.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is not set")
        
        openai.api_key = self.api_key
    
    def generate_blog_content(self, topic: str, keywords: str, language: str) -> Dict:
        """
        Генерирует заголовок и содержание блога на основе темы и ключевых слов
        
        Args:
            topic (str): Основная тема блога
            keywords (str): Ключевые слова для SEO
            language (str): Язык генерации ('en' или 'de')
            
        Returns:
            Dict: Словарь с заголовком, содержанием и метаописанием
        """
        try:
            lang_prompt = "English" if language == "en" else "German"
            
            system_prompt = f"""
            You are a professional blog writer for a tech company focusing on AI solutions. 
            Write a well-structured, informative blog post in {lang_prompt}.
            The content should be engaging, include real-world examples, and be SEO optimized.
            Format the content with proper Markdown headings, paragraphs, bullet points, and highlight key concepts.
            Include a compelling title that would attract clicks.
            Include a meta description for SEO purposes (150-160 characters).
            """
            
            user_prompt = f"""
            Write a comprehensive blog post about: {topic}
            
            Use these keywords for SEO optimization (include them naturally): {keywords}
            
            The blog post should:
            1. Have a catchy, SEO-friendly title
            2. Include an introduction that engages the reader
            3. Have 3-5 main sections with headings
            4. Include practical examples or case studies
            5. End with a conclusion and call-to-action
            6. Be between 800-1200 words
            
            Respond with a JSON object with the following structure:
            {{
                "title": "Your generated title here",
                "content": "The full blog post content in Markdown",
                "meta_description": "SEO-optimized meta description"
            }}
            """
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo-1106",  # Используем модель с поддержкой JSON
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # Получаем содержимое ответа
            content = response.choices[0].message.content
            
            # Если ответ в формате JSON строки, парсим его
            import json
            blog_data = json.loads(content)
            
            return blog_data
            
        except Exception as e:
            logger.error(f"Error generating blog content: {str(e)}")
            raise
    
    def generate_image(self, prompt: str) -> Optional[str]:
        """
        Генерирует изображение на основе промпта с использованием DALL-E
        
        Args:
            prompt (str): Описание для генерации изображения
            
        Returns:
            Optional[str]: URL сгенерированного изображения или None при ошибке
        """
        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            # Получаем URL изображения
            image_url = response.data[0].url
            
            return image_url
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return None
    
    def create_image_prompt(self, blog_title: str, topic: str) -> str:
        """
        Создает детальный промпт для генерации изображения на основе заголовка и темы блога
        
        Args:
            blog_title (str): Заголовок блога
            topic (str): Основная тема блога
            
        Returns:
            str: Промпт для генерации изображения
        """
        try:
            system_prompt = """
            You are an expert at creating detailed image generation prompts for DALL-E.
            Your task is to create a detailed, descriptive prompt that will result in a professional, 
            visually appealing image relevant to a blog post.
            The prompt should describe a realistic, photographic style image that would work well as a blog header.
            Focus on creating prompts that will generate clean, professional images without text elements.
            """
            
            user_prompt = f"""
            Create a detailed image generation prompt for a blog post with the title: "{blog_title}"
            
            The blog is about: {topic}
            
            The image should be:
            - Professional and suitable for a business blog
            - Visually appealing and attention-grabbing
            - Related to the topic but abstract enough to be versatile
            - Without any text elements
            - Suitable as a header image for the blog post
            
            Provide only the image prompt text, nothing else.
            """
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Получаем содержимое ответа
            prompt = response.choices[0].message.content
            
            # Ограничиваем длину промпта
            if len(prompt) > 1000:
                prompt = prompt[:997] + "..."
                
            return prompt
            
        except Exception as e:
            logger.error(f"Error creating image prompt: {str(e)}")
            return f"Professional blog header image related to {topic}"  # Fallback prompt
