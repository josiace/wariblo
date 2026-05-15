# Wariblo - Influencer Marketing Platform

Wariblo is a two-sided marketplace platform connecting influencers and advertisers in Africa.

## Features

- **User Authentication**: Role-based registration (Influencer/Advertiser)
- **Influencer Profiles**: Social media metrics, niche, location, rates
- **Advertiser Profiles**: Company information, industry, logo
- **Campaign Management**: Create, edit, delete campaigns with budgets and deadlines
- **Application Workflow**: Influencers apply to campaigns, advertisers accept/reject
- **Messaging System**: Direct communication between users
- **Admin Panel**: Full Django admin integration

## Tech Stack

- **Backend**: Django 4.2.6 (Pure Django, no DRF, no REST API)
- **Frontend**: Django Templates + Bootstrap 5
- **Database**: SQLite (PostgreSQL-ready)
- **Authentication**: Django session-based auth

## Project Structure

```
wariblo/
├── accounts/          # Authentication + custom user model
├── influencers/       # Influencer profiles and dashboard
├── advertisers/       # Advertiser profiles and dashboard
├── campaigns/         # Campaign management
├── applications/     # Application workflow
├── messaging/         # Internal messaging system
├── core/              # Landing page and shared pages
├── static/            # Static files
├── media/             # User uploads
└── templates/         # HTML templates
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wariblo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Frontend: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## User Flows

### Influencer Flow
1. Register as an influencer
2. Complete profile (social metrics, niche, location)
3. Browse available campaigns
4. Apply to campaigns with pitch and proposed price
5. Track application status
6. Communicate with advertisers after acceptance

### Advertiser Flow
1. Register as an advertiser
2. Complete company profile
3. Create campaigns (title, description, budget, requirements)
4. Publish campaigns (change status to 'open')
5. Review applications
6. Accept or reject applications
7. Communicate with influencers

## Database Schema

### Core Models
- **User**: Custom user model with role field (influencer/advertiser/admin)
- **InfluencerProfile**: Social metrics, niche, rates, location
- **AdvertiserProfile**: Company info, industry, logo
- **Campaign**: Title, description, budget, niche, platform, deadline, status
- **Application**: Campaign, influencer, pitch, price, status
- **Conversation**: Participants (many-to-many with User)
- **Message**: Conversation, sender, content, timestamp

## Color System

- Primary: Blue (#1E3A8A)
- Secondary: Green (#10B981)
- Background: White / Light gray (#F9FAFB)
- Text: Dark gray (#111827)

## Production Deployment

For production deployment:

1. Change `DEBUG = False` in settings.py
2. Set up PostgreSQL database
3. Configure static files serving (whitenoise or similar)
4. Set up a production web server (Gunicorn + Nginx)
5. Configure environment variables for sensitive data
6. Set up HTTPS/SSL

## Contributing

This is a production-ready MVP built for the African market. Contributions are welcome.

## License

Proprietary - All rights reserved.
