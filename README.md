# Intrusion Detection With Django

Implemented using Lazy Algorithm.
Uses Django-user-agents to get device properties. Uses an API (ipgeolocation) to get location.

# How it works
- Stores user devices information (alongside location) when registering
- Cross-check to see if none of the details matches, when trying to login

