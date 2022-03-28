import ky from 'ky';
import { PredictionAPIRequest, PredictionAPIResponse } from '../../types/api';

type PredictionAPI = (requestJson: PredictionAPIRequest) => Promise<number>;

export const getPredictedFare: PredictionAPI = async (requestJson) => {
  const { prediction }: PredictionAPIResponse = await ky
    .post('https://us-central1-uber-fares.cloudfunctions.net/ml-prediction-fn', {
      json: requestJson,
    })
    .json();
  return +prediction.toFixed(2);
};
