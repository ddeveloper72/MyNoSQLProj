from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from mongoengine import Q
from .models import User, Task, Project, TaskMetadata, Milestone
from datetime import datetime, timedelta
import json

class UserListView(View):
    """Demonstrate MongoDB user operations"""
    
    def get(self, request):
        """Get all users or search by query parameters"""
        try:
            # Get query parameters
            search = request.GET.get('search', '')
            
            if search:
                # MongoDB text search capabilities
                users = User.objects(
                    Q(username__icontains=search) | 
                    Q(email__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search)
                )
            else:
                users = User.objects.all()
            
            # Convert to JSON-serializable format
            users_data = []
            for user in users:
                users_data.append({
                    'id': str(user.id),
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'date_joined': user.date_joined.isoformat() if user.date_joined else None,
                    'is_active': user.is_active,
                    'profile_data': user.profile_data,
                    'tags': user.tags
                })
            
            return JsonResponse({
                'status': 'success',
                'users': users_data,
                'count': len(users_data)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    def post(self, request):
        """Create a new user"""
        try:
            data = json.loads(request.body)
            
            user = User(
                username=data['username'],
                email=data['email'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                profile_data=data.get('profile_data', {}),
                tags=data.get('tags', [])
            )
            user.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'User created successfully',
                'user_id': str(user.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)


class TaskListView(View):
    """Demonstrate MongoDB task operations with complex queries"""
    
    def get(self, request):
        """Get tasks with filtering and aggregation"""
        try:
            # Query parameters
            status = request.GET.get('status')
            priority = request.GET.get('priority')
            user_id = request.GET.get('assigned_to')
            
            # Build query
            query = Q()
            if status:
                query &= Q(status=status)
            if priority:
                query &= Q(priority=int(priority))
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    query &= Q(assigned_to=user)
                except User.DoesNotExist:
                    pass
            
            tasks = Task.objects(query).order_by('-created_at')
            
            # Convert to JSON
            tasks_data = []
            for task in tasks:
                task_data = {
                    'id': str(task.id),
                    'title': task.title,
                    'description': task.description,
                    'status': task.status,
                    'priority': task.priority,
                    'created_at': task.created_at.isoformat() if task.created_at else None,
                    'updated_at': task.updated_at.isoformat() if task.updated_at else None,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                    'created_by': {
                        'id': str(task.created_by.id),
                        'username': task.created_by.username
                    } if task.created_by else None,
                    'assigned_to': [
                        {'id': str(user.id), 'username': user.username} 
                        for user in task.assigned_to
                    ],
                    'custom_fields': task.custom_fields
                }
                
                # Include metadata if present
                if task.metadata:
                    task_data['metadata'] = {
                        'estimated_hours': task.metadata.estimated_hours,
                        'actual_hours': task.metadata.actual_hours,
                        'difficulty': task.metadata.difficulty,
                        'category': task.metadata.category,
                        'external_links': task.metadata.external_links
                    }
                
                tasks_data.append(task_data)
            
            return JsonResponse({
                'status': 'success',
                'tasks': tasks_data,
                'count': len(tasks_data)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)


class ProjectAnalyticsView(View):
    """Demonstrate MongoDB aggregation and analytics"""
    
    def get(self, request):
        """Get project analytics using MongoDB aggregation"""
        try:
            # Get basic counts
            total_users = User.objects.count()
            total_tasks = Task.objects.count()
            total_projects = Project.objects.count()
            
            # Task status distribution
            task_statuses = {}
            for status in ['pending', 'in_progress', 'completed', 'cancelled']:
                task_statuses[status] = Task.objects(status=status).count()
            
            # Tasks by priority
            task_priorities = {}
            for priority in range(1, 6):
                task_priorities[f'priority_{priority}'] = Task.objects(priority=priority).count()
            
            # Recent tasks (last 7 days)
            week_ago = datetime.now() - timedelta(days=7)
            recent_tasks = Task.objects(created_at__gte=week_ago).count()
            
            # Users with most tasks
            user_task_counts = []
            for user in User.objects.only('username', 'email'):
                task_count = Task.objects(created_by=user).count()
                if task_count > 0:
                    user_task_counts.append({
                        'username': user.username,
                        'email': user.email,
                        'task_count': task_count
                    })
            
            # Sort by task count
            user_task_counts.sort(key=lambda x: x['task_count'], reverse=True)
            
            return JsonResponse({
                'status': 'success',
                'analytics': {
                    'totals': {
                        'users': total_users,
                        'tasks': total_tasks,
                        'projects': total_projects
                    },
                    'task_status_distribution': task_statuses,
                    'task_priority_distribution': task_priorities,
                    'recent_tasks_count': recent_tasks,
                    'top_users_by_tasks': user_task_counts[:10]
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)


def mongodb_connection_test(request):
    """Test MongoDB connection and create sample data"""
    try:
        # Test connection by creating a sample user
        test_user = User(
            username='test_user_' + str(datetime.now().timestamp()),
            email=f'test_{datetime.now().timestamp()}@example.com',
            first_name='Test',
            last_name='User',
            profile_data={'test': True, 'created_by': 'connection_test'},
            tags=['test', 'sample']
        )
        test_user.save()
        
        # Create a sample task
        test_task = Task(
            title='Sample Task',
            description='This is a test task created to verify MongoDB connection',
            created_by=test_user,
            assigned_to=[test_user],
            metadata=TaskMetadata(
                estimated_hours=2.5,
                difficulty='easy',
                category='testing'
            ),
            custom_fields={'test': True, 'environment': 'development'}
        )
        test_task.save()
        
        # Create a sample project
        test_project = Project(
            name='Sample Project',
            description='A test project to verify MongoDB functionality',
            owner=test_user,
            team_members=[test_user],
            settings={'test_mode': True, 'notifications': False},
            milestones=[
                Milestone(
                    title='Setup Complete',
                    description='MongoDB setup and testing completed',
                    target_date=datetime.now() + timedelta(days=1),
                    completed=True,
                    completion_date=datetime.now()
                )
            ]
        )
        test_project.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'MongoDB connection successful! Sample data created.',
            'data': {
                'user_id': str(test_user.id),
                'task_id': str(test_task.id),
                'project_id': str(test_project.id),
                'database': 'nosql_project_db'
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'MongoDB connection failed: {str(e)}'
        }, status=500)


def index(request):
    """Home page with API documentation"""
    context = {
        'title': 'Django NoSQL Project',
        'description': 'A Django project demonstrating MongoDB integration with MongoEngine',
        'endpoints': [
            {'url': '/api/users/', 'method': 'GET', 'description': 'List users with optional search'},
            {'url': '/api/users/', 'method': 'POST', 'description': 'Create new user'},
            {'url': '/api/tasks/', 'method': 'GET', 'description': 'List tasks with filtering'},
            {'url': '/api/analytics/', 'method': 'GET', 'description': 'Get project analytics'},
            {'url': '/api/test-connection/', 'method': 'GET', 'description': 'Test MongoDB connection'},
        ]
    }
    return render(request, 'djangonosql/index.html', context)
