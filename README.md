# Stock Management Multi-Tenant System

A **multi-tenant stock management web application** built with **Django**, designed for SaaS-style usage. The project implements role-based access control with a multi-schema architecture using **django-tenants**, allowing multiple organizations (tenants) to use the system securely with isolated data.

---

## **Project Overview**

This project is structured as a **multi-tenant SaaS application** with three user roles:

1. **Super Admin**
   - Creates and manages **admin users**.
   - Exists in the **public schema**.
   
2. **Admin**
   - Created by the Super Admin.
   - Automatically generates a **tenant** for their organization.
   - Can create **staff** and **customer users** within their tenant.
   - Can manage stocks/products for their tenant.

3. **Staff**
   - Created by Admin.
   - Can manage stock items and perform tenant-specific operations.

4. **Customer**
   - Created by Admin.
   - Can view products or stock items (based on business logic).

---

## **Key Features**

- **Multi-Tenant Architecture**
  - Each admin has a **separate tenant schema** in PostgreSQL.
  - Data for each tenant is fully isolated.
  
- **Role-Based Access Control**
  - Different permissions for **Super Admin, Admin, Staff, and Customer**.

- **Stock Management**
  - Admins and staff can **create, update, and list products**.
  - Each stock item is tied to the **tenant schema**.

- **JWT Authentication**
  - API endpoints secured using **JWT Bearer Tokens**.
  - Only authenticated users can access tenant-specific resources.

- **Automatic Tenant Creation**
  - When an Admin is created, a **tenant and schema** are automatically created.
  - Domain and tenant association is managed automatically.

- **Django REST Framework API**
  - CRUD operations for stock items.
  - Tenant-specific API access based on user roles.

---

## **Technology Stack**

- **Backend:** Django 5, Django REST Framework
- **Database:** PostgreSQL (with multi-schema support using django-tenants)
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Python Version:** 3.13
- **Libraries:** django-tenants, djangorestframework, psycopg2, django-cors-headers

---

## **Project Structure**

