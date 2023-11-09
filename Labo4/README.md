# LAB 4: S3 ACCESS CONTROL
Authors : Valzino Benjamin, Urizar Pablo

### TASK 1: ACCESSING THE CONSOLE AS AN IAM USER
**2. Open the Amazon EC2 console. Choose EC2 Dashboard. Many API Error messages display. This is expected.**
![task1_2.png](screenshots%2Ftask1_2.png)

**3. Attempt some actions in the Amazon EC2 console :**
![task1_3.png](screenshots%2Ftask1_3.png)

A message displays "You are not authorized to perform this operation" as expected.

**4. To explore what you can access in the Amazon S3 console, open it :**
![task1_4.png](screenshots%2Ftask1_4.png)

The `Access` column displays the message "Insufficient permissions" for all the three buckets as expected.

### TASK 2: ANALYZING THE IDENTITY-BASED POLICY APPLIED TO THE IAM USER
Review the IAM policy details.
![task2_2.png](screenshots%2Ftask2_2.png)

DeveloperGroupPolicy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "cloudformation:Describe*",
                "cloudformation:Get*",
                "cloudformation:List*",
                "iam:Describe*",
                "iam:GetAccountAuthorizationDetails",
                "iam:GetGroup",
                "iam:GetGroupPolicy",
                "iam:GetPolicy",
                "iam:GetPolicyVersion",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "iam:GetUser",
                "iam:GetUserPolicy",
                "iam:List*",
                "logs:Desc*",
                "logs:Get*",
                "logs:List*",
                "s3:CreateBucket",
                "s3:ListAllMyBuckets",
                "s3:ListBucket",
                "s3:PutAccountPublicAccessBlock",
                "s3:PutBucketOwnershipControls",
                "s3:PutBucketPublicAccessBlock",
                "sts:AssumeRole"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```

### TASK 3: ATTEMPTING WRITE-LEVEL ACCESS TO AWS SERVICES

**1. Attempt to create an S3 bucket :**
![task3_1.png](screenshots%2Ftask3_1.png)

**2. Access the bucket and attempt to upload an object. A message displays `Upload failed` as expected :**
![task3_2.png](screenshots%2Ftask3_2.png)

**3. Review the policy details for Amazon S3 access :**

We were able to create the S3 bucket thanks to the S3 permission `s3:CreateBucket`. We can also list the S3 buckets
created thanks to `s3:ListAllMyBuckets`. Finally, we can list the content of a bucket with `s3:ListBucket`.

The permission that is missing in our policy for us to be able to upload objects to the bucket is `s3:PutObject`.
Additionally, we could also add `s3:GetObject` to allow us to retrieve an object from un S3 bucket. Since they were
not explicity allowed they are denied by default. 

### TASK 4: ASSUMING AN IAM ROLE AND REVIEWING A RESOURCE-BASED POLICY

**1. Try to download an object from the buckets that were created during lab setup :**
![task4_1.png](screenshots%2Ftask4_1.png)

**2. Assume the BucketsAccessRole IAM role in the console :**

<img src='screenshots/task4_2.png' width='300'>

**3. Try to download an object from Amazon S3 again :**
As expected, we were able to download the image since the S3 permission `s3:GetObject` on `bucket1` is allowed.
![Image2-GrD.jpg](Image2-GrD.jpg)

**4. Test IAM access with the BucketsAccessRole :**
As expected, an error message displays that we no longer have permissions to view the IAM user groups page because
BucketsAccessRole does not have the iam:ListGroups action applied to it.
![task4_4.png](screenshots%2Ftask4_4.png)

`AccessDenied` error page appears as expected.

**5. Assume the devuser role again, and test access to the user groups page :**
Now that we unassumed the BucketsAccessRole, we have the permissions that are assigned to the devuser IAM user
(through this user's membership in the DeveloperGroup). We are able to view the user groups page again.
![task4_5.png](screenshots%2Ftask4_5.png)

**6. Analyze the IAM policy that is associated with the BucketsAccessRole :**
![task4_6.png](screenshots%2Ftask4_6.png)

**7. Save a copy of the GrantBucket1Access policy to your computer**

**8. Complete your analysis of the BucketsAccessRole details :**
![task4_8.png](screenshots%2Ftask4_8.png)

**9. Assume the BucketsAccessRole, and try to upload an image to bucket2 :**
![task4_9.png](screenshots%2Ftask4_9.png)

### TASK 5: UNDERSTANDING RESOURCE-BASED POLICIES

### TASK 6: FIND A WAY TO UPLOAD AN OBJECT TO BUCKET3

### TASK 7: DESIGN AND IMPLEMENT PERMISSION POLICIES FOR S3

