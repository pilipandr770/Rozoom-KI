from dataclasses import dataclass
from typing import Dict


@dataclass
class Agent:
    name: str
    description: str
    system_prompt: str


# Registry of agents
AGENTS: Dict[str, Agent] = {}


def register_agent(agent: Agent):
    AGENTS[agent.name] = agent


def get_agent(name: str) -> Agent:
    return AGENTS.get(name)


def choose_agent_by_metadata(metadata: dict) -> Agent:
    """Simple routing rules: checks metadata.topic or keywords."""
    topic = (metadata or {}).get('topic', '') or ''
    topic = topic.lower()
    # If a domain was explicitly selected, route to that agent
    selected = (metadata or {}).get('selected_domain')
    if selected:
        return AGENTS.get(selected)
    if 'billing' in topic or 'price' in topic or 'payment' in topic:
        return AGENTS.get('billing')
    if 'tech' in topic or 'error' in topic or 'bug' in topic:
        return AGENTS.get('tech')
    if 'sales' in topic or 'buy' in topic or 'package' in topic:
        return AGENTS.get('sales')
    return AGENTS.get('general')


# Register some default agents
register_agent(Agent(
    name='general',
    description='General assistant for generic questions',
    system_prompt='You are a helpful general assistant for Rozoom-KI.'
))

register_agent(Agent(
    name='sales',
    description='Sales assistant: convert visitors to paying customers, explain packages',
    system_prompt='You are a friendly sales assistant. Focus on packages, benefits, and clear CTAs.'
))

register_agent(Agent(
    name='tech',
    description='Technical assistant: help with integration, bugs, architecture',
    system_prompt='You are a technical assistant. Provide concise, actionable technical guidance.'
))

register_agent(Agent(
    name='billing',
    description='Billing assistant: pricing, invoices, payment issues',
    system_prompt='You are a billing assistant. Help with payments, invoices, and Stripe-related questions.'
))

# Greeter agent: welcomes and collects domain choice
register_agent(Agent(
    name='greeter',
    description='Welcome agent: greets visitor and asks about their needs',
    system_prompt=('You are a friendly greeter. Introduce yourself, ask which area the client needs '
                   'development in (Web, Mobile, ML, Automation, Other). Offer clickable options and '
                   'explain that submitting a short technical brief is free and non-binding.')
))

# Domain-specific agents
register_agent(Agent(
    name='web',
    description='Web development agent',
    system_prompt='You are a web development expert. Help the user form a short technical brief for web projects.'
))

register_agent(Agent(
    name='mobile',
    description='Mobile development agent',
    system_prompt='You are a mobile development expert. Help the user form a short technical brief for mobile apps.'
))

register_agent(Agent(
    name='ml',
    description='Machine learning agent',
    system_prompt='You are a machine learning specialist. Help the user define data, target metrics and scope.'
))

register_agent(Agent(
    name='automation',
    description='Automation and integration agent',
    system_prompt='You are an automation specialist. Help the user specify inputs, triggers and desired outcomes.'
))

register_agent(Agent(
    name='other',
    description='Other domains',
    system_prompt='You are a general domain expert. Help clarify the user needs and suggest a category.'
))


def list_domain_options():
    return [
        {'key': 'web', 'label': 'Web development'},
        {'key': 'mobile', 'label': 'Mobile apps'},
        {'key': 'ml', 'label': 'Machine learning / AI'},
        {'key': 'automation', 'label': 'Automation / Integrations'},
        {'key': 'other', 'label': 'Other / Consultation'},
    ]
