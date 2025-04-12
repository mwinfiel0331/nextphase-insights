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
                # Form sections
                'company_info': {
                    'company_name': 'string',
                    'industry': 'string',
                    'team_size': 'number',
                    'timeline': 'string'
                },
                'process_details': {
                    'process_name': 'string',
                    'process_description': 'string',
                    'current_challenges': 'string',
                    'desired_outcomes': 'string'
                },
                'documentation': {
                    'attachments': 'array',
                    'additional_notes': 'string'
                },
                # System fields
                'user_id': 'string',
                'status': 'string',
                'created_at': 'timestamp',
                'updated_at': 'timestamp',
                'submitted_at': 'timestamp'
            },
            'statuses': [
                'DRAFT',
                'SUBMITTED',
                'IN_REVIEW',
                'COMPLETED',
                'ARCHIVED'
            ],
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