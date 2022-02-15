import { atom, atomFamily } from 'recoil';

export const markerPositions = atomFamily({
  key: 'markerPositions',
  default: {
    lat: 40.73016,
    lng: -74.00452,
  },
});

export const passengerCount = atom({
  key: 'passengerCount',
  default: 1,
});

export const predictionYear = atom({
  key: 'predictionYear',
  default: 0,
});

export const predictionYearError = atom({
  key: 'predictionYearError',
  default: false,
});

export const predictedFare = atom({
  key: 'predictedFare',
  default: 0,
});
