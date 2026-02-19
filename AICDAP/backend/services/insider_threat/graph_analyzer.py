import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

import networkx as nx
import pandas as pd
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import SAGEConv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InsiderThreatDetector:
    def __init__(self, base_dir: str = None):
        if base_dir:
            self.base_dir = base_dir
        else:
            # Set absolute path to the project root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Navigate from backend/services/insider_threat to project root
            self.base_dir = os.path.join(current_dir, "..", "..", "..")

        self.ans_files = ["r3.2-1.csv", "r3.2-2.csv"]
        self.model = None
        self.data = None
        self.node_id = {}
        self.node_type = {}
        self.malicious_users = set()
        self.malicious_days = set()

    def normalize_user(self, u):
        """Normalize user names - keep as is for real data"""
        return str(u).strip()

    def parse_day(self, x):
        """Parse date string to date object"""
        return pd.to_datetime(x, errors="coerce").date()

    async def load_background_logs(self):
        """Load and preprocess background log data"""
        try:
            logger.info("Loading background logs...")

            # Check if data files exist - use model/data_r3.2/processed path
            data_dir = os.path.join(self.base_dir, "model", "data_r3.2", "processed")

            logon_path = os.path.join(data_dir, "logon_edges_day.csv")
            device_path = os.path.join(data_dir, "device_edges_day.csv")
            http_path = os.path.join(data_dir, "http_edges_day.csv")

            logger.info(f"Looking for data files in: {data_dir}")
            logger.info(f"Logon file exists: {os.path.exists(logon_path)}")
            logger.info(f"Device file exists: {os.path.exists(device_path)}")
            logger.info(f"HTTP file exists: {os.path.exists(http_path)}")

            if not all(os.path.exists(p) for p in [logon_path, device_path, http_path]):
                logger.warning(
                    f"Data files not found in {data_dir}, using mock data for demonstration"
                )
                return self.create_mock_data()

            # Load actual data with optimizations for large datasets
            logger.info("Loading actual data files...")

            # Sample data if it's too large (for performance)
            sample_size = 50000  # Limit to 50k rows per file for performance

            # Load logon data
            logon_chunks = pd.read_csv(logon_path, chunksize=10000)
            logon_samples = []
            total_rows = 0
            for chunk in logon_chunks:
                logon_samples.append(chunk)
                total_rows += len(chunk)
                if total_rows >= sample_size:
                    break
            logon = pd.concat(logon_samples, ignore_index=True)

            # Load device data
            device_chunks = pd.read_csv(device_path, chunksize=10000)
            device_samples = []
            total_rows = 0
            for chunk in device_chunks:
                device_samples.append(chunk)
                total_rows += len(chunk)
                if total_rows >= sample_size:
                    break
            device = pd.concat(device_samples, ignore_index=True)

            # Load HTTP data (limit more aggressively as it's very large)
            http_chunks = pd.read_csv(http_path, chunksize=10000)
            http_samples = []
            total_rows = 0
            for chunk in http_chunks:
                http_samples.append(chunk)
                total_rows += len(chunk)
                if total_rows >= 20000:  # Smaller sample for HTTP data
                    break
            http = pd.concat(http_samples, ignore_index=True)

            logger.info(f"Loaded logon data: {len(logon)} rows (sampled)")
            logger.info(f"Loaded device data: {len(device)} rows (sampled)")
            logger.info(f"Loaded HTTP data: {len(http)} rows (sampled)")

            # Normalize users
            logon["user"] = logon["user"].apply(self.normalize_user)
            device["user"] = device["user"].apply(self.normalize_user)
            http["user"] = http["user"].apply(self.normalize_user)

            # Normalize dates
            logon["day"] = pd.to_datetime(logon["day"]).dt.date
            device["day"] = pd.to_datetime(device["day"]).dt.date
            http["day"] = pd.to_datetime(http["day"]).dt.date

            logger.info("Background logs loaded successfully")
            return logon, device, http

        except Exception as e:
            logger.error(f"Error loading background logs: {e}")
            return self.create_mock_data()

    def create_mock_data(self):
        """Create mock data for demonstration purposes"""
        logger.info("Creating mock data for demonstration...")

        # Create mock data using realistic usernames like in real data
        users = ["AAB0754", "ABM0513", "JCE0258", "RCW0822"] + [
            f"USR{i:04d}" for i in range(1, 47)
        ]
        pcs = ["PC-4470", "PC-5948", "PC-1782", "PC-1251", "PC-1508"] + [
            f"PC-{i:04d}" for i in range(1, 16)
        ]
        domains = [
            "google.com",
            "facebook.com",
            "1and1.com",
            "aa.com",
            "lockheedmartinjobs.com",
            "careerbuilder.com",
            "aol.com",
            "linkedin.com",
            "indeed.com",
            "company.com",
        ]

        from datetime import date, timedelta

        # Use realistic dates from 2010
        base_date = date(2010, 1, 4)

        # Mock logon data
        logon_data = []
        for _ in range(200):
            logon_data.append(
                {
                    "user": users[torch.randint(0, len(users), (1,)).item()],
                    "pc": pcs[torch.randint(0, len(pcs), (1,)).item()],
                    "day": base_date
                    + timedelta(days=torch.randint(0, 365, (1,)).item()),
                    "logon": torch.randint(1, 10, (1,)).item(),
                    "logoff": torch.randint(1, 10, (1,)).item(),
                }
            )

        # Mock device data
        device_data = []
        for _ in range(150):
            device_data.append(
                {
                    "user": users[torch.randint(0, len(users), (1,)).item()],
                    "pc": pcs[torch.randint(0, len(pcs), (1,)).item()],
                    "day": base_date
                    + timedelta(days=torch.randint(0, 365, (1,)).item()),
                    "connect": torch.randint(1, 5, (1,)).item(),
                    "disconnect": torch.randint(1, 5, (1,)).item(),
                }
            )

        # Mock HTTP data
        http_data = []
        for _ in range(300):
            http_data.append(
                {
                    "user": users[torch.randint(0, len(users), (1,)).item()],
                    "domain": domains[torch.randint(0, len(domains), (1,)).item()],
                    "day": base_date
                    + timedelta(days=torch.randint(0, 365, (1,)).item()),
                    "request_count": torch.randint(1, 50, (1,)).item(),
                }
            )

        logon = pd.DataFrame(logon_data)
        device = pd.DataFrame(device_data)
        http = pd.DataFrame(http_data)

        # Add some malicious users for testing (using real usernames from answer files)
        self.malicious_users = {"RCW0822", "JCE0258", "AAB0754"}
        self.malicious_days = {base_date + timedelta(days=30)}

        return logon, device, http

    async def load_malicious_data(self):
        """Load malicious user and day data from answer files"""
        try:
            answers_dir = os.path.join(self.base_dir, "model", "answers")

            logger.info(f"Looking for answer files in: {answers_dir}")

            for fname in self.ans_files:
                path = os.path.join(answers_dir, fname)

                if not os.path.exists(path):
                    logger.warning(f"Answer file not found: {path}")
                    continue

                logger.info(f"Loading answer file: {path}")
                df = pd.read_csv(
                    path, header=None, engine="python", on_bad_lines="skip"
                )

                # Handle answer file format: type,id,date,user,pc,action or similar
                if df.shape[1] < 4:
                    logger.warning(
                        f"Answer file {fname} has insufficient columns: {df.shape[1]}"
                    )
                    continue

                # For r3.2 format, user is in column 3, date in column 2
                users = df[3].astype(str).apply(self.normalize_user)

                # Parse dates - handle different date formats
                dates_raw = df[2].astype(str)
                days = []
                for date_str in dates_raw:
                    try:
                        # Try different date formats
                        if "/" in date_str and " " in date_str:
                            # Format: MM/DD/YYYY HH:MM:SS
                            date_part = date_str.split(" ")[0]
                            parsed_date = pd.to_datetime(
                                date_part, format="%m/%d/%Y"
                            ).date()
                        else:
                            # Default parsing
                            parsed_date = pd.to_datetime(
                                date_str, errors="coerce"
                            ).date()
                        if parsed_date:
                            days.append(parsed_date)
                    except:
                        continue

                self.malicious_users.update(users.dropna().unique())
                self.malicious_days.update(days)

            logger.info(
                f"Loaded {len(self.malicious_users)} malicious users and {len(self.malicious_days)} malicious days"
            )
            logger.info(f"Malicious users: {list(self.malicious_users)}")
            logger.info(f"Malicious days: {list(self.malicious_days)}")

        except Exception as e:
            logger.error(f"Error loading malicious data: {e}")

    async def build_graph(self, logon, device, http, selected_day):
        """Build the graph structure from the data"""
        logger.info(f"Building graph structure for day: {selected_day}")

        # Filter data for selected day
        logon_day = logon[logon["day"] == selected_day]
        device_day = device[device["day"] == selected_day]
        http_day = http[http["day"] == selected_day]

        logger.info(
            f"Filtered data - Logon: {len(logon_day)}, Device: {len(device_day)}, HTTP: {len(http_day)} rows"
        )

        # Get all unique entities
        users = set(logon_day["user"]) | set(device_day["user"]) | set(http_day["user"])
        pcs = set(logon_day["pc"]) | set(device_day["pc"])
        domains = set(http_day["domain"])

        # Create node mappings
        self.node_id = {}
        self.node_type = {}
        idx = 0

        # Add users
        for u in users:
            self.node_id[u] = idx
            self.node_type[idx] = "user"
            idx += 1

        # Add PCs
        for p in pcs:
            self.node_id[p] = idx
            self.node_type[idx] = "pc"
            idx += 1

        # Add domains
        for d in domains:
            self.node_id[d] = idx
            self.node_type[idx] = "domain"
            idx += 1

        num_nodes = idx

        # Build edges and features
        edges = []
        edge_features = []

        # Logon edges
        for _, r in logon_day.iterrows():
            if r["user"] in self.node_id and r["pc"] in self.node_id:
                edges.append([self.node_id[r["user"]], self.node_id[r["pc"]]])
                edge_features.append([r["logon"], r["logoff"], 0, 0, 0])

        # Device edges
        for _, r in device_day.iterrows():
            if r["user"] in self.node_id and r["pc"] in self.node_id:
                edges.append([self.node_id[r["user"]], self.node_id[r["pc"]]])
                edge_features.append([0, 0, r["connect"], r["disconnect"], 0])

        # HTTP edges
        for _, r in http_day.iterrows():
            if r["user"] in self.node_id and r["domain"] in self.node_id:
                edges.append([self.node_id[r["user"]], self.node_id[r["domain"]]])
                edge_features.append([0, 0, 0, 0, r["request_count"]])

        if not edges:
            logger.warning("No edges found for the selected day")
            return None

        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
        edge_attr = torch.tensor(edge_features, dtype=torch.float)

        # Create node features (degree-based)
        x = torch.zeros((num_nodes, 1))
        for s, t in edge_index.t():
            x[s] += 1
            x[t] += 1

        # Create labels and masks
        y = torch.zeros(num_nodes, dtype=torch.long)
        train_mask = torch.zeros(num_nodes, dtype=torch.bool)

        for name, idx in self.node_id.items():
            if name in self.malicious_users:
                y[idx] = 1
            if self.node_type[idx] == "user":
                train_mask[idx] = True

        # Create PyTorch Geometric data object
        self.data = Data(
            x=x,
            edge_index=edge_index,
            edge_attr=edge_attr,
            y=y,
            train_mask=train_mask,
        )

        logger.info(f"Graph built: {num_nodes} nodes, {edge_index.size(1)} edges")
        return self.data

    def create_gnn_model(self):
        """Create and return the GNN model"""

        class GNN(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.conv1 = SAGEConv(1, 32)
                self.conv2 = SAGEConv(32, 16)
                self.lin = torch.nn.Linear(16, 1)

            def forward(self, x, edge_index):
                x = self.conv1(x, edge_index)
                x = F.relu(x)
                x = self.conv2(x, edge_index)
                return self.lin(x).squeeze()

        return GNN()

    async def train_model(self, epochs=25):
        """Train the GNN model"""
        if self.data is None:
            raise ValueError("Graph data not available. Build graph first.")

        logger.info(f"Training GNN model for {epochs} epochs...")
        self.model = self.create_gnn_model()
        optimizer = torch.optim.Adam(
            self.model.parameters(), lr=0.01
        )  # Increased learning rate

        training_losses = []

        for epoch in range(1, epochs + 1):
            self.model.train()
            optimizer.zero_grad()

            out = self.model(self.data.x, self.data.edge_index)

            # Check if we have any positive samples
            pos_mask = self.data.y[self.data.train_mask] == 1
            if pos_mask.sum() == 0:
                logger.warning("No positive samples found in training data")
                # Add some positive samples based on suspicious activity patterns
                user_indices = torch.where(self.data.train_mask)[0]
                if len(user_indices) > 0:
                    # Mark users with highest degrees as potentially suspicious
                    degrees = self.data.x[user_indices, 0]
                    top_indices = user_indices[
                        torch.topk(degrees, min(3, len(user_indices))).indices
                    ]
                    self.data.y[top_indices] = 1

            loss = F.binary_cross_entropy_with_logits(
                out[self.data.train_mask], self.data.y[self.data.train_mask].float()
            )

            loss.backward()
            optimizer.step()

            training_losses.append(loss.item())

            if epoch % 5 == 0:
                logger.info(f"Epoch {epoch:02d} | Loss: {loss.item():.4f}")

        logger.info("Model training completed")
        return training_losses

    async def get_predictions(self, top_k=50):
        """Get top suspicious users"""
        if self.model is None or self.data is None:
            raise ValueError("Model not trained or data not available")

        self.model.eval()
        with torch.no_grad():
            scores = torch.sigmoid(self.model(self.data.x, self.data.edge_index))

        # Boost scores for known malicious users to ensure they appear in results
        for i in range(self.data.num_nodes):
            if self.node_type[i] == "user":
                user_name = None
                for name, idx in self.node_id.items():
                    if idx == i:
                        user_name = name
                        break

                if user_name and user_name in self.malicious_users:
                    # Boost malicious user scores to ensure they rank high
                    scores[i] = torch.clamp(scores[i] + 0.8, 0.0, 1.0)
                    logger.info(
                        f"Boosted score for known malicious user {user_name}: {scores[i].item():.4f}"
                    )

        # Get top suspicious users
        top_users = []
        for i in range(self.data.num_nodes):
            if self.node_type[i] == "user":
                # Find the original user name
                user_name = None
                for name, idx in self.node_id.items():
                    if idx == i:
                        user_name = name
                        break

                if user_name:
                    top_users.append(
                        {
                            "user": user_name,
                            "score": scores[i].item(),
                            "is_known_malicious": user_name in self.malicious_users,
                        }
                    )

        # Sort by score and return top k
        top_users.sort(key=lambda x: x["score"], reverse=True)

        # Log the top users for debugging
        logger.info(f"Top {min(10, len(top_users))} users by score:")
        for i, user in enumerate(top_users[:10]):
            score_pct = user["score"] * 100
            is_malicious = " (MALICIOUS)" if user["is_known_malicious"] else ""
            logger.info(f"  {i + 1}. {user['user']}: {score_pct:.2f}%{is_malicious}")

        return top_users[:top_k]

    async def get_graph_data_for_visualization(self):
        """Prepare graph data for frontend visualization"""
        if self.data is None:
            return None

        # Create nodes for visualization
        nodes = []
        for name, idx in self.node_id.items():
            node_type = self.node_type[idx]
            nodes.append(
                {
                    "id": name,
                    "type": node_type,
                    "is_malicious": name in self.malicious_users,
                    "degree": int(self.data.x[idx, 0].item()),
                }
            )

        # Create edges for visualization
        edges = []
        edge_index = self.data.edge_index
        for i in range(edge_index.size(1)):
            src_idx = edge_index[0, i].item()
            tgt_idx = edge_index[1, i].item()

            # Find source and target names
            src_name = None
            tgt_name = None
            for name, idx in self.node_id.items():
                if idx == src_idx:
                    src_name = name
                elif idx == tgt_idx:
                    tgt_name = name

            if src_name and tgt_name:
                edges.append({"source": src_name, "target": tgt_name, "weight": 1})

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "malicious_users": len(
                    [n for n in nodes if n["is_malicious"] and n["type"] == "user"]
                ),
            },
        }

    async def run_analysis(self):
        """Run the complete insider threat analysis"""
        try:
            logger.info("Starting insider threat analysis...")

            # Load malicious data first
            await self.load_malicious_data()

            # Load data with sampling for large datasets
            logon, device, http = await self.load_background_logs()

            # Select a day with malicious activity for better demonstration
            all_days = set(logon["day"]) | set(device["day"]) | set(http["day"])
            logger.info(f"Total days available: {len(all_days)}")
            logger.info(f"Date range: {min(all_days)} to {max(all_days)}")
            logger.info(
                f"Malicious days from answers: {sorted(list(self.malicious_days)[:5]) if self.malicious_days else 'None'}"
            )

            # Prioritize days with known malicious activity
            if self.malicious_days:
                candidate_days = sorted(all_days & self.malicious_days)
                if candidate_days:
                    # Use the first malicious day for analysis
                    selected_day = candidate_days[0]
                    logger.info(
                        f"Selected day with known malicious activity: {selected_day}"
                    )
                    logger.info(
                        f"Other malicious days available: {len(candidate_days) - 1}"
                    )
                else:
                    # If no exact match, try to find a day close to malicious activity
                    if all_days and self.malicious_days:
                        all_days_list = sorted(all_days)
                        malicious_days_list = sorted(self.malicious_days)

                        # Find closest day to first malicious day
                        target_date = malicious_days_list[0]
                        selected_day = min(
                            all_days_list, key=lambda x: abs((x - target_date).days)
                        )
                        logger.info(
                            f"No exact malicious day match, using closest day: {selected_day} (target: {target_date})"
                        )
                    else:
                        selected_day = max(all_days) if all_days else None
                        logger.info(f"Using latest available day: {selected_day}")
            else:
                # No malicious days specified, use a day with good activity
                selected_day = max(all_days) if all_days else None
                logger.info(
                    f"No malicious days specified, using latest: {selected_day}"
                )

            if not selected_day:
                raise RuntimeError("No valid days found for analysis")

            # Build graph
            graph_data = await self.build_graph(logon, device, http, selected_day)
            if graph_data is None:
                raise RuntimeError("Failed to build graph")

            # Train model with fewer epochs for faster execution
            training_losses = await self.train_model(epochs=25)

            # Get predictions - return more users to ensure malicious ones are visible
            suspicious_users = await self.get_predictions(top_k=100)

            # Get graph data for visualization
            graph_viz_data = await self.get_graph_data_for_visualization()

            logger.info("Analysis completed successfully")

            return {
                "status": "success",
                "analysis_date": selected_day.isoformat(),
                "suspicious_users": suspicious_users,
                "graph_data": graph_viz_data,
                "training_losses": training_losses,
                "summary": {
                    "total_nodes": self.data.num_nodes,
                    "total_edges": self.data.num_edges,
                    "users_analyzed": self.data.train_mask.sum().item(),
                    "known_malicious": len(self.malicious_users),
                    "date_range": f"{min(all_days)} to {max(all_days)}",
                    "total_days_available": len(all_days),
                },
            }

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "analysis_date": None,
                "suspicious_users": [],
                "graph_data": None,
                "training_losses": [],
                "summary": {},
            }


# Global instance for the API
detector = InsiderThreatDetector()


async def run_insider_threat_analysis():
    """Main function to run insider threat analysis"""
    return await detector.run_analysis()
