export type PredictionAPIRequest = {
  pickup: {
    lat: number;
    lng: number;
  };
  dropoff: {
    lat: number;
    lng: number;
  };
  passenger_count: number;
  year: number;
};

export type PredictionAPIResponse = {
  prediction: number;
};
