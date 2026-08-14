import os
from datetime import datetime, timedelta
from .extensions import db
from .models import Service, TrainingCourse, Project, Testimonial, AdminUser, ContactMessage, ConsultationRequest, EnrollmentRequest

def seed_database():
    """Seed sample catalog data based on dev_requirements.txt specifications."""
    
    # 1. Services
    services_data = [
        {
            'title': 'Cloud Consulting',
            'slug': 'cloud-consulting',
            'icon': 'fa-cloud',
            'category': 'Cloud & Infrastructure',
            'short_desc': 'Architect, migrate, and optimize enterprise workloads across AWS, Azure, and Google Cloud with multi-cloud reliability.',
            'long_desc': 'Our Cloud Consulting services enable organizations to modernize legacy infrastructure, optimize cloud expenditure, and implement resilient multi-cloud architectures. We deliver full lifecycle support from cloud readiness assessment to seamless migration and continuous security monitoring.',
            'features_list': 'AWS & Azure Cloud Migration, Cloud Cost Optimization (FinOps), Cloud-Native Architecture, Disaster Recovery & High Availability',
            'platforms': 'AWS • Azure • Google Cloud • Cloud Native'
        },
        {
            'title': 'DevOps Consulting',
            'slug': 'devops-consulting',
            'icon': 'fa-code-branch',
            'category': 'DevOps & Automation',
            'short_desc': 'Streamline software delivery cycles with CI/CD pipelines, Infrastructure as Code (IaC), and automated compliance.',
            'long_desc': 'Empower your development and operations teams with modern DevOps methodologies. We build fully automated continuous integration and continuous deployment (CI/CD) pipelines, implement GitOps workflows, and manage infrastructure declaratively with Terraform and Ansible.',
            'features_list': 'Automated CI/CD Pipelines, Infrastructure as Code (Terraform/Ansible), Container Orchestration, GitOps Workflows',
            'platforms': 'Docker • Kubernetes • Terraform • Ansible • Jenkins'
        },
        {
            'title': 'Infrastructure Solutions',
            'slug': 'infrastructure-solutions',
            'icon': 'fa-server',
            'category': 'Cloud & Infrastructure',
            'short_desc': 'Design and deploy robust enterprise server, storage, and networking architectures tailored for hybrid environments.',
            'long_desc': 'We provide end-to-end data center and cloud infrastructure design, virtualisation (KVM/VMware), storage area networks, and high-performance network topology engineered for 99.99% uptime and zero data loss resiliency.',
            'features_list': 'Enterprise Server Virtualization, Network Topology Design, SAN/NAS Storage Configuration, Hybrid Cloud Integration',
            'platforms': 'VMware • KVM • SAN/NAS • Hybrid Cloud'
        },
        {
            'title': 'ERP Implementation & Support',
            'slug': 'erp-implementation-support',
            'icon': 'fa-layer-group',
            'category': 'Enterprise Systems',
            'short_desc': 'Transform business operations with connected ERP solutions that streamline processes, automate workflows, and improve enterprise-wide visibility.',
            'long_desc': 'Transform business operations with connected ERP solutions that streamline processes, automate workflows, and improve enterprise-wide visibility across leading enterprise platforms.',
            'features_list': 'ERP Implementation & Configuration, System Integration & APIs, Data Migration & Modernization, Workflow Automation, Upgrades & Optimization, Managed ERP Support',
            'platforms': 'SAP • NetSuite • Dynamics 365 • Odoo • Oracle'
        },
        {
            'title': 'CRM Solutions & Integration',
            'slug': 'crm-solutions-integration',
            'icon': 'fa-users-gear',
            'category': 'Customer Experience & CRM',
            'short_desc': 'Build smarter customer experiences with integrated CRM solutions that connect sales, service, data, and automation.',
            'long_desc': 'Build smarter customer experiences with integrated CRM solutions that connect sales, service, data, and automation across enterprise platforms.',
            'features_list': 'CRM Implementation, System & API Integration, Sales & Service Automation, Custom CRM Development, Data Migration & Analytics, CRM Support & Optimization',
            'platforms': 'Salesforce • Dynamics 365 • HubSpot • Zoho • Custom CRM'
        },
        {
            'title': 'Lean Six Sigma & IT Process Optimization',
            'slug': 'lean-six-sigma-it-process-optimization',
            'icon': 'fa-sliders',
            'category': 'Process Optimization & Advisory',
            'short_desc': 'Optimize IT operations through data-driven process improvement that reduces waste, lowers costs, improves service delivery, and increases system efficiency.',
            'long_desc': 'Optimize IT operations through data-driven process improvement that reduces waste, lowers costs, improves service delivery, and increases system efficiency.',
            'features_list': 'IT Process Optimization, Cost & Waste Reduction, Incident & Service Management Improvement, Workflow & Deployment Optimization, Root Cause & Problem Analysis, Automation Opportunity Assessment, System & Resource Optimization, KPI & Performance Improvement',
            'platforms': 'Lean • Six Sigma • DMAIC • Root Cause Analysis • Process Mapping • KPI Analysis'
        },
        {
            'title': 'Digital Transformation',
            'slug': 'digital-transformation',
            'icon': 'fa-rocket',
            'category': 'Strategy & Advisory',
            'short_desc': 'Modernize business processes, legacy monoliths, and operational workflows through state-of-the-art tech adoption.',
            'long_desc': 'Accelerate your business agility by transitioning from monolithic legacy systems to microservices and cloud-native solutions. Our digital transformation experts work closely with executives to execute strategic tech roadmaps.',
            'features_list': 'Legacy Codebase Modernization, Business Process Automation, Enterprise API Integration, Technology Governance Roadmap',
            'platforms': 'Microservices • Cloud-Native • Enterprise APIs'
        },
        {
            'title': 'Systems Administration',
            'slug': 'systems-administration',
            'icon': 'fa-terminal',
            'category': 'Systems & IT Ops',
            'short_desc': 'Comprehensive Linux and Windows server administration, patch management, security hardening, and performance tuning.',
            'long_desc': 'Ensure rock-solid stability across your server fleet. Our certified system administrators handle OS installations, kernel optimization, Active Directory configuration, backup execution, and proactive kernel patching.',
            'features_list': 'Linux (RHEL/Ubuntu/Debian) Management, Windows Server & Active Directory, Automated Patching & Security Hardening, Performance Tuning',
            'platforms': 'Linux RHEL/Ubuntu • Windows Server • Active Directory'
        },
        {
            'title': 'Application Deployment',
            'slug': 'application-deployment',
            'icon': 'fa-cubes',
            'category': 'DevOps & Automation',
            'short_desc': 'Seamless production deployment of web applications, microservices, and mobile backend services with zero downtime.',
            'long_desc': 'Deploy software faster and without user disruption. We implement blue-green deployments, canary releases, and rolling updates across Kubernetes clusters and traditional web application server pools.',
            'features_list': 'Blue-Green & Canary Deployments, Microservices Containerization, Load Balancing & Reverse Proxies, SSL/TLS Encryption Management',
            'platforms': 'Kubernetes • NGINX • Microservices • Docker'
        },
        {
            'title': 'Database Administration',
            'slug': 'database-administration',
            'icon': 'fa-database',
            'category': 'Database & Analytics',
            'short_desc': 'Enterprise MySQL, PostgreSQL, and SQL Server DBA services: replication, indexing, backup, and high availability.',
            'long_desc': 'Keep your vital business data safe, fast, and accessible. We handle complex database cluster setups, master-slave replication, query performance tuning, automated backup validation, and point-in-time recovery.',
            'features_list': 'MySQL/MariaDB & PostgreSQL Clustering, Performance Optimization & Indexing, Disaster Recovery & Automated Backups, Database Security Hardening',
            'platforms': 'MySQL • PostgreSQL • MariaDB • SQL Server'
        },
        {
            'title': 'Managed IT Services',
            'slug': 'managed-it-services',
            'icon': 'fa-headset',
            'category': 'Managed Services',
            'short_desc': '24/7 proactive infrastructure monitoring, helpdesk support, incident management, and SLA-driven maintenance.',
            'long_desc': 'Outsource your IT operations to a dedicated team of experts. We monitor server metrics round-the-clock using Icinga2, Prometheus, and Grafana, guaranteeing swift incident response and proactive system health management.',
            'features_list': '24/7 System Health Monitoring, Incident Response & SLA Guarantees, Proactive Maintenance, Executive IT Health Reporting',
            'platforms': 'Prometheus • Grafana • Icinga2 • SLA Helpdesk'
        },
        {
            'title': 'IT Support',
            'slug': 'it-support',
            'icon': 'fa-tools',
            'category': 'Managed Services',
            'short_desc': 'On-demand technical troubleshooting, hardware/software support, remote desktop assistance, and user access management.',
            'long_desc': 'Provide your employees with rapid resolution for workplace tech issues. We manage helpdesk tickets, workstation setup, software licensing, anti-malware enforcement, and remote user support.',
            'features_list': 'Tier 1 to Tier 3 Helpdesk Support, Remote Desktop Troubleshooting, Workstation Deployment & Security, User Access Provisioning',
            'platforms': 'Tier 1-3 Support • Remote Admin • Security Policy'
        },
        {
            'title': 'Technology Advisory',
            'slug': 'technology-advisory',
            'icon': 'fa-lightbulb',
            'category': 'Strategy & Advisory',
            'short_desc': 'Strategic IT consulting, CTO-as-a-Service, technology procurement, compliance auditing, and security assessments.',
            'long_desc': 'Gain expert technical leadership without the overhead of a full-time executive. Our advisory practice guides tech stack selection, vendor evaluations, cybersecurity risk audits, and IT budget optimization.',
            'features_list': 'Fractional CTO / Technical Leadership, Cybersecurity Compliance Auditing, Vendor Evaluation & Contract Negotiation, IT Strategy & Budget Planning',
            'platforms': 'CTO Advisory • Compliance • IT Architecture'
        }
    ]
    for s in services_data:
        existing = Service.query.filter_by(slug=s['slug']).first()
        if existing:
            existing.title = s['title']
            existing.icon = s['icon']
            existing.category = s['category']
            existing.short_desc = s['short_desc']
            existing.long_desc = s['long_desc']
            existing.features_list = s['features_list']
            existing.platforms = s.get('platforms')
        else:
            db.session.add(Service(**s))

    # 2. Professional Training Courses
    if TrainingCourse.query.count() == 0:
        courses_data = [
            {
                'title': 'AWS Cloud Engineering',
                'slug': 'aws-cloud-engineering',
                'icon': 'fa-aws',
                'image': 'images/courses/aws-cloud.svg',
                'short_desc': 'Master AWS core services (EC2, S3, VPC, IAM, RDS) and build enterprise cloud solutions. Prepares for AWS Solutions Architect Certification.',
                'long_desc': 'This comprehensive bootcamp covers hands-on AWS architecture, networking, security controls, serverless application building with Lambda, and automated infrastructure deployment.',
                'duration': '10 Weeks',
                'delivery_mode': 'Online Live & Hybrid',
                'skill_level': 'Beginner to Advanced',
                'syllabus_list': 'AWS Architecture Fundamentals|VPC & Networking Security|EC2, Auto-Scaling & Load Balancing|RDS & DynamoDB Management|AWS Lambda & Serverless|Certification Exam Prep',
                'featured': True
            },
            {
                'title': 'Microsoft Azure',
                'slug': 'microsoft-azure',
                'icon': 'fa-microsoft',
                'image': 'images/courses/azure-cloud.svg',
                'short_desc': 'Learn Microsoft Azure cloud infrastructure, Azure Active Directory, Virtual Machines, and Azure DevOps integration.',
                'long_desc': 'Gain industry-grade expertise in managing enterprise Azure environments, building hybrid cloud connections, configuring Azure AD SSO, and automating resource groups.',
                'duration': '8 Weeks',
                'delivery_mode': 'Online Live & Onsite',
                'skill_level': 'Intermediate',
                'syllabus_list': 'Azure Identity & Access (Azure AD)|Azure Virtual Networks & VPNs|Azure Storage & Databases|Azure Web Apps & Containers|Azure Monitoring & Security',
                'featured': True
            },
            {
                'title': 'DevOps Engineering',
                'slug': 'devops-engineering',
                'icon': 'fa-infinity',
                'image': '/static/images/courses/devops-engineering.svg',
                'short_desc': 'Become a full-stack DevOps practitioner using Git, Jenkins, GitHub Actions, Terraform, Ansible, Docker, and Kubernetes.',
                'long_desc': 'Learn to bridge software development and operations. Build production-grade continuous integration and continuous deployment pipelines from scratch.',
                'duration': '12 Weeks',
                'delivery_mode': 'Online Live & Hybrid',
                'skill_level': 'Intermediate to Advanced',
                'syllabus_list': 'Version Control with Git & GitHub|CI/CD with Jenkins & GitHub Actions|Infrastructure as Code with Terraform|Configuration Management with Ansible|Containerization with Docker|Kubernetes Cluster Orchestration',
                'featured': True
            },
            {
                'title': 'Cybersecurity',
                'slug': 'cybersecurity',
                'icon': 'fa-user-shield',
                'image': '/static/images/courses/cybersecurity.svg',
                'short_desc': 'Practical ethical hacking, network defense, threat analysis, incident response, and SIEM security logging.',
                'long_desc': 'Protect digital assets against modern cyber threats. Learn network vulnerability auditing, penetration testing tools, firewalls, and incident mitigation strategies.',
                'duration': '10 Weeks',
                'delivery_mode': 'Online Live & Onsite',
                'skill_level': 'Beginner to Intermediate',
                'syllabus_list': 'Network Security Fundamentals|Vulnerability Scanning & Assessment|Ethical Hacking & Penetration Testing|SIEM & Threat Monitoring|Incident Handling & Forensics',
                'featured': True
            },
            {
                'title': 'Software Development',
                'slug': 'software-development',
                'icon': 'fa-code',
                'image': '/static/images/courses/software-dev.svg',
                'short_desc': 'Full-stack Web Application Development using Python, JavaScript, REST APIs, SQL, and modern frontend frameworks.',
                'long_desc': 'Build production-ready, database-driven web applications. Learn backend API development with Python/Flask/Django and modern responsive frontend design.',
                'duration': '12 Weeks',
                'delivery_mode': 'Online Live & Hybrid',
                'skill_level': 'Beginner to Intermediate',
                'syllabus_list': 'Python & Core Programming|HTML5, CSS3 & JavaScript ES6+|RESTful API Design & Flask/Django|Relational Databases & SQL|Git Version Control & Web Deployment',
                'featured': True
            },
            {
                'title': 'Data Analytics',
                'slug': 'data-analytics',
                'icon': 'fa-chart-line',
                'image': '/static/images/courses/data-analytics.svg',
                'short_desc': 'Transform raw data into business intelligence using SQL, Python (Pandas/NumPy), Power BI, and Tableau dashboards.',
                'long_desc': 'Equip yourself with high-demand data analytics capabilities. Clean complex datasets, perform statistical analysis, and construct executive dashboard visuals.',
                'duration': '8 Weeks',
                'delivery_mode': 'Online Live',
                'skill_level': 'Beginner to Intermediate',
                'syllabus_list': 'SQL Data Extraction & Querying|Python Data Analysis with Pandas|Data Visualization with Power BI|Statistical Methods for Business|Interactive Dashboard Creation',
                'featured': True
            },
            {
                'title': 'Linux Administration',
                'slug': 'linux-administration',
                'icon': 'fa-linux',
                'image': '/static/images/courses/linux-admin.svg',
                'short_desc': 'Hands-on Red Hat / Ubuntu Linux systems management: command line, shell scripting, storage, users, and network security.',
                'long_desc': 'Master the backbone operating system of enterprise IT. Gain deep proficiency in Linux terminal navigation, systemd services, SSH hardening, Bash scripting, and LVM storage management.',
                'duration': '8 Weeks',
                'delivery_mode': 'Online Live & Onsite',
                'skill_level': 'Beginner to Intermediate',
                'syllabus_list': 'Linux Architecture & Command Line|User, Group & Permission Management|Storage, Partitioning & LVM|Networking & Firewalld/UFW|Bash Shell Automation Scripting',
                'featured': True
            },
            {
                'title': 'Docker & Kubernetes',
                'slug': 'docker-kubernetes',
                'icon': 'fa-dharmachakra',
                'image': '/static/images/courses/docker-k8s.svg',
                'short_desc': 'Containerize microservices with Docker and orchestrate scalable container clusters with Kubernetes (CKA concepts).',
                'long_desc': 'Designed for developers and sysadmins looking to master container orchestration. Create multi-container Docker applications, manage Helm charts, and deploy Kubernetes clusters.',
                'duration': '6 Weeks',
                'delivery_mode': 'Online Live & Hybrid',
                'skill_level': 'Intermediate to Advanced',
                'syllabus_list': 'Docker Engine & Container Mechanics|Multi-Container Applications with Docker Compose|Kubernetes Pods, Services & Deployments|ConfigMaps, Secrets & Persistent Volumes|Helm Package Manager & Cluster Ingress',
                'featured': True
            },
            {
                'title': 'IT Support Fundamentals',
                'slug': 'it-support-fundamentals',
                'icon': 'fa-laptop-medical',
                'image': '/static/images/courses/it-support.svg',
                'short_desc': 'Foundational course in hardware maintenance, operating systems troubleshooting, networking basics, and customer support skills.',
                'long_desc': 'Kickstart your tech career with fundamental IT skills. Ideal for beginners aiming for entry-level helpdesk, desktop support, and IT support technician positions.',
                'duration': '6 Weeks',
                'delivery_mode': 'Online Live & Onsite',
                'skill_level': 'Beginner',
                'syllabus_list': 'Computer Hardware & System Assembly|Windows & macOS OS Setup|TCP/IP Networking & Wi-Fi Troubleshooting|Ticketing Systems & Customer Service|Security & Malware Remediation',
                'featured': True
            },
            {
                'title': 'Corporate Technology Training',
                'slug': 'corporate-technology-training',
                'icon': 'fa-building-user',
                'image': '/static/images/courses/corporate-training.svg',
                'short_desc': 'Tailored upskilling programs for enterprise teams in Cloud Adoption, DevOps Culture, Cybersecurity Awareness, and IT Ops.',
                'long_desc': 'Customized workforce training engineered to match your organization’s tech stack. Delivered onsite or virtually with hands-on labs and real enterprise case studies.',
                'duration': 'Customized (1 - 4 Weeks)',
                'delivery_mode': 'Onsite or Virtual Cohorts',
                'skill_level': 'All Experience Levels',
                'syllabus_list': 'Customized Curriculum Assessment|Hands-On Corporate Sandbox Labs|Executive Tech Strategy Alignment|Post-Training Skill Evaluations',
                'featured': True
            }
        ]
        for c in courses_data:
            db.session.add(TrainingCourse(**c))

    # 3. Projects & Contracts
    Project.query.delete()
    projects_data = [
        {
            'title': 'Enterprise Multi-Region Cloud Migration',
            'slug': 'enterprise-multi-region-cloud-migration',
            'industry': 'Financial Services',
            'tech_stack': 'AWS • Cloud Infrastructure • PostgreSQL • Infrastructure Automation',
            'category': 'Cloud Migration',
            'short_desc': 'Delivered a secure multi-region cloud migration program that modernized enterprise infrastructure, improved scalability, strengthened resilience, and enhanced operational continuity.',
            'long_desc': '360IT delivered a secure multi-region cloud migration program that modernized enterprise infrastructure, improved scalability, strengthened resilience, and enhanced operational continuity for financial services systems.',
            'image': '/static/images/projects/project-cloud-migration.svg',
            'featured': True
        },
        {
            'title': 'Government Health Platform Modernization',
            'slug': 'government-health-platform-modernization',
            'industry': 'Government & Healthcare',
            'tech_stack': 'Kubernetes • Docker • CI/CD • Cloud Monitoring',
            'category': 'DevOps Implementation',
            'short_desc': 'Delivered a modern application platform that streamlined software delivery, improved platform reliability, and accelerated the deployment of critical public health services.',
            'long_desc': 'Delivered a modern application platform using Kubernetes, Docker, automated CI/CD pipelines, and cloud monitoring that streamlined software delivery and accelerated public health services.',
            'image': '/static/images/projects/project-devops.svg',
            'featured': True
        },
        {
            'title': 'Telecommunications Infrastructure Modernization',
            'slug': 'telecommunications-infrastructure-modernization',
            'industry': 'Telecommunications',
            'tech_stack': 'Linux • Virtualization • Enterprise Monitoring • Active Directory',
            'category': 'Infrastructure Modernization',
            'short_desc': 'Modernized enterprise infrastructure through virtualization, centralized monitoring, and resilient platform architecture to improve performance, availability, and operational efficiency.',
            'long_desc': 'Modernized enterprise infrastructure through Linux virtualization, centralized enterprise monitoring, and resilient platform architecture to maximize availability and performance.',
            'image': '/static/images/projects/project-telecom.svg',
            'featured': True
        },
        {
            'title': 'Government Digital Transformation',
            'slug': 'government-digital-transformation',
            'industry': 'Government',
            'tech_stack': 'Enterprise Applications • Azure • PostgreSQL • Workflow Automation',
            'category': 'Government Technology Projects',
            'short_desc': 'Digitized government operations through enterprise applications, workflow automation, and secure digital services, improving operational efficiency and service delivery.',
            'long_desc': 'Digitized government operations through secure enterprise applications, PostgreSQL database clusters, Azure cloud, and automated document approval workflows.',
            'image': '/static/images/projects/project-gov-transformation.svg',
            'featured': True
        },
        {
            'title': 'Enterprise Workflow & Business Rules Automation',
            'slug': 'enterprise-workflow-business-rules-automation',
            'industry': 'Multi-Industry',
            'tech_stack': 'Workflow Automation • Business Rules • Enterprise Applications • API Integration',
            'category': 'Business Automation',
            'short_desc': 'Configured enterprise workflows, approval processes, and business rules that automated critical operations, standardized processes, and supported successful implementations across multiple industries.',
            'long_desc': 'Configured enterprise workflows, approval processes, and business rules that automated critical operations, standardized processes, and supported successful implementations across multiple industries.',
            'image': '/static/images/projects/project-managed-it.svg',
            'featured': True
        },
        {
            'title': 'Enterprise Document Automation',
            'slug': 'enterprise-document-automation',
            'industry': 'Business Process Automation',
            'tech_stack': 'Document Automation • Template Management • Workflow Integration • Enterprise Applications',
            'category': 'Business Automation',
            'short_desc': 'Implemented intelligent document automation solutions for checks, letters, invoices, reports, certificates, compliance documentation, and business forms, reducing manual effort while improving consistency, accuracy, and compliance.',
            'long_desc': 'Implemented intelligent document automation solutions for checks, letters, invoices, reports, certificates, compliance documentation, and business forms, reducing manual effort while improving consistency, accuracy, and compliance.',
            'image': '/static/images/projects/project-education.svg',
            'featured': True
        },
        {
            'title': 'High-Availability Database Solutions',
            'slug': 'high-availability-database-solutions',
            'industry': 'Logistics & Supply Chain',
            'tech_stack': 'MySQL • High Availability • Database Clustering • Linux',
            'category': 'Infrastructure Modernization',
            'short_desc': 'Delivered highly available database platforms that strengthened business continuity, improved application performance, and supported mission-critical logistics operations.',
            'long_desc': 'Delivered highly available database platforms with MySQL Galera clustering and proxy failover, strengthening business continuity and performance for global logistics.',
            'image': '/static/images/projects/project-database.svg',
            'featured': True
        },
        {
            'title': 'Cybersecurity Assessment & Infrastructure Hardening',
            'slug': 'cybersecurity-assessment-infrastructure-hardening',
            'industry': 'Financial Services',
            'tech_stack': 'SIEM • Vulnerability Management • Security Automation • Endpoint Protection',
            'category': 'Cybersecurity Assessment',
            'short_desc': 'Strengthened enterprise security through comprehensive assessments, infrastructure hardening, and proactive security improvements that enhanced organizational resilience.',
            'long_desc': 'Strengthened enterprise security through comprehensive assessments, SIEM integration, vulnerability management, endpoint protection, and security automation playbooks.',
            'image': '/static/images/projects/project-security.svg',
            'featured': True
        },
        {
            'title': 'Enterprise Analytics & Business Intelligence',
            'slug': 'enterprise-analytics-business-intelligence',
            'industry': 'Manufacturing',
            'tech_stack': 'Power BI • SQL • Data Engineering • Analytics',
            'category': 'Business Intelligence',
            'short_desc': 'Delivered enterprise reporting and analytics solutions that transformed operational data into actionable insights, enabling informed business decisions and improved operational visibility.',
            'long_desc': 'Delivered enterprise reporting and analytics solutions using Power BI dashboards and SQL data engineering, converting plant data into actionable business intelligence.',
            'image': '/static/images/projects/project-bi.svg',
            'featured': True
        },
        {
            'title': 'Enterprise Commerce Platform',
            'slug': 'enterprise-commerce-platform',
            'industry': 'Retail & E-Commerce',
            'tech_stack': 'JavaScript • Python • APIs • Cloud Applications',
            'category': 'Software Development',
            'short_desc': 'Developed scalable digital commerce solutions that integrated inventory management, payment processing, and customer engagement to support business growth.',
            'long_desc': 'Developed scalable digital commerce solutions with JavaScript, Python, REST APIs, and cloud applications to power real-time inventory management and checkout.',
            'image': '/static/images/projects/project-retail.svg',
            'featured': True
        },
        {
            'title': '24/7 Managed Infrastructure Services',
            'slug': '24-7-managed-infrastructure-services',
            'industry': 'Energy & Utilities',
            'tech_stack': 'Infrastructure Monitoring • Linux • Automation • Secure Remote Access',
            'category': 'Managed IT Services',
            'short_desc': 'Delivered proactive infrastructure management, monitoring, maintenance, and technical support to ensure secure, reliable, and highly available enterprise environments.',
            'long_desc': 'Delivered 24/7 proactive infrastructure management, continuous monitoring, maintenance, and technical support to ensure secure and highly available environments.',
            'image': '/static/images/projects/project-managed-it.svg',
            'featured': True
        }
    ]
    for p in projects_data:
        db.session.add(Project(**p))

    # 4. Testimonials
    Testimonial.query.delete()
    testimonials_data = [
        {
            'name': 'David Miller',
            'position': 'Chief Information Officer',
            'organization': 'Apex Financial Holdings',
            'service_type': 'Consulting',
            'quote': '360IT Learning & Consulting transformed our cloud infrastructure. Their team executed our AWS migration flawlessly with zero disruption to active customer transactions.',
            'avatar': '/static/images/testimonials/avatar1.jpg',
            'rating': 5
        },
        {
            'name': 'Dr. Amanda Vance',
            'position': 'Director of ICT',
            'organization': 'Federal Ministry of Innovation',
            'service_type': 'Consulting & Contracts',
            'quote': 'Their expertise in government technology contracts is unmatched. They delivered our digital portal on time, fully secured, and strictly within budget.',
            'avatar': '/static/images/testimonials/avatar2.jpg',
            'rating': 5
        },
        {
            'name': 'James Mitchell',
            'position': 'Senior DevOps Engineer',
            'organization': 'FinTech PayGlobal',
            'service_type': 'Training',
            'quote': 'The AWS and DevOps Engineering bootcamp completely transformed my career! The hands-on labs with Docker, Kubernetes, and Terraform were directly applicable to enterprise job requirements.',
            'avatar': '/static/images/testimonials/avatar3.jpg',
            'rating': 5
        },
        {
            'name': 'Sarah Jenkins',
            'position': 'VP of Engineering',
            'organization': 'CloudScale Systems',
            'service_type': 'Consulting',
            'quote': 'Working with 360IT Consulting on our CI/CD pipeline automation reduced our product deployment cycle from 2 weeks to under 30 minutes.',
            'avatar': '/static/images/testimonials/avatar4.jpg',
            'rating': 5
        },
        {
            'name': 'Michael Reynolds',
            'position': 'Systems Administrator',
            'organization': 'FirstHealth Medical Group',
            'service_type': 'Training',
            'quote': 'The Linux Administration training was intense, highly practical, and thoroughly engaging. The instructors are real-world consultants who know their stuff inside out.',
            'avatar': '/static/images/testimonials/avatar5.jpg',
            'rating': 5
        },
        {
            'name': 'Grace Taylor',
            'position': 'Operations Lead',
            'organization': 'Logistics 360',
            'service_type': 'Managed IT Services',
            'quote': 'Their 24/7 Managed IT Services give us absolute peace of mind. System bottlenecks are identified and resolved before our teams even notice.',
            'avatar': '/static/images/testimonials/avatar6.jpg',
            'rating': 5
        }
    ]
    for t in testimonials_data:
        db.session.add(Testimonial(**t))

    # 5. Default Admin User
    if AdminUser.query.filter_by(username='admin').first() is None:
        admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'Admin@360it!2026')
        admin_user = AdminUser(
            username='admin',
            email='admin@360it-learning.com',
            full_name='360IT Administrator',
            role='Super Admin',
            must_change_password=True
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)

    # 6. Sample Contact Messages
    if ContactMessage.query.count() == 0:
        sample_messages = [
            {
                'name': 'Robert Chen',
                'email': 'robert.chen@techcorp.io',
                'phone': '+1 (555) 234-5678',
                'subject': 'IT Consulting Services',
                'message': 'We are looking to migrate our monolithic e-commerce application to AWS microservices and would like to schedule a technical assessment.',
                'status': 'New',
                'is_read': False,
                'created_at': datetime.utcnow() - timedelta(hours=3)
            },
            {
                'name': 'Sarah Jenkins',
                'email': 'sjenkins@innovatehealth.org',
                'phone': '+1 (555) 987-6543',
                'subject': 'General Enquiry',
                'message': 'Do you offer customized group discounts for corporate tech training cohorts of 15+ engineers?',
                'status': 'In Review',
                'admin_notes': 'Reviewed by admissions lead. Follow up scheduled.',
                'is_read': True,
                'created_at': datetime.utcnow() - timedelta(days=1)
            },
            {
                'name': 'Marcus Vance',
                'email': 'mvance@cloudnet.com',
                'phone': '+1 (555) 345-6789',
                'subject': 'Projects & Contracts',
                'message': 'Inquiring about RFP specifications for state government cloud infrastructure modernization contract.',
                'status': 'Replied',
                'admin_notes': 'Sent contract portfolio PDF and proposal schedule.',
                'is_read': True,
                'created_at': datetime.utcnow() - timedelta(days=3)
            }
        ]
        for m in sample_messages:
            db.session.add(ContactMessage(**m))

    # 7. Sample Course Enrollment Applications
    if EnrollmentRequest.query.count() == 0:
        sample_enrollments = [
            {
                'name': 'Alexander Wright',
                'email': 'alex.wright@devmail.io',
                'phone': '+1 (555) 876-5432',
                'course_title': 'AWS Cloud Engineering',
                'delivery_mode': 'Online Live Interactive',
                'message': 'I have 2 years of Linux sysadmin experience and want to pivot to Cloud Architecture.',
                'status': 'Pending',
                'is_read': False,
                'created_at': datetime.utcnow() - timedelta(hours=5)
            },
            {
                'name': 'Elena Rostova',
                'email': 'elena.rostova@datawave.com',
                'phone': '+1 (555) 654-3210',
                'course_title': 'DevOps Engineering',
                'delivery_mode': 'Hybrid',
                'message': 'Applying for the upcoming weekend batch starting next month.',
                'status': 'Reviewed',
                'admin_notes': 'Pre-assessment test sent to candidate.',
                'is_read': True,
                'created_at': datetime.utcnow() - timedelta(days=2)
            },
            {
                'name': 'David Miller',
                'email': 'dmiller@cyberdef.org',
                'phone': '+1 (555) 432-1098',
                'course_title': 'Cybersecurity',
                'delivery_mode': 'Onsite Corporate Training',
                'message': 'Enrolling 3 junior SOC analysts from our team.',
                'status': 'Accepted',
                'admin_notes': 'Approved by training director. Invoice dispatched.',
                'is_read': True,
                'created_at': datetime.utcnow() - timedelta(days=4)
            },
            {
                'name': 'Carlos Mendez',
                'email': 'carlos.mendez@sysops.net',
                'phone': '+1 (555) 210-9876',
                'course_title': 'Docker & Kubernetes',
                'delivery_mode': 'Online Live Interactive',
                'message': 'Interested in CKA preparation module.',
                'status': 'Enrolled',
                'admin_notes': 'Payment verified. Course access credentials generated.',
                'is_read': True,
                'created_at': datetime.utcnow() - timedelta(days=6)
            }
        ]
        for e in sample_enrollments:
            db.session.add(EnrollmentRequest(**e))

    # 8. Sample Consultation Requests
    if ConsultationRequest.query.count() == 0:
        sample_consultations = [
            {
                'name': 'Patricia Taylor',
                'email': 'ptaylor@enterprise-ops.com',
                'phone': '+1 (555) 789-0123',
                'organization': 'Enterprise Operations Corp',
                'service_interest': 'Cloud Consulting',
                'message': 'We require fractional CTO guidance for multi-cloud architecture setup.',
                'status': 'Pending',
                'is_read': False,
                'created_at': datetime.utcnow() - timedelta(hours=8)
            }
        ]
        for c in sample_consultations:
            db.session.add(ConsultationRequest(**c))

    db.session.commit()

