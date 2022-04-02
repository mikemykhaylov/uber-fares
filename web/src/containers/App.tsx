import React from 'react';
import { Container, Stack } from '@chakra-ui/react';
import Map from '../components/map/Map';
import Hero from './Hero';
import 'mapbox-gl/dist/mapbox-gl.css';
import PredictedFare from '../components/fares/PredictedFare';

const App = () => {
  return (
    <>
      <Map />
      <Container maxWidth="1200px" zIndex={1} pos="relative">
        <Hero />
        <Stack
          direction="row"
          w="100%"
          spacing={8}
          pt={{ base: 8, lg: 10 }}
          alignItems="flex-start"
        >
          <PredictedFare />
        </Stack>
      </Container>
    </>
  );
};

export default App;
