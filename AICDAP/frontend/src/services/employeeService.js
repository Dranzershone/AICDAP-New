import { supabase } from '../lib/supabase';

export class EmployeeService {
  // Get all employees
  static async getAllEmployees() {
    try {
      const { data, error } = await supabase
        .from('employees')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error('Error fetching employees:', error);
      return { data: null, error: error.message };
    }
  }

  // Get employee by ID
  static async getEmployeeById(id) {
    try {
      const { data, error } = await supabase
        .from('employees')
        .select('*')
        .eq('id', id)
        .single();

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error('Error fetching employee:', error);
      return { data: null, error: error.message };
    }
  }

  // Create a new employee
  static async createEmployee(employee) {
    try {
      const { data, error } = await supabase
        .from('employees')
        .insert([{
          name: employee.name,
          email: employee.email.toLowerCase(),
          department: employee.department,
          status: employee.status || 'active',
          created_by: (await supabase.auth.getUser()).data.user?.id
        }])
        .select()
        .single();

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error('Error creating employee:', error);
      return { data: null, error: error.message };
    }
  }

  // Update an employee
  static async updateEmployee(id, updates) {
    try {
      const { data, error } = await supabase
        .from('employees')
        .update({
          name: updates.name,
          email: updates.email?.toLowerCase(),
          department: updates.department,
          status: updates.status,
          updated_at: new Date().toISOString()
        })
        .eq('id', id)
        .select()
        .single();

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error('Error updating employee:', error);
      return { data: null, error: error.message };
    }
  }

  // Delete an employee
  static async deleteEmployee(id) {
    try {
      const { error } = await supabase
        .from('employees')
        .delete()
        .eq('id', id);

      if (error) throw error;
      return { error: null };
    } catch (error) {
      console.error('Error deleting employee:', error);
      return { error: error.message };
    }
  }

  // Bulk insert employees (for CSV import)
  static async bulkCreateEmployees(employees) {
    try {
      const user = (await supabase.auth.getUser()).data.user;

      const employeesWithMetadata = employees.map(emp => ({
        name: emp.name,
        email: emp.email.toLowerCase(),
        department: emp.department,
        status: 'active',
        created_by: user?.id
      }));

      const { data, error } = await supabase
        .from('employees')
        .insert(employeesWithMetadata)
        .select();

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error('Error bulk creating employees:', error);
      return { data: null, error: error.message };
    }
  }

  // Check if email already exists
  static async checkEmailExists(email, excludeId = null) {
    try {
      let query = supabase
        .from('employees')
        .select('id, email')
        .eq('email', email.toLowerCase());

      if (excludeId) {
        query = query.neq('id', excludeId);
      }

      const { data, error } = await query;

      if (error) throw error;
      return { exists: data.length > 0, error: null };
    } catch (error) {
      console.error('Error checking email:', error);
      return { exists: false, error: error.message };
    }
  }

  // Get employees by department
  static async getEmployeesByDepartment(department) {
    try {
      const { data, error } = await supabase
        .from('employees')
        .select('*')
        .eq('department', department)
        .order('name');

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error('Error fetching employees by department:', error);
      return { data: null, error: error.message };
    }
  }

  // Get departments list
  static async getDepartments() {
    try {
      const { data, error } = await supabase
        .from('employees')
        .select('department')
        .not('department', 'is', null)
        .not('department', 'eq', '');

      if (error) throw error;

      // Extract unique departments
      const departments = [...new Set(data.map(emp => emp.department))];
      return { data: departments, error: null };
    } catch (error) {
      console.error('Error fetching departments:', error);
      return { data: null, error: error.message };
    }
  }

  // Get employee statistics
  static async getEmployeeStats() {
    try {
      const { data: allEmployees, error: allError } = await supabase
        .from('employees')
        .select('id, status, department, created_at');

      if (allError) throw allError;

      const totalEmployees = allEmployees.length;
      const activeEmployees = allEmployees.filter(emp => emp.status === 'active').length;
      const departments = [...new Set(allEmployees.map(emp => emp.department))].length;

      // Count employees added this month
      const currentMonth = new Date().getMonth();
      const currentYear = new Date().getFullYear();
      const thisMonthEmployees = allEmployees.filter(emp => {
        const empDate = new Date(emp.created_at);
        return empDate.getMonth() === currentMonth && empDate.getFullYear() === currentYear;
      }).length;

      return {
        data: {
          total: totalEmployees,
          active: activeEmployees,
          departments,
          thisMonth: thisMonthEmployees
        },
        error: null
      };
    } catch (error) {
      console.error('Error fetching employee stats:', error);
      return { data: null, error: error.message };
    }
  }

  // Search employees
  static async searchEmployees(searchTerm, filters = {}) {
    try {
      let query = supabase
        .from('employees')
        .select('*');

      // Add search term filter
      if (searchTerm) {
        query = query.or(`name.ilike.%${searchTerm}%,email.ilike.%${searchTerm}%`);
      }

      // Add department filter
      if (filters.department) {
        query = query.eq('department', filters.department);
      }

      // Add status filter
      if (filters.status) {
        query = query.eq('status', filters.status);
      }

      const { data, error } = await query.order('name');

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error('Error searching employees:', error);
      return { data: null, error: error.message };
    }
  }
}

export default EmployeeService;
