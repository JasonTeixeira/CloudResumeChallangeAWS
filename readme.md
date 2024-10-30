### **Static Website Hosting on AWS**

![AWS Cloud Portfolio](https://github.com/JasonTeixeira/CloudResumeChallangeAWS/blob/main/AWS%20Cloud%20Portfolio.png)

# **Hosting a Static Website on AWS with CloudFront and Route 53**

This project involves hosting a static website on **AWS S3**, serving the content through **CloudFront** for content delivery optimization, managing the domain with **Route 53**, and securing the site with **HTTPS using AWS Certificate Manager (ACM)**. This guide walks through each step, from buying the domain to setting up certificates, configuring DNS, and deploying the site on AWS.

---

## **Table of Contents**

1. [Project Overview](https://www.notion.so/12fa5fa99ece806e9502de4dee496a0a?pvs=21)
2. [Architecture](https://www.notion.so/12fa5fa99ece806e9502de4dee496a0a?pvs=21)
3. [Steps Undertaken](https://www.notion.so/12fa5fa99ece806e9502de4dee496a0a?pvs=21)
    - Buying the Domain
    - Configuring Route 53 Hosted Zone
    - Setting up the S3 Bucket
    - Configuring Bucket Policies
    - Creating the CloudFront Distribution
    - Configuring SSL with AWS Certificate Manager
    - Setting up DNS Records in Route 53
4. [Additional Considerations](https://www.notion.so/12fa5fa99ece806e9502de4dee496a0a?pvs=21)
5. [How to Test and Validate](https://www.notion.so/12fa5fa99ece806e9502de4dee496a0a?pvs=21)
6. [Conclusion](https://www.notion.so/12fa5fa99ece806e9502de4dee496a0a?pvs=21)

---

## **Project Overview**

The goal of this project is to **host a static website** on AWS while ensuring that the site is served via **HTTPS** with a custom domain (e.g., `jasonteixeira.com` and `www.jasonteixeira.com`). AWS provides **S3** for object storage, **CloudFront** as the content delivery network (CDN), **Route 53** for DNS management, and **Certificate Manager (ACM)** for generating and managing SSL certificates.

### **Objectives:**

- Host static content with AWS S3.
- Ensure global accessibility and performance using CloudFront.
- Use custom domains with Route 53 for DNS management.
- Secure the site using HTTPS.
- Automate redirection from HTTP to HTTPS and from `www` to the root domain.

---

## **Architecture**

### **High-Level Architecture Diagram**

```sql
sql
Copy code
[ S3 Bucket ]  <-- Origin for Static Files
      |
[ CloudFront Distribution ] <-- CDN with HTTPS Enabled
      |
[ Route 53 ] <-- DNS Management
      |
[ Custom Domain ] <-- HTTPS: jasonteixeira.com, www.jasonteixeira.com

```

- **S3 Bucket**: Stores static files (HTML, CSS, JS, etc.).
- **CloudFront**: Accelerates content delivery via edge locations.
- **Route 53**: Manages DNS and points the domain to CloudFront.
- **AWS Certificate Manager (ACM)**: Provides SSL/TLS certificates for secure HTTPS connections.

---

## **Steps Undertaken**

### **1. Buying the Domain**

We purchased the domain **jasonteixeira.com** directly from **Route 53** to ensure seamless integration with the AWS ecosystem. Route 53 automatically creates a **hosted zone** for the domain after purchase, which is required to manage DNS records.

---

### **2. Configuring Route 53 Hosted Zone**

After the domain purchase, a **hosted zone** was created in **Route 53**. This hosted zone will manage the DNS records for `jasonteixeira.com` and `www.jasonteixeira.com`. We added the following records:

- **A (Alias) Record**: Redirects the root domain to the CloudFront distribution.
- **A (Alias) Record for www**: Redirects `www.jasonteixeira.com` to the same CloudFront distribution.

---

### **3. Setting Up the S3 Bucket**

- Created an **S3 bucket** named `jasonteixeira-blog`.
- Enabled **static website hosting** in the bucket.
- Uploaded the static files (HTML, CSS, JS) to the S3 bucket.

---

### **4. Configuring Bucket Policies**

To allow CloudFront to access the S3 bucket content, we set the following **bucket policy**:

```json
json
Copy code
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::jasonteixeira-blog/*"
        }
    ]
}

```

This policy ensures that any user accessing the website via CloudFront can retrieve the objects in the S3 bucket.

---

### **5. Creating the CloudFront Distribution**

1. Created a **CloudFront distribution** with the S3 bucket as the **origin**.
2. Set the **viewer protocol policy** to redirect HTTP to HTTPS.
3. Added the **alternate domain names (CNAMEs)**:
    - `jasonteixeira.com`
    - `www.jasonteixeira.com`
4. Selected the SSL certificate from **ACM** to enable HTTPS.

---

### **6. Configuring SSL with AWS Certificate Manager**

1. Requested an SSL certificate via **AWS ACM** for both domains:
    - `jasonteixeira.com`
    - `www.jasonteixeira.com`
2. Validated the domain ownership using **DNS validation**.
3. ACM issued the certificates, which were then attached to the CloudFront distribution.

---

### **7. Setting Up DNS Records in Route 53**

After the CloudFront distribution was deployed, we added the **A (Alias) records** for the domain:

- **A Record for jasonteixeira.com** → Points to the CloudFront distribution.
- **A Record for [www.jasonteixeira.com](http://www.jasonteixeira.com/)** → Points to the same CloudFront distribution.

This ensures that both the root domain and the www subdomain resolve to the website hosted on CloudFront.

---

## **Additional Considerations**

- **HTTP to HTTPS Redirection**: Configured in CloudFront to ensure secure connections.
- **www to Non-www Redirection**: Route 53 ensures that both `www` and the root domain point to the same CloudFront distribution.
- **Cache Invalidation**: To ensure that the latest content is served, a cache invalidation request can be issued in CloudFront when files are updated.
- **Performance**: CloudFront improves performance by caching content at multiple edge locations globally.
- **Monitoring**: AWS CloudWatch can be integrated to monitor CloudFront metrics and S3 access logs.

---

## **How to Test and Validate**

1. **Test DNS Propagation:**
    - Use tools like **DNS Checker** to ensure that DNS records have propagated.
2. **Access the Website:**
    - Visit `https://jasonteixeira.com` and `https://www.jasonteixeira.com`.
    - Ensure the content loads correctly over HTTPS.
3. **Validate Redirection:**
    - Visit `http://jasonteixeira.com` and ensure it redirects to HTTPS.
    - Visit `http://www.jasonteixeira.com` and ensure it redirects to the root domain.
4. **Cache Validation:**
    - If content does not update, issue a **cache invalidation** request in CloudFront.

---

## **Conclusion**

This project successfully deployed a static website on AWS using S3, CloudFront, Route 53, and ACM. The architecture ensures high availability, security, and performance by leveraging CloudFront as a CDN and Route 53 for DNS management. With SSL certificates from ACM, the website serves content securely over HTTPS.

This setup is suitable for:

- Personal websites and portfolios.
- Static business websites.
- Documentation sites and blogs.

---


