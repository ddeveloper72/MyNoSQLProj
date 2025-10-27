try:
    from mongoengine import Document, fields
    from datetime import datetime

    # MongoDB Document Models using MongoEngine

    class User(Document):
        """User document for NoSQL database"""
        username = fields.StringField(max_length=50, required=True, unique=True)
        email = fields.EmailField(required=True)
        first_name = fields.StringField(max_length=30)
        last_name = fields.StringField(max_length=30)
        date_joined = fields.DateTimeField(default=datetime.now)
        is_active = fields.BooleanField(default=True)
        
        # MongoDB allows flexible schemas - we can add custom fields
        profile_data = fields.DictField()  # Flexible JSON-like data
        tags = fields.ListField(fields.StringField(max_length=20))  # Array of strings
        
        meta = {
            'collection': 'users',
            'indexes': ['username', 'email']
        }
        
        def __str__(self):
            return f"{self.username} ({self.email})"


    class TaskMetadata(fields.EmbeddedDocument):
        """Embedded document for task metadata"""
        estimated_hours = fields.FloatField(min_value=0)
        actual_hours = fields.FloatField(min_value=0)
        difficulty = fields.StringField(choices=['easy', 'medium', 'hard'])
        category = fields.StringField(max_length=50)
        external_links = fields.ListField(fields.URLField())
        
        def __str__(self):
            return f"Metadata: {self.category} - {self.difficulty}"


    class Milestone(fields.EmbeddedDocument):
        """Embedded document for project milestones"""
        title = fields.StringField(max_length=100, required=True)
        description = fields.StringField()
        target_date = fields.DateTimeField()
        completed = fields.BooleanField(default=False)
        completion_date = fields.DateTimeField()
        
        def __str__(self):
            return f"{self.title} - {'✓' if self.completed else '○'}"


    class Task(Document):
        """Task document demonstrating embedded documents and references"""
        title = fields.StringField(max_length=200, required=True)
        description = fields.StringField()
        created_by = fields.ReferenceField(User, required=True)  # Reference to User
        assigned_to = fields.ListField(fields.ReferenceField(User))  # Multiple users
        
        # Embedded document for task metadata
        metadata = fields.EmbeddedDocumentField(TaskMetadata)
        
        status = fields.StringField(choices=['pending', 'in_progress', 'completed', 'cancelled'], default='pending')
        priority = fields.IntField(min_value=1, max_value=5, default=3)
        
        created_at = fields.DateTimeField(default=datetime.now)
        updated_at = fields.DateTimeField(default=datetime.now)
        due_date = fields.DateTimeField()
        
        # Flexible schema - custom fields
        custom_fields = fields.DictField()
        
        meta = {
            'collection': 'tasks',
            'indexes': ['created_by', 'status', 'created_at']
        }
        
        def save(self, *args, **kwargs):
            self.updated_at = datetime.now()
            return super().save(*args, **kwargs)
        
        def __str__(self):
            return f"{self.title} - {self.status}"


    class Project(Document):
        """Project document with complex nested structures"""
        name = fields.StringField(max_length=100, required=True)
        description = fields.StringField()
        owner = fields.ReferenceField(User, required=True)
        team_members = fields.ListField(fields.ReferenceField(User))
        
        # Nested structure for project settings
        settings = fields.DictField()
        
        # Array of embedded documents
        milestones = fields.ListField(fields.EmbeddedDocumentField(Milestone))
        
        created_at = fields.DateTimeField(default=datetime.now)
        is_active = fields.BooleanField(default=True)
        
        meta = {
            'collection': 'projects',
            'indexes': ['name', 'owner', 'created_at']
        }
        
        def __str__(self):
            return self.name

except ImportError:
    # If mongoengine is not available, create placeholder classes
    print("Warning: mongoengine not available. Creating placeholder models.")
    
    class User:
        pass
    
    class Task:
        pass
    
    class Project:
        pass
    
    class TaskMetadata:
        pass
    
    class Milestone:
        pass
