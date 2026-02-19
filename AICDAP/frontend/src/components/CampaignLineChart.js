import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import CampaignService from "../services/campaignService";
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  OutlinedInput,
  Checkbox,
  ListItemText,
} from "@mui/material";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
);

const CampaignLineChart = () => {
  const [chartData, setChartData] = useState({});
  const [loading, setLoading] = useState(true);
  const [campaigns, setCampaigns] = useState([]);
  const [selectedCampaigns, setSelectedCampaigns] = useState([]);

  useEffect(() => {
    const fetchCampaigns = async () => {
      const { data, error } = await CampaignService.getAllCampaigns();
      if (error) {
        console.error("Error fetching campaigns:", error);
      } else {
        setCampaigns(data);
        // Select the first two campaigns by default
        if (data.length > 0) {
          setSelectedCampaigns(data.slice(0, 2).map((c) => c.id));
        }
      }
    };
    fetchCampaigns();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      if (selectedCampaigns.length === 0) {
        setChartData({});
        setLoading(false);
        return;
      }

      setLoading(true);
      const { data, error } =
        await CampaignService.getCampaignAnalytics(selectedCampaigns);
      if (error) {
        console.error("Error fetching campaign analytics:", error);
        setLoading(false);
        return;
      }

      const datasets = data.map((analytics, index) => {
        const campaign = campaigns.find((c) => c.id === analytics.campaignId);
        const campaignName = campaign ? campaign.name : `Campaign ${index + 1}`;

        const chartDataset = {
          label: campaignName,
          data: [
            analytics.total_sent,
            analytics.total_opened,
            analytics.total_clicked,
            analytics.landing_viewed,
            analytics.total_submitted,
            analytics.total_reported,
            analytics.avg_time_to_click,
          ],
          borderColor: "#f38020",
          backgroundColor: "rgba(243, 128, 32, 0.1)",
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 5,
        };
        return chartDataset;
      });

      const labels = [
        "Delivered",
        "Opened",
        "Clicked",
        "Landing Viewed",
        "Credential Submitted",
        "Reported",
        "Avg Time to Click (sec)",
      ];

      setChartData({
        labels: labels,
        datasets: datasets,
      });
      setLoading(false);
    };

    if (campaigns.length > 0) {
      fetchData();
    }
  }, [selectedCampaigns, campaigns]);

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedCampaigns(typeof value === "string" ? value.split(",") : value);
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Campaign Engagement Comparison (Line Chart)",
        font: { size: 18 },
      },
      tooltip: {
        mode: "index",
        intersect: false,
      },
      legend: {
        position: "top",
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 2,
        },
      },
    },
    interaction: {
      mode: "nearest",
      axis: "x",
      intersect: false,
    },
    animation: {
      duration: 1500,
      easing: "easeInOutQuart",
    },
  };

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 4 }}>
        <InputLabel id="campaign-select-label">Select Campaigns</InputLabel>
        <Select
          labelId="campaign-select-label"
          id="campaign-select"
          multiple
          value={selectedCampaigns}
          onChange={handleChange}
          input={<OutlinedInput label="Select Campaigns" />}
          renderValue={(selected) =>
            campaigns
              .filter((c) => selected.includes(c.id))
              .map((c) => c.name)
              .join(", ")
          }
        >
          {campaigns.map((campaign) => (
            <MenuItem key={campaign.id} value={campaign.id}>
              <Checkbox checked={selectedCampaigns.indexOf(campaign.id) > -1} />
              <ListItemText primary={campaign.name} />
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {loading ? (
        <div>Loading...</div>
      ) : !chartData.datasets || chartData.datasets.length === 0 ? (
        <div>No data to display. Please select at least one campaign.</div>
      ) : (
        <Line data={chartData} options={options} />
      )}
    </Box>
  );
};

export default CampaignLineChart;
