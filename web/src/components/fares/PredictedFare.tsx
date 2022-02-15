import { Box, Skeleton, Stat, StatHelpText, StatLabel, StatNumber } from '@chakra-ui/react';
import React from 'react';
import { useRecoilValue } from 'recoil';
import { predictedFare, predictionYear } from '../../state/atoms';

const PredictedFare = () => {
  const fare = useRecoilValue(predictedFare);

  const year = useRecoilValue(predictionYear);
  const date = new Date();
  date.setFullYear(year);

  return (
    <Box
      boxShadow="lg"
      borderRadius={8}
      flexGrow={1}
      flexBasis={0}
      px={{ base: 8, lg: 10 }}
      py={6}
      bgColor="white"
    >
      <Stat>
        <StatLabel fontSize="xl">Predicted fare</StatLabel>
        <StatNumber fontSize="4xl">
          <Skeleton mt={2} borderRadius={4} w="max-content" isLoaded={fare !== 0}>
            {`$${fare}`}
          </Skeleton>
        </StatNumber>
        <Skeleton mt={2} borderRadius={4} w="max-content" isLoaded={fare !== 0}>
          <StatHelpText>
            {date.toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </StatHelpText>
        </Skeleton>
      </Stat>
    </Box>
  );
};

export default PredictedFare;
