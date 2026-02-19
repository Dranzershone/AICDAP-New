import { supabase } from "../lib/supabase";

export class CampaignService {
  // Get all campaigns
  static async getAllCampaigns() {
    try {
      const { data, error } = await supabase
        .from("campaigns")
        .select(
          `
          *,
          campaign_targets (
            id,
            department,
            employee_count,
            employees:campaign_target_employees (
              employee_id,
              employees (
                id,
                name,
                email
              )
            )
          )
        `,
        )
        .order("created_at", { ascending: false });

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error("Error fetching campaigns:", error);
      return { data: null, error: error.message };
    }
  }

  // Get campaign by ID
  static async getCampaignById(id) {
    try {
      const { data, error } = await supabase
        .from("campaigns")
        .select(
          `
          *,
          campaign_targets (
            id,
            department,
            employee_count,
            employees:campaign_target_employees (
              employee_id,
              employees (
                id,
                name,
                email,
                department
              )
            )
          )
        `,
        )
        .eq("id", id)
        .single();

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error("Error fetching campaign:", error);
      return { data: null, error: error.message };
    }
  }

  // Create a new campaign
  static async createCampaign(campaignData) {
    try {
      const user = (await supabase.auth.getUser()).data.user;

      // Start a transaction to create campaign and its targets
      const { data: campaign, error: campaignError } = await supabase
        .from("campaigns")
        .insert([
          {
            name: campaignData.name,
            description: campaignData.description,
            template_id: campaignData.template_id,
            template_name: campaignData.template_name,
            status: campaignData.status || "active",
            total_targets: campaignData.total_targets || 0,
            total_sent: 0,
            total_opened: 0,
            total_clicked: 0,
            total_reported: 0,
            created_by: user?.id,
          },
        ])
        .select()
        .single();

      if (campaignError) throw campaignError;

      // Create campaign targets
      if (campaignData.targets && campaignData.targets.length > 0) {
        const targetData = campaignData.targets.map((target) => ({
          campaign_id: campaign.id,
          department: target.name,
          employee_count: target.employeeCount,
          created_by: user?.id,
        }));

        const { data: targets, error: targetsError } = await supabase
          .from("campaign_targets")
          .insert(targetData)
          .select();

        if (targetsError) throw targetsError;

        // Create individual employee targets
        for (const target of campaignData.targets) {
          if (target.employees && target.employees.length > 0) {
            const campaignTarget = targets.find(
              (t) => t.department === target.name,
            );

            const employeeTargets = target.employees.map((employee) => ({
              campaign_target_id: campaignTarget.id,
              employee_id: employee.id,
              status: "pending",
              created_by: user?.id,
            }));

            const { error: employeeTargetsError } = await supabase
              .from("campaign_target_employees")
              .insert(employeeTargets);

            if (employeeTargetsError) throw employeeTargetsError;
          }
        }
      }

      return { data: campaign, error: null };
    } catch (error) {
      console.error("Error creating campaign:", error);
      return { data: null, error: error.message };
    }
  }

  // Update a campaign
  static async updateCampaign(id, updates) {
    try {
      const { data, error } = await supabase
        .from("campaigns")
        .update({
          name: updates.name,
          description: updates.description,
          status: updates.status,
          updated_at: new Date().toISOString(),
        })
        .eq("id", id)
        .select()
        .single();

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error("Error updating campaign:", error);
      return { data: null, error: error.message };
    }
  }

  // Delete a campaign
  static async deleteCampaign(id) {
    try {
      // Delete related records first due to foreign key constraints
      await supabase
        .from("campaign_target_employees")
        .delete()
        .eq("campaign_target_id", id);
      await supabase.from("campaign_targets").delete().eq("campaign_id", id);

      const { error } = await supabase.from("campaigns").delete().eq("id", id);

      if (error) throw error;
      return { error: null };
    } catch (error) {
      console.error("Error deleting campaign:", error);
      return { error: error.message };
    }
  }

  // Update campaign statistics
  static async updateCampaignStats(campaignId, stats) {
    try {
      const { data, error } = await supabase
        .from("campaigns")
        .update({
          total_sent: stats.total_sent,
          total_opened: stats.total_opened,
          total_clicked: stats.total_clicked,
          total_reported: stats.total_reported,
          updated_at: new Date().toISOString(),
        })
        .eq("id", campaignId)
        .select()
        .single();

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error("Error updating campaign stats:", error);
      return { data: null, error: error.message };
    }
  }

  // Get campaign statistics
  static async getCampaignStats() {
    try {
      const { data: campaigns, error: campaignsError } = await supabase
        .from("campaigns")
        .select(
          "id, status, total_targets, total_sent, total_opened, total_clicked, total_reported, created_at",
        );

      if (campaignsError) throw campaignsError;

      const totalCampaigns = campaigns.length;
      const activeCampaigns = campaigns.filter(
        (c) => c.status === "active",
      ).length;
      const completedCampaigns = campaigns.filter(
        (c) => c.status === "completed",
      ).length;
      const totalTargets = campaigns.reduce(
        (sum, c) => sum + (c.total_targets || 0),
        0,
      );
      const totalSent = campaigns.reduce(
        (sum, c) => sum + (c.total_sent || 0),
        0,
      );
      const totalOpened = campaigns.reduce(
        (sum, c) => sum + (c.total_opened || 0),
        0,
      );
      const totalClicked = campaigns.reduce(
        (sum, c) => sum + (c.total_clicked || 0),
        0,
      );
      const totalReported = campaigns.reduce(
        (sum, c) => sum + (c.total_reported || 0),
        0,
      );

      // Calculate this month's campaigns
      const currentMonth = new Date().getMonth();
      const currentYear = new Date().getFullYear();
      const thisMonthCampaigns = campaigns.filter((c) => {
        const campaignDate = new Date(c.created_at);
        return (
          campaignDate.getMonth() === currentMonth &&
          campaignDate.getFullYear() === currentYear
        );
      }).length;

      return {
        data: {
          total: totalCampaigns,
          active: activeCampaigns,
          completed: completedCampaigns,
          thisMonth: thisMonthCampaigns,
          totalTargets,
          totalSent,
          totalOpened,
          totalClicked,
          totalReported,
          openRate:
            totalSent > 0 ? ((totalOpened / totalSent) * 100).toFixed(1) : 0,
          clickRate:
            totalSent > 0 ? ((totalClicked / totalSent) * 100).toFixed(1) : 0,
          reportRate:
            totalSent > 0 ? ((totalReported / totalSent) * 100).toFixed(1) : 0,
        },
        error: null,
      };
    } catch (error) {
      console.error("Error fetching campaign stats:", error);
      return { data: null, error: error.message };
    }
  }

  // Get campaigns by status
  static async getCampaignsByStatus(status) {
    try {
      const { data, error } = await supabase
        .from("campaigns")
        .select("*")
        .eq("status", status)
        .order("created_at", { ascending: false });

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error("Error fetching campaigns by status:", error);
      return { data: null, error: error.message };
    }
  }

  // Update employee target status
  static async updateEmployeeTargetStatus(
    campaignTargetId,
    employeeId,
    status,
    metadata = {},
  ) {
    try {
      const { data, error } = await supabase
        .from("campaign_target_employees")
        .update({
          status,
          opened_at: status === "opened" ? new Date().toISOString() : undefined,
          clicked_at:
            status === "clicked" ? new Date().toISOString() : undefined,
          reported_at:
            status === "reported" ? new Date().toISOString() : undefined,
          metadata,
          updated_at: new Date().toISOString(),
        })
        .eq("campaign_target_id", campaignTargetId)
        .eq("employee_id", employeeId)
        .select()
        .single();

      if (error) throw error;
      return { data, error: null };
    } catch (error) {
      console.error("Error updating employee target status:", error);
      return { data: null, error: error.message };
    }
  }

  static async getTemplates() {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/templates`,
      );
      if (!response.ok) {
        throw new Error("Failed to fetch templates");
      }
      const data = await response.json();
      return { data: data.templates, error: null };
    } catch (error) {
      console.error("Error fetching templates:", error);
      return { data: null, error: error.message };
    }
  }

  static async launchCampaign(campaignData) {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/campaigns/launch`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(campaignData),
        },
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to launch campaign");
      }

      const data = await response.json();
      return { data, error: null };
    } catch (error) {
      console.error("Error launching campaign:", error);
      return { data: null, error: error.message };
    }
  }

  static async getCampaignAnalytics(campaignIds) {
    try {
      const analyticsData = await Promise.all(
        campaignIds.map(async (campaignId) => {
          const response = await fetch(
            `${process.env.REACT_APP_BACKEND_URL}/api/campaigns/${campaignId}/stats`,
          );
          if (!response.ok) {
            throw new Error(
              `Failed to fetch analytics for campaign ${campaignId}`,
            );
          }
          const data = await response.json();
          return { campaignId, ...data };
        }),
      );
      return { data: analyticsData, error: null };
    } catch (error) {
      console.error("Error fetching campaign analytics:", error);
      return { data: null, error: error.message };
    }
  }
}

export default CampaignService;
