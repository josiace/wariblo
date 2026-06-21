# Wariblo - Influencer Marketing Platform

Wariblo is a two-sided marketplace platform connecting influencers and advertisers in Africa.

## Features

### Core Features
- **User Authentication**: Role-based registration (Influencer/Advertiser)
- **Influencer Profiles**: Social media metrics, niche, location, rates
- **Advertiser Profiles**: Company information, industry, logo
- **Campaign Management**: Create, edit, delete campaigns with budgets and deadlines
- **Application Workflow**: Influencers apply to campaigns, advertisers accept/reject
- **Messaging System**: Direct communication between users
- **Admin Panel**: Full Django admin integration

### Advanced Features (v3.0)
- **REST API**: Full REST API with Django REST Framework
- **Security**: Rate limiting with django-axes, HSTS, SSL configuration
- **Monitoring**: Error tracking with Sentry
- **Performance**: Database indexes, WhiteNoise for static files
- **Async Tasks**: Celery for background tasks (emails, notifications)
- **Advanced Search**: Search by keywords, niche, platform, budget with sorting options
- **Analytics Dashboard**: Campaign analytics with views, clicks, conversion rates, ROI
- **Statistics Charts**: Interactive charts (Chart.js) for campaign and application statistics
- **Sidebar Navigation**: Modern sidebar menu for dashboard navigation
- **Review System**: Multi-category reviews (communication, professionalism, quality, timeliness)
- **Notification System**: Real-time notification badges and alerts
- **Skeleton Loaders**: Loading states for better UX
- **Breadcrumbs**: Navigation breadcrumbs for better orientation
- **Platform Badges**: Visual badges for Instagram, TikTok, YouTube, Twitter, Facebook
- **Popularity Indicators**: Visual indicators showing campaign popularity
- **Currency System**: Dynamic currency conversion based on user location
- **Country Selection**: 54 African countries with phone codes and flags

## Tech Stack

- **Backend**: Django 4.2.6
- **API**: Django REST Framework 3.14.0
- **Frontend**: Django Templates + Custom CSS (No Bootstrap)
- **Charts**: Chart.js 4.4.0
- **Database**: SQLite (PostgreSQL-ready)
- **Authentication**: Django session-based auth + Token auth for API
- **Security**: django-axes (rate limiting), HSTS, SSL
- **Monitoring**: Sentry (error tracking)
- **Async Tasks**: Celery + Redis
- **Static Files**: WhiteNoise (compression)

## Project Structure

```
wariblo/
├── accounts/          # Authentication + custom user model
├── influencers/       # Influencer profiles and dashboard
├── advertisers/       # Advertiser profiles and dashboard
├── campaigns/         # Campaign management
├── applications/     # Application workflow
├── messaging/         # Internal messaging system
├── core/              # Landing page, currency, countries, async tasks
├── reviews/           # Review and rating system
├── analytics/         # Campaign analytics and user activity tracking
├── api/               # REST API endpoints
├── static/            # Static files (CSS custom)
│   └── css/
│       └── main.css   # Custom CSS with flame color theme
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

5. **Load countries and currencies**
   ```bash
   python manage.py load_countries
   python manage.py load_currencies
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Frontend: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## User Flows

### Influencer Flow
1. Register as an influencer
2. Select country and phone number
3. Complete profile (social metrics, niche, location)
4. Browse available campaigns with advanced search and filters
5. Apply to campaigns with pitch and proposed price
6. Track application status with statistics
7. Communicate with advertisers after acceptance
8. Leave reviews for completed campaigns

### Advertiser Flow
1. Register as an advertiser
2. Select country and phone number
3. Complete company profile
4. Create campaigns (title, description, budget, requirements)
5. Publish campaigns (change status to 'open')
6. Review applications with analytics
7. Accept or reject applications
8. Communicate with influencers
9. Track campaign performance with analytics
10. Leave reviews for influencers

## Database Schema

### Core Models
- **User**: Custom user model with role field (influencer/advertiser/admin), phone number, country
- **Country**: ISO code, name, phone code, flag emoji (54 African countries)
- **Currency**: ISO code, symbol, exchange rate to USD
- **InfluencerProfile**: Social metrics, niche, rates, location, profile image
- **AdvertiserProfile**: Company info, industry, logo
- **Campaign**: Title, description, budget, niche, platform, deadline, status
- **Application**: Campaign, influencer, pitch, price, status
- **Conversation**: Participants (many-to-many with User)
- **Message**: Conversation, sender, content, timestamp
- **Review**: Multi-category reviews with ratings, helpful votes, verification
- **CampaignAnalytics**: Views, clicks, shares, conversion rate, ROI, engagement rate
- **UserActivity**: Activity tracking (view, click, apply, share, message, review)

## Color System (Flame Theme)

- Primary: Orange Red Flame (#E63900)
- Secondary: Gold Yellow (#FFC107)
- Accent: Deep Pink (#C71585)
- Background: Light Rose (#FFF5F0)
- Text: Black (#000000)
- Status colors: Pending (Yellow), Accepted (Green), Rejected (Red), Draft (Gray)

## Production Deployment

For production deployment:

1. Change `DEBUG = False` in settings.py
2. Set up PostgreSQL database
3. Configure static files serving (whitenoise or similar)
4. Set up a production web server (Gunicorn + Nginx)
5. Configure environment variables for sensitive data
6. Set up HTTPS/SSL
7. Run `python manage.py load_countries` and `python manage.py load_currencies`

## Contributing

This is a production-ready MVP built for the African market with modern UX/UI and advanced features. Contributions are welcome.

## License

Proprietary - All rights reserved.
