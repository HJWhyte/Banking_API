**Infrastructure Choices**

**Main Application - Python FastAPI**
**
Containerization: Docker**
The main application will be hosted in a Docker container. Docker enables packaging applications and their dependencies into containers, ensuring consistency across environments. Once dockerized, the container images can be pushed to a container registry (e.g., Amazon ECS).

**Database: MongoDB Atlas**
MongoDB Atlas is a fully managed MongoDB service, offering scalability, automatic backups, and security features. A cluster can be set up and configured directly within the FastAPI application.

**Container Orchestration - Amazon EKS:**
EKS is a fully managed Kubernetes service, providing the benefits of Kubernetes without the operational overhead. It ensures scalability, flexibility, and easy management of containerized applications. An EKS cluster can be set up with the necessary worker nodes and the correct container image via ECS.

**Other AWS Services:**
**Application Load Balancer (ALB):** Can be used to distribute traffic across multiple targets to ensure high availability, and it can be configured within the EKS cluster.

**IAM Roles:** Can be established within EKS and Load Balancer to secure AWS services.

**CloudWatch:** Provides active monitoring and logging for the given AWS resources, helping track application performance and troubleshoot issues. It can be configured to monitor ECS and EKS cluster metrics. FastAPI logs can also be directly streamed to CloudWatch for centralized viewing.

**Linking of Services:**

**FastAPI and MongoDB**:
FastAPI connects to MongoDB Atlas using the connection string provided by MongoDB Atlas. Ensure network connectivity between FastAPI instances in the EKS cluster and the MongoDB Atlas cluster.

**FastAPI and AWS ALB:**
ALB routes incoming traffic to FastAPI services running in the EKS cluster. Set up Target Groups in ALB to direct traffic to the appropriate service.

**FastAPI and AWS IAM Roles:**
IAM roles associated with the EKS worker nodes grant permissions for the FastAPI application to interact with other AWS services. IAM roles for ALB enable communication between ALB and EKS.

**FastAPI and CloudWatch:**
FastAPI logs are streamed to CloudWatch for centralized logging. CloudWatch Alarms monitor metrics from the EKS and ECS clusters.





