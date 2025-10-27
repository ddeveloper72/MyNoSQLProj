"# MyNoSQLProj - Django MongoDB Integration

A Django project demonstrating NoSQL database integration using MongoDB Atlas and MongoEngine ODM.

## 🚀 Features

- **MongoDB Integration**: Full MongoDB Atlas connectivity using MongoEngine ODM
- **Document-Based Models**: Flexible schema design with embedded documents and references
- **RESTful API**: JSON API endpoints for data operations
- **Real-time Analytics**: Aggregation and reporting capabilities
- **Interactive Web Interface**: Built-in web interface for testing and documentation

## 📋 Prerequisites

- Python 3.8+
- MongoDB Atlas account (or local MongoDB instance)
- Git

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ddeveloper72/MyNoSQLProj.git
   cd MyNoSQLProj
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   # source .venv/bin/activate    # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/
   MONGODB_DB_NAME=task_manager
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   Open http://localhost:8000 in your browser

## 🏗️ Project Structure

```
MyNoSQLProj/
├── djangonosql/           # Main Django app
│   ├── models.py         # MongoDB document models
│   ├── views.py          # API views and endpoints
│   ├── urls.py           # URL routing
│   └── templates/        # HTML templates
├── MyNoSQLProj/          # Django project settings
│   ├── settings.py       # Configuration
│   └── urls.py           # Main URL configuration
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in git)
└── README.md            # This file
```

## 📊 MongoDB Document Models

### User Document
```python
{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2025-10-27T18:30:00Z",
  "is_active": true,
  "profile_data": {"department": "Engineering", "level": "Senior"},
  "tags": ["developer", "full-stack"]
}
```

### Task Document with Embedded Metadata
```python
{
  "title": "Implement user authentication",
  "description": "Add OAuth2 authentication system",
  "created_by": ObjectId("..."),
  "assigned_to": [ObjectId("...")],
  "status": "in_progress",
  "priority": 4,
  "metadata": {
    "estimated_hours": 8.0,
    "difficulty": "medium",
    "category": "backend"
  },
  "custom_fields": {"client": "Internal", "sprint": "Sprint-23"}
}
```

### Project Document with Milestones
```python
{
  "name": "E-commerce Platform",
  "description": "Complete online shopping solution",
  "owner": ObjectId("..."),
  "team_members": [ObjectId("...")],
  "settings": {"notifications": true, "public": false},
  "milestones": [
    {
      "title": "MVP Release",
      "target_date": "2025-12-01T00:00:00Z",
      "completed": false
    }
  ]
}
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with documentation |
| `/api/users/` | GET | List users with optional search |
| `/api/users/` | POST | Create new user |
| `/api/tasks/` | GET | List tasks with filtering |
| `/api/analytics/` | GET | Project analytics and statistics |
| `/api/test-connection/` | GET | Test MongoDB connection |

### Example API Usage

**Create a user:**
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_doe",
    "email": "jane@example.com",
    "first_name": "Jane",
    "tags": ["designer", "ui-ux"]
  }'
```

**Search users:**
```bash
curl "http://localhost:8000/api/users/?search=jane"
```

**Filter tasks:**
```bash
curl "http://localhost:8000/api/tasks/?status=in_progress&priority=4"
```

## 🎯 NoSQL Features Demonstrated

- **Document Storage**: Flexible, schema-less document structure
- **Embedded Documents**: Nested objects within documents (TaskMetadata, Milestones)
- **References**: Relationships between documents using ObjectId references
- **Arrays**: Lists of values and references (tags, team_members, assigned_to)
- **Dynamic Fields**: Custom fields with DictField for evolving schemas
- **Indexing**: Database indexes for optimized query performance
- **Aggregation**: Complex data analysis and reporting
- **Text Search**: Multi-field search capabilities

## 🔧 Development

**Running tests:**
```bash
python manage.py test
```

**Database operations:**
- No migrations needed - MongoDB is schema-less
- Data is created dynamically as documents are saved
- Use the `/api/test-connection/` endpoint to create sample data

**Environment Setup:**
```bash
# Quick start script
bash run_server.sh
```

## 📦 Dependencies

- **Django 5.2.7**: Web framework
- **mongoengine 0.29.1**: MongoDB ODM for Django
- **pymongo 4.15.3**: MongoDB driver
- **python-dotenv 1.2.1**: Environment variable management
- **dnspython 2.8.0**: DNS resolver for MongoDB Atlas

## 🔒 Security Notes

- Environment variables are used for sensitive configuration
- `.env` file is excluded from version control
- Default secret key is only used as fallback for development
- MongoDB connection strings contain credentials and should be secured

## 🚀 Deployment

For production deployment:

1. Set secure environment variables
2. Use a production WSGI server (gunicorn, uwsgi)
3. Configure proper logging and monitoring
4. Set `DEBUG=False` in production
5. Use MongoDB Atlas with proper network security

## 📖 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [MongoEngine Documentation](http://mongoengine.org/)
- [MongoDB Atlas](https://www.mongodb.com/atlas)
- [MongoDB University](https://university.mongodb.com/)

## 📄 License

This project is for educational purposes and demonstration of Django-MongoDB integration.

---

**Author**: ddeveloper72  
**Created**: October 27, 2025  
**Technologies**: Django, MongoDB, MongoEngine, Python" 
