import ky from 'ky';
import { PredictionAPIRequest, PredictionAPIResponse } from '../../types/api';

type PredictionAPI = (requestJson: PredictionAPIRequest) => Promise<number>;

export const getPredictedFare: PredictionAPI = async (requestJson) => {
  const { prediction }: PredictionAPIResponse = await ky
    .post('https://ml-prediction-fn-iqfu6jcr7q-uc.a.run.app', {
      json: requestJson,
    })
    .json();
  return +prediction.toFixed(2);
};
