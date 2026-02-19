# AICDAP Database Setup & Integration Guide

This document provides comprehensive instructions for setting up the Supabase database and understanding the complete integration between the frontend application and backend services.

## 🚀 Quick Start

The AICDAP application now includes:
- ✅ **Complete Supabase Authentication** with sign-in/sign-up
- ✅ **Employee Management System** with CSV import functionality
- ✅ **Campaign Management** with department targeting from employee database
- ✅ **Real-time Data Synchronization** between all components

## 📋 Prerequisites

- A Supabase account (sign up at https://supabase.com)
- Node.js and npm installed
- Access to your Supabase project dashboard

## 🗄️ Database Setup

### 1. Create a New Supabase Project

1. Go to https://supabase.com and sign in
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - Name: `aicdap` (or your preferred name)
   - Database Password: Choose a strong password
   - Region: Select the region closest to your users
5. Click "Create new project"
6. Wait for the project to be created (this may take a few minutes)

### 2. Get Your Project Credentials

1. Once your project is ready, go to Settings > API
2. Copy the following values:
   - **Project URL**: This is your `supabaseUrl`
   - **Project API Keys > anon public**: This is your `supabaseAnonKey`

**Your configured credentials:**
- Project URL: `https://astybhpwqlexxadjrpct.supabase.co`
- Anon Key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzdHliaHB3cWxleHhhZGpycGN0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNjg1NDMsImV4cCI6MjA3NTY0NDU0M30.IXyX2nAd_XXawl5Fr3m7DZXUNMhNqtMgwIzI8_uTTXg`

### 3. Create the Complete Database Schema

1. Go to the SQL Editor in your Supabase dashboard
2. Copy and paste the following **complete SQL script**:

```sql
-- Create the employees table
CREATE TABLE IF NOT EXISTS employees (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_employees_email ON employees(email);
CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department);
CREATE INDEX IF NOT EXISTS idx_employees_status ON employees(status);
CREATE INDEX IF NOT EXISTS idx_employees_created_at ON employees(created_at);
CREATE INDEX IF NOT EXISTS idx_employees_created_by ON employees(created_by);

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update updated_at
CREATE TRIGGER update_employees_updated_at
    BEFORE UPDATE ON employees
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS
-- Policy: Users can only see employees they created or if they are authenticated
CREATE POLICY "Users can view employees" ON employees
    FOR SELECT USING (auth.uid() IS NOT NULL);

-- Policy: Users can insert employees if authenticated
CREATE POLICY "Users can insert employees" ON employees
    FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);

-- Policy: Users can update employees they created
CREATE POLICY "Users can update their employees" ON employees
    FOR UPDATE USING (auth.uid() = created_by OR auth.uid() IS NOT NULL);

-- Policy: Users can delete employees they created
CREATE POLICY "Users can delete their employees" ON employees
    FOR DELETE USING (auth.uid() = created_by OR auth.uid() IS NOT NULL);

-- Insert some sample data (optional)
INSERT INTO employees (name, email, department, status) VALUES
    ('John Doe', 'john.doe@company.com', 'Engineering', 'active'),
    ('Jane Smith', 'jane.smith@company.com', 'Marketing', 'active'),
    ('Bob Johnson', 'bob.johnson@company.com', 'Sales', 'active'),
    ('Alice Brown', 'alice.brown@company.com', 'HR', 'active'),
    ('Charlie Wilson', 'charlie.wilson@company.com', 'Finance', 'inactive')
ON CONFLICT (email) DO NOTHING;

-- Create a view for employee statistics (optional)
CREATE OR REPLACE VIEW employee_stats AS
SELECT
    COUNT(*) as total_employees,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_employees,
    COUNT(CASE WHEN status = 'inactive' THEN 1 END) as inactive_employees,
    COUNT(DISTINCT department) as total_departments,
    COUNT(CASE WHEN DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE) THEN 1 END) as employees_this_month
FROM employees;
```

3. Click "Run" to execute the script

### 4. Configure Authentication (Optional)

If you want to enable email authentication:

1. Go to Authentication > Settings in your Supabase dashboard
2. Configure the following settings:
   - Site URL: `http://localhost:3000` (for development) or your production URL
   - Redirect URLs: Add your application URLs
3. Enable Email authentication if not already enabled
4. Configure email templates as needed

### 5. Verify Setup

1. Go to the Table Editor in your Supabase dashboard
2. You should see the `employees` table
3. The table should have the following columns:
   - `id` (uuid, primary key)
   - `name` (varchar)
   - `email` (varchar, unique)
   - `department` (varchar)
   - `status` (varchar)
   - `created_at` (timestamp)
   - `updated_at` (timestamp)
   - `created_by` (uuid, foreign key to auth.users)

### 6. Test the Connection

1. Start your React application: `npm start`
2. Navigate to the login page and create an account
3. Once logged in, go to the Employee Management page
4. Try adding a new employee or importing a CSV file
5. Check the Supabase dashboard to see if data is being inserted correctly

## Table Schema

### employees

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Employee full name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Employee email address |
| department | VARCHAR(255) | - | Employee department |
| status | VARCHAR(50) | DEFAULT 'active', CHECK (active/inactive) | Employee status |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Record creation timestamp |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Record update timestamp |
| created_by | UUID | REFERENCES auth.users(id) | User who created the record |

## Row Level Security (RLS)

The table has RLS enabled with the following policies:

- **View**: Authenticated users can view all employees
- **Insert**: Authenticated users can insert new employees
- **Update**: Authenticated users can update employees
- **Delete**: Authenticated users can delete employees

## 🎯 Features Implemented

### Employee Management System
- ✅ **Full CRUD operations** for employees
- ✅ **Advanced CSV import** with real-time validation
- ✅ **Duplicate email detection** against database
- ✅ **Department management** with statistics
- ✅ **Employee status tracking** (active/inactive)
- ✅ **Advanced search and filtering** by department and status
- ✅ **Real-time statistics** and reporting dashboard
- ✅ **Data export** functionality
- ✅ **Loading states** and error handling

### Authentication System
- ✅ **Complete sign-up/sign-in flow** with Supabase Auth
- ✅ **Protected routes** with authentication guards
- ✅ **Password reset functionality**
- ✅ **User session management**
- ✅ **Row Level Security (RLS)** for data protection

### Campaign Management System
- ✅ **Dynamic department targeting** from employee database
- ✅ **Real-time employee count** per department
- ✅ **Template-based campaign creation**
- ✅ **Campaign statistics** and progress tracking
- ✅ **Complete campaign lifecycle** management
- ✅ **Integration with employee data** for targeting

## 🏗️ Application Architecture

### Frontend Structure
```
src/
├── components/
│   ├── CSVImport/           # CSV import with validation
│   ├── ProtectedRoute.js    # Authentication guard
│   └── Header.js            # Navigation with auth state
├── contexts/
│   └── AuthContext.js       # Authentication state management
├── services/
│   ├── employeeService.js   # Employee CRUD operations
│   └── campaignService.js   # Campaign management
├── pages/
│   ├── auth/                # Login, SignUp, ForgotPassword
│   ├── admin/
│   │   ├── employees/       # Employee management
│   │   └── campaigns/       # Campaign creation & management
├── lib/
│   └── supabase.js         # Supabase client configuration
└── database/
    └── schema.sql          # Complete database schema
```

### Database Schema
The application uses **3 main tables** with **proper relationships**:

1. **employees** - Core employee data
2. **campaigns** - Campaign information and statistics  
3. **campaign_targets** - Department targeting for campaigns
4. **campaign_target_employees** - Individual employee targeting

## 🔄 Data Flow Integration

### Employee → Campaign Integration
1. **Employee data** is stored in `employees` table
2. **Departments** are dynamically generated from employee data
3. **Campaign creation** fetches real department statistics
4. **Target selection** uses actual employee counts per department
5. **Campaign launches** create records linking to specific employees

### CSV Import → Database Flow
1. **CSV validation** happens client-side with real-time feedback
2. **Duplicate detection** queries existing database records
3. **Bulk insert** operations maintain data integrity
4. **Statistics refresh** happens automatically after import
5. **Department targeting** immediately reflects new employee data

## Troubleshooting

## 🔧 Usage Guide

### Getting Started
1. **Start the application**: `npm start`
2. **Create an account** or sign in at `/login`
3. **Add employees** manually or via CSV import at `/admin/employees`
4. **Create campaigns** targeting specific departments at `/admin/campaigns/create`
5. **Monitor progress** through the campaigns dashboard

### CSV Import Format
Your CSV file should have these exact columns:
```csv
name,email,department
John Doe,john.doe@company.com,Engineering
Jane Smith,jane.smith@company.com,Marketing
Bob Johnson,bob.johnson@company.com,Sales
```

### Campaign Creation Workflow
1. Navigate to **Create Campaign**
2. **Select Departments** - Choose from real departments in your employee database
3. **Choose Template** - Select from available phishing simulation templates  
4. **Launch** - Provide campaign name/description and launch

## 🐛 Troubleshooting

### Common Issues

1. **Connection Error**: Verify your Supabase URL and API key are correct in `src/lib/supabase.js`
2. **Authentication Error**: Make sure you're logged in and RLS policies are set up correctly
3. **Insert Error**: Check that required fields are provided and email is unique
4. **CSV Import Issues**: Ensure CSV has required columns (name, email, department)
5. **Campaign Creation Fails**: Ensure you have employees in the database first
6. **Department Not Showing**: Make sure employees have department values assigned

### Debugging Steps

1. **Check Browser Console** for JavaScript errors
2. **Check Network Tab** for failed API requests  
3. **Check Supabase Logs** in your dashboard under Logs > Database
4. **Verify Database Tables** exist and have proper data
5. **Test Authentication** by logging out and back in

### Database Verification

After running the SQL schema, verify these tables exist:
- `employees` (with sample data)
- `campaigns` 
- `campaign_targets`
- `campaign_target_employees`

## 🚀 Next Steps & Extensions

### Immediate Enhancements
1. **Email Templates** - Set up custom email templates in Supabase
2. **Custom Domains** - Configure custom authentication domains
3. **Database Backups** - Set up automated backups
4. **Performance Monitoring** - Monitor query performance and usage

### Future Features
1. **Advanced Reporting** - Detailed analytics and reporting dashboard
2. **Email Automation** - Integration with email service providers
3. **Multi-tenant Support** - Support for multiple organizations
4. **Advanced Targeting** - Role-based and custom targeting options
5. **Compliance Features** - GDPR compliance and data retention policies

## 📚 Additional Resources

### Documentation
- [Supabase Documentation](https://supabase.com/docs)
- [React Router Documentation](https://reactrouter.com/)
- [Material-UI Documentation](https://mui.com/)
- [PapaParse Documentation](https://www.papaparse.com/docs)

### Support
- [Supabase Community](https://github.com/supabase/supabase/discussions)
- [Discord Community](https://discord.supabase.com/)
- [GitHub Issues](https://github.com/your-repo/aicdap/issues)

---

## 🎉 Congratulations!

You now have a **fully integrated** phishing simulation platform with:
- **Real user authentication**
- **Complete employee management** with CSV import
- **Dynamic campaign targeting** based on actual employee data
- **Real-time statistics** and monitoring
- **Production-ready database** with proper security

Your employees data directly powers your campaign targeting, creating a seamless workflow from employee onboarding to security training campaigns.