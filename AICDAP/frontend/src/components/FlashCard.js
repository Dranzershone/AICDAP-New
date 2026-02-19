import React, { useState } from "react";
import { Box, Typography } from "@mui/material";
import "../styles/flashcard.css";

const FlashCard = ({ card, onFlip }) => {
  const [isFlipped, setIsFlipped] = useState(false);

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
    if (onFlip) {
      onFlip(!isFlipped);
    }
  };

  // Handle keyboard interaction (spacebar)
  React.useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.code === "Space") {
        e.preventDefault();
        setIsFlipped((prev) => !prev);
        if (onFlip) {
          onFlip(!isFlipped);
        }
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [onFlip, isFlipped]);

  return (
    <Box className="flashcard-container">
      <Box
        className={`flashcard ${isFlipped ? "flipped" : ""}`}
        onClick={handleFlip}
      >
        {/* Front Side */}
        <Box className="flashcard-front">
          <Box className="flashcard-content">
            <Typography className="flashcard-label">
              {card.category === "security" ? "Security Education" : "Platform Tutorial"}
            </Typography>
            <Typography className="flashcard-text">
              {card.question}
            </Typography>
            <Typography className="flashcard-hint">
              Click to reveal answer (or press Space)
            </Typography>
          </Box>
        </Box>

        {/* Back Side */}
        <Box className="flashcard-back">
          <Box className="flashcard-content">
            <Typography className="flashcard-label">Answer</Typography>
            <Typography className="flashcard-text">
              {card.answer}
            </Typography>
            <Typography className="flashcard-hint">
              {card.tags && card.tags.length > 0 ? (
                <>Tags: {card.tags.join(", ")}</>
              ) : (
                "Click to hide answer"
              )}
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default FlashCard;
