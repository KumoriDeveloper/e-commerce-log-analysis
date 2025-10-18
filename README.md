# E-Commerce Log Analysis System

Система анализа логов e-commerce платформы с использованием RAG (Retrieval-Augmented Generation) и машинного обучения для автоматического обнаружения и решения инцидентов.

## 🚀 Возможности

- **Анализ логов в реальном времени** - обработка пользовательских сессий и выявление проблем
- **Обнаружение узких мест** - автоматическое выявление медленных запросов и ошибок
- **RAG-система** - поиск похожих инцидентов и генерация решений на основе исторических данных
- **Векторный поиск** - семантический поиск решений с использованием Elasticsearch
- **Метрики производительности** - отслеживание эффективности системы и снижения жалоб
- **Redis кэширование** - быстрый доступ к метрикам и данным

## 📋 Требования

- Python 3.8+
- Redis
- Elasticsearch
- OpenAI API ключ

## 🛠 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/e-commerce-log-analysis.git
cd e-commerce-log-analysis
```


2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения:
```bash
cp config.py.example config.py
# Отредактируйте config.py с вашими настройками
```

4. Запустите Redis и Elasticsearch:
```bash
# Redis
redis-server

# Elasticsearch
elasticsearch
```

## 🔧 Конфигурация

Создайте файл `config.py` на основе `config.py.example`:

```python
# OpenAI API ключ
OPENAI_API_KEY = "your-openai-api-key"

# Redis настройки
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Elasticsearch настройки
ELASTICSEARCH_HOST = "localhost:9200"
```

## 📖 Использование

### Базовое использование

```python
import asyncio
from bot import RealTimeLogAnalyzer, LogEntry
from datetime import datetime

async def main():
    # Инициализация анализатора
    analyzer = RealTimeLogAnalyzer(openai_api_key="your-api-key")
    
    # Создание тестовых логов
    logs = [
        LogEntry(
            timestamp=datetime.now(),
            session_id="sess_123",
            user_id="user_456",
            event_type="checkout",
            event_data={"step": "payment", "amount": 100.0},
            error_code="PAYMENT_TIMEOUT",
            response_time=8.5
        )
    ]
    
    # Обработка логов
    result = await analyzer.process_session_logs(logs)
    
    if result:
        print("Инцидент обнаружен и обработан!")
        print(f"Решение: {result['solution']}")

asyncio.run(main())
```

### Запуск примера

```bash
python example.py
```

## 🏗 Архитектура

### Основные компоненты

- **LogProcessor** - обработка и анализ логов
- **IncidentVectorStore** - хранение инцидентов в Elasticsearch
- **EnhancedRAGSystem** - RAG-система с OpenAI
- **RealTimeLogAnalyzer** - основной анализатор

### Поток данных

1. Логи поступают в систему
2. LogProcessor анализирует сессию и выявляет проблемы
3. RAG-система ищет похожие инциденты
4. Генерируется решение на основе найденных случаев
5. Результат сохраняется в векторном хранилище
6. Метрики обновляются в Redis

## 📊 Метрики

Система отслеживает следующие метрики:

- Количество обработанных сессий
- Количество обнаруженных инцидентов
- Количество сгенерированных решений
- Снижение жалоб клиентов (до 25% за 6 месяцев)

## 🔍 Обнаружение проблем

Система автоматически обнаруживает:

- **Медленные запросы** - время ответа > 2 секунд
- **Повторяющиеся ошибки** - одинаковые ошибки в сессии
- **Паттерны ошибок** - timeout, database, payment, auth, API
- **Узкие места** - множественные медленные запросы

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Поддержка

Если у вас есть вопросы или предложения, создайте [Issue](https://github.com/yourusername/e-commerce-log-analysis/issues) в репозитории.

## 🚀 Roadmap

- [ ] Веб-интерфейс для мониторинга
- [ ] Интеграция с популярными системами логирования
- [ ] Машинное обучение для улучшения предсказаний
- [ ] API для внешних систем
- [ ] Docker контейнеризация
