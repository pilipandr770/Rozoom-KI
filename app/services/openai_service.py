import os
import openai
import logging
import requests
import time
from flask import current_app
from datetime import datetime
from typing import Tuple, Dict, List, Optional
from openai import APIError, APIConnectionError, RateLimitError, AuthenticationError

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
            raise ValueError("OpenAI API key is not set. Please set OPENAI_API_KEY environment variable.")
        
        # Логируем информацию о ключе (без самого ключа)
        logger.info(f"OpenAI API key configured: {'Yes' if self.api_key else 'No'}")
        logger.info(f"OpenAI API key length: {len(self.api_key) if self.api_key else 0}")
        logger.info(f"OpenAI API key starts with: {self.api_key[:10] if self.api_key else 'None'}...")
        
        openai.api_key = self.api_key
    
    def test_connection(self) -> tuple[bool, str]:
        """
        Тестирует подключение к OpenAI API с детальной диагностикой
        
        Returns:
            tuple: (успех, сообщение с деталями)
        """
        try:
            logger.info("Testing OpenAI API connection with detailed diagnostics...")
            
            # Проверяем конфигурацию
            if not self.api_key:
                return False, "API ключ не настроен"
            
            if not self.api_key.startswith('sk-'):
                return False, "API ключ имеет неправильный формат"
            
            logger.info(f"API key format: OK (length: {len(self.api_key)})")
            
            # Проверяем базовое подключение
            logger.info("Testing basic connectivity to OpenAI API...")
            
            # Простой тестовый запрос - получение списка моделей
            response = openai.models.list()
            
            if response.data:
                model_count = len(response.data)
                logger.info(f"OpenAI API connection successful. Available models: {model_count}")
                return True, f"Подключение успешно. Доступно моделей: {model_count}"
            else:
                logger.warning("OpenAI API connection test returned empty response")
                return False, "API вернул пустой ответ"
                
        except APIConnectionError as e:
            error_msg = f"Ошибка сетевого подключения: {str(e)}"
            logger.error(f"OpenAI API connection error: {error_msg}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details'}")
            return False, error_msg
        except AuthenticationError as e:
            error_msg = f"Ошибка аутентификации: {str(e)}"
            logger.error(f"OpenAI API authentication error: {error_msg}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details'}")
            return False, error_msg
        except RateLimitError as e:
            error_msg = f"Превышен лимит запросов: {str(e)}"
            logger.error(f"OpenAI API rate limit error: {error_msg}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details'}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            logger.error(f"Unexpected error testing OpenAI connection: {error_msg}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details'}")
            return False, error_msg
    
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
            logger.info(f"Starting blog content generation for topic: {topic}, language: {language}")
            
            # Тестируем подключение перед генерацией
            connection_ok, connection_message = self.test_connection()
            if not connection_ok:
                raise Exception(f"Failed to connect to OpenAI API: {connection_message}")
            
            lang_prompt = "English" if language == "en" else "German"
            
            system_prompt = f"""
            You are a professional blog writer for a tech company focusing on AI solutions. 
            Write a well-structured, informative blog post in {lang_prompt}.
            The content should be engaging, include real-world examples, and be SEO optimized.
            Format the content with proper Markdown headings, paragraphs, bullet points, and highlight key concepts.
            DO NOT use any icons, Font Awesome, or HTML elements like <i class="fa..."></i> in your content.
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
            7. IMPORTANT: DO NOT use any Font Awesome icons or HTML tags for icons (like <i class="fa..."></i>)
            8. DO NOT include any icons next to headings, titles, or author names
            
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
                response_format={"type": "json_object"},
                timeout=60  # Добавляем таймаут 60 секунд
            )
            
            # Получаем содержимое ответа
            content = response.choices[0].message.content
            
            # Если ответ в формате JSON строки, парсим его
            import json
            blog_data = json.loads(content)
            
            return blog_data
            
        except APIConnectionError as e:
            logger.error(f"OpenAI API connection error: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details'}")
            raise Exception("Ошибка подключения к OpenAI API")
        except AuthenticationError as e:
            logger.error(f"OpenAI API authentication error: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details'}")
            raise Exception("Ошибка аутентификации OpenAI API")
        except RateLimitError as e:
            logger.error(f"OpenAI API rate limit error: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details'}")
            raise Exception("Превышен лимит запросов к OpenAI API")
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details'}")
            raise Exception(f"Ошибка API OpenAI: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating blog content: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details'}")
            raise Exception(f"Ошибка генерации содержимого блога: {str(e)}")
    
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
            
        except APIConnectionError as e:
            logger.error(f"OpenAI connection error during image generation: {str(e)}")
            return None
        except RateLimitError as e:
            logger.error(f"OpenAI rate limit error during image generation: {str(e)}")
            return None
        except AuthenticationError as e:
            logger.error(f"OpenAI authentication error during image generation: {str(e)}")
            return None
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
