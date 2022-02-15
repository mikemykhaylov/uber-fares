import React from 'react';
import Coordinate from './Coordinate';

const CoordDisplay = () => {
  return (
    <>
      <Coordinate type="pickup" />
      <Coordinate type="dropoff" />
    </>
  );
};

export default CoordDisplay;
