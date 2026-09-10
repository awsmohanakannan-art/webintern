"""
Domain-Specific 4-Week Internship Task Blueprint Engine for WebIntern Platform.
Generates tailored weekly milestones based on internship track domain.
"""

def get_domain_tasks(title, sector_name=""):
    t_lower = title.lower()
    clean_title = title.replace(' Internship', '')
    
    if 'cloud' in t_lower or 'devops' in t_lower:
        return [
            (1, "Week 1: Cloud Infrastructure & Virtual Machine Provisioning (AWS / Azure / GCP)",
             f"Configure cloud IAM security roles, launch virtual compute instances, set up VPC networking, Security Groups, and SSH access keys for {clean_title}.",
             "Cloud Infrastructure Architecture Diagram PDF & VPC Provisioning Setup Report",
             "1. Log into Cloud Management Console.\n2. Configure IAM roles & security policies.\n3. Provision Linux virtual machine instance.\n4. Configure Security Group firewall rules.",
             "Proper VPC configuration, secure SSH key management, clean architectural diagram."),
            (2, "Week 2: Cloud Storage, Object Stores & Managed Relational Database (S3 & RDS)",
             "Deploy S3 Object Buckets with CORS policies, configure lifecycle rules, and set up a managed Relational Database instance (PostgreSQL/MySQL RDS).",
             "Database Connection Test Script & Storage Architecture Configuration Log PDF",
             "1. Provision cloud object storage bucket.\n2. Configure bucket access policies.\n3. Launch managed RDS database.\n4. Verify backend database connectivity.",
             "Correct storage bucket access policies, database schema deployment, security compliance."),
            (3, "Week 3: Containerization & Microservices Orchestration (Docker & Kubernetes EKS/AKS)",
             "Build multi-stage Docker container images, push to container registry (ECR/DockerHub), and write Kubernetes Deployment & Service Manifest YAML files.",
             "Dockerfile, K8s Deployment Manifest YAMLs, and Container Status Log PDF",
             "1. Containerize application service.\n2. Push image to container registry.\n3. Write K8s Deployment & Service manifests.\n4. Deploy microservice to Kubernetes cluster.",
             "Optimized Dockerfile layer sizes, valid K8s manifests, zero crash-loop errors."),
            (4, "Week 4: Serverless Architectures, CI/CD Pipeline & Cloud Capstone Release",
             "Build serverless functions (AWS Lambda/Azure Functions), configure GitHub Actions CI/CD pipeline, and perform final cloud infrastructure deployment.",
             "Final Cloud DevOps Architecture Capstone Report PDF, GitHub Actions Workflow YAML & Live Endpoint URL",
             "1. Implement serverless function handler.\n2. Set up GitHub Actions workflow.\n3. Trigger automated build & deploy.\n4. Compile final capstone documentation.",
             "Automated CI/CD pipeline execution, live cloud endpoint response, high documentation quality.")
        ]
    elif 'full stack' in t_lower or 'web development' in t_lower or 'software development' in t_lower or 'frontend' in t_lower or 'backend' in t_lower:
        return [
            (1, "Week 1: Modern Responsive Frontend UI/UX Design (HTML5, CSS3, JavaScript ES6+)",
             f"Design responsive client-side user interfaces with component layouts, flexbox/grid, and semantic HTML for {clean_title}.",
             "Frontend Source Code Repository Link & Wireframe Documentation PDF",
             "1. Wireframe UI components.\n2. Code responsive layouts using modern CSS.\n3. Implement client-side DOM interactions.\n4. Test cross-browser responsiveness.",
             "Semantic HTML structure, mobile responsiveness, clean UI design."),
            (2, "Week 2: Backend RESTful API Architecture & Relational Database Design",
             "Develop modular REST API endpoints (Node.js/Express or Python/Flask), configure ORM models, and implement CRUD database operations.",
             "Postman API Collection Export JSON & Backend API Server Repository",
             "1. Design database schema models.\n2. Implement REST controller routes.\n3. Connect relational database.\n4. Validate endpoint HTTP status codes.",
             "Proper RESTful route conventions, error handling middleware, robust database modeling."),
            (3, "Week 3: User Authentication, State Management & Full-Stack API Integration",
             "Implement JWT/OAuth authentication, password hashing, protected routes, and integrate frontend state management with backend APIs.",
             "Authentication Integration Code & End-to-End Test Suite Execution Report PDF",
             "1. Add password hashing & JWT token issuance.\n2. Create authentication middleware.\n3. Connect client fetch calls.\n4. Manage state updates.",
             "Secure token handling, protected endpoint validation, smooth user experience."),
            (4, "Week 4: Production Deployment, Containerization & Full-Stack Capstone Release",
             "Package web app using Docker, deploy to cloud hosting, optimize database queries, and finalize production documentation.",
             "Live Web Platform URL, Architecture Capstone Report PDF & GitHub Repository",
             "1. Create Docker container build.\n2. Deploy app to cloud environment.\n3. Perform performance tuning.\n4. Compile capstone documentation.",
             "Live working application URL, complete documentation, zero console errors.")
        ]
    elif 'artificial intelligence' in t_lower or 'machine learning' in t_lower or 'deep learning' in t_lower or 'data science' in t_lower or 'analytics' in t_lower:
        return [
            (1, "Week 1: Data Wrangling, EDA & Feature Engineering (Pandas, NumPy)",
             f"Perform exploratory data analysis on raw datasets, clean missing data, encode categorical variables, and generate statistical plots for {clean_title}.",
             "Jupyter Notebook (.ipynb) & Data Analysis Insights Report PDF",
             "1. Import raw dataset.\n2. Clean missing & duplicate values.\n3. Perform univariate/bivariate EDA.\n4. Engineer predictive features.",
             "Thorough data cleaning, clear statistical visualizations, logical feature selection."),
            (2, "Week 2: Supervised & Unsupervised Machine Learning Model Training",
             "Implement regression, classification (Random Forest, XGBoost), and clustering models; evaluate accuracy, precision, recall, and F1-score.",
             "ML Model Training Scripts, Confusion Matrix Plots & Evaluation Report PDF",
             "1. Split train/test datasets.\n2. Train multiple ML algorithms.\n3. Tune hyperparameters.\n4. Generate ROC/AUC metrics.",
             "High model accuracy/generalization, proper cross-validation, clear metric comparison."),
            (3, "Week 3: Neural Networks, Deep Learning & PyTorch/TensorFlow Frameworks",
             "Build Convolutional Neural Networks (CNN) or Recurrent Neural Networks (RNN) for complex pattern recognition and sequential data processing.",
             "Deep Learning Architecture Code & Loss/Accuracy Training Curve Log PDF",
             "1. Design neural network layers.\n2. Define loss function & optimizer.\n3. Train model with early stopping.\n4. Plot training loss curves.",
             "Effective network architecture, convergence of loss function, zero overfitting."),
            (4, "Week 4: MLOps Deployment, FastAPI Inference Service & Capstone Model Release",
             "Serialize trained models, expose RESTful inference endpoints using FastAPI/Streamlit, and prepare model card documentation.",
             "Live Interactive ML Demo Web App URL, Model Performance Summary PDF & Code Repository",
             "1. Export trained model file.\n2. Build FastAPI inference route.\n3. Deploy Streamlit user interface.\n4. Document model performance.",
             "Functional real-time prediction endpoint, clean UI demo, complete capstone documentation.")
        ]
    elif 'cybersecurity' in t_lower or 'ethical hacking' in t_lower or 'cyber' in t_lower:
        return [
            (1, "Week 1: Network Traffic Analysis, Protocol Assessment & Wireshark Inspection",
             f"Analyze TCP/IP packets, inspect SSL/TLS handshakes, identify unencrypted traffic vulnerabilities, and audit firewall configurations in {clean_title}.",
             "Packet Capture Analysis (.pcap) Audit Report PDF & Security Log",
             "1. Capture live network traffic.\n2. Filter TCP/UDP streams.\n3. Inspect packet headers.\n4. Document security gaps.",
             "Accurate protocol analysis, identification of security anomalies, clear reporting."),
            (2, "Week 2: Vulnerability Scanning, Port Enumeration & Threat Assessment (Nmap)",
             "Conduct network reconnaissance, scan active hosts, discover open ports, identify CVE vulnerabilities, and prioritize security risks.",
             "Nmap Vulnerability Assessment Report PDF & Remediation Action Plan",
             "1. Execute target host discovery.\n2. Run service version scans.\n3. Match CVE database vulnerabilities.\n4. Rank threat severity levels.",
             "Comprehensive host scanning, accurate CVE classification, prioritized remediation plan."),
            (3, "Week 3: Web Application Penetration Testing & OWASP Top 10 Exploitation",
             "Test web application security against SQL Injection, Cross-Site Scripting (XSS), CSRF, and broken access controls in a controlled environment.",
             "Web Vulnerability Audit Report PDF & Code Hardening Guidelines",
             "1. Test input sanitization.\n2. Execute SQLi & XSS payloads.\n3. Verify session management.\n4. Formulate code fixes.",
             "Demonstrated understanding of OWASP risks, valid POC exploits, actionable fix guidelines."),
            (4, "Week 4: Incident Response, Cryptographic Hardening & Security Audit Capstone",
             "Formulate incident response playbooks, configure AES/RSA encryption mechanisms, conduct final security audit, and document hardening policies.",
             "Executive Cybersecurity Audit Capstone Report PDF & Hardening Checklist",
             "1. Draft incident response plan.\n2. Implement cryptographic controls.\n3. Conduct re-assessment audit.\n4. Finalize executive security report.",
             "Professional incident response structure, sound cryptographic policies, executive quality report.")
        ]
    elif 'generative' in t_lower or 'llm' in t_lower or 'prompt' in t_lower:
        return [
            (1, "Week 1: Prompt Engineering Strategies, Tokenization & LLM API Integration",
             f"Implement zero-shot, few-shot, and chain-of-thought prompt templates using OpenAI / Anthropic APIs and analyze token consumption for {clean_title}.",
             "Prompt Engineering Evaluation Notebook & API Integration Log PDF",
             "1. Set up API credentials.\n2. Design structured system prompts.\n3. Compare reasoning techniques.\n4. Measure token efficiency.",
             "Effective prompt structure, minimal hallucination, clear token cost analysis."),
            (2, "Week 2: Retrieval-Augmented Generation (RAG) & Vector Database Indexing",
             "Build RAG pipeline by chunking unstructured documents, generating text embeddings, and querying vector databases (ChromaDB/Pinecone).",
             "Vector Indexing Code Repository & RAG Query Performance Log PDF",
             "1. Extract document text.\n2. Generate vector embeddings.\n3. Index into ChromaDB.\n4. Perform semantic similarity search.",
             "Accurate context retrieval, fast vector query responses, high relevance scores."),
            (3, "Week 3: Autonomous AI Agents, Tool Calling & LangChain Framework",
             "Develop multi-agent workflows using LangChain / AutoGen with function calling capabilities for external API integration.",
             "AI Agent Workflow Code & Execution Trace Logs PDF",
             "1. Define agent tools & schemas.\n2. Implement reasoning loop.\n3. Connect external web search/math tools.\n4. Validate agent decisions.",
             "Robust agent decision loops, proper error handling on tool calls, execution safety."),
            (4, "Week 4: Fine-Tuning Open Source LLMs, Model Guardrails & Capstone App Release",
             "Fine-tune open-source models with QLoRA on specialized datasets, implement safety guardrails, and deploy Streamlit web UI.",
             "Live GenAI Web App URL, Fine-Tuning Performance Report PDF & GitHub Repository",
             "1. Format fine-tuning dataset.\n2. Train model with QLoRA.\n3. Add output guardrails.\n4. Deploy Streamlit interface.",
             "Functional interactive GenAI demo, verified guardrails, complete capstone documentation.")
        ]
    elif 'embedded' in t_lower or 'iot' in t_lower or 'robotics' in t_lower or 'vlsi' in t_lower or 'electrical' in t_lower or 'mechanical' in t_lower or 'civil' in t_lower:
        return [
            (1, "Week 1: System Design, Component Specification & Circuit/CAD Modeling",
             f"Perform technical requirements analysis, select hardware/software components, and design initial 3D/Schematic models for {clean_title}.",
             "Schematic Diagram / CAD Model Documentation PDF & Component BOM",
             "1. Review design constraints.\n2. Draft schematic/CAD layouts.\n3. Perform load/power calculations.\n4. Compile Bill of Materials.",
             "Accurate engineering calculations, clear schematic/CAD drawings, complete BOM."),
            (2, "Week 2: Firmware Programming, Simulation & Subsystem Integration",
             "Develop embedded C/C++ firmware or simulation scripts, configure sensor/actuator interfaces, and test subsystem communication.",
             "Firmware Source Code Repository & Simulation Results Log PDF",
             "1. Write sensor driver code.\n2. Run SPICE/MATLAB simulations.\n3. Calibrate signal data.\n4. Verify control loops.",
             "Clean modular firmware code, accurate simulation validation, stable control loops."),
            (3, "Week 3: System Optimization, Prototype Calibration & Stress Testing",
             "Perform thermal/stress testing, optimize power consumption or structural loads, and refine control algorithms under operational conditions.",
             "Test Execution Log & Stress Analysis Report PDF",
             "1. Run load/stress tests.\n2. Monitor power/thermal output.\n3. Tune algorithm parameters.\n4. Fix failure edge cases.",
             "Rigorous testing documentation, verified stability margins, effective tuning."),
            (4, "Week 4: Final Hardware/Software Capstone Validation & Video Demonstration",
             "Finalize complete engineering documentation, compile technical specifications, record functional demonstration, and submit capstone.",
             "Final Engineering Capstone Report PDF, Video Demonstration Link & Source Package",
             "1. Assemble final prototype data.\n2. Record video demonstration.\n3. Prepare user manual.\n4. Submit complete capstone package.",
             "Comprehensive engineering report, clear video demonstration, professional presentation.")
        ]
    elif 'marketing' in t_lower or 'business' in t_lower or 'management' in t_lower or 'hr' in t_lower or 'finance' in t_lower:
        return [
            (1, "Week 1: Market Research, Competitive Analysis & Strategic Positioning",
             f"Conduct market research, analyze competitor strategies, identify target audience personas, and define strategic positioning for {clean_title}.",
             "Market Research & Competitor Analysis Report PDF",
             "1. Gather industry market data.\n2. Perform SWOT & PESTLE analysis.\n3. Map customer personas.\n4. Define value proposition.",
             "Data-driven market insights, clear SWOT analysis, realistic customer personas."),
            (2, "Week 2: Strategy Execution, Campaign Design & Financial/Operational Planning",
             "Develop end-to-end execution roadmap, design multi-channel marketing campaigns or financial models, and set key KPI benchmarks.",
             "Campaign Architecture & Financial Model Spreadsheet / Report PDF",
             "1. Formulate campaign messaging.\n2. Build financial projection models.\n3. Establish funnel conversion targets.\n4. Draft operational timeline.",
             "Feasible campaign strategy, accurate financial formulas, actionable KPIs."),
            (3, "Week 3: Campaign Optimization, Performance Analytics & Conversion Tuning",
             "Analyze campaign performance metrics, perform A/B test analysis, optimize customer acquisition cost (CAC) and customer lifetime value (LTV).",
             "Performance Analytics Summary & Optimization Log PDF",
             "1. Track campaign funnel metrics.\n2. Analyze conversion bottlenecks.\n3. Run ROI sensitivity tests.\n4. Refine channel allocation.",
             "Rigor of metric calculations, clear channel recommendations, actionable insights."),
            (4, "Week 4: Executive Strategy Capstone Pitch & Board Recommendation",
             "Synthesize strategy findings, build executive presentation deck, record strategy pitch video, and submit final capstone.",
             "Executive Strategy Capstone Deck PDF, Video Pitch Link & Strategy Brief",
             "1. Compile final strategy deck.\n2. Record executive pitch video.\n3. Draft implementation roadmap.\n4. Submit capstone package.",
             "Polished executive presentation, compelling pitch video, strategic depth.")
        ]
    else:
        return [
            (1, "Week 1: Industry Standards, Domain Fundamentals & Baseline Proposal",
             f"Conduct foundational research in {clean_title}, analyze industry frameworks, and submit baseline technical proposal.",
             "Technical Proposal & Literature Review Report PDF",
             "1. Review domain literature.\n2. Identify key problem statement.\n3. Formulate project scope.\n4. Submit proposal PDF.",
             "Clear problem formulation, realistic project scope, quality documentation."),
            (2, "Week 2: Module Development & Practical Implementation",
             f"Execute core practical deliverables, build system components, and implement domain methodology for {clean_title}.",
             "Module Deliverables Package & Technical Implementation Log PDF",
             "1. Develop core module components.\n2. Apply domain techniques.\n3. Log implementation steps.\n4. Document initial results.",
             "High quality implementation, adherence to project scope, thorough logging."),
            (3, "Week 3: Performance Evaluation, Refinement & Reviewer Feedback Integration",
             f"Perform rigorous testing, refine project deliverables, resolve technical issues, and incorporate mentor evaluation feedback for {clean_title}.",
             "Performance Evaluation Report & Optimization Log PDF",
             "1. Execute test scenarios.\n2. Measure performance metrics.\n3. Implement reviewer feedback.\n4. Refine deliverable outputs.",
             "Thorough evaluation testing, effective feedback implementation, high accuracy."),
            (4, "Week 4: Final Capstone Finalization & Portfolio Presentation",
             f"Finalize project documentation, compile technical capstone, record presentation video, and submit portfolio for certification in {clean_title}.",
             "Final Capstone Portfolio PDF, Video Walkthrough Link & Source Artifacts",
             "1. Assemble final portfolio documentation.\n2. Record technical walkthrough.\n3. Prepare executive summary.\n4. Submit capstone package.",
             "Comprehensive capstone documentation, clear presentation video, high professional standard.")
        ]
