import { useState, useEffect } from 'react';
import { api } from '../services/api';

export const useRiskPrediction = () => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeLocation = async (latitude, longitude) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getRiskPrediction(latitude, longitude);
      setPrediction(data);
      return data;
    } catch (err) {
      setError(err.message || 'Failed to predict landslide risk');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const clearPrediction = () => {
    setPrediction(null);
    setError(null);
  };

  return {
    prediction,
    loading,
    error,
    analyzeLocation,
    clearPrediction
  };
};
