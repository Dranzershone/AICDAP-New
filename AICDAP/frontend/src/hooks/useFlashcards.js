import { useState, useCallback, useMemo } from "react";
import flashcardsData from "../data/flashcards.json";

export const useFlashcards = (initialCategory = "all") => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [category, setCategory] = useState(initialCategory);
  const [visitedCards, setVisitedCards] = useState(new Set());

  // Filter cards by category
  const filteredCards = useMemo(() => {
    if (category === "all") {
      return flashcardsData;
    }
    return flashcardsData.filter((card) => card.category === category);
  }, [category]);

  // Get current card
  const currentCard = useMemo(
    () =>
      filteredCards[currentIndex] || (filteredCards.length > 0 ? filteredCards[0] : null),
    [filteredCards, currentIndex],
  );

  // Navigate to next card
  const nextCard = useCallback(() => {
    setCurrentIndex((prev) => (prev + 1) % filteredCards.length);
    if (currentCard && currentCard.id) {
      setVisitedCards((prev) => new Set([...prev, currentCard.id]));
    }
  }, [filteredCards.length, currentCard]);

  // Navigate to previous card
  const prevCard = useCallback(() => {
    setCurrentIndex((prev) =>
      prev === 0 ? filteredCards.length - 1 : prev - 1,
    );
  }, [filteredCards.length]);

  // Jump to specific card
  const jumpToCard = useCallback((index) => {
    if (index >= 0 && index < filteredCards.length) {
      setCurrentIndex(index);
    }
  }, [filteredCards.length]);

  // Change category
  const changeCategory = useCallback((newCategory) => {
    setCategory(newCategory);
    setCurrentIndex(0);
    setVisitedCards(new Set());
  }, []);

  // Get cards by category
  const getCardsByCategory = useCallback(() => {
    const categories = {};
    flashcardsData.forEach((card) => {
      if (!categories[card.category]) {
        categories[card.category] = [];
      }
      categories[card.category].push(card);
    });
    return categories;
  }, []);

  // Calculate progress
  const progress = useMemo(() => {
    if (filteredCards.length === 0) return 0;
    return ((currentIndex + 1) / filteredCards.length) * 100;
  }, [currentIndex, filteredCards.length]);

  return {
    currentCard,
    currentIndex,
    totalCards: filteredCards.length,
    category,
    filteredCards,
    nextCard,
    prevCard,
    jumpToCard,
    changeCategory,
    getCardsByCategory,
    visitedCards,
    progress,
  };
};
