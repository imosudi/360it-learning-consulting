from .extensions import db
from .models import Service, TrainingCourse, Project, Testimonial

def seed_database():
    """Seed sample catalog data based on dev_requirements.txt specifications."""
    
    # 1. Services
    if Service.query.count() == 0:
        services_data = [
            {
                'title': 'Cloud Consulting',
                'slug': 'cloud-consulting',
                'icon': 'fa-cloud',
                'category': 'Cloud & Infrastructure',
                'short_desc': 'Architect, migrate, and optimize enterprise workloads across AWS, Azure, and Google Cloud with multi-cloud reliability.',
                'long_desc': 'Our Cloud Consulting services enable organizations to modernize legacy infrastructure, optimize cloud expenditure, and implement resilient multi-cloud architectures. We deliver full lifecycle support from cloud readiness assessment to seamless migration and continuous security monitoring.',
                'features_list': 'AWS & Azure Cloud Migration, Cloud Cost Optimization (FinOps), Cloud-Native Architecture, Disaster Recovery & High Availability'
            },
            {
                'title': 'DevOps Consulting',
                'slug': 'devops-consulting',
                'icon': 'fa-code-branch',
                'category': 'DevOps & Automation',
                'short_desc': 'Streamline software delivery cycles with CI/CD pipelines, Infrastructure as Code (IaC), and automated compliance.',
                'long_desc': 'Empower your development and operations teams with modern DevOps methodologies. We build fully automated continuous integration and continuous deployment (CI/CD) pipelines, implement GitOps workflows, and manage infrastructure declaratively with Terraform and Ansible.',
                'features_list': 'Automated CI/CD Pipelines, Infrastructure as Code (Terraform/Ansible), Container Orchestration, GitOps Workflows'
            },
            {
                'title': 'Infrastructure Solutions',
                'slug': 'infrastructure-solutions',
                'icon': 'fa-server',
                'category': 'Cloud & Infrastructure',
                'short_desc': 'Design and deploy robust enterprise server, storage, and networking architectures tailored for hybrid environments.',
                'long_desc': 'We provide end-to-end data center and cloud infrastructure design, virtualisation (KVM/VMware), storage area networks, and high-performance network topology engineered for 99.99% uptime and zero data loss resiliency.',
                'features_list': 'Enterprise Server Virtualization, Network Topology Design, SAN/NAS Storage Configuration, Hybrid Cloud Integration'
            },
            {
                'title': 'Digital Transformation',
                'slug': 'digital-transformation',
                'icon': 'fa-rocket',
                'category': 'Strategy & Advisory',
                'short_desc': 'Modernize business processes, legacy monoliths, and operational workflows through state-of-the-art tech adoption.',
                'long_desc': 'Accelerate your business agility by transitioning from monolithic legacy systems to microservices and cloud-native solutions. Our digital transformation experts work closely with executives to execute strategic tech roadmaps.',
                'features_list': 'Legacy Codebase Modernization, Business Process Automation, Enterprise API Integration, Technology Governance Roadmap'
            },
            {
                'title': 'Systems Administration',
                'slug': 'systems-administration',
                'icon': 'fa-terminal',
                'category': 'Systems & IT Ops',
                'short_desc': 'Comprehensive Linux and Windows server administration, patch management, security hardening, and performance tuning.',
                'long_desc': 'Ensure rock-solid stability across your server fleet. Our certified system administrators handle OS installations, kernel optimization, Active Directory configuration, backup execution, and proactive kernel patching.',
                'features_list': 'Linux (RHEL/Ubuntu/Debian) Management, Windows Server & Active Directory, Automated Patching & Security Hardening, Performance Tuning'
            },
            {
                'title': 'Application Deployment',
                'slug': 'application-deployment',
                'icon': 'fa-cubes',
                'category': 'DevOps & Automation',
                'short_desc': 'Seamless production deployment of web applications, microservices, and mobile backend services with zero downtime.',
                'long_desc': 'Deploy software faster and without user disruption. We implement blue-green deployments, canary releases, and rolling updates across Kubernetes clusters and traditional web application server pools.',
                'features_list': 'Blue-Green & Canary Deployments, Microservices Containerization, Load Balancing & Reverse Proxies, SSL/TLS Encryption Management'
            },
            {
                'title': 'Database Administration',
                'slug': 'database-administration',
                'icon': 'fa-database',
                'category': 'Database & Analytics',
                'short_desc': 'Enterprise MySQL, PostgreSQL, and SQL Server DBA services: replication, indexing, backup, and high availability.',
                'long_desc': 'Keep your vital business data safe, fast, and accessible. We handle complex database cluster setups, master-slave replication, query performance tuning, automated backup validation, and point-in-time recovery.',
                'features_list': 'MySQL/MariaDB & PostgreSQL Clustering, Performance Optimization & Indexing, Disaster Recovery & Automated Backups, Database Security Hardening'
            },
            {
                'title': 'Managed IT Services',
                'slug': 'managed-it-services',
                'icon': 'fa-headset',
                'category': 'Managed Services',
                'short_desc': '24/7 proactive infrastructure monitoring, helpdesk support, incident management, and SLA-driven maintenance.',
                'long_desc': 'Outsource your IT operations to a dedicated team of experts. We monitor server metrics round-the-clock using Icinga2, Prometheus, and Grafana, guaranteeing swift incident response and proactive system health management.',
                'features_list': '24/7 System Health Monitoring, Incident Response & SLA Guarantees, Proactive Maintenance, Executive IT Health Reporting'
            },
            {
                'title': 'IT Support',
                'slug': 'it-support',
                'icon': 'fa-tools',
                'category': 'Managed Services',
                'short_desc': 'On-demand technical troubleshooting, hardware/software support, remote desktop assistance, and user access management.',
                'long_desc': 'Provide your employees with rapid resolution for workplace tech issues. We manage helpdesk tickets, workstation setup, software licensing, anti-malware enforcement, and remote user support.',
                'features_list': 'Tier 1 to Tier 3 Helpdesk Support, Remote Desktop Troubleshooting, Workstation Deployment & Security, User Access Provisioning'
            },
            {
                'title': 'Technology Advisory',
                'slug': 'technology-advisory',
                'icon': 'fa-lightbulb',
                'category': 'Strategy & Advisory',
                'short_desc': 'Strategic IT consulting, CTO-as-a-Service, technology procurement, compliance auditing, and security assessments.',
                'long_desc': 'Gain expert technical leadership without the overhead of a full-time executive. Our advisory practice guides tech stack selection, vendor evaluations, cybersecurity risk audits, and IT budget optimization.',
                'features_list': 'Fractional CTO / Technical Leadership, Cybersecurity Compliance Auditing, Vendor Evaluation & Contract Negotiation, IT Strategy & Budget Planning'
            }
        ]
        for s in services_data:
            db.session.add(Service(**s))

    # 2. Professional Training Courses
    if TrainingCourse.query.count() == 0:
        courses_data = [
            {
                'title': 'AWS Cloud Engineering',
                'slug': 'aws-cloud-engineering',
                'icon': 'fa-aws',
                'image': '/static/images/courses/aws-cloud.svg',
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
                'image': '/static/images/courses/azure-cloud.svg',
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
    if Project.query.count() == 0:
        projects_data = [
            {
                'title': 'Enterprise Multi-Region Cloud Migration',
                'slug': 'cloud-migration-enterprise',
                'industry': 'Financial Services',
                'tech_stack': 'AWS, Terraform, EC2, RDS PostgreSQL, CloudFront',
                'category': 'Cloud Migration',
                'short_desc': 'Migrated 45+ core banking and analytical microservices from legacy on-premises servers to high-availability multi-region AWS cloud.',
                'long_desc': '360IT Learning & Consulting executed a zero-downtime migration strategy for a leading regional bank. Built automated Infrastructure as Code using Terraform and implemented automated failover.',
                'image': '/static/images/projects/project-cloud-migration.svg',
                'featured': True
            },
            {
                'title': 'Government Health Portal DevOps Pipeline',
                'slug': 'government-health-devops',
                'industry': 'Government & Healthcare',
                'tech_stack': 'Kubernetes, Docker, GitLab CI, Helm, Prometheus',
                'category': 'DevOps Implementation',
                'short_desc': 'Designed and implemented automated CI/CD pipelines and Kubernetes container clusters for nationwide public healthcare portal.',
                'long_desc': 'Engineered a resilient container infrastructure capable of scaling to over 500,000 daily active users while maintaining compliance with health data security protocols.',
                'image': '/static/images/projects/project-devops.svg',
                'featured': True
            },
            {
                'title': 'Telecom Infrastructure Modernization',
                'slug': 'telecom-infrastructure-modernization',
                'industry': 'Telecommunications',
                'tech_stack': 'KVM Virtualization, GlusterFS, Active Directory, Icinga2',
                'category': 'Infrastructure Modernization',
                'short_desc': 'Upgraded enterprise virtualisation clusters, SAN storage, and centralized monitoring for major telecommunications provider.',
                'long_desc': 'Replaced legacy blade servers with redundant KVM virtualization clusters and GlusterFS distributed storage, delivering 40% performance gain and 99.999% system availability.',
                'image': '/static/images/projects/project-telecom.svg',
                'featured': True
            },
            {
                'title': 'Government Agency Digital Transformation',
                'slug': 'government-digital-transformation',
                'industry': 'Government',
                'tech_stack': 'Python, Flask, PostgreSQL, Docker, Azure AD',
                'category': 'Government Technology Projects',
                'short_desc': 'Digitized manual document approval workflows and public service request tracking for state government ministry.',
                'long_desc': 'Transformed legacy paper-based government operations into a secure web portal featuring role-based access control and digital signature verification.',
                'image': '/static/images/projects/project-gov-transformation.svg',
                'featured': True
            },
            {
                'title': 'High-Availability Database Cluster Deployment',
                'slug': 'high-availability-database-cluster',
                'industry': 'Logistics & Supply Chain',
                'tech_stack': 'MySQL Galera Cluster, ProxySQL, Keepalived, Linux',
                'category': 'Enterprise Systems Deployment',
                'short_desc': 'Built real-time multi-master MySQL cluster for global logistics tracking system handling millions of daily sensor events.',
                'long_desc': 'Architected high-speed database replication and automated failover proxying with ProxySQL and Keepalived to guarantee zero data loss during hardware failures.',
                'image': '/static/images/projects/project-database.svg',
                'featured': True
            },
            {
                'title': 'FinTech Cybersecurity Audit & Hardening',
                'slug': 'fintech-cybersecurity-hardening',
                'industry': 'Financial Services',
                'tech_stack': 'OpenVAS, Suricata IDS, Wazuh SIEM, Ansible',
                'category': 'Cybersecurity Assessment',
                'short_desc': 'Executed comprehensive vulnerability assessment, intrusion detection integration, and security policy automation for payment gateway.',
                'long_desc': 'Delivered end-to-end security assessment, closed 30+ critical infrastructure vulnerabilities, and implemented automated security compliance playbooks using Ansible.',
                'image': '/static/images/projects/project-security.svg',
                'featured': True
            },
            {
                'title': 'Higher Education LMS Digital Modernization',
                'slug': 'education-lms-modernization',
                'industry': 'Education',
                'tech_stack': 'AWS Lambda, DynamoDB, React, Node.js',
                'category': 'Digital Transformation',
                'short_desc': 'Modernized digital learning platform supporting over 25,000 active university students with online exams and video lectures.',
                'long_desc': 'Refactored monolith learning management system into serverless cloud microservices, reducing server hosting costs by 65% while handling peak exam load effortlessly.',
                'image': '/static/images/projects/project-education.svg',
                'featured': True
            },
            {
                'title': 'Manufacturing BI & Analytics Pipeline',
                'slug': 'manufacturing-bi-analytics',
                'industry': 'Manufacturing',
                'tech_stack': 'Python, SQL Server, Power BI, Apache Airflow',
                'category': 'Business Intelligence Solutions',
                'short_desc': 'Built automated ETL pipelines and real-time executive analytics dashboards for multi-plant manufacturing group.',
                'long_desc': 'Integrated plant IoT sensor data and ERP inventory records into centralized data warehouse, enabling real-time equipment efficiency tracking and predictive maintenance alerts.',
                'image': '/static/images/projects/project-bi.svg',
                'featured': True
            },
            {
                'title': 'Retail E-Commerce Microservices Platform',
                'slug': 'retail-ecommerce-microservices',
                'industry': 'Retail & E-Commerce',
                'tech_stack': 'JavaScript, Python, Docker, NGINX, Redis',
                'category': 'Software Development',
                'short_desc': 'Custom software development for nationwide retail chain featuring real-time inventory management and payment gateway integration.',
                'long_desc': 'Developed modular, scalable web application backend with Redis caching and NGINX load balancing, powering seamless shopping experiences across mobile and web.',
                'image': '/static/images/projects/project-retail.svg',
                'featured': True
            },
            {
                'title': '24/7 Managed IT Infrastructure Support',
                'slug': 'managed-it-infrastructure-support',
                'industry': 'Energy & Utilities',
                'tech_stack': 'Icinga2, Grafana, Ansible, OpenVPN, Linux',
                'category': 'Managed IT Services',
                'short_desc': 'Full 24/7 managed infrastructure support for utility provider managing remote solar and grid station nodes.',
                'long_desc': 'Configured secure VPN tunnels to remote telemetry nodes, implemented automated alert escalation via Grafana & Icinga2, and maintained 99.98% operational uptime.',
                'image': '/static/images/projects/project-managed-it.svg',
                'featured': True
            }
        ]
        for p in projects_data:
            db.session.add(Project(**p))

    # 4. Testimonials
    if Testimonial.query.count() == 0:
        testimonials_data = [
            {
                'name': 'David Adebayo',
                'position': 'Chief Information Officer',
                'organization': 'Apex Financial Holdings',
                'service_type': 'Consulting',
                'quote': '360IT Learning & Consulting transformed our cloud infrastructure. Their team executed our AWS migration flawlessly with zero disruption to active customer transactions.',
                'avatar': '/static/images/testimonials/avatar1.jpg',
                'rating': 5
            },
            {
                'name': 'Dr. Amina Yusuf',
                'position': 'Director of ICT',
                'organization': 'Federal Ministry of Innovation',
                'service_type': 'Consulting & Contracts',
                'quote': 'Their expertise in government technology contracts is unmatched. They delivered our digital portal on time, fully secured, and strictly within budget.',
                'avatar': '/static/images/testimonials/avatar2.jpg',
                'rating': 5
            },
            {
                'name': 'Emmanuel Nwosu',
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
                'name': 'Michael Omole',
                'position': 'Systems Administrator',
                'organization': 'FirstHealth Medical Group',
                'service_type': 'Training',
                'quote': 'The Linux Administration training was intense, highly practical, and thoroughly engaging. The instructors are real-world consultants who know their stuff inside out.',
                'avatar': '/static/images/testimonials/avatar5.jpg',
                'rating': 5
            },
            {
                'name': 'Grace Kalu',
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
            
    db.session.commit()
