# ARCHITECTURE

## Overview

Rozoom-KI is a modern web application built with Python/Flask on the backend and a responsive HTML/CSS/JavaScript frontend. The application serves as both a company website and a platform for delivering AI-enhanced services to clients.

### Core Technologies

- **Backend**: Python 3.10+, Flask 2.3+
- **Database**: SQLite (development), PostgreSQL (production on Render)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla + minimal libraries)
- **Deployment**: Render (web service + PostgreSQL)
- **AI Integration**: OpenAI API, custom model integration

### Application Structure

- **Flask app** with modular blueprints:
  - `pages` - Main website pages (home, about, services, etc.)
  - `blog` - Blog functionality with articles and categories
  - `shop` - E-commerce features with Stripe integration
  - `api` - REST API endpoints for the chat widget and other services
  - `legal` - Legal pages and privacy-related functionality

- **Architecture Layers**:
  - `routes` → `services` → `models` → `repositories`
  - Clear separation of concerns with dependency injection

- **Multilingual Support**:
  - Primary languages: German (DE) and English (EN)
  - Future language: Ukrainian (UA)

## Database Architecture

### Schema Design

To isolate data between projects and subsystems, we use multiple schemas in a single PostgreSQL database on Render:

- `rozoom_ki_schema` - Main application schema (users, translations, settings, etc.)
- `rozoom_ki_clients` - Storage for client requests, specifications, and related metadata
- `rozoom_ki_shop` - Orders, payments, pricing, and related e-commerce/Stripe tables
- `rozoom_ki_projects` - Project-specific artifacts when storing project-specific resources

Schema creation script: `scripts/db/create_schemas.sql`

### Database Configuration

- **Development**: SQLite for simplicity and zero-configuration
- **Production**: PostgreSQL on Render for scalability and advanced features
- **Schema Handling**: Automatic schema handling in app initialization
  - For SQLite: Schema prefixes are automatically removed
  - For PostgreSQL: Search path is configured appropriately

### User and Permission Recommendation

Configure an application role/user (`rozoom_app_user`) with a search path pointing to `rozoom_ki_schema,public` and explicitly specify the schema when working with data from other subsystems.

### Database Models

The primary models in the system include:

1. **User**: End users and administrators
   - Authentication data
   - Profile information
   - Permission settings

2. **Lead**: Prospective clients from contact forms
   - Contact details
   - Message content
   - Tracking information

3. **Order**: Client purchases and subscriptions
   - Package information
   - Payment amounts
   - Stripe session IDs

4. **ChatMessage**: Conversations with AI assistants
   - Message role (system/user/assistant)
   - Content
   - Metadata and context
   - Timestamps

## Chat Widget Architecture

The chat widget is a key feature providing interactive AI assistance to website visitors.

### Overview

Purpose: Embed a lightweight JavaScript frontend widget that communicates with a secure backend API, proxying requests to OpenAI while maintaining context and security.

### Components

#### Frontend Widget
- Lightweight, embeddable JavaScript module
- Supports session context persistence
- Handles message sending and displaying responses
- Provides typing indicators and response streaming
- Responsive design that adapts to all device sizes

#### Backend API
- Endpoint: `/api/chat` 
- Authenticates requests from the website
- Implements rate limiting and request throttling
- Adds context (client options, conversation history)
- Securely communicates with OpenAI API
- Logs conversations and analyzes user needs

#### Multi-Agent Controller
- Server-side component that routes requests between specialized "agents"
- Agent types: SalesAgent, TechAgent, BillingAgent
- Each agent has:
  - Custom prompt templates
  - Local memory/short-term context
  - Specific permissions and capabilities
  - Domain expertise in their area

### Message Flow

1. Client sends message → Backend `/api/chat`
2. Multi-agent controller analyzes intent/metadata and selects appropriate agent(s)
3. OpenAI API (Chat Completion) is called with the agent's prompt+context
4. Response is returned to client and optionally saved to database (`rozoom_ki_clients` / `rozoom_ki_schema`)

### Security and Privacy

- All requests undergo CSRF/Rate-limit checks and origin verification (CORS)
- OpenAI token stored securely in environment variables (not in code)
- User logs and messages have defined retention policies
- PII (Personally Identifiable Information) is masked or encrypted
- Regular security audits and penetration testing

### Technical Challenges

- **Cost Management**: High message volume increases OpenAI API costs
- **Latency**: Requires async processing and streaming responses for good UX
- **Content Moderation**: Content filtering using OpenAI moderation API
- **Context Management**: Maintaining relevant conversation context without token explosion
- **Multi-Language Support**: Ensuring quality responses in German, English, and eventually Ukrainian

## Frontend Architecture

### Design Philosophy

The frontend follows a clean, modern design philosophy prioritizing:
- User experience and accessibility
- Mobile-first responsive design
- Performance optimization
- Minimal JavaScript dependencies

### Component Structure

- **Base Template**: Provides the common structure for all pages
  - Header with navigation
  - Main content area
  - Footer with links
  - Chat widget overlay

- **Page Templates**: Extend the base template with specific content
  - Home page with featured sections
  - Services overview with service cards
  - Contact page with form and map
  - Legal pages with standardized formatting
  - Blog with articles and sidebar

### CSS Architecture

- **Organization**: Modular CSS with component-specific styles
- **Variables**: CSS custom properties for colors, spacing, shadows
- **Responsive**: Mobile-first media queries
- **Performance**: Minimal use of heavy frameworks, focus on vanilla CSS

### JavaScript Architecture

- **Modularity**: Self-contained JS components
- **Progressive Enhancement**: Core functionality works without JS
- **Event Delegation**: Efficient event handling
- **Components**:
  - Form validation
  - Chat widget functionality
  - Flash message handling
  - Lazy loading for images

## API Structure

The API is organized around REST principles with the following endpoints:

### Public API Endpoints

- `GET /api/blog/posts` - Retrieve blog posts (paginated)
- `GET /api/blog/posts/{id}` - Get specific blog post details
- `GET /api/services` - List available services
- `POST /api/contact` - Submit contact form

### Authenticated API Endpoints

- `POST /api/chat` - Send message to chat assistant
- `POST /api/orders` - Create a new order
- `GET /api/orders/{id}` - Get order details
- `POST /api/payments/webhook` - Stripe webhook handler

### API Security

- CSRF protection for all state-changing operations
- Rate limiting to prevent abuse
- Input validation and sanitization
- JWT-based authentication for protected endpoints

## Deployment Architecture

### Development Environment

- Local development with Flask development server
- SQLite database for simplicity
- Environment variables loaded from `.env` file
- Flask debug mode enabled

### Production Environment (Render)

- Gunicorn WSGI server with multiple workers
- PostgreSQL database with multiple schemas
- Environment variables set in Render dashboard
- Static assets served with proper caching headers

### CI/CD Pipeline

- GitHub Actions for automated testing
- Automated deployment to Render on successful merge to main
- Database migrations applied automatically

## Security Considerations

- HTTPS everywhere
- Secure cookie settings
- Content Security Policy (CSP)
- Regular dependency updates
- Proper error handling and logging
- Data encryption at rest and in transit

