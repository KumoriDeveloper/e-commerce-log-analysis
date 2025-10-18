#!/usr/bin/env python3
"""
Пример использования E-Commerce Log Analysis System

Этот скрипт демонстрирует основные возможности системы анализа логов
для e-commerce платформы.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List

# Импортируем основные классы из bot.py
from bot import (
    RealTimeLogAnalyzer, 
    LogEntry, 
    SessionAnalysis,
    LogProcessor,
    IncidentVectorStore,
    EnhancedRAGSystem
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_sample_logs() -> List[LogEntry]:
    """Создает примеры логов для демонстрации"""
    base_time = datetime.now()
    
    logs = [
        # Успешная сессия просмотра товаров
        LogEntry(
            timestamp=base_time,
            session_id="sess_001",
            user_id="user_123",
            event_type="page_view",
            event_data={"page": "/products", "product_id": "prod_456"},
            response_time=0.5
        ),
        LogEntry(
            timestamp=base_time + timedelta(seconds=2),
            session_id="sess_001",
            user_id="user_123",
            event_type="add_to_cart",
            event_data={"product_id": "prod_456", "quantity": 2},
            response_time=0.8
        ),
        
        # Проблемная сессия с ошибками
        LogEntry(
            timestamp=base_time + timedelta(minutes=1),
            session_id="sess_002",
            user_id="user_789",
            event_type="checkout",
            event_data={"step": "payment", "amount": 150.0},
            error_code="PAYMENT_TIMEOUT",
            response_time=8.5
        ),
        LogEntry(
            timestamp=base_time + timedelta(minutes=1, seconds=10),
            session_id="sess_002",
            user_id="user_789",
            event_type="error",
            event_data={"error": "Payment gateway timeout", "retry_count": 1},
            error_code="API_TIMEOUT",
            response_time=10.2
        ),
        LogEntry(
            timestamp=base_time + timedelta(minutes=1, seconds=20),
            session_id="sess_002",
            user_id="user_789",
            event_type="error",
            event_data={"error": "Database connection failed"},
            error_code="DB_CONNECTION_ERROR",
            response_time=12.1
        ),
        
        # Сессия с медленными запросами
        LogEntry(
            timestamp=base_time + timedelta(minutes=2),
            session_id="sess_003",
            user_id="user_456",
            event_type="search",
            event_data={"query": "laptop", "filters": {"price_range": "500-1000"}},
            response_time=3.2
        ),
        LogEntry(
            timestamp=base_time + timedelta(minutes=2, seconds=5),
            session_id="sess_003",
            user_id="user_456",
            event_type="search",
            event_data={"query": "gaming laptop", "filters": {"brand": "ASUS"}},
            response_time=4.8
        ),
        LogEntry(
            timestamp=base_time + timedelta(minutes=2, seconds=10),
            session_id="sess_003",
            user_id="user_456",
            event_type="search",
            event_data={"query": "gaming laptop", "filters": {"brand": "MSI"}},
            response_time=6.1
        ),
    ]
    
    return logs

async def demonstrate_log_processing():
    """Демонстрация обработки логов"""
    logger.info("=== Демонстрация обработки логов ===")
    
    # Создаем процессор логов
    processor = LogProcessor()
    
    # Получаем примеры логов
    all_logs = create_sample_logs()
    
    # Группируем логи по сессиям
    sessions = {}
    for log in all_logs:
        if log.session_id not in sessions:
            sessions[log.session_id] = []
        sessions[log.session_id].append(log)
    
    # Анализируем каждую сессию
    for session_id, session_logs in sessions.items():
        logger.info(f"\n--- Анализ сессии {session_id} ---")
        
        # Обнаруживаем узкие места
        bottlenecks = processor.detect_bottlenecks(session_logs)
        
        if bottlenecks:
            logger.info(f"Обнаружены узкие места: {bottlenecks}")
        else:
            logger.info("Узких мест не обнаружено")
        
        # Показываем статистику сессии
        errors = [log for log in session_logs if log.error_code]
        response_times = [log.response_time for log in session_logs if log.response_time]
        
        logger.info(f"Количество событий: {len(session_logs)}")
        logger.info(f"Количество ошибок: {len(errors)}")
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            logger.info(f"Среднее время ответа: {avg_response:.2f} сек")

async def demonstrate_rag_system():
    """Демонстрация RAG-системы (требует OpenAI API ключ)"""
    logger.info("\n=== Демонстрация RAG-системы ===")
    
    # Проверяем наличие API ключа
    try:
        from config import OPENAI_API_KEY
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
            logger.warning("OpenAI API ключ не настроен. Пропускаем демонстрацию RAG-системы.")
            return
    except ImportError:
        logger.warning("Файл config.py не найден. Создайте его на основе config.py.example")
        return
    
    # Инициализируем RAG-систему
    vector_store = IncidentVectorStore()
    rag_system = EnhancedRAGSystem(OPENAI_API_KEY, vector_store)
    
    # Создаем описание инцидента
    incident_description = """
    Пользователь пытается совершить покупку на сумму $150, но процесс оплаты 
    завершается с ошибкой таймаута. Повторные попытки также не удаются. 
    Время ответа платежного шлюза превышает 8 секунд.
    """
    
    try:
        # Получаем embedding для поиска похожих случаев
        logger.info("Получение векторного представления инцидента...")
        embedding = await rag_system.get_embedding(incident_description)
        logger.info(f"Размерность embedding: {len(embedding)}")
        
        # Ищем похожие инциденты
        logger.info("Поиск похожих инцидентов...")
        similar_cases = await vector_store.semantic_search(embedding)
        logger.info(f"Найдено похожих случаев: {len(similar_cases)}")
        
        # Генерируем решение
        if similar_cases:
            logger.info("Генерация решения на основе найденных случаев...")
            solution = await rag_system.generate_solution(incident_description, similar_cases)
            logger.info(f"Предложенное решение:\n{solution}")
        else:
            logger.info("Похожих случаев не найдено. Генерация базового решения...")
            solution = await rag_system._generate_initial_solution(incident_description)
            logger.info(f"Базовое решение:\n{solution}")
            
    except Exception as e:
        logger.error(f"Ошибка при работе с RAG-системой: {e}")

async def demonstrate_full_analysis():
    """Демонстрация полного анализа с метриками"""
    logger.info("\n=== Демонстрация полного анализа ===")
    
    # Инициализируем анализатор (без реального API ключа для демо)
    analyzer = RealTimeLogAnalyzer(openai_api_key="demo-key")
    
    # Получаем примеры логов
    all_logs = create_sample_logs()
    
    # Группируем по сессиям
    sessions = {}
    for log in all_logs:
        if log.session_id not in sessions:
            sessions[log.session_id] = []
        sessions[log.session_id].append(log)
    
    # Обрабатываем каждую сессию
    for session_id, session_logs in sessions.items():
        logger.info(f"\n--- Обработка сессии {session_id} ---")
        
        try:
            result = await analyzer.process_session_logs(session_logs)
            
            if result:
                logger.info("🚨 ИНЦИДЕНТ ОБНАРУЖЕН!")
                logger.info(f"Описание: {result.get('incident_description', 'N/A')}")
                logger.info(f"Узкие места: {result.get('bottlenecks', [])}")
                logger.info(f"Найдено похожих случаев: {result.get('similar_cases_found', 0)}")
            else:
                logger.info("✅ Сессия обработана без инцидентов")
                
        except Exception as e:
            logger.error(f"Ошибка при обработке сессии {session_id}: {e}")
    
    # Получаем отчет о производительности
    report = analyzer.get_performance_report()
    logger.info("\n📊 ОТЧЕТ О ПРОИЗВОДИТЕЛЬНОСТИ:")
    logger.info(json.dumps(report, indent=2, ensure_ascii=False))

async def main():
    """Главная функция демонстрации"""
    logger.info("🚀 Запуск демонстрации E-Commerce Log Analysis System")
    logger.info("=" * 60)
    
    try:
        # Демонстрация обработки логов
        await demonstrate_log_processing()
        
        # Демонстрация RAG-системы
        await demonstrate_rag_system()
        
        # Демонстрация полного анализа
        await demonstrate_full_analysis()
        
        logger.info("\n✅ Демонстрация завершена успешно!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка во время демонстрации: {e}")
        raise

if __name__ == "__main__":
    # Запуск демонстрации
    asyncio.run(main())
