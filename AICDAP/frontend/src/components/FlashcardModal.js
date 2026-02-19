import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Chip,
  IconButton,
  LinearProgress,
} from "@mui/material";
import {
  ArrowBack,
  ArrowForward,
  Close,
} from "@mui/icons-material";
import FlashCard from "./FlashCard";
import { useFlashcards } from "../hooks/useFlashcards";
import "../styles/flashcard.css";

const FlashcardModal = ({ open, onClose }) => {
  const {
    currentCard,
    currentIndex,
    totalCards,
    category,
    nextCard,
    prevCard,
    changeCategory,
    progress,
  } = useFlashcards();

  const handleCategoryChange = (newCategory) => {
    changeCategory(newCategory);
  };

  const handleNextCard = () => {
    nextCard();
  };

  const handlePrevCard = () => {
    prevCard();
  };

  if (!currentCard) {
    return null;
  }

  const categories = [
    { value: "all", label: "All Cards" },
    { value: "security", label: "Security Education" },
    { value: "platform", label: "Platform Tutorials" },
  ];

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle sx={{ pb: 2 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography variant="h6">Learning Mode - Flashcards</Typography>
          <IconButton
            aria-label="close"
            onClick={onClose}
            sx={{
              color: "text.primary",
            }}
          >
            <Close />
          </IconButton>
        </Box>
      </DialogTitle>

      <DialogContent sx={{ pb: 0 }}>
        <Box className="flashcard-modal">
          {/* Category Filter */}
          <Box className="flashcard-category-filter">
            {categories.map((cat) => (
              <Chip
                key={cat.value}
                label={cat.label}
                onClick={() => handleCategoryChange(cat.value)}
                className={`flashcard-category-chip ${
                  category === cat.value ? "active" : ""
                }`}
                variant={category === cat.value ? "filled" : "outlined"}
                color={category === cat.value ? "primary" : "default"}
                sx={{
                  transition: "all 0.2s ease-in-out",
                }}
              />
            ))}
          </Box>

          {/* Progress Bar */}
          <Box>
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                mb: 1,
              }}
            >
              <Typography variant="caption" className="flashcard-progress">
                Card {currentIndex + 1} of {totalCards}
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.7 }}>
                {Math.round(progress)}% Complete
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={progress}
              sx={{
                borderRadius: 1,
                height: 6,
                backgroundColor: "action.hover",
                "& .MuiLinearProgress-bar": {
                  borderRadius: 1,
                  background: "linear-gradient(90deg, #f38020 0%, #ff9d47 100%)",
                },
              }}
            />
          </Box>

          {/* Flashcard */}
          <Box className="flashcard-modal-card">
            <FlashCard
              card={currentCard}
            />
          </Box>

          {/* Card Info */}
          {currentCard.tags && currentCard.tags.length > 0 && (
            <Box sx={{ display: "flex", gap: 0.5, flexWrap: "wrap", justifyContent: "center" }}>
              {currentCard.tags.map((tag) => (
                <Chip
                  key={tag}
                  label={tag}
                  size="small"
                  variant="outlined"
                  sx={{ fontSize: "0.75rem" }}
                />
              ))}
            </Box>
          )}
        </Box>
      </DialogContent>

      <DialogActions
        sx={{
          display: "flex",
          justifyContent: "space-between",
          p: 2,
          pt: 0,
          gap: 1,
        }}
      >
        <Button
          onClick={handlePrevCard}
          disabled={totalCards <= 1}
          startIcon={<ArrowBack />}
          variant="outlined"
        >
          Previous
        </Button>

        <Box sx={{ display: "flex", gap: 1 }}>
          <Button onClick={onClose} variant="outlined">
            Close
          </Button>
          <Button
            onClick={handleNextCard}
            disabled={totalCards <= 1}
            endIcon={<ArrowForward />}
            variant="contained"
          >
            Next
          </Button>
        </Box>
      </DialogActions>
    </Dialog>
  );
};

export default FlashcardModal;
