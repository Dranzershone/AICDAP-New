import React, { useState } from "react";
import { Button, Input, Box, Typography } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

export default function CsvUploadForm() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a CSV file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8080/employee/import", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setMessage(data.message || "Upload successful!");
    } catch (err) {
      setMessage("Upload failed: " + err.message);
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 2,
        p: 3,
        alignItems: "center",
        border: "1px dashed",
        borderColor: "primary.main",
        borderRadius: 2,
      }}
    >
      <Input
        accept=".csv"
        type="file"
        onChange={handleFileChange}
        style={{ marginBottom: "1rem" }}
      />
      <Button
        variant="contained"
        color="primary"
        startIcon={<CloudUploadIcon />}
        type="submit"
      >
        Upload
      </Button>
      {message && <Typography color="text.secondary">{message}</Typography>}
    </Box>
  );
}
