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

-- Create campaigns table
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    template_id INTEGER,
    template_name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed', 'draft')),
    total_targets INTEGER DEFAULT 0,
    total_sent INTEGER DEFAULT 0,
    total_opened INTEGER DEFAULT 0,
    total_clicked INTEGER DEFAULT 0,
    total_reported INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    launched_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL
);

-- Create campaign targets table (departments selected for campaigns)
CREATE TABLE IF NOT EXISTS campaign_targets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    department VARCHAR(255) NOT NULL,
    employee_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL
);

-- Create campaign target employees table (individual employees targeted)
CREATE TABLE IF NOT EXISTS campaign_target_employees (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    campaign_target_id UUID REFERENCES campaign_targets(id) ON DELETE CASCADE,
    employee_id UUID REFERENCES employees(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'opened', 'clicked', 'reported')),
    sent_at TIMESTAMP WITH TIME ZONE,
    opened_at TIMESTAMP WITH TIME ZONE,
    clicked_at TIMESTAMP WITH TIME ZONE,
    reported_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    UNIQUE(campaign_target_id, employee_id)
);

-- Create indexes for campaigns
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_created_at ON campaigns(created_at);
CREATE INDEX IF NOT EXISTS idx_campaigns_created_by ON campaigns(created_by);

-- Create indexes for campaign targets
CREATE INDEX IF NOT EXISTS idx_campaign_targets_campaign_id ON campaign_targets(campaign_id);
CREATE INDEX IF NOT EXISTS idx_campaign_targets_department ON campaign_targets(department);

-- Create indexes for campaign target employees
CREATE INDEX IF NOT EXISTS idx_campaign_target_employees_target_id ON campaign_target_employees(campaign_target_id);
CREATE INDEX IF NOT EXISTS idx_campaign_target_employees_employee_id ON campaign_target_employees(employee_id);
CREATE INDEX IF NOT EXISTS idx_campaign_target_employees_status ON campaign_target_employees(status);

-- Create triggers for campaign tables
CREATE TRIGGER update_campaigns_updated_at
    BEFORE UPDATE ON campaigns
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaign_targets_updated_at
    BEFORE UPDATE ON campaign_targets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaign_target_employees_updated_at
    BEFORE UPDATE ON campaign_target_employees
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS) for campaign tables
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaign_targets ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaign_target_employees ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for campaigns
CREATE POLICY "Users can view campaigns" ON campaigns
    FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "Users can insert campaigns" ON campaigns
    FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "Users can update their campaigns" ON campaigns
    FOR UPDATE USING (auth.uid() = created_by OR auth.uid() IS NOT NULL);

CREATE POLICY "Users can delete their campaigns" ON campaigns
    FOR DELETE USING (auth.uid() = created_by OR auth.uid() IS NOT NULL);

-- Create RLS policies for campaign targets
CREATE POLICY "Users can view campaign targets" ON campaign_targets
    FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "Users can insert campaign targets" ON campaign_targets
    FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "Users can update campaign targets" ON campaign_targets
    FOR UPDATE USING (auth.uid() = created_by OR auth.uid() IS NOT NULL);

CREATE POLICY "Users can delete campaign targets" ON campaign_targets
    FOR DELETE USING (auth.uid() = created_by OR auth.uid() IS NOT NULL);

-- Create RLS policies for campaign target employees
CREATE POLICY "Users can view campaign target employees" ON campaign_target_employees
    FOR SELECT USING (auth.uid() IS NOT NULL);

CREATE POLICY "Users can insert campaign target employees" ON campaign_target_employees
    FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "Users can update campaign target employees" ON campaign_target_employees
    FOR UPDATE USING (auth.uid() = created_by OR auth.uid() IS NOT NULL);

CREATE POLICY "Users can delete campaign target employees" ON campaign_target_employees
    FOR DELETE USING (auth.uid() = created_by OR auth.uid() IS NOT NULL);

-- Create view for campaign statistics
CREATE OR REPLACE VIEW campaign_stats AS
SELECT
    COUNT(*) as total_campaigns,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_campaigns,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_campaigns,
    COUNT(CASE WHEN status = 'paused' THEN 1 END) as paused_campaigns,
    COUNT(CASE WHEN DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE) THEN 1 END) as campaigns_this_month,
    SUM(total_targets) as total_targets_all_campaigns,
    SUM(total_sent) as total_emails_sent,
    SUM(total_opened) as total_emails_opened,
    SUM(total_clicked) as total_emails_clicked,
    SUM(total_reported) as total_emails_reported,
    CASE
        WHEN SUM(total_sent) > 0 THEN ROUND((SUM(total_opened)::numeric / SUM(total_sent)) * 100, 2)
        ELSE 0
    END as overall_open_rate,
    CASE
        WHEN SUM(total_sent) > 0 THEN ROUND((SUM(total_clicked)::numeric / SUM(total_sent)) * 100, 2)
        ELSE 0
    END as overall_click_rate,
    CASE
        WHEN SUM(total_sent) > 0 THEN ROUND((SUM(total_reported)::numeric / SUM(total_sent)) * 100, 2)
        ELSE 0
    END as overall_report_rate
FROM campaigns;
