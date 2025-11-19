"""
This file contains detailed descriptions of career choices as well as examples. Multiple descriptions and examples are included
to provide variety and depth to the display of information. 

major_descriptions = [] -> Dictionary with all majors as keys and their descriptions and examples as values.
"""

major_descriptions = {
    "Biomedical Engineering": {
        "descriptions": [
            "Merge biology and engineering to develop medical devices, prosthetics, and imaging systems.",
            "Conduct research on biomaterials, biomechanics, and tissue engineering for healthcare solutions.",
            "Innovate in healthcare technology to improve patient care, diagnostics, and rehabilitation."
        ],
        "examples": [
            "Biomedical Device Engineer, Clinical Engineer, Biomaterials Scientist",
            "Medical Imaging Engineer, Bioinstrumentation Engineer, Tissue Engineer",
            "Rehabilitation Engineer, Biomechanics Researcher, Medical Robotics Engineer"
        ]
    },
    "Biology": {
        "descriptions": [
            "Investigate living organisms at molecular, cellular, and ecological levels.",
            "Explore genetics, evolution, physiology, and ecosystems through hands-on research.",
            "Apply biological knowledge to medicine, conservation, biotechnology, and environmental sciences."
        ],
        "examples": [
            "Biologist, Genetic Counselor, Environmental Scientist",
            "Lab Researcher, Microbiologist, Biotech Specialist",
            "Conservation Biologist, Professor, Biochemistry Researcher"
        ]
    },
    "Business": {
        "descriptions": [
            "Learn how organizations operate, including management, finance, marketing, and strategy.",
            "Explore entrepreneurship, operations, leadership, and decision-making in a corporate context.",
            "Focus on analytics, organizational behavior, and global business trends."
        ],
        "examples": [
            "Marketing Manager, Financial Analyst, Entrepreneur",
            "Business Consultant, Operations Manager, Accountant",
            "Project Manager, Investment Banker, HR Director"
        ]
    },
    "Chemical Engineering": {
        "descriptions": [
            "Use chemical processes to design materials, fuels, and pharmaceuticals.",
            "Optimize production systems and scale laboratory research to industrial applications.",
            "Develop sustainable manufacturing processes and innovations in energy, materials, and biotech."
        ],
        "examples": [
            "Process Engineer, Chemical Plant Manager, Pharmaceutical Engineer",
            "Materials Engineer, Petrochemical Engineer, Energy Engineer",
            "Biochemical Engineer, Nanotechnology Researcher, Environmental Engineer"
        ]
    },
    "Civil Engineering": {
        "descriptions": [
            "Plan, design, and construct infrastructure like bridges, roads, and buildings.",
            "Integrate environmental science and urban planning for sustainable communities.",
            "Manage construction projects, water resources, and transportation systems efficiently."
        ],
        "examples": [
            "Structural Engineer, Transportation Engineer, Construction Manager",
            "Geotechnical Engineer, Urban Planner, Environmental Engineer",
            "Water Resources Engineer, Surveyor, Municipal Engineer"
        ]
    },
    "Computational Science": {
        "descriptions": [
            "Use mathematical modeling and computer simulation to solve scientific and engineering problems.",
            "Develop algorithms to simulate physical, biological, and social systems.",
            "Apply high-performance computing to understand complex data-driven phenomena."
        ],
        "examples": [
            "Computational Scientist, Simulation Engineer, Research Scientist",
            "Climate Modeler, Bioinformatics Specialist, Computational Physicist",
            "Data Modeling Engineer, Systems Analyst, Scientific Software Developer"
        ]
    },
    "Computer Engineering": {
        "descriptions": [
            "Design computer hardware and embedded systems combining electrical engineering and computer science.",
            "Work on microprocessors, system architecture, and low-level software integration.",
            "Build high-performance computing devices, IoT systems, and custom electronics."
        ],
        "examples": [
            "Hardware Engineer, Embedded Systems Engineer, FPGA Engineer",
            "Systems Designer, Computer Architect, IoT Developer",
            "Firmware Engineer, AI Hardware Engineer, Robotics Hardware Developer"
        ]
    },
    "Computer Science": {
        "descriptions": [
            "Study algorithms, programming languages, and software development to build complex systems.",
            "Explore artificial intelligence, data structures, and computational theory.",
            "Work at the intersection of computation, logic, and data to solve modern challenges."
        ],
        "examples": [
            "Software Engineer, Data Scientist, Machine Learning Engineer",
            "AI Researcher, Backend Developer, Systems Architect",
            "DevOps Engineer, Cybersecurity Specialist, Game Developer"
        ]
    },
    "Cybersecurity": {
        "descriptions": [
            "Protect computer systems and networks from cyber threats and attacks.",
            "Study cryptography, network security, and risk management to safeguard digital assets.",
            "Design secure software, detect vulnerabilities, and respond to security incidents."
        ],
        "examples": [
            "Security Analyst, Penetration Tester, Cryptographer",
            "Security Engineer, Incident Response Specialist, Cybersecurity Consultant",
            "Network Security Architect, Forensics Specialist, Chief Information Security Officer (CISO)"
        ]
    },
    "Data Science": {
        "descriptions": [
            "Analyze large datasets to extract insights and inform decision-making.",
            "Use machine learning, statistics, and computing to model complex phenomena.",
            "Work in analytics, AI, or business intelligence to solve real-world problems."
        ],
        "examples": [
            "Data Scientist, Business Intelligence Analyst, Machine Learning Engineer",
            "Statistician, Quantitative Analyst, Research Scientist",
            "AI Developer, Data Engineer, Predictive Modeler"
        ]
    },
    "Electrical Engineering": {
        "descriptions": [
            "Design and analyze electrical systems, from electronics to large power grids.",
            "Study signals, circuits, electromagnetism, and communication technologies.",
            "Work on innovations in robotics, telecommunications, and energy systems."
        ],
        "examples": [
            "Power Systems Engineer, Electronics Engineer, Telecommunications Engineer",
            "Control Systems Engineer, Semiconductor Engineer, Embedded Systems Engineer",
            "Robotics Engineer, RF Engineer, Electric Vehicle Engineer"
        ]
    },
    "Engineering": {
        "descriptions": [
            "Solve real-world problems by designing structures, machines, and systems using math and science.",
            "Combine theory and practice across disciplines like mechanical, civil, and electrical engineering.",
            "Innovate through applied research and development to build technologies that shape our world."
        ],
        "examples": [
            "Mechanical Engineer, Civil Engineer, Electrical Engineer",
            "Industrial Engineer, Systems Engineer, Project Engineer",
            "Aerospace Engineer, Robotics Engineer, Manufacturing Engineer"
        ]
    },
    "Environmental Engineering": {
        "descriptions": [
            "Apply engineering principles to protect the environment and human health.",
            "Design solutions for water treatment, pollution control, and sustainable infrastructure.",
            "Integrate ecology, chemistry, and civil systems to build greener communities."
        ],
        "examples": [
            "Water Resources Engineer, Air Quality Engineer, Waste Management Engineer",
            "Sustainability Consultant, Environmental Project Manager, Remediation Engineer",
            "Climate Engineer, Regulatory Engineer, Environmental Scientist"
        ]
    },
    "Health Science": {
        "descriptions": [
            "Study anatomy, physiology, and health systems to support patient care.",
            "Learn about preventive medicine, research, and wellness in diverse populations.",
            "Prepare for careers in clinical practice, medical research, or public health."
        ],
        "examples": [
            "Nurse, Physician Assistant, Medical Researcher",
            "Physical Therapist, Public Health Specialist, Lab Technician",
            "Health Educator, Clinical Research Coordinator, Pharmacist"
        ]
    },
    "Mechanical Engineering": {
        "descriptions": [
            "Develop mechanical devices, from engines and HVAC systems to robots.",
            "Combine dynamics, thermodynamics, and materials science to engineer moving systems.",
            "Innovate in manufacturing, automotive, aerospace, and energy sectors."
        ],
        "examples": [
            "Automotive Engineer, HVAC Engineer, Robotics Engineer",
            "Design Engineer, Aerospace Engineer, Production Engineer",
            "Thermal Systems Engineer, Manufacturing Engineer, Mechatronics Engineer"
        ]
    },
    "Mechatronics Engineering": {
        "descriptions": [
            "Combine mechanics, electronics, and computing to build smart machines and robots.",
            "Work on control systems, automation, and sensor integration in modern devices.",
            "Innovate in robotics, automated manufacturing, and cyber-physical systems."
        ],
        "examples": [
            "Automation Engineer, Robotics Engineer, Control Systems Engineer",
            "Embedded Systems Developer, Mechatronics Designer, Smart Device Engineer",
            "Industrial Robotics Programmer, Autonomous Systems Developer, Sensor Engineer"
        ]
    },
    "Performing Arts": {
        "descriptions": [
            "Develop talent in acting, dance, music, or theater production for live performances.",
            "Experiment with storytelling, movement, and expression across stage and screen.",
            "Train in performance technique, stage design, and audience dynamics."
        ],
        "examples": [
            "Actor, Dancer, Stage Director",
            "Playwright, Choreographer, Voice Actor",
            "Theater Producer, Drama Teacher, Performance Coach"
        ]
    },
    "Psychology": {
        "descriptions": [
            "Understand human behavior, cognition, and emotion through scientific study.",
            "Apply psychological theories to clinical, social, and developmental contexts.",
            "Explore mental health, brain function, and therapeutic practices."
        ],
        "examples": [
            "Clinical Psychologist, Counselor, Behavioral Researcher",
            "School Psychologist, Organizational Psychologist, Therapist",
            "Neuropsychologist, Human Factors Specialist, Psychometrist"
        ]
    },
    "Visual Arts": {
        "descriptions": [
            "Explore mediums like painting, sculpture, digital art, and design.",
            "Focus on conceptual and technical skills to create meaningful visual work.",
            "Blend traditional and modern techniques in creative expression and visual storytelling."
        ],
        "examples": [
            "Graphic Designer, Illustrator, Photographer",
            "Animator, Art Director, Curator",
            "Fine Artist, Sculptor, Museum Specialist"
        ]
    },
    "Music": {
        "descriptions": [
            "Develop creativity in performance, composition, and music theory.",
            "Study different genres, instruments, and the history of music.",
            "Combine technical skill with artistic expression to build a career in music."
        ],
        "examples": [
            "Musician, Composer, Sound Engineer",
            "Conductor, Music Teacher, Producer",
            "Music Therapist, Arranger, Performer"
        ]
    },
    "Economics": {
        "descriptions": [
            "Analyze how resources are produced, distributed, and consumed in society.",
            "Use quantitative methods to study markets, trade, and policy impacts.",
            "Understand global economics, finance, and decision-making at institutional levels."
        ],
        "examples": [
            "Economist, Financial Analyst, Policy Advisor",
            "Market Researcher, Risk Analyst, Economic Consultant",
            "Investment Banker, Public Policy Analyst, Professor"
        ]
    },
    "Information Technology": {
        "descriptions": [
            "Manage IT infrastructure, networks, and system administration in organizations.",
            "Implement and maintain software, hardware, and user support systems.",
            "Solve business problems using technology, data management, and system design."
        ],
        "examples": [
            "IT Manager, Systems Administrator, Network Engineer",
            "Database Administrator, Help Desk Coordinator, IT Support Specialist",
            "Enterprise Architect, Cloud Solutions Architect, DevOps Engineer"
        ]
    }
}

