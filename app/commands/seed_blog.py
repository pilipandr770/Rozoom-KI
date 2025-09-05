import click
from flask.cli import with_appcontext
from app import db
from app.models import User, BlogPost, BlogCategory, BlogTag
from datetime import datetime, timedelta
import random

@click.command('seed-blog')
@with_appcontext
def seed_blog_command():
    """Seed the database with sample blog data."""
    seed_blog()
    click.echo('Seeded blog with sample data.')

def seed_blog():
    """Add sample blog data to the database."""
    # Create test user if it doesn't exist
    user = User.query.filter_by(email='admin@rozoom-ki.com').first()
    if not user:
        user = User(email='admin@rozoom-ki.com', name='Admin User')
        db.session.add(user)
        db.session.commit()
    
    # Create categories
    categories = [
        ('Web Development', 'web-development', 'Articles about web development and design'),
        ('AI & Machine Learning', 'ai-machine-learning', 'Insights into AI and machine learning technologies'),
        ('Business & Technology', 'business-technology', 'Where business meets technology'),
        ('Product Updates', 'product-updates', 'Latest updates on our products and services')
    ]
    
    category_objects = []
    for name, slug, description in categories:
        category = BlogCategory.query.filter_by(slug=slug).first()
        if not category:
            category = BlogCategory(name=name, slug=slug, description=description)
            db.session.add(category)
            category_objects.append(category)
    
    db.session.commit()
    
    # If no categories were added, load existing ones
    if not category_objects:
        category_objects = BlogCategory.query.all()
    
    # Create tags
    tags = [
        ('Python', 'python'),
        ('JavaScript', 'javascript'),
        ('Flask', 'flask'),
        ('React', 'react'),
        ('AI', 'ai'),
        ('Machine Learning', 'machine-learning'),
        ('Web Design', 'web-design'),
        ('Business', 'business'),
        ('Startups', 'startups'),
        ('Technology', 'technology'),
        ('Cloud', 'cloud'),
        ('Security', 'security')
    ]
    
    tag_objects = []
    for name, slug in tags:
        tag = BlogTag.query.filter_by(slug=slug).first()
        if not tag:
            tag = BlogTag(name=name, slug=slug)
            db.session.add(tag)
            tag_objects.append(tag)
    
    db.session.commit()
    
    # If no tags were added, load existing ones
    if not tag_objects:
        tag_objects = BlogTag.query.all()
    
    # Create blog posts
    posts = [
        {
            'title': 'How AI is Transforming Web Development',
            'slug': 'how-ai-is-transforming-web-development',
            'content': '<p>Artificial Intelligence (AI) is revolutionizing the web development industry in unprecedented ways. From automating repetitive tasks to enhancing user experiences through personalization, AI technologies are becoming an essential part of modern web development workflows.</p><h2>Automating Repetitive Tasks</h2><p>One of the most significant benefits of AI in web development is automation. Developers can now use AI-powered tools to generate code, test applications, and identify bugs more efficiently than ever before. This automation saves valuable time and resources, allowing developers to focus on more creative and complex aspects of their projects.</p><p>For example, AI code completion tools can suggest code snippets based on context, helping developers write code faster and with fewer errors. Similarly, AI-powered testing tools can automatically generate test cases and identify potential issues before they reach production.</p><h2>Personalized User Experiences</h2><p>AI is also transforming how websites interact with users. By analyzing user behavior and preferences, AI algorithms can deliver personalized content, product recommendations, and experiences tailored to individual users.</p><p>This level of personalization was once a luxury reserved for tech giants with massive data teams. Now, even small businesses can implement AI-driven personalization through accessible tools and platforms.</p><h2>Chatbots and Conversational Interfaces</h2><p>AI-powered chatbots have evolved from simple rule-based systems to sophisticated conversational agents capable of understanding natural language and context. These intelligent assistants can handle customer inquiries, provide support, and even guide users through complex processes on websites.</p><p>As natural language processing continues to advance, we can expect chatbots to become even more integral to web experiences, providing seamless and human-like interactions.</p><h2>Design and Creativity</h2><p>Contrary to fears that AI might replace creative roles, AI tools are actually enhancing the creative process for designers and developers. AI-powered design tools can generate layout suggestions, color palettes, and even entire design concepts based on specific parameters and brand guidelines.</p><p>These tools don\'t replace human creativity but rather augment it by providing inspiration and handling tedious aspects of the design process.</p><h2>The Future of Web Development</h2><p>As AI continues to evolve, we can expect even deeper integration into web development workflows. From predictive analytics that anticipate user needs to advanced accessibility features that make the web more inclusive, AI will continue to push the boundaries of what\'s possible in web development.</p><p>For web developers and businesses alike, embracing AI technologies isn\'t just about staying current—it\'s about unlocking new possibilities and creating more intelligent, responsive, and user-centered web experiences.</p>',
            'excerpt': 'Discover how artificial intelligence is revolutionizing web development processes, from automated coding to personalized user experiences, and how developers are leveraging AI to create smarter websites.',
            'image_url': '/static/img/blog/ai-web-dev.jpg',
            'category': 'AI & Machine Learning',
            'tags': ['AI', 'Web Design', 'Technology']
        },
        {
            'title': 'Building Scalable Applications with Flask',
            'slug': 'building-scalable-applications-with-flask',
            'content': '<p>Flask\'s simplicity and flexibility make it an excellent choice for building scalable web applications. While it\'s often categorized as a microframework, Flask is capable of powering complex, high-traffic applications when properly structured and optimized.</p><h2>Modular Architecture with Blueprints</h2><p>One of Flask\'s most powerful features for scalability is Blueprints. These allow you to organize your application into discrete components, each with its own views, templates, and static files. This modular approach makes it easier to maintain and scale your codebase as your application grows.</p><p>For example, you might have separate blueprints for user authentication, admin interfaces, and public-facing features. This separation of concerns keeps your code organized and makes it easier for teams to work on different parts of the application simultaneously.</p><h2>Database Optimization</h2><p>As your Flask application scales, database performance becomes increasingly important. Here are some strategies to optimize database interactions:</p><ul><li>Use SQLAlchemy\'s lazy loading judiciously to prevent N+1 query problems</li><li>Implement database connection pooling to efficiently manage database connections</li><li>Consider using read replicas for read-heavy workloads</li><li>Implement proper indexing based on your query patterns</li></ul><h2>Caching Strategies</h2><p>Implementing effective caching is crucial for scalable applications. Flask integrates well with various caching solutions:</p><p>Flask-Caching provides a simple way to cache views, functions, or specific parts of your templates. For more advanced caching, you might consider Redis as a caching backend, which allows for distributed caching across multiple servers.</p><p>When implementing caching, focus on identifying the most expensive operations in your application and caching their results when possible.</p><h2>Asynchronous Processing</h2><p>For long-running tasks or operations that don\'t need to complete within the request-response cycle, implement asynchronous processing using tools like Celery or Redis Queue.</p><p>This approach prevents requests from blocking while waiting for time-consuming tasks to complete, improving the responsiveness of your application even under heavy load.</p><h2>Deployment Considerations</h2><p>As your Flask application scales, you\'ll need to move beyond the built-in development server to more robust deployment options:</p><ul><li>Use Gunicorn or uWSGI as WSGI servers</li><li>Implement load balancing across multiple application instances</li><li>Consider containerization with Docker for consistent deployment environments</li><li>Utilize orchestration tools like Kubernetes for managing containerized applications at scale</li></ul><h2>Monitoring and Performance Tuning</h2><p>Implement comprehensive monitoring to identify bottlenecks and opportunities for optimization. Tools like Prometheus, Grafana, and Flask-MonitoringDashboard can provide valuable insights into your application\'s performance.</p><p>Regularly profile your application to identify slow functions or queries that might be affecting overall performance.</p><h2>Conclusion</h2><p>With the right architecture and optimization strategies, Flask can scale to handle significant traffic and complex application requirements. The key is to leverage Flask\'s flexibility while implementing best practices for performance and maintainability.</p><p>By focusing on modular design, efficient database usage, effective caching, and proper deployment configurations, you can build Flask applications that grow seamlessly with your user base and business needs.</p>',
            'excerpt': 'Learn practical strategies for building highly scalable web applications using Flask, including blueprint organization, database optimization, caching techniques, and deployment best practices.',
            'image_url': '/static/img/blog/flask-scaling.jpg',
            'category': 'Web Development',
            'tags': ['Python', 'Flask', 'Web Design']
        },
        {
            'title': 'The Business Case for AI Integration',
            'slug': 'the-business-case-for-ai-integration',
            'content': '<p>As artificial intelligence technologies mature, businesses across industries are facing a critical decision: when and how to integrate AI into their operations and offerings. This article explores the compelling business case for AI adoption and provides a framework for evaluating AI opportunities.</p><h2>Beyond the Hype: Real Business Value</h2><p>While AI has generated significant hype, its business value is increasingly tangible and measurable. According to McKinsey, AI could potentially deliver additional global economic output of $13 trillion by 2030, boosting GDP by about 1.2 percent annually.</p><p>The most successful AI implementations focus not on technology for its own sake but on solving specific business problems and creating measurable value through:</p><ul><li>Revenue growth through enhanced products, services, and customer experiences</li><li>Cost reduction through automation and operational efficiency</li><li>Improved decision-making with data-driven insights</li><li>Risk mitigation through predictive analytics and enhanced security</li></ul><h2>Customer Experience Enhancement</h2><p>AI offers unprecedented opportunities to personalize and enhance customer experiences. From recommendation engines that increase customer engagement to conversational AI that provides 24/7 support, businesses are using AI to meet rising customer expectations.</p><p>For example, a retail business might implement AI to analyze customer browsing behavior and purchase history to deliver targeted product recommendations, increasing average order values and customer satisfaction simultaneously.</p><h2>Operational Efficiency</h2><p>AI excels at automating routine, repetitive tasks, allowing employees to focus on higher-value activities. Machine learning algorithms can optimize supply chains, manage inventory, schedule maintenance, and streamline administrative processes.</p><p>Manufacturing companies are using AI for predictive maintenance, reducing downtime by up to 50% and increasing equipment life by years. Similarly, financial institutions are automating document processing and compliance checks, reducing processing times from days to minutes.</p><h2>Data-Driven Decision Making</h2><p>Perhaps AI\'s most transformative business impact is its ability to extract actionable insights from vast amounts of data. AI can identify patterns and trends that would be impossible for humans to detect, enabling more informed strategic decisions.</p><p>Healthcare organizations are using predictive analytics to anticipate patient needs and optimize resource allocation. Retailers are leveraging AI to forecast demand with unprecedented accuracy, reducing waste and stockouts.</p><h2>Building Your AI Business Case</h2><p>When evaluating potential AI initiatives, consider this framework:</p><ol><li><strong>Problem identification:</strong> Start with a clear business problem rather than a desire to use AI.</li><li><strong>Value quantification:</strong> Estimate the financial impact of solving the problem.</li><li><strong>Data assessment:</strong> Evaluate whether you have the necessary data in terms of quality, quantity, and accessibility.</li><li><strong>Implementation approach:</strong> Determine whether to build custom solutions, use pre-built APIs, or implement AI platforms.</li><li><strong>Risk evaluation:</strong> Consider ethical implications, regulatory requirements, and change management needs.</li></ol><h2>Starting Small and Scaling</h2><p>Successful AI adoption typically follows an iterative approach. Begin with pilot projects that address well-defined problems and can demonstrate quick wins. Use these initial successes to build organizational confidence and knowledge before tackling more complex implementations.</p><p>As your AI initiatives mature, focus on creating a cohesive AI strategy that aligns with your broader business objectives rather than implementing disconnected point solutions.</p><h2>Conclusion</h2><p>The business case for AI is increasingly compelling across industries. By focusing on specific business problems, quantifying potential value, and taking an iterative approach to implementation, organizations can realize significant competitive advantages through AI integration.</p><p>The question is no longer whether AI will transform your industry, but how quickly you\'ll adapt to the new competitive landscape it creates.</p>',
            'excerpt': 'Explore how businesses are leveraging artificial intelligence to drive revenue growth, enhance operational efficiency, and gain competitive advantages in today's rapidly evolving market.',
            'image_url': '/static/img/blog/business-ai.jpg',
            'category': 'Business & Technology',
            'tags': ['AI', 'Business', 'Technology']
        },
        {
            'title': 'Introducing Our New Chat Widget',
            'slug': 'introducing-our-new-chat-widget',
            'content': '<p>We\'re excited to announce the launch of our new AI-powered chat widget, designed to enhance customer support and provide instant assistance to website visitors. This new feature represents our commitment to leveraging cutting-edge technology to improve user experience.</p><h2>Intelligent Assistance at Your Fingertips</h2><p>Our new chat widget uses advanced natural language processing to understand and respond to customer inquiries in real-time. Unlike traditional chatbots that rely on rigid decision trees, our solution can interpret complex questions, understand context, and provide relevant, helpful responses.</p><p>The widget can answer questions about our services, provide product recommendations, troubleshoot common issues, and even help users navigate our website more effectively.</p><h2>Key Features</h2><h3>Multi-Agent Intelligence</h3><p>The chat widget is powered by a multi-agent system that routes conversations to specialized AI agents based on the topic. Whether you need technical support, billing information, or sales assistance, your conversation will be handled by the most appropriate agent with the right expertise.</p><h3>Context-Aware Conversations</h3><p>Our chat widget maintains conversation context, allowing for natural back-and-forth exchanges without requiring users to repeat information. This creates a more human-like interaction experience and saves time for our customers.</p><h3>Seamless Human Handoff</h3><p>While our AI can handle most inquiries, there are times when human expertise is needed. The chat widget can seamlessly transfer conversations to our customer support team when necessary, along with the full conversation history to ensure continuity.</p><h3>Multilingual Support</h3><p>To better serve our global customer base, the chat widget supports multiple languages, including English, German, and soon Ukrainian. Users can communicate in their preferred language and receive responses in kind.</p><h3>Mobile-Optimized Interface</h3><p>The widget is designed to work flawlessly across devices, with special attention paid to the mobile experience. The interface adjusts automatically to screen size, ensuring convenient access whether you\'re on a desktop, tablet, or smartphone.</p><h2>Privacy and Security</h2><p>We\'ve built the chat widget with privacy and security as top priorities. All conversations are encrypted, and we\'ve implemented strict data retention policies. Users have the option to request deletion of their conversation history at any time.</p><p>Additionally, the widget is GDPR compliant and only collects information necessary to provide assistance.</p><h2>Continuous Improvement</h2><p>Our chat widget uses machine learning to continuously improve its responses based on user interactions. As more customers use the feature, it becomes increasingly effective at resolving inquiries quickly and accurately.</p><p>We regularly review conversation analytics to identify areas where the widget can be improved, ensuring it provides maximum value to our users.</p><h2>Try It Today</h2><p>Our new chat widget is live on all pages of our website. Look for the chat icon in the bottom right corner of your screen to start a conversation and experience the benefits of intelligent, instant support.</p><p>We welcome your feedback on this new feature as we continue to refine and enhance it in the coming months.</p>',
            'excerpt': 'We're excited to announce our new AI-powered chat widget, designed to provide instant, intelligent support to all website visitors through natural language understanding and specialized virtual agents.',
            'image_url': '/static/img/blog/chat-widget.jpg',
            'category': 'Product Updates',
            'tags': ['AI', 'Technology', 'Product Updates']
        },
        {
            'title': 'Securing Your Web Applications: Best Practices',
            'slug': 'securing-your-web-applications-best-practices',
            'content': '<p>Web application security is more critical than ever as businesses increasingly rely on web-based solutions for essential operations. With cyber threats constantly evolving, protecting your applications requires a comprehensive, proactive approach.</p><h2>Understanding the Threat Landscape</h2><p>Before implementing security measures, it\'s important to understand the most common threats facing web applications today:</p><ul><li><strong>Injection attacks</strong> (SQL, NoSQL, OS, etc.) where malicious code is inserted into vulnerable applications</li><li><strong>Cross-Site Scripting (XSS)</strong> which allows attackers to inject client-side scripts into web pages</li><li><strong>Cross-Site Request Forgery (CSRF)</strong> where unauthorized commands are transmitted from a user the website trusts</li><li><strong>Broken Authentication</strong> vulnerabilities that compromise passwords, keys, or session tokens</li><li><strong>Security Misconfigurations</strong> resulting from incomplete default configurations or open cloud storage</li></ul><h2>Essential Security Practices</h2><h3>Input Validation and Sanitization</h3><p>Never trust user input. Implement thorough validation and sanitization for all data coming into your application, regardless of source. This includes parameters in URLs, form inputs, cookies, and API responses.</p><p>For example, when handling SQL queries, use parameterized statements or prepared statements instead of directly incorporating user input into query strings.</p><h3>Authentication and Authorization</h3><p>Implement robust authentication systems with the following features:</p><ul><li>Multi-factor authentication for sensitive functions</li><li>Strong password policies with enforcement</li><li>Secure password storage using modern hashing algorithms (e.g., bcrypt, Argon2)</li><li>Account lockout policies to prevent brute force attacks</li><li>Session management with secure, HttpOnly, and SameSite cookies</li></ul><p>For authorization, follow the principle of least privilege, ensuring users only have access to the resources they need. Implement role-based access control (RBAC) for more granular permission management.</p><h3>HTTPS Everywhere</h3><p>Secure all communication with HTTPS, including internal APIs and administrative interfaces. Configure TLS correctly, using modern protocols and ciphers while disabling older, vulnerable options.</p><p>Implement HTTP Strict Transport Security (HSTS) to ensure browsers always use secure connections to your site.</p><h3>Security Headers</h3><p>Implement security headers to provide an additional layer of protection:</p><ul><li>Content-Security-Policy (CSP) to prevent XSS attacks</li><li>X-XSS-Protection as a backup defense against XSS</li><li>X-Frame-Options to prevent clickjacking</li><li>X-Content-Type-Options to prevent MIME-type sniffing</li></ul><h3>Regular Updates and Patching</h3><p>Maintain a rigorous update schedule for all components of your application stack, including frameworks, libraries, and the underlying infrastructure. Many successful breaches exploit known vulnerabilities that could have been patched.</p><p>Use automated tools to scan for outdated dependencies and security vulnerabilities in your code.</p><h2>Security Testing</h2><p>Incorporate security testing throughout your development lifecycle:</p><ul><li><strong>Static Application Security Testing (SAST)</strong> to analyze source code for security vulnerabilities</li><li><strong>Dynamic Application Security Testing (DAST)</strong> to test running applications for vulnerabilities</li><li><strong>Regular penetration testing</strong> to simulate real-world attacks</li><li><strong>Security code reviews</strong> to catch issues automated tools might miss</li></ul><h2>Monitoring and Incident Response</h2><p>Even with the best prevention measures, security incidents can occur. Implement comprehensive monitoring to detect potential breaches:</p><ul><li>Log security-relevant events and maintain audit trails</li><li>Use intrusion detection systems to identify suspicious activity</li><li>Set up alerts for unusual behavior patterns</li><li>Develop and regularly test an incident response plan</li></ul><h2>Security as a Culture</h2><p>Finally, build security awareness throughout your organization. Provide regular training for developers, implement secure coding guidelines, and make security review an integral part of your development process.</p><p>Remember that web application security is not a one-time project but an ongoing process that requires constant attention and adaptation as new threats emerge.</p>',
            'excerpt': 'Learn essential strategies and best practices for securing your web applications against common vulnerabilities, from input validation and authentication to monitoring and incident response.',
            'image_url': '/static/img/blog/web-security.jpg',
            'category': 'Web Development',
            'tags': ['Security', 'Web Design', 'Technology']
        },
    ]
    
    # Create posts if they don't exist
    for post_data in posts:
        post = BlogPost.query.filter_by(slug=post_data['slug']).first()
        if not post:
            # Get category
            category = BlogCategory.query.filter_by(name=post_data['category']).first()
            
            # Get tags
            post_tags = []
            for tag_name in post_data['tags']:
                tag = BlogTag.query.filter_by(name=tag_name).first()
                if tag:
                    post_tags.append(tag)
            
            # Create post
            post = BlogPost(
                title=post_data['title'],
                slug=post_data['slug'],
                content=post_data['content'],
                excerpt=post_data['excerpt'],
                image_url=post_data['image_url'],
                published=True,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                author=user,
                category=category,
                tags=post_tags
            )
            
            db.session.add(post)
    
    db.session.commit()
