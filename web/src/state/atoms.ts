import { atom, atomFamily } from 'recoil';

export const markerPositions = atomFamily({
  key: 'markerPosition',
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
  key: 'year',
  default: -1,
});

export const validationErrors = atom({
  key: 'validationErrors',
  default: {
    passengerCount: false,
  },
});

export const predictedFare = atom({
  key: 'predictedFare',
  default: -1,
});
