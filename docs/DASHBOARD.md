# User Dashboard Documentation

This document describes the user dashboard functionality for the Rozoom-KI project.

## Overview

The dashboard allows users to:
- View project progress and details
- Communicate with project managers
- View and pay invoices
- Update their profile information

## Key Features

### Authentication
- User registration and login
- Password reset functionality
- Session management

### Projects Management
- List of user projects with status indicators
- Detailed project view with progress tracking
- Task lists and project updates
- Project milestone tracking

### Messaging System
- Communication with project managers and admins
- Ability to attach files to messages
- Message organization (inbox/sent)
- Project-specific messaging

### Invoicing and Payments
- View invoices for projects
- Download invoice PDFs
- Pay invoices online
- Track payment status

### User Profile
- Update personal information
- Change password
- Manage communication preferences

## Technical Implementation

### Models
- User: Authentication and profile info
- Project: Core project data
- ProjectTask: Individual tasks within a project
- ProjectUpdate: Status updates and milestones
- Message: Communication between users and admins
- MessageAttachment: Files attached to messages
- Invoice: Billing information for projects
- Payment: Payment records for invoices

### Routes
- `/dashboard/`: Main dashboard view
- `/dashboard/profile`: User profile management
- `/dashboard/projects`: Project listing
- `/dashboard/project/<id>`: Individual project details
- `/dashboard/messages`: Messaging center
- `/dashboard/invoices`: Invoice management

### Integration Points
- Project questionnaire submissions are linked to projects
- Admin interface can update project status
- Email notifications for important updates

## Future Enhancements

1. Real-time notifications for project updates
2. Calendar integration for project milestones
3. Document storage for project deliverables
4. Multiple payment method support
5. Project feedback and rating system
