import os
import logging
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


class SupabaseClient:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.client: Optional[Client] = None
        self.service_client: Optional[Client] = None

    async def initialize(self):
        """Initialize Supabase clients"""
        try:
            if not self.supabase_url or not self.supabase_anon_key:
                raise ValueError("Supabase URL and anon key must be set")

            # Initialize regular client
            self.client = create_client(self.supabase_url, self.supabase_anon_key)

            # Initialize service client if service key is available
            if self.supabase_service_key:
                self.service_client = create_client(
                    self.supabase_url, self.supabase_service_key
                )
            else:
                logger.warning(
                    "Service role key not set, using anon key for all operations"
                )
                self.service_client = self.client

            logger.info("Supabase clients initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase clients: {str(e)}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """Check Supabase connection health"""
        try:
            if not self.client:
                return {"status": "error", "message": "Client not initialized"}

            # Simple query to test connection
            result = self.client.table("employees").select("id").limit(1).execute()

            return {
                "status": "healthy",
                "message": "Connection successful",
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def get_campaign(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign by ID"""
        try:
            result = (
                self.service_client.table("campaigns")
                .select("*")
                .eq("id", campaign_id)
                .single()
                .execute()
            )
            return result.data if result.data else None
        except Exception as e:
            logger.error(f"Error getting campaign {campaign_id}: {str(e)}")
            return None

    async def get_campaign_targets(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get all targets for a campaign"""
        try:
            # First get the campaign_target_ids for this campaign
            campaign_targets_result = (
                self.service_client.table("campaign_targets")
                .select("id, department")
                .eq("campaign_id", campaign_id)
                .execute()
            )

            if not campaign_targets_result.data:
                return []

            campaign_target_ids = [
                target["id"] for target in campaign_targets_result.data
            ]

            # Get campaign target employees (without join)
            logger.info(
                f"DEBUG: Using FIXED get_campaign_targets method for campaign {campaign_id}"
            )
            result = (
                self.service_client.table("campaign_target_employees")
                .select("id, employee_id, status, campaign_target_id")
                .in_("campaign_target_id", campaign_target_ids)
                .eq("status", "pending")
                .execute()
            )

            targets = []
            if result.data:
                # Get unique employee IDs
                employee_ids = list(set([row["employee_id"] for row in result.data]))

                # Get employee details separately
                employees_result = (
                    self.service_client.table("employees")
                    .select("id, name, email, department")
                    .in_("id", employee_ids)
                    .execute()
                )

                # Create employee lookup
                employee_lookup = {}
                if employees_result.data:
                    employee_lookup = {emp["id"]: emp for emp in employees_result.data}

                # Create a lookup for campaign target departments
                dept_lookup = {
                    target["id"]: target["department"]
                    for target in campaign_targets_result.data
                }

                for row in result.data:
                    employee_id = row["employee_id"]

                    if employee_id not in employee_lookup:
                        logger.error(f"Employee not found for ID: {employee_id}")
                        continue

                    employee = employee_lookup[employee_id]
                    targets.append(
                        {
                            "id": row["id"],
                            "email": employee["email"],
                            "name": employee["name"],
                            "department": employee["department"],
                            "employee_id": employee["id"],
                            "campaign_target_id": row["campaign_target_id"],
                        }
                    )

            return targets
        except Exception as e:
            logger.error(f"Error getting campaign targets for {campaign_id}: {str(e)}")
            return []

    async def update_campaign_status(self, campaign_id: str, status: str) -> bool:
        """Update campaign status"""
        try:
            result = (
                self.service_client.table("campaigns")
                .update(
                    {
                        "status": status,
                        "updated_at": datetime.utcnow().isoformat(),
                        "launched_at": datetime.utcnow().isoformat()
                        if status == "active"
                        else None,
                    }
                )
                .eq("id", campaign_id)
                .execute()
            )
            return True
        except Exception as e:
            logger.error(f"Error updating campaign status: {str(e)}")
            return False

    async def update_target_status(
        self,
        target_id: str,
        status: str,
        tracking_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update target employee status"""
        try:
            update_data = {
                "status": status,
                "updated_at": datetime.utcnow().isoformat(),
            }

            if tracking_id:
                update_data["tracking_id"] = tracking_id

            if status == "sent":
                update_data["sent_at"] = datetime.utcnow().isoformat()
            elif status == "opened":
                update_data["opened_at"] = datetime.utcnow().isoformat()
            elif status == "clicked":
                update_data["clicked_at"] = datetime.utcnow().isoformat()
            elif status == "reported":
                update_data["reported_at"] = datetime.utcnow().isoformat()

            if metadata:
                update_data["metadata"] = metadata

            result = (
                self.service_client.table("campaign_target_employees")
                .update(update_data)
                .eq("id", target_id)
                .execute()
            )
            return True
        except Exception as e:
            logger.error(f"Error updating target status: {str(e)}")
            return False

    async def update_campaign_stats(
        self, campaign_id: str, stats: Dict[str, Any]
    ) -> bool:
        """Update campaign statistics"""
        try:
            update_data = {
                "total_targets": stats.get("total_targets"),
                "total_sent": stats.get("total_sent"),
                "total_opened": stats.get("total_opened"),
                "total_clicked": stats.get("total_clicked"),
                "total_reported": stats.get("total_reported"),
                "updated_at": datetime.utcnow().isoformat(),
            }

            # Filter out None values so we don't overwrite with null
            update_data = {k: v for k, v in update_data.items() if v is not None}

            result = (
                self.service_client.table("campaigns")
                .update(update_data)
                .eq("id", campaign_id)
                .execute()
            )
            return True
        except Exception as e:
            logger.error(f"Error updating campaign stats: {str(e)}")
            return False

    async def record_tracking_event(
        self,
        tracking_id: str,
        event_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Record a tracking event and return the campaign_id"""
        try:
            # First, get the target by tracking_id
            target_result = (
                self.service_client.table("campaign_target_employees")
                .select("id, campaign_target_id")
                .eq("tracking_id", tracking_id)
                .single()
                .execute()
            )

            if not target_result.data:
                logger.warning(f"No target found for tracking_id: {tracking_id}")
                return None

            target_id = target_result.data["id"]
            campaign_target_id = target_result.data["campaign_target_id"]

            # Update target status based on event type
            if event_type == "opened":
                await self.update_target_status(target_id, "opened", metadata=metadata)
            elif event_type == "clicked" or event_type == "landed":
                await self.update_target_status(target_id, "clicked", metadata=metadata)
            elif event_type == "submitted":
                await self.update_target_status(
                    target_id, "submitted", metadata=metadata
                )
            elif event_type == "reported":
                await self.update_target_status(
                    target_id, "reported", metadata=metadata
                )

            # Get campaign_id
            campaign_target = (
                self.service_client.table("campaign_targets")
                .select("campaign_id")
                .eq("id", campaign_target_id)
                .single()
                .execute()
            )

            if not campaign_target.data:
                logger.warning(f"No campaign target found for id: {campaign_target_id}")
                return None

            campaign_id = campaign_target.data["campaign_id"]

            return campaign_id
        except Exception as e:
            logger.error(f"Error recording tracking event: {str(e)}")
            return None

    async def get_campaign_stats(self, campaign_id: str) -> Dict[str, Any]:
        """Get comprehensive campaign statistics"""
        try:
            # Get campaign basic info
            campaign = await self.get_campaign(campaign_id)
            if not campaign:
                return {}

            # Get detailed stats from campaign_target_employees
            # First get the campaign_target_ids for this campaign
            campaign_targets_result = (
                self.service_client.table("campaign_targets")
                .select("id")
                .eq("campaign_id", campaign_id)
                .execute()
            )

            if not campaign_targets_result.data:
                return {
                    "total_targets": 0,
                    "total_sent": 0,
                    "total_opened": 0,
                    "total_clicked": 0,
                    "total_submitted": 0,
                    "total_reported": 0,
                    "total_failed": 0,
                    "open_rate": 0.0,
                    "click_rate": 0.0,
                    "submit_rate": 0.0,
                    "report_rate": 0.0,
                    "last_updated": datetime.utcnow().isoformat(),
                }

            campaign_target_ids = [
                target["id"] for target in campaign_targets_result.data
            ]

            # Now get the employee target data
            result = (
                self.service_client.table("campaign_target_employees")
                .select("status, sent_at, opened_at, clicked_at, reported_at")
                .in_("campaign_target_id", campaign_target_ids)
                .execute()
            )

            stats = {
                "total_targets": 0,
                "total_sent": 0,
                "total_opened": 0,
                "total_clicked": 0,
                "total_submitted": 0,
                "total_reported": 0,
                "total_failed": 0,
                "open_rate": 0.0,
                "click_rate": 0.0,
                "submit_rate": 0.0,
                "report_rate": 0.0,
                "last_updated": datetime.utcnow().isoformat(),
            }

            if result.data:
                stats["total_targets"] = len(result.data)
                total_click_time = 0
                clicks_with_time = 0

                for row in result.data:
                    status = row["status"]
                    if status == "sent" or row.get("sent_at"):
                        stats["total_sent"] += 1
                    if status == "opened" or row.get("opened_at"):
                        stats["total_opened"] += 1
                    if status == "clicked" or row.get("clicked_at"):
                        stats["total_clicked"] += 1
                        if row.get("sent_at") and row.get("clicked_at"):
                            sent_at = datetime.fromisoformat(row["sent_at"])
                            clicked_at = datetime.fromisoformat(row["clicked_at"])
                            total_click_time += (clicked_at - sent_at).total_seconds()
                            clicks_with_time += 1
                    if status == "submitted":
                        stats["total_submitted"] += 1
                    if status == "reported" or row.get("reported_at"):
                        stats["total_reported"] += 1
                    if status == "failed":
                        stats["total_failed"] += 1

                # Add landing viewed (same as clicked)
                stats["landing_viewed"] = stats["total_clicked"]

                # Calculate average time to click
                if clicks_with_time > 0:
                    stats["avg_time_to_click"] = total_click_time / clicks_with_time
                else:
                    stats["avg_time_to_click"] = 0

                # Calculate rates
                if stats["total_sent"] > 0:
                    stats["open_rate"] = (
                        stats["total_opened"] / stats["total_sent"]
                    ) * 100
                    stats["click_rate"] = (
                        stats["total_clicked"] / stats["total_sent"]
                    ) * 100
                    stats["submit_rate"] = (
                        stats["total_submitted"] / stats["total_sent"]
                    ) * 100
                    stats["report_rate"] = (
                        stats["total_reported"] / stats["total_sent"]
                    ) * 100

            return stats

        except Exception as e:
            logger.error(f"Error getting campaign stats: {str(e)}")
            return {}

    async def get_employees_by_departments(
        self, departments: List[str]
    ) -> List[Dict[str, Any]]:
        """Get employees by department list"""
        try:
            result = (
                self.client.table("employees")
                .select("id, name, email, department")
                .in_("department", departments)
                .eq("status", "active")
                .execute()
            )
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting employees by departments: {str(e)}")
            return []

    async def create_tracking_table_if_not_exists(self):
        """Create tracking events table if it doesn't exist"""
        try:
            # This would typically be done via migrations
            # For now, we'll just log that we attempted it
            logger.info("Tracking table creation attempted")
            return True
        except Exception as e:
            logger.error(f"Error creating tracking table: {str(e)}")
            return False
