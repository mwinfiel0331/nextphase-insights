from datetime import datetime

COLLECTIONS_CONFIG = {
    'users': {
        'indexes': [
            {
                'fields': [
                    ('user_type', 'ASCENDING'),
                    ('created_at', 'DESCENDING')
                ],
                'queryScope': 'COLLECTION',
                'name': 'users_by_type_and_date'
            }
        ],
        'metadata': {
            'description': 'User profiles and authentication data',
            'created_at': datetime.now()
        }
    },
    'intakes': {
        'indexes': [
            {
                'fields': [
                    ('user_id', 'ASCENDING'),
                    ('created_at', 'DESCENDING')
                ],
                'queryScope': 'COLLECTION',
                'name': 'intakes_by_user_and_date'
            },
            {
                'fields': [
                    ('status', 'ASCENDING'),
                    ('created_at', 'DESCENDING')
                ],
                'queryScope': 'COLLECTION',
                'name': 'intakes_by_status_and_date'
            }
        ],
        'metadata': {
            'description': 'Process intake form submissions',
            'schema': {
                'company_info': {
                    'company_name': 'string',
                    'contact_name': 'string',
                    'industry': 'string',
                    'company_size': 'string',
                    'contact_email': 'string',
                    'contact_role': 'string'
                },
                'process_assessment': {
                    'business_description': 'string',
                    'current_challenges': 'string',
                    'main_pain_point': 'string',
                    'partnership_goals': 'string'
                },
                'tools_assessment': {
                    'tool_selections': 'map'
                },
                'process_details': {
                    'manual_processes': 'number',
                    'hours_per_week': 'number'
                },
                'documentation': {
                    'attachments': 'array'
                },
                'system_fields': {
                    'user_id': 'string',
                    'status': 'string',
                    'created_at': 'timestamp',
                    'updated_at': 'timestamp'
                }
            },
            'statuses': ['DRAFT', 'SUBMITTED', 'IN_REVIEW', 'COMPLETED'],
            'created_at': datetime.now()
        }
    },
    'config': {
        'documents': {
            'industries': {
                'list': [
                    "Technology",
                    "Healthcare",
                    "Finance",
                    "Manufacturing",
                    "Retail",
                    "Education",
                    "Other"
                ],
                'updated_at': datetime.now()
            }
        },
        'metadata': {
            'description': 'System configuration and lookup values',
            'created_at': datetime.now()
        }
    }
}