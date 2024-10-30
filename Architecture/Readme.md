### **Explanation of the CloudFormation Template**

1. **S3 Bucket:**
    - This bucket is configured with public read access to host static website content, with `index.html` as the home page and `404.html` for errors.
    - The `WebsiteBucketPolicy` grants public read permissions.
2. **ACM Certificate:**
    - The certificate is created for `jasonteixeira.com` and `www.jasonteixeira.com` with **DNS validation**.
3. **CloudFront Distribution:**
    - CloudFront serves content from the S3 bucket with **HTTPS** enforced.
    - A certificate from ACM is applied to the CloudFront distribution for secure communication.
4. **Route 53 Hosted Zone & A Records:**
    - An A-record is created for the root domain (`jasonteixeira.com`) and `www` subdomain, both pointing to the CloudFront distribution using **Alias Target**.
5. **Deployment Process:**
    - When this CloudFormation template is applied, it sets up the entire infrastructure and integrates the S3 bucket with CloudFront and Route 53.

---

### **How to Deploy the CloudFormation Template**

1. Save the above YAML content to a file named **`static-website.yaml`**.
2. Use the AWS CLI to create a CloudFormation stack:
    
    ```bash
    bash
    Copy code
    aws cloudformation create-stack --stack-name static-website-stack --template-body file://static-website.yaml --capabilities CAPABILITY_NAMED_IAM
    
    ```
    
3. Wait for the stack to be deployed:
    
    ```bash
    bash
    Copy code
    aws cloudformation wait stack-create-complete --stack-name static-website-stack
    
    ```
    

---

### **Additional Considerations:**

- **Content Deployment:** Upload your static content (like `index.html`) to the S3 bucket.
- **Cache Invalidation:** Invalidate CloudFront cache when content changes using:
    
    ```bash
    bash
    Copy code
    aws cloudfront create-invalidation --distribution-id <distribution-id> --paths "/*"
    
    ```
    
- **Monitor Costs:** Monitor usage to control S3 and CloudFront costs.
