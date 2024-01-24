# Multi-Tenancy in Flask

An example repo of multi-tenancy implement in the Flask

Refer the blog for full info https://medium.com/@mahshooq/multi-tenancy-in-flask-f5a5960fc9e4

In this blog, I share my journey overcoming challenges in developing a multi-tenant SAAS application, addressing questions like:

- How to structure a Flask application for a multi-tenant SAAS architecture with isolated tenant data?
- How to separate the public schema for general information from tenant-specific schemas?
- How to implement user authentication and link users with specific tenants?
- How to manage database migrations separately for public and tenant schemas?
- How to dynamically create a new schema in the database for each new tenant during the registration process?
- How to implement middleware for seamless switching between public and tenant schemas based on incoming requests?
- Why choose schemas over databases for each tenant, and what performance improvements are observed?
