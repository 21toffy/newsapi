# 9ja News API - Backend

> The single source of truth for Nigerian news 🇳🇬

## Overview

9ja News API is a Django-based REST API that aggregates news from major Nigerian news sources including Vanguard, Punch, and more. It provides a clean, simple interface for developers to access Nigerian news programmatically.

## Features

- 📰 **News Aggregation**: Scrapes and serves news from multiple Nigerian sources
- 🔍 **Search Functionality**: Search across all news sources with keywords
- 📊 **Categorization**: Politics, Business, Entertainment, Technology, Sports, Health
- 🔐 **API Key Authentication**: Secure access with rate limiting
- 📱 **RESTful API**: Clean JSON responses for easy integration
- 🕒 **Real-time Updates**: Fresh news content updated regularly

## Quick Start with Docker

```bash
# Clone the repository
git clone <repository-url>
cd 9janewsapi/newsapi

# Start with Docker Compose
docker-compose up --build

# The API will be available at http://localhost:8000
```

## Manual Setup

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment setup**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Database setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Run the server**
```bash
python manage.py runserver
```

## API Usage

### Authentication
All API requests require an API key. Get yours by registering at the frontend application.

### Base URL
```
https://api.api.9janewsapi.com.ng/api/
```

### Endpoints

#### Get News by Category
```http
GET /api/vanguard/apikey={YOUR_API_KEY}/{category}/
```

**Categories**: `politics`, `business`, `entertainment`, `technology`, `sports`, `health`

**Example**:
```bash
curl "https://api.api.9janewsapi.com.ng/api/vanguard/apikey=your_key_here/politics/"
```

#### Search News
```http
GET /api/search/apikey={YOUR_API_KEY}/{search_term}
```

**Example**:
```bash
curl "https://api.api.9janewsapi.com.ng/api/search/apikey=your_key_here/president%20buhari"
```

### Response Format

```json
{
  "message": "Success!",
  "data": [
    {
      "id": "unique_id",
      "title": "News headline",
      "summary": "Brief description of the news",
      "date": "2024-01-01",
      "photo": "https://image-url.com/image.jpg",
      "link": "https://full-article-url.com"
    }
  ]
}
```

## Rate Limits

- **Free Tier**: 1000 requests per day
- **Contact sales** for higher limits

## Development

### Project Structure
```
newsapi/
├── api/                    # News scraping and API endpoints
├── users/                  # User management and API keys
├── newsapi/               # Django settings and config
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-container setup
└── manage.py             # Django management script
```

### Adding New News Sources

1. Create a new scraper module in `api/`
2. Follow the pattern in `vanguard.py`
3. Add URL patterns in `api/urls.py`
4. Update documentation

### Running Tests
```bash
python manage.py test
```

### Code Style
We use Black for code formatting:
```bash
black .
```

## Deployment

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://localhost:6379/0
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- 📧 Email: support@9janews.com
- 🐛 Issues: [GitHub Issues](link-to-issues)
- 📖 Docs: [Full Documentation](link-to-docs)


# Contribution Guidelines

Thank you for contributing to this project! 🎉  
To keep our codebase clean and consistent, we follow a few simple rules for **commits** and **branch names**.  

---

## 📌 Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

<type>(<scope>): <short description>

[optional body]

[optional footer(s)]


### Common Types
- **feat** – a new feature  
- **fix** – a bug fix  
- **docs** – documentation changes  
- **style** – formatting changes (no code impact)  
- **refactor** – code restructuring without behavior change  
- **test** – adding or updating tests  
- **chore** – maintenance tasks  

### Examples

feat(auth): add Google login support
fix(api): handle null user ID in profile endpoint
docs(readme): update setup instructions


### Rules
1. Use **lowercase** for types and scopes.  
2. Keep the subject line short (≤ 72 characters).  
3. Use the body to explain **why** the change was made, not just **what**.  
4. Reference issues in the footer when relevant:  

Closes #42
 

---

## 🌱 Branch Naming Guidelines

We use a structured format for branch names:

<type>/<short-description>


### Common Types
- **feat/** – for new features  
- **fix/** – for bug fixes  
- **docs/** – for documentation updates  
- **chore/** – for maintenance tasks  
- **refactor/** – for code refactoring  
- **test/** – for adding/updating tests  
- **release/** – for release preparation  

### Rules
1. Use **lowercase** with hyphens (`-`) to separate words.  
2. Keep it short but descriptive.  
3. Match the branch type to the commit type when possible.  

### Examples

feat/add-user-auth
fix/payment-timeout-bug
docs/update-contributing-guide
refactor/api-service-layer
release/v1.2.0


---

## ✅ Summary
- **Branches** describe *what you’re working on*.  
- **Commits** describe *what changed and why*.  
- Following these rules helps everyone understand the project history at a glance.  

---

👉 You can even enforce these rules automatically using tools like **commitlint** and **husky**.  



---

Made with ❤️ for the Nigerian developer community

