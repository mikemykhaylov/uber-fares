import { Button, Heading, Stack } from '@chakra-ui/react';
import { FaUber, MdOnlinePrediction } from 'react-icons/all';
import React, { useState } from 'react';
import { useRecoilValue, useSetRecoilState } from 'recoil';
import {
  markerPositions,
  passengerCount,
  predictedFare,
  predictionYear,
  predictionYearError,
} from '../state/atoms';
import { getPredictedFare } from '../api';

const GetFares = () => {
  const [loading, setLoading] = useState(false);

  const pickup = useRecoilValue(markerPositions('pickup'));
  const dropoff = useRecoilValue(markerPositions('dropoff'));
  const year = useRecoilValue(predictionYear);
  // eslint-disable-next-line @typescript-eslint/naming-convention
  const passenger_count = useRecoilValue(passengerCount);

  const setIsError = useSetRecoilState(predictionYearError);

  const setPredictedFare = useSetRecoilState(predictedFare);

  const handleGetPrediction = async () => {
    if (year === 0) {
      setIsError(true);
      return;
    }
    setIsError(false);
    setLoading(true);
    setPredictedFare(0);
    const prediction = await getPredictedFare({ pickup, dropoff, passenger_count, year });
    setPredictedFare(prediction);
    setLoading(false);
  };

  return (
    <>
      <Heading size="md">Get rates</Heading>
      <Stack
        justifyContent={{ base: 'space-between', lg: 'flex-start' }}
        alignItems="flex-start"
        direction={{ base: 'column', sm: 'row', lg: 'column' }}
        spacing={4}
        mt={4}
      >
        <Button
          leftIcon={<MdOnlinePrediction />}
          colorScheme="blue"
          onClick={handleGetPrediction}
          isLoading={loading}
        >
          Past predicted rates
        </Button>
        <Button
          colorScheme="blackAlpha"
          bgColor="gray.900"
          leftIcon={<FaUber />}
          _hover={{
            bgColor: 'gray.800',
          }}
          _active={{
            bgColor: 'gray.700',
          }}
        >
          Current Uber rates
        </Button>
      </Stack>
    </>
  );
};

export default GetFares;
